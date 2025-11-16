import argparse
from pathlib import Path

import matplotlib.pyplot as plt

def gerar_histograma(graus, caminho_saida, titulo):
    
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)

    #lista os valores dos graus
    valores_grau = list(graus.values())

    #tamanho da figura png
    fig, ax = plt.subplots(figsize=(8, 6))

    # bins do histigrama
    minimo = min(valores_grau)
    maximo = max(valores_grau)
    bins = range(minimo, maximo + 2) #botei mais 2 bins pra evitar bordas pq o vertice que tem 4 e/ou 5 graus 
    #cairiam no mesmo emaranhado se nao colocasse

    #desenha e configura o histograma
    ax.hist(valores_grau, bins=bins, edgecolor="black", align="left")

    ax.set_xlabel("Grau (nº de conexões)")
    ax.set_ylabel("Quantidade de bairros")
    ax.set_title(titulo)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    #salva
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)

# mesma coisa do outro eu noa sei pra que serve o cli e nao sei se isso entraria la

