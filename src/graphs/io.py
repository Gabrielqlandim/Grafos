import pandas as pd
import os
from .graph import Grafo
    

#===================================================================#

#Lógica para ler o arquivo e transformar em um grafo python

def criar_grafo(caminho_csv: str | None = None):
    #Criando um dataframe com as informações do grafo
    if caminho_csv is None:
        caminho_csv = os.path.join(os.path.dirname(__file__), "../../data/adjacencias_bairros.csv")
    df = pd.read_csv(caminho_csv)

    #Criando um objeto do tipo grafo
    g = Grafo()

    #Para cada linha do arquivo, adicionamos uma aresta que liga o vértice de origem ao de destino
    for _, linha in df.iterrows():
        g.adicionar_aresta(linha['bairro_origem'], linha['bairro_destino'], linha['peso(distancia em km)'])

    # Não imprimir para manter o CLI limpo
    return g.grafo