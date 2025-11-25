import pandas as pd
import math
import json

def ler_csv_bairros(caminho):
    df = pd.read_csv(caminho)
    return df.sort_values(by='bairro').reset_index(drop=True)

def ler_csv_densidade(caminho):
    dens = pd.read_csv(caminho)
    return dens.sort_values(by='bairro').reset_index(drop=True)

def ler_adjacencias(caminho):
    return pd.read_csv(caminho)

def ler_microrregioes(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return json.load(f)

def calcular_posicoes(df, raio_minimo=200):
    num_vertices = len(df)
    raio = max(raio_minimo, num_vertices * 10)
    angulo_entre = 2 * math.pi / num_vertices
    posicoes = {}
    for i, row in df.iterrows():
        bairro = row['bairro']
        microrregiao = row['microrregiao']
        x = raio * math.cos(i * angulo_entre)
        y = raio * math.sin(i * angulo_entre)
        posicoes[bairro] = (x, y, microrregiao)
    return posicoes, raio

def gerar_svg(posicoes, adjacencias, densidade_df, microrregioes, raio, percurso_nd_setubal):

    cores_microrregiao = {
        1: '#E74C3C',
        2: '#3498DB',
        3: '#2ECC71',
        4: '#F1C40F',
        5: '#9B59B6',
        6: '#E67E22',
    }

    dens_dict = pd.Series(densidade_df.densidade_ego.values, index=densidade_df.bairro).to_dict()

    dens_min_max = {}
    for _, row in densidade_df.iterrows():
        micror = row['microrregiao'] if 'microrregiao' in row else None
        if micror is not None:
            if micror not in dens_min_max:
                dens_min_max[micror] = [row['densidade_ego'], row['densidade_ego']]
            else:
                dens_min_max[micror][0] = min(dens_min_max[micror][0], row['densidade_ego'])
                dens_min_max[micror][1] = max(dens_min_max[micror][1], row['densidade_ego'])

    def calcular_opacidade(bairro, microrregiao):
        dens = dens_dict.get(bairro, 0.5)
        min_d, max_d = dens_min_max.get(microrregiao, (0,1))
        if max_d - min_d == 0:
            return 0.8  
        fator = (dens - min_d) / (max_d - min_d)  
        opacidade = 1 - 0.9 * (fator ** 2)  
        return max(0.1, opacidade)  


    svg = f'<svg id="meuSVG" width="100%" height="100vh" viewBox="-{raio+50} -{raio+50} {2*(raio+50)} {2*(raio+50)}" style="border:1px solid black">\n'

    for _, row in adjacencias.iterrows():
        origem = row['bairro_origem']
        destino = row['bairro_destino']
        peso = row['peso(distancia em km)']
        if origem in posicoes and destino in posicoes:
            x1, y1, _ = posicoes[origem]
            x2, y2, _ = posicoes[destino]
            nome_aresta = row['Aresta']
            peso = row['peso(distancia em km)']
            svg += f'<line class="aresta" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#cccccc" stroke-width="1.5" title="{peso} km" data-origem="{origem}" data-destino="{destino}" data-nome="{nome_aresta}" data-peso="{peso}" />\n'

    for bairro, (x, y, microrregiao) in posicoes.items():
        cor = cores_microrregiao.get(microrregiao, 'lightgray')
        opacidade = calcular_opacidade(bairro, microrregiao)
        
        densidade = dens_dict.get(bairro, 0)  
        grau = int(densidade_df.loc[densidade_df['bairro'] == bairro, 'grau'].values[0])
        
        svg += f'<circle class="vertice" cx="{x}" cy="{y}" r="30" fill="{cor}" fill-opacity="{opacidade}" data-nome="{bairro}" data-microrregiao="{microrregiao}" data-densidade="{densidade:.3f}" data-grau="{grau}" />\n'
        svg += f'<text x="{x}" y="{y}" font-size="8" text-anchor="middle" dominant-baseline="middle">{bairro}</text>\n'

    svg += f'''
    <rect id="fundoTextoNome" x="-500" y="-150" width="1000" height="100" fill="white" fill-opacity="0.9" visibility="hidden" rx="20" ry="20"/>
    <text id="textoNome" x="0" y="-100" font-size="50" text-anchor="middle" dominant-baseline="middle" fill="black"></text>
    <rect id="fundoTextoConecta" x="-500" y="-40" width="1000" height="100" fill="white" fill-opacity="0.9" visibility="hidden" rx="20" ry="20"/>
    <text id="textoConecta" x="0" y="10" font-size="50" text-anchor="middle" dominant-baseline="middle" fill="black"></text>
    <rect id="fundoTextoLista" x="-500" y="70" width="1000" height="100" fill="white" fill-opacity="0.9" visibility="hidden" rx="20" ry="20"/>
    <text id="textoLista" x="0" y="100" font-size="40" text-anchor="middle" dominant-baseline="middle" fill="black"></text>
    <rect id="fundoTextoMicrorregiao" x="-500" y="-270" width="1000" height="100" fill="white" fill-opacity="0.9" visibility="hidden" rx="20" ry="20"/>
    <text id="textoMicrorregiao" x="0" y="-220" font-size="40" text-anchor="middle" dominant-baseline="middle" fill="black"></text>
    '''

    svg += '''
    <style>
        .dim { opacity: 0.2; transition: opacity 0.3s; }
        .destacado { stroke: black; stroke-width: 3; opacity: 1 !important; }
        text { white-space: pre; }
        .item-legenda { cursor: pointer; }
    </style>
    <script>
        const vertices = document.querySelectorAll('.vertice');
        const arestas = document.querySelectorAll('.aresta');
        const percursoNDSetubal = ''' + json.dumps(percurso_nd_setubal) + ''';
        let microrSelecionada = null;
        let percursoAtivo = false;

        function escurecerTodos() {
            vertices.forEach(v => v.classList.add('dim'));
            arestas.forEach(a => a.classList.add('dim'));
        }

        function restaurarTodos() {
            vertices.forEach(v => v.classList.remove('dim', 'destacado'));
            arestas.forEach(a => a.classList.remove('dim', 'destacado'));
        }

        function verticesNamed(nome){
            return Array.from(vertices).find(v => v.getAttribute('data-nome') === nome);
        }

        vertices.forEach(v => {
            v.addEventListener('mouseenter', () => {
                escurecerTodos();
                v.classList.add('destacado');
                const nome = v.getAttribute('data-nome');
                const dens = v.getAttribute('data-densidade');
                const grau = v.getAttribute('data-grau');
                let listaArestas = [];
                arestas.forEach(a => {
                    const origem = a.getAttribute('data-origem');
                    const destino = a.getAttribute('data-destino');
                    const nomeA = a.getAttribute('data-nome');
                    if(origem === nome || destino === nome){
                        a.classList.add('destacado');
                        a.classList.remove('dim');
                        vertices.forEach(other => {
                            if(other.getAttribute('data-nome') === origem || other.getAttribute('data-nome') === destino){
                                other.classList.add('destacado');
                                other.classList.remove('dim');
                            }
                        });
                        listaArestas.push(nomeA + ' - conecta ' + origem + ' e ' + destino);
                    }
                });
                const textoLista = document.getElementById('textoLista');
                textoLista.innerHTML = '';
                listaArestas.forEach((linha, i) => {
                    const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
                    tspan.setAttribute("x", 0);
                    tspan.setAttribute("dy", i === 0 ? 0 : 50);
                    tspan.setAttribute("text-anchor", "middle");
                    tspan.textContent = linha;
                    textoLista.appendChild(tspan);
                });
                document.getElementById('fundoTextoLista').setAttribute('height', Math.max(100, listaArestas.length * 50));
                document.getElementById('textoNome').textContent = nome + ' | Grau: ' + grau + ' | Densidade: ' + dens;
                document.getElementById('fundoTextoNome').setAttribute('visibility', 'visible');
                document.getElementById('fundoTextoConecta').setAttribute('visibility', 'hidden');
                document.getElementById('fundoTextoLista').setAttribute('visibility', 'visible');
            });
            v.addEventListener('mouseleave', () => {
                restaurarTodos();
                document.getElementById('textoNome').textContent = '';
                document.getElementById('textoConecta').textContent = '';
                document.getElementById('textoLista').innerHTML = '';
                document.getElementById('fundoTextoNome').setAttribute('visibility', 'hidden');
                document.getElementById('fundoTextoConecta').setAttribute('visibility', 'hidden');
                document.getElementById('fundoTextoLista').setAttribute('visibility', 'hidden');
            });
        });

        arestas.forEach(a => {
            a.addEventListener('mouseenter', () => {
                escurecerTodos();
                a.classList.add('destacado');
                const nome = a.getAttribute('data-nome');
                const peso = a.getAttribute('data-peso');
                const origem = a.getAttribute('data-origem');
                const destino = a.getAttribute('data-destino');
                vertices.forEach(v => {
                    const vNome = v.getAttribute('data-nome');
                    if(vNome === origem || vNome === destino){
                        v.classList.add('destacado');
                        v.classList.remove('dim');
                    }
                });
                document.getElementById('textoNome').textContent = nome + ' - ' + peso + ' km';
                document.getElementById('textoConecta').textContent = 'Conecta ' + origem + ' ↔ ' + destino;
                document.getElementById('fundoTextoNome').setAttribute('visibility', 'visible');
                document.getElementById('fundoTextoConecta').setAttribute('visibility', 'visible');
                document.getElementById('fundoTextoLista').setAttribute('visibility', 'hidden');
            });
            a.addEventListener('mouseleave', () => {
                restaurarTodos();
                document.getElementById('textoNome').textContent = '';
                document.getElementById('textoConecta').textContent = '';
                document.getElementById('textoLista').innerHTML = '';
                document.getElementById('fundoTextoNome').setAttribute('visibility', 'hidden');
                document.getElementById('fundoTextoConecta').setAttribute('visibility', 'hidden');
                document.getElementById('fundoTextoLista').setAttribute('visibility', 'hidden');
            });
        });

        const legendas = document.querySelectorAll('.item-legenda[data-microrregiao]');
        const textoListaCentral = document.getElementById('textoLista');
        const textoMicror = document.getElementById('textoMicrorregiao');
        const microrData = ''' + json.dumps(microrregioes) + ''';

        legendas.forEach(item => {
            item.addEventListener('click', () => {
                const micror = item.getAttribute('data-microrregiao');
                if(microrSelecionada === micror){
                    restaurarTodos();
                    textoListaCentral.innerHTML = '';
                    textoMicror.textContent = '';
                    document.getElementById('fundoTextoLista').setAttribute('visibility', 'hidden');
                    document.getElementById('fundoTextoMicrorregiao').setAttribute('visibility', 'hidden');
                    microrSelecionada = null;
                    return;
                }
                microrSelecionada = micror;
                restaurarTodos();
                escurecerTodos();
                let bairrosDaMicror = [];
                vertices.forEach(v => {
                    if(v.getAttribute('data-microrregiao') === micror){
                        v.classList.remove('dim');
                        v.classList.add('destacado');
                        bairrosDaMicror.push(v.getAttribute('data-nome'));
                    }
                });
                arestas.forEach(a => {
                    const origem = verticesNamed(a.getAttribute('data-origem'));
                    const destino = verticesNamed(a.getAttribute('data-destino'));
                    if(origem.getAttribute('data-microrregiao') === micror && destino.getAttribute('data-microrregiao') === micror){
                        a.classList.remove('dim');
                        a.classList.add('destacado');
                    }
                });
                textoListaCentral.innerHTML = '';
                const metade = Math.ceil(bairrosDaMicror.length / 2);
                const espaco = 50;
                const y_inicial = 0;
                bairrosDaMicror.forEach((bairro, i) => {
                    const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
                    const coluna = i < metade ? -200 : 200;
                    const index_coluna = i < metade ? i : i - metade;
                    tspan.setAttribute("x", coluna);
                    tspan.setAttribute("y", y_inicial + index_coluna * espaco);
                    tspan.setAttribute("text-anchor", "middle");
                    tspan.textContent = bairro;
                    textoListaCentral.appendChild(tspan);
                });
                const alturaLista = Math.max(100, Math.ceil(bairrosDaMicror.length / 2) * espaco + 20);
                const y_caixa = y_inicial - 20;
                document.getElementById('fundoTextoLista').setAttribute('height', alturaLista);
                document.getElementById('fundoTextoLista').setAttribute('y', y_caixa);
                const microrInfo = microrData.find(m => m.microrregiao === micror);
                if(microrInfo){
                    textoMicror.textContent = `Microrregião ${micror} | Ordem: ${microrInfo.ordem} | Tamanho: ${microrInfo.tamanho} | Densidade: ${microrInfo.densidade.toFixed(3)}`;
                }
                document.getElementById('fundoTextoMicrorregiao').setAttribute('visibility', 'visible');
                document.getElementById('fundoTextoLista').setAttribute('visibility', 'visible');
            });
        });

        const btnPercurso = document.getElementById("nova-descoberta-btn");
        btnPercurso.addEventListener("click", () => {
            if(percursoAtivo){
                restaurarTodos();
                document.getElementById("textoNome").textContent = '';
                document.getElementById("textoConecta").textContent = '';
                document.getElementById("textoLista").innerHTML = '';
                document.getElementById("fundoTextoNome").setAttribute("visibility", "hidden");
                document.getElementById("fundoTextoConecta").setAttribute("visibility", "hidden");
                document.getElementById("fundoTextoLista").setAttribute("visibility", "hidden");
                percursoAtivo = false;
                return;
            }
            percursoAtivo = true;
            restaurarTodos();
            escurecerTodos();
            const origem = percursoNDSetubal.origem;
            const destino = percursoNDSetubal.destino;
            const custo = percursoNDSetubal.custo;
            const caminho = percursoNDSetubal.caminho_bairros;
            caminho.forEach(nomeBairro => {
                const v = verticesNamed(nomeBairro);
                if (v) {
                    v.classList.remove("dim");
                    v.classList.add("destacado");
                }
            });
            arestas.forEach(a => {
                const o = a.getAttribute("data-origem");
                const d = a.getAttribute("data-destino");
                for (let i = 0; i < caminho.length - 1; i++) {
                    if ((caminho[i] === o && caminho[i+1] === d) ||
                        (caminho[i] === d && caminho[i+1] === o)) {
                        a.classList.remove("dim");
                        a.classList.add("destacado");
                    }
                }
            });
            document.getElementById("textoNome").textContent =
                `Percurso: ${origem} → ${destino} | Custo: ${custo} km`;
            const textoLista = document.getElementById("textoLista");
            textoLista.innerHTML = "";
            const percursoTexto = caminho.join(' → ');
            const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
            tspan.setAttribute("x", 0);
            tspan.setAttribute("y", 0);
            tspan.setAttribute("text-anchor", "middle");
            tspan.setAttribute("font-size", "24");
            tspan.textContent = percursoTexto;
            textoLista.appendChild(tspan);

            document.getElementById("fundoTextoNome").setAttribute("visibility", "visible");
            document.getElementById("fundoTextoLista").setAttribute("visibility", "visible");
        });
    </script>
    '''
    svg += '</svg>'
    return svg


def gerar_html(svg_content):
    return f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Vértices em Círculo por Microrregião</title>

<style>
    .legenda-container {{
        position: fixed;
        left: 20px;
        top: 20px;
        background: white;
        padding: 20px;
        border-radius: 12px;
        font-family: Arial;
        font-size: 18px;
        box-shadow: 0 0 10px rgba(0,0,0,0.2);
        width: 270px;
        z-index: 9999;
    }}

    .item-legenda {{
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        cursor: pointer;
    }}

    .cor-box {{
        width: 25px;
        height: 25px;
        margin-right: 10px;
        border-radius: 5px;
        border: 1px solid black;
    }}
</style>

</head>
<body style="margin:0; padding:0;">

<!-- LEGENDA -->
<div class="legenda-container">
    <h3 style="margin-top:0;">Microrregiões</h3>
    <div class="item-legenda" data-microrregiao="1"><div class="cor-box" style="background:#E74C3C;"></div><span>Centro</span></div>
    <div class="item-legenda" data-microrregiao="2"><div class="cor-box" style="background:#3498DB;"></div><span>Norte</span></div>
    <div class="item-legenda" data-microrregiao="3"><div class="cor-box" style="background:#2ECC71;"></div><span>Nordeste</span></div>
    <div class="item-legenda" data-microrregiao="4"><div class="cor-box" style="background:#F1C40F;"></div><span>Oeste</span></div>
    <div class="item-legenda" data-microrregiao="5"><div class="cor-box" style="background:#9B59B6;"></div><span>Sudoeste</span></div>
    <div class="item-legenda" data-microrregiao="6"><div class="cor-box" style="background:#E67E22;"></div><span>Sul</span></div>
    <div class="item-legenda" id="nova-descoberta-btn"><div class="cor-box" style="background:white; border:2px dashed black;"></div><span>Nova Descoberta → Setúbal</span></div>
</div>

{svg_content}

<!-- BARRA DE GRADIENTE DE DENSIDADE -->
<div style="
    position: fixed;
    right: 20px;
    top: 50%;
    transform: translateY(-50%);
    display: flex;
    align-items: center;
    z-index: 9999;
">
    <!-- Palavra "Densidade" ao lado -->
    <span style="margin-right: 10px; writing-mode: vertical-lr; transform: rotate(180deg); font-size: 14px;">Densidade</span>
    
    <!-- Barra de gradiente -->
    <div style="
        width: 40px;
        height: 300px;
        border: 1px solid black;
        border-radius: 8px;
        background: linear-gradient(to top, rgba(26,188,156,0.1), rgba(26,188,156,1));
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        padding: 5px;
        box-sizing: border-box;
    ">
        <span style="writing-mode: vertical-lr; transform: rotate(180deg); font-size: 14px;">Alta</span>
        <span style="writing-mode: vertical-lr; transform: rotate(180deg); font-size: 14px;">Baixa</span>
    </div>
</div>

</body>
</html>
'''

def salvar_html(html_content, caminho):
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html_content)

if __name__ == "__main__":
    df = ler_csv_bairros('data/bairros_unique.csv')
    dens = ler_csv_densidade('out/ego_bairro.csv')
    adj = ler_adjacencias('data/adjacencias_bairros.csv')
    micror = ler_microrregioes('out/microrregioes.json')
    with open('out/percurso_nova_descoberta_setubal.json', 'r', encoding='utf-8') as f:
        percurso_nd_setubal = json.load(f)
    posicoes, raio = calcular_posicoes(df)
    svg = gerar_svg(posicoes, adj, dens, micror, raio, percurso_nd_setubal)
    html = gerar_html(svg)
    salvar_html(html, 'out/grafo_interativo.html')
    print("HTML gerado com sucesso: grafo_interativo.html")
