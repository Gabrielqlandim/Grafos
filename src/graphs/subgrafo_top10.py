from pathlib import Path
import math
import matplotlib.pyplot as plt

#Nessa função eu listo os maiores vestices por grau
def pegar_top10(graus, nome):
    #essa linhas de codigo eu primeiro fiz eles se organizarem porordem 
    #drescente e depois se houver igualdade eu faço o desempate no nome por ordem alfabetica
    ordenados = sorted(graus.items(), key=lambda x: (-x[1], x[0]))
    return [v for v, _g in ordenados[:nome]]

#aqui ele recebe os nos de top10, transforma em um conjunnto e em um dicionario. 
#no for ele pega e bota no dicionario so os vizinhos do vertices escolhidos que estao no bolo de top10 
def subgrafo_induzido(grafo, nos):
    
    nos_set = set(nos)
    sub = {u: {} for u in nos}
    for u in nos:
        for v, peso in grafo[u].items():
            if v in nos_set:
                sub[u][v] = peso
                sub[v][u] = peso
    return sub

#aqui é so a posição dos vertices no circulo que vai mostrar a relação deles
def layout_circular(grafo, raio=1.0):
    
    vertices = sorted(grafo.keys())
    n = len(vertices)
    pos = {}
    if n == 0:
        return pos
    ang = 2 * math.pi / n
    for i, v in enumerate(vertices):
        t = i * ang
        pos[v] = (raio * math.cos(t), raio * math.sin(t))
    return pos


def desenhar_subgrafo(grafo, pos, graus, caminho_saida, titulo):
    
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    #tamanho do png
    fig, ax = plt.subplots(figsize=(9, 9))

    # as arestas que ja foram desenhadas pra nao desenhar novamente
    arestas_vistas = set()
    for u, viz in grafo.items():
        for v in viz.keys():

            #tupla que garante a nao direcionalidade
            a = frozenset((u, v))

            #verifica se ja foi desenhada 
            if a in arestas_vistas:
                continue
            #aqui se desenhou ele marca como feito 
            arestas_vistas.add(a)

            #pega a posição entre os vertices e desenha a aresta
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            ax.plot([x1, x2], [y1, y2], color="lightgray", linewidth=1.0, zorder=1)

    #aqui é o desenho dos vertices
    for v, (x, y) in pos.items():
        #tamanho das bolinhas
        tam = 1500 + 150 * graus[v]
        ax.scatter(x, y, s=tam, edgecolors="black", zorder=2)
        ax.text(x, y, v, ha="center", va="center", fontsize=8, weight="bold", zorder=3)

    #configurações do grafo
    ax.set_title(titulo)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)