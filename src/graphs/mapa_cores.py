import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt

from src.graphs.io import criar_grafo


def calcular_graus(grafo):
    
    graus = {}

    #garante que todo vértice comece com grau 0
    for vertice in grafo.keys():
        graus[vertice] = 0

    arestas_vistas = set()

    for u, vizinhos in grafo.items():
        for v in vizinhos.keys():
            #representa a aresta sem direção
            aresta = frozenset((u, v))

            #se ja foi contado passa a frente
            if aresta in arestas_vistas:
                continue

            arestas_vistas.add(aresta)

            #aumenta em 1 o grau do vertice
            graus[u] = graus.get(u, 0) + 1
            graus[v] = graus.get(v, 0) + 1

    return graus

#aqui tambem é a mesma situação do subgrafo. Posição dos vertices no circulo que vai mostrar a relação deles 
def layout_circular(grafo, raio=1.0):
    
    vertices = sorted(grafo.keys())
    n = len(vertices)

    posicoes = {}

    if n == 0:
        return posicoes

    angulo_base = 2 * math.pi / n

    for i, vertice in enumerate(vertices):
        angulo = i * angulo_base
        x = raio * math.cos(angulo)
        y = raio * math.sin(angulo)
        posicoes[vertice] = (x, y)

    return posicoes

#aqui desenha o grafo com as cores baseadas no grau de cada vertice
def desenhar_mapa_cores(grafo, graus, posicoes, caminho_saida, titulo):
    
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    #tamanho da imagem png
    fig, ax = plt.subplots(figsize=(40, 40))

    #desenha as arestas
    arestas_vistas = set()
    for u, vizinhos in grafo.items():
        for v in vizinhos.keys():
            aresta = frozenset((u, v))
            if aresta in arestas_vistas:
                continue
            arestas_vistas.add(aresta)

            x1, y1 = posicoes[u]
            x2, y2 = posicoes[v]
            ax.plot([x1, x2], [y1, y2], color="black", linewidth=0.6, alpha=0.2, zorder=1)

    #trata os dados necessarios para botar na imagem: coordenadas, cores, tamanhos e nome
    xs = []
    ys = []
    cores = []
    tamanhos = []
    labels = []

    for vertice, (x, y) in posicoes.items():
        xs.append(x)
        ys.append(y)
        cores.append(graus[vertice])          # usamos o grau como valor da cor
        tamanhos.append(900 + 70 * graus[vertice])
        labels.append(vertice)

    #desenha os vértices
    scatter = ax.scatter(
        xs,
        ys,
        s=tamanhos,
        c=cores,
        cmap="viridis",
        edgecolors="black",
        zorder=2,
    )

    #coloca o nome do bairro em cima dos vértices
    for x, y, nome in zip(xs, ys, labels):
        ax.text(x, y, nome, ha="center", va="center", fontsize=9, weight="bold", zorder=3)

    #a barra de cores e o grau delas
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.8)
    cbar.set_label("Grau (nº de conexões)")

    ax.set_title(titulo)
    ax.axis("off")

    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)


#mesma situação dos outros
def main():
    parser = argparse.ArgumentParser(
        description="Gera um mapa de cores por grau."
    )

    parser.add_argument(
        "--dataset",
        type=str,
        required=True,
        help="Caminho para data/adjacencias_bairros.csv",
    )
    parser.add_argument(
        "--out",
        type=str,
        default="out/mapa_cores_grau.png",
        help="Arquivo PNG de saída",
    )
    parser.add_argument(
        "--title",
        type=str,
        default="Mapa de cores por grau",
        help="Título do gráfico",
    )

    args = parser.parse_args()

    #carrega o grafo
    grafo = criar_grafo(args.dataset)

    #calcula graus
    graus = calcular_graus(grafo)

    #calcula posições em círculo
    posicoes = layout_circular(grafo, raio=1.0)

    #desenha e salva a figura
    desenhar_mapa_cores(
        grafo=grafo,
        graus=graus,
        posicoes=posicoes,
        caminho_saida=args.out,
        titulo=args.title,
    )

    print(f"Figura gerada")


if __name__ == "__main__":
    main()
