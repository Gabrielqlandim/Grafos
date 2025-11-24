import pandas as pd
import os
from .graph import Grafo
import math
from pathlib import Path
import csv
import matplotlib.pyplot as plt


#Lógica para ler o arquivo e transformar em um grafo python

def criar_grafo(caminho_csv: str | Path | None = None):
    #Criando um dataframe com as informações do grafo
    if caminho_csv is None:
        caminho_csv = r"data\adjacencias_bairros.csv"
    caminho_str = str(caminho_csv)
    df = pd.read_csv(caminho_str)

    #Criando um objeto do tipo grafo
    g = Grafo()

    #Para cada linha do arquivo, adicionamos uma aresta que liga o vértice de origem ao de destino
    for _, linha in df.iterrows():
        if 'adjacencias_bairros' in caminho_str:
            g.adicionar_aresta(linha['bairro_origem'], linha['bairro_destino'], linha['peso(distancia em km)'])

        #Para a parte 2
        elif 'airlines' in caminho_str:
            #Seta os vétices de origem e destino como as cidades e o peso como a duração do voo
            g.adicionar_aresta(linha['source_city'], linha['destination_city'], linha['duration'])

    return g.grafo 



def ler_pares_enderecos(caminho_csv: Path):
    
    #Lê data/enderecos.csv com colunas: X,Y,bairro_X,bairro_Y
    #Retorna uma lista de dicionario
    
    pares = []
    with caminho_csv.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # normaliza nomes de bairros
            pares.append({
                "X": row["X"].strip(),
                "Y": row["Y"].strip(),
                "bairro_X": row["bairro_X"].strip(),
                "bairro_Y": row["bairro_Y"].strip(),
            })
    return pares

def desenhar_grafo(grafo, caminho=None, pos=None, mostrar_pesos=True, titulo="Grafo com Caminho"):
    
    #Desenha um grafo não direcionado e destaca um caminho em vermelho.

    #Gera posições em círculo (necessário coordenadas para desenhar no matplotlib)
    if pos is None:
        n = len(grafo)
        angulo = 2 * math.pi / n
        pos = {v: (math.cos(i * angulo), math.sin(i * angulo)) for i, v in enumerate(grafo)}

    plt.figure(figsize=(8, 8))

    #Lista de arestas desenhadas, para evitar repetição
    desenhadas = set()

    #DESENHA TODAS AS ARESTAS
    #Loop duplo percorre todos os vértices e suas conexões
    for v1 in grafo:
        for v2, peso in grafo[v1].items():

            #Caso a aresta ainda não tenha sido desenhada, desenha ela
            if (v2, v1) not in desenhadas:
                #salva as posições dos dois vértices
                x1, y1 = pos[v1]
                x2, y2 = pos[v2]

                #Plota os vértices e salva na lista de arestas desenhadas
                plt.plot([x1, x2], [y1, y2], 'k-', linewidth=1)
                desenhadas.add((v1, v2))

                #Desenha também o peso da aresta
                if mostrar_pesos:
                    plt.text((x1 + x2)/2, (y1 + y2)/2, str(peso), color='blue', fontsize=9, ha='center', va='center')

    #DESTACA O CAMINHO  EM VERMELHO
    if caminho and len(caminho) > 1:
        #Percorre todos os vértices do caminho
        for i in range(len(caminho) - 1):
            v1, v2 = caminho[i], caminho[i + 1]

            #Obtém as posições dos vértices e plota uma linha vermelha para destacar
            if v1 in pos and v2 in pos:
                x1, y1 = pos[v1]
                x2, y2 = pos[v2]
                plt.plot([x1, x2], [y1, y2], 'r-', linewidth=3, zorder=2)

    #DESENHAR VÉRTICES
    #Percorre a lista de posições e   
    for vertice, (x, y) in pos.items():
        cor = 'lightcoral' if caminho and vertice in caminho else 'orange'
        plt.scatter(x, y, s=400, color=cor, edgecolors='black', zorder=3)
        plt.text(x, y, vertice, fontsize=12, ha='center', va='center', weight='bold')

    #Exibe o grafo
    plt.axis('off')
    plt.title(titulo)
    plt.show()