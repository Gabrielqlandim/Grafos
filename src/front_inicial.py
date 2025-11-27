from pathlib import Path

def gerar_html_inicial():
    return '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<title>Projeto Final: Grafos do Recife + Comparação de Algoritmos</title>
<style>
    body {
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        height: 100vh;
        margin: 0;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        background-color: #f7f7f7;
        color: #333;
    }

    h1 {
        font-size: 2em;
        margin-bottom: 10px;
        font-weight: 500;
        text-align: center;
        color: #222;
    }

    .participantes {
        font-size: 1em;
        margin-bottom: 50px;
        color: #555;
        text-align: center;
    }

    .container {
        display: flex;
        gap: 25px;
    }

    button {
        padding: 15px 40px;
        font-size: 16px;
        border: 2px solid #333;
        border-radius: 8px;
        background: transparent;
        color: #333;
        cursor: pointer;
        transition: all 0.2s ease-in-out;
        font-weight: 500;
    }

    button:hover {
        transform: scale(1.05);
    }

    #parte1-btn {
        border-color: #3498DB;
        color: #3498DB;
    }

    #parte1-btn:hover {
        background-color: #3498DB;
        color: #fff;
    }

    #parte2-btn {
        border-color: #E74C3C;
        color: #E74C3C;
    }

    #parte2-btn:hover {
        background-color: #E74C3C;
        color: #fff;
    }
</style>
</head>
<body>
<h1>Projeto Final: Grafos do Recife + Comparação de Algoritmos</h1>
<div class="participantes">
    Gabriel Landim, Maria Fernanda Ordonho, Pedro Sampaio e Rafaela Vidal
</div>
<div class="container">
    <button id="parte1-btn">Parte 1</button>
    <button id="parte2-btn">Parte 2</button>
</div>

<script>
document.getElementById("parte1-btn").addEventListener("click", () => {
    window.location.href = "grafo_interativo_parte1.html";
});

document.getElementById("parte2-btn").addEventListener("click", () => {
    window.location.href = "grafo_interativo_parte2.html";
});
</script>

</body>
</html>
'''

def salvar_html(nome_arquivo: str, conteudo: str):
    path = Path(nome_arquivo)
    path.parent.mkdir(parents=True, exist_ok=True)  # garante que a pasta 'out' exista
    with open(path, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print(f"Arquivo '{nome_arquivo}' criado com sucesso!")

def main():
    html = gerar_html_inicial()
    salvar_html("out/grafo_interativo.html", html)

if __name__ == "__main__":
    main()
