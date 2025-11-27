import pandas as pd
import math
import json
from src.parte2.main_2 import g, dijkstra

def ler_csv_voos(caminho):
    df = pd.read_csv(caminho)
    return df.sort_values(by='source_city').reset_index(drop=True)

def ler_adjacencias(caminho):
    return pd.read_csv(caminho)

def calcular_posicoes(df, raio_minimo=200):
    # pegar todas as cidades únicas (origem + destino)
    cidades_unicas = pd.concat([df['source_city'], df['destination_city']]).unique()
    num_vertices = len(cidades_unicas)

    raio = max(raio_minimo, num_vertices * 10)
    angulo_entre = 2 * math.pi / num_vertices

    posicoes = {}
    for i, cidade in enumerate(cidades_unicas):
        x = raio * math.cos(i * angulo_entre)
        y = raio * math.sin(i * angulo_entre)
        posicoes[cidade] = (x, y)

    return posicoes, raio

def gerar_svg(posicoes, adjacencias, raio):
    cores_cidades = {
        1: '#E74C3C',
        2: '#3498DB',
        3: '#2ECC71',
        4: '#F1C40F',
        5: '#9B59B6',
        6: '#E67E22',
    }

    svg = f'<svg id="meuSVG" width="100%" height="100vh" viewBox="-{raio+50} -{raio+50} {2*(raio+50)} {2*(raio+50)}" style="border:1px solid black">\n'

    # desenhar arestas
    for _, row in adjacencias.iterrows():
        origem = row['source_city']
        destino = row['destination_city']
        if origem in posicoes and destino in posicoes:
            x1, y1 = posicoes[origem]
            x2, y2 = posicoes[destino]
            nome_aresta = row['flight']
            peso = row['duration']
            paradas = row['stops']
            preco = row['price']

            svg += (
                f'<line class="aresta" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
                f'stroke="#cccccc" stroke-width="1.5" title="Duração: {peso}" '
                f'data-origem="{origem}" data-destino="{destino}" '
                f'data-nome="{nome_aresta}" data-peso="{peso}" '
                f'data-paradas="{paradas}" data-preco="{preco}" />\n'
            )

    # desenhar vértices com cores cíclicas
    for i, (cidade, (x, y)) in enumerate(posicoes.items(), start=1):
        cor = cores_cidades[(i - 1) % 6 + 1]  # pega a cor cíclica de 1 a 6
        svg += f'<circle class="vertice" cx="{x}" cy="{y}" r="30" fill="{cor}" data-nome="{cidade}" />\n'
        svg += f'<text x="{x}" y="{y}" font-size="8" text-anchor="middle" dominant-baseline="middle">{cidade}</text>\n'

    svg += '</svg>'
    return svg

def salvar_html(html_content, caminho):
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(html_content)

def gerar_html(svg_content, voos_json):
    return f"""
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Mapa de Voos</title>

    <style>
        body {{
            margin: 0;
            display: flex;
            height: 100vh;
            font-family: Arial, sans-serif;
            background: #f4f6f8;
        }}

       #mapa {{
    margin-left: 250px; /* desloca mapa para não sobrepor menu */
    flex: 1;
    background: white;
}}

#btnMenorCaminho {{
    margin-top: 10px;
    width: 100%;
    padding: 8px 12px;
    background: #2ECC71; /* verde destacado */
    color: white;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 14px;
    transition: background 0.3s, transform 0.2s;
}}

#btnMenorCaminho:hover {{
    background: #27ae60; /* verde mais escuro ao passar o mouse */
    transform: scale(1.03);
}}


        #painel {{
    width: 430px;
    right: 0;
    top: 0;
    position: fixed;
    height: 100vh;
    overflow-y: auto;
    display: none;
    background: #ffffff; /* COR DE FUNDO ADICIONADA */
    box-shadow: -2px 0 10px rgba(0,0,0,0.1); /* sombra opcional para destacar */
    padding: 15px;
    z-index: 20; /* garantir que fique sobre o mapa */
}}

        #menuCaminho {{
    position: fixed;
    left: 0;
    top: 0;
    width: 250px;
    height: 100vh;
    background: #ffffff;
    border-right: 1px solid #ccc;
    padding: 15px;
    box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    overflow-y: auto;
    z-index: 10;
}}

        #painel h2 {{
            text-align: center;
            margin-bottom: 15px;
            font-size: 18px;
        }}

        .lista-container {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}

        .coluna {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}

        .coluna h3 {{
            text-align: center;
            font-size: 15px;
            margin: 5px 0;
            color: #2c3e50;
        }}

        .voo-card {{
            background: #f9fafb;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            font-size: 12px;
            transition: 0.2s;
        }}

        .voo-card:hover {{
            transform: scale(1.02);
            background: #eef5ff;
        }}

        .vertice:hover {{
        stroke: #999999; /* borda escura */
        stroke-width: 3;
        cursor: pointer;
        transition: transform 0.2s, stroke-width 0.2s;
        }}

    .aresta:hover {{
        stroke: #999999; /* cor azul destacada */
        stroke-width: 3;
        cursor: pointer;
        transition: stroke 0.2s, stroke-width 0.2s;
    }}


        .voo-card strong {{
            color: #34495e;
        }}

        .voo-card span {{
            display: block;
            margin-top: 2px;
        }}

        .vertice {{
            cursor: pointer;
        }}

        .filtros {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-bottom: 15px;
        }}

        .filtro {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .filtro label {{
            min-width: 80px;
            font-weight: bold;
            color: #2c3e50;
            font-size: 13px;
        }}

        .filtro select, #btnFiltrar {{
            flex: 1;
            padding: 6px 10px;
            font-size: 13px;
            border: 1px solid #ccc;
            border-radius: 8px;
            background: #f9fafb;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            cursor: pointer;
            transition: 0.2s;
        }}

        .filtro select:hover, #btnFiltrar:hover {{
            background: #eef5ff;
            border-color: #3498DB;
        }}

        #btnFiltrar {{
            margin-top: 5px;
            background: #3498DB;
            color: white;
            font-weight: bold;
            border: none;
        }}
    </style>
</head>

<body>

<!-- BOTÃO DE VOLTAR MINIMALISTA NO LADO DIREITO -->
<a href="grafo_interativo.html" 
   style="
       position: fixed;
       top: 20px;
       right: 20px;
       z-index: 10000;
       padding: 8px 16px;
       color: #333;
       font-weight: 600;
       text-decoration: none;
       border: 2px solid #333;
       border-radius: 6px;
       transition: all 0.2s ease-in-out;
       background: transparent;
   "
   onmouseover="this.style.backgroundColor='#333'; this.style.color='white';"
   onmouseout="this.style.backgroundColor='transparent'; this.style.color='#333';"
>
   ← Voltar
</a>


<div id="menuCaminho">
        <h2>Menor Caminho</h2>
        <div class="filtro">
        <label for="algoritmo">Algoritmo:</label>
        <select id="algoritmo">
            <option value="dijkstra">Dijkstra</option>
            <option value="bfs">BFS</option>
            <option value="dfs">DFS</option>
            <option value="bellman">Bellman-Ford</option>
        </select>
        </div>
        <div class="filtro">
            <label for="origem">Origem:</label>
            <select id="origem"></select>
        </div>
        <div class="filtro">
            <label for="destino">Destino:</label>
            <select id="destino"></select>
        </div>
        <button id="btnMenorCaminho">Calcular Menor Caminho</button>
        <div id="resultadoCaminho"></div>
    </div>

    <div id="mapa">
        {svg_content}
    </div>

    <div id="painel">
        <h2>Voos Conectados</h2>

        <div class="filtros">
            <div class="filtro">
                <label for="ordenarDuracao">Duração:</label>
                <select id="ordenarDuracao">
                    <option value="">--</option>
                    <option value="asc">Menor → Maior</option>
                    <option value="desc">Maior → Menor</option>
                </select>
            </div>

            <div class="filtro">
                <label for="ordenarPreco">Preço:</label>
                <select id="ordenarPreco">
                    <option value="">--</option>
                    <option value="asc">Menor → Maior</option>
                    <option value="desc">Maior → Menor</option>
                </select>
            </div>

            <div class="filtro">
                <label for="ordenarParadas">Paradas:</label>
                <select id="ordenarParadas">
                    <option value="">--</option>
                    <option value="zero">0</option>
                    <option value="one">1</option>
                </select>
            </div>

            <button id="btnFiltrar">Filtrar</button>
        </div>

        <div class="lista-container">
            <div class="coluna" id="partidas">
                <h3>🛫Partidas</h3>
            </div>

            <div class="coluna" id="chegadas">
                <h3>🛬Chegadas</h3>
            </div>
        </div>
    </div>

    <script>
        const voos = {voos_json}; // dados já passados do Python
const vertices = document.querySelectorAll('.vertice');
const arestas = document.querySelectorAll('.aresta');

const colPartidas = document.getElementById('partidas');
const colChegadas = document.getElementById('chegadas');
const painel = document.getElementById('painel');

// filtros do painel de voos
const ordenarDuracao = document.getElementById('ordenarDuracao');
const ordenarPreco = document.getElementById('ordenarPreco');
const ordenarParadas = document.getElementById('ordenarParadas');
const btnFiltrar = document.getElementById('btnFiltrar');

// elementos do menu de menor caminho
const selectOrigem = document.getElementById("origem");
const selectDestino = document.getElementById("destino");
const btnMenorCaminho = document.getElementById("btnMenorCaminho");
const resultadoCaminho = document.getElementById("resultadoCaminho");

document.getElementById("mapa").addEventListener("click", event => {{
    const target = event.target;
    if(target.classList.contains("vertice")) {{
        mostrarVoos(target.getAttribute('data-nome'));
    }}
    if(target.classList.contains("aresta")) {{
        mostrarVoosAresta(
            target.getAttribute('data-origem'), 
            target.getAttribute('data-destino')
        );
    }}
}});


// popular selects de cidades
const cidades = [...new Set(voos.map(v => v.source_city).concat(voos.map(v => v.destination_city)))];
cidades.forEach(c => {{
    let o = document.createElement("option"); o.value = c; o.text = c; selectOrigem.appendChild(o);
    let d = document.createElement("option"); d.value = c; d.text = c; selectDestino.appendChild(d);
}});

// função para ordenar e filtrar voos
function ordenarVoos(voosArray) {{
    if (ordenarDuracao.value) {{
        voosArray.sort((a,b) => ordenarDuracao.value === 'asc' ? a.duration - b.duration : b.duration - a.duration);
    }}
    if (ordenarPreco.value) {{
        voosArray.sort((a,b) => ordenarPreco.value === 'asc' ? a.price - b.price : b.price - a.price);
    }}
    if (ordenarParadas.value) {{
        voosArray = voosArray.filter(v => String(v.stops).toLowerCase() === ordenarParadas.value.toLowerCase());
    }}
    return voosArray;
}}

function bfsJS(voos, origem, destino) {{
    const fila = [origem];
    const visitado = new Set([origem]);
    const prev = {{}};

    while (fila.length > 0) {{
        const atual = fila.shift();

        if (atual === destino) break;

        voos.filter(v => v.source_city === atual).forEach(v => {{
            if (!visitado.has(v.destination_city)) {{
                visitado.add(v.destination_city);
                prev[v.destination_city] = atual;
                fila.push(v.destination_city);
            }}
        }});
    }}

    const caminho = [];
    let u = destino;
    while (u !== undefined) {{
        caminho.unshift(u);
        u = prev[u];
    }}

    return caminho[0] === origem ? {{ caminho, custo: caminho.length - 1 }} : {{ caminho: [], custo: Infinity }};
}}


function dfsJS(voos, origem, destino) {{
    const visitado = new Set();
    const prev = {{}};

    function dfs(atual) {{
        visitado.add(atual);
        if (atual === destino) return true;

        for (let v of voos.filter(v => v.source_city === atual)) {{
            if (!visitado.has(v.destination_city)) {{
                prev[v.destination_city] = atual;
                if (dfs(v.destination_city)) return true;
            }}
        }}
        return false;
    }}

    dfs(origem);

    const caminho = [];
    let u = destino;
    while (u !== undefined) {{
        caminho.unshift(u);
        u = prev[u];
    }}

    return caminho[0] === origem ? {{ caminho, custo: caminho.length - 1 }} : {{ caminho: [], custo: Infinity }};
}}


function bellmanFordJS(voos, origem, destino) {{
    const cidades = [...new Set(voos.map(v => v.source_city).concat(voos.map(v => v.destination_city)))];
    const dist = {{}};
    const prev = {{}};

    cidades.forEach(c => dist[c] = Infinity);
    dist[origem] = 0;

    for (let i = 0; i < cidades.length - 1; i++) {{
        voos.forEach(v => {{
            if (dist[v.source_city] + v.duration < dist[v.destination_city]) {{
                dist[v.destination_city] = dist[v.source_city] + v.duration;
                prev[v.destination_city] = v.source_city;
            }}
        }});
    }}

    const caminho = [];
    let u = destino;
    while (u !== undefined) {{
        caminho.unshift(u);
        u = prev[u];
    }}

    return caminho[0] === origem ? {{ caminho, custo: dist[destino] }} : {{ caminho: [], custo: Infinity }};
}}


function dijkstraJS(voos, origem, destino) {{
    const cidades = [...new Set(voos.map(v => v.source_city).concat(voos.map(v => v.destination_city)))];
    const dist = {{}};
    const prev = {{}};
    const q = new Set(cidades);

    cidades.forEach(c => {{
        dist[c] = Infinity;
        prev[c] = null;
    }});
    dist[origem] = 0;

    while (q.size > 0) {{
        let u = null;
        q.forEach(c => {{ if (u === null || dist[c] < dist[u]) u = c; }});

        q.delete(u);

        if (u === destino) break;

        voos.filter(v => v.source_city === u).forEach(v => {{
            const alt = dist[u] + v.duration; // ou outro peso
            if (alt < dist[v.destination_city]) {{
                dist[v.destination_city] = alt;
                prev[v.destination_city] = u;
            }}
        }});
    }}

    // Reconstruir caminho
    const caminho = [];
    let u = destino;
    if (prev[u] !== null || u === origem) {{
        while (u) {{
            caminho.unshift(u);
            u = prev[u];
        }}
    }}

    return {{ caminho: caminho, custo: dist[destino] }};
}}


// limpar listas do painel
function limparListas() {{
    colPartidas.innerHTML = "<h3>🛫Partidas</h3>";
    colChegadas.innerHTML = "<h3>🛬Chegadas</h3>";
}}

// mostrar voos de uma cidade
let cidadeAtiva = null;
function mostrarVoos(cidade){{
    limparListas();
    painel.style.display = "block";  // mostra painel
    cidadeAtiva = cidade;
    painel.removeAttribute('data-origem');
    painel.removeAttribute('data-destino');

    // voos que saem da cidade (Partidas)
    let partidas = voos.filter(v => v.source_city === cidade);
    partidas = ordenarVoos(partidas);

    partidas.forEach(v => {{
        const card = document.createElement('div');
        card.className = "voo-card";
        card.innerHTML = `
            <strong>${{v.flight}}</strong>
            <span>Origem: ${{v.source_city}}</span>
            <span>Destino: ${{v.destination_city}}</span>
            <span>Classe: ${{v.class}}</span>
            <span>Duração: ${{v.duration}}h</span>
            <span>Preço: ₹${{v.price}}</span>
            <span>Paradas: ${{v.stops}}</span>
            <span>Dias Faltantes: ${{v.days_left}}</span>
        `;
        colPartidas.appendChild(card);
    }});

    // voos que chegam na cidade (Chegadas)
    let chegadas = voos.filter(v => v.destination_city === cidade);
    chegadas = ordenarVoos(chegadas);

    chegadas.forEach(v => {{
        const card = document.createElement('div');
        card.className = "voo-card";
        card.innerHTML = `
            <strong>${{v.flight}}</strong>
            <span>Origem: ${{v.source_city}}</span>
            <span>Destino: ${{v.destination_city}}</span>
            <span>Classe: ${{v.class}}</span>
            <span>Duração: ${{v.duration}}h</span>
            <span>Preço: ₹${{v.price}}</span>
            <span>Paradas: ${{v.stops}}</span>
            <span>Dias Faltantes: ${{v.days_left}}</span>
        `;
        colChegadas.appendChild(card);
    }});
}}


// mostrar voos de uma aresta (duas colunas: x→y e y→x)
function mostrarVoosAresta(origem, destino) {{
    limparListas();
    painel.style.display = "block";  // mostra painel
    cidadeAtiva = null;
    
    painel.dataset.origem = origem;
    painel.dataset.destino = destino;


    // voos de origem → destino
    let voosOrigemDestino = voos.filter(v => v.source_city === origem && v.destination_city === destino);
    voosOrigemDestino = ordenarVoos(voosOrigemDestino);

    // voos de destino → origem
    let voosDestinoOrigem = voos.filter(v => v.source_city === destino && v.destination_city === origem);
    voosDestinoOrigem = ordenarVoos(voosDestinoOrigem);

    // atualizar colunas
    colPartidas.innerHTML = `<h3>${{origem}} → ${{destino}}</h3>`;
    colChegadas.innerHTML = `<h3>${{destino}} → ${{origem}}</h3>`;

    voosOrigemDestino.forEach(v => {{
        const card = document.createElement('div');
        card.className = "voo-card";
        card.innerHTML = `
            <strong>${{v.flight}}</strong>
            <span>Origem: ${{v.source_city}}</span>
            <span>Destino: ${{v.destination_city}}</span>
            <span>Classe: ${{v.class}}</span>
            <span>Duração: ${{v.duration}}h</span>
            <span>Preço: ₹${{v.price}}</span>
            <span>Paradas: ${{v.stops}}</span>
            <span>Dias Faltantes: ${{v.days_left}}</span>
        `;
        colPartidas.appendChild(card);
    }});

    voosDestinoOrigem.forEach(v => {{
        const card = document.createElement('div');
        card.className = "voo-card";
        card.innerHTML = `
            <strong>${{v.flight}}</strong>
            <span>Origem: ${{v.source_city}}</span>
            <span>Destino: ${{v.destination_city}}</span>
            <span>Classe: ${{v.class}}</span>
            <span>Duração: ${{v.duration}}h</span>
            <span>Preço: ₹${{v.price}}</span>
            <span>Paradas: ${{v.stops}}</span>
            <span>Dias Faltantes: ${{v.days_left}}</span>
        `;
        colChegadas.appendChild(card);
    }});
}}



// destacar caminho no mapa
function destacarCaminho(caminho) {{
    arestas.forEach(a => a.setAttribute("stroke", "#cccccc")); // reset
    for(let i = 0; i < caminho.length-1; i++) {{
        const o = caminho[i], d = caminho[i+1];
        const linha = document.querySelector(`.aresta[data-origem="${{o}}"][data-destino="${{d}}"]`);
        if(linha) linha.setAttribute("stroke", "#E74C3C");
    }}
}}

// eventos dos vértices
vertices.forEach(vertice => {{
    vertice.addEventListener('click', event => {{
        event.stopPropagation();
        mostrarVoos(vertice.getAttribute('data-nome'));
    }});
}});

// eventos das arestas
arestas.forEach(aresta => {{
    aresta.addEventListener('click', event => {{
        event.stopPropagation();
        const origem = aresta.getAttribute('data-origem');
        const destino = aresta.getAttribute('data-destino');
        mostrarVoosAresta(origem, destino);
    }});
}});

btnFiltrar.addEventListener("click", () => {{
    if(cidadeAtiva) {{
        mostrarVoos(cidadeAtiva);
    }} else if(painel.dataset.origem && painel.dataset.destino) {{
        mostrarVoosAresta(painel.dataset.origem, painel.dataset.destino);
    }}
}});



btnMenorCaminho.addEventListener("click", () => {{
    const origem = selectOrigem.value;
    const destino = selectDestino.value;
    const algoritmo = document.getElementById("algoritmo").value;

    if (!origem || !destino) {{
        resultadoCaminho.innerHTML = "<p>Escolha origem e destino</p>";
        return;
    }}

    if (origem === destino) {{
        resultadoCaminho.innerHTML = "<p>O voo não pode partir e chegar na mesma cidade!</p>";
        return;
    }}

    let resultado;

    if (algoritmo === "dijkstra") {{
        resultado = dijkstraJS(voos, origem, destino);
    }} 
    else if (algoritmo === "bfs") {{
        resultado = bfsJS(voos, origem, destino);
    }}
    else if (algoritmo === "dfs") {{
        resultado = dfsJS(voos, origem, destino);
    }} 
    else if (algoritmo === "bellman") {{
        resultado = bellmanFordJS(voos, origem, destino);
    }}

    // destacar caminho no mapa e mostrar custo
    if (resultado.caminho.length === 0) {{
        resultadoCaminho.innerHTML = "<p>Nenhum caminho encontrado</p>";
    }} else {{
        destacarCaminho(resultado.caminho);
        resultadoCaminho.innerHTML = `
            <p><strong>Algoritmo:</strong> ${{algoritmo.toUpperCase()}}</p>
            <p><strong>Caminho:</strong> ${{resultado.caminho.join(" → ")}}</p>
            <p><strong>Custo Total:</strong> ${{resultado.custo}}h</p>
        `;
    }}
}});



document.addEventListener("click", event => {{
    if(!painel.contains(event.target) && !event.target.classList.contains('vertice')) {{
        painel.style.display = "none";
        limparListas();
        cidadeAtiva = null;
        ordenarDuracao.value = "";
        ordenarPreco.value = "";
        ordenarParadas.value = "";
    }}
}});


    </script>

</body>
</html>
"""


if __name__ == "__main__":
    caminho_voos = "data/airlines_spicejet.csv"
    caminho_adjacencias = "data/airlines_spicejet.csv"

    df_voos = ler_csv_voos(caminho_voos)
    df_adjacencias = ler_adjacencias(caminho_adjacencias)

    posicoes, raio = calcular_posicoes(df_voos)
    svg = gerar_svg(posicoes, df_adjacencias, raio)

    # Converter o DataFrame de voos em JSON
    voos_json = df_voos.to_dict(orient='records')

    html = gerar_html(svg, json.dumps(voos_json))
    salvar_html(html, "out/grafo_interativo_parte2.html")

    print("HTML gerado com sucesso na pasta 'out': grafo_interativo_parte2.html")
