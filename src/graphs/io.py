import pandas as pd
import os

class Grafo:

    def __init__(self):
        #Estrutura do grafo em dicionário de dicionários
        #Cada chave é um vértice, onde seus valores são outros dicionários, contendo seus vértices adjacentes como chaves e peso da aresta como valor
        self.grafo = {}
    
    def adicionar_vertice(self, vertice):
        #Adiciona um novo vértice ao grafo se ainda não existir
        if vertice not in self.grafo:
            self.grafo[vertice] = {}
    
    def adicionar_aresta(self, origem, destino, peso):
        #Adiciona uma aresta não direcionada com peso

        #Caso o vértice não exista, adiciona
        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)
        
        #Como o grafo é não direcionado, adiciona a aresta nos dois sentidos
        self.grafo[origem][destino] = peso
        self.grafo[destino][origem] = peso
    
    def obter_vizinhos(self, vertice):
        #Retorna os vizinhos de um vértice (e seus pesos)
        return self.grafo.get(vertice, {})
    
    def vertices(self):
        #Retorna todos os vértices do grafo.
        return list(self.grafo.keys())
    
    def arestas(self):
        #Retorna todas as arestas sem duplicar (por ser não direcionado)
        visitadas = set()
        lista_arestas = []
        
        for v1 in self.grafo:
            for v2, peso in self.grafo[v1].items():
                if (v2, v1) not in visitadas:
                    lista_arestas.append((v1, v2, peso))
                    visitadas.add((v1, v2))
        return lista_arestas
    
    def __str__(self):
        #Representação textual do grafo
        texto = "Grafo Ponderado Não Direcionado:\n"
        for v, vizinhos in self.grafo.items():
            conexoes = ", ".join([f"{v2}({p})" for v2, p in vizinhos.items()])
            texto += f"  {v}: {conexoes}\n"
        return texto
    

#===================================================================#

#Lógica para ler o arquivo e transformar em um grafo python

#Criando um dataframe com as informações do grafo
caminho_csv = os.path.join(os.path.dirname(__file__), "../../data/adjacencias-bairros.csv")
df = pd.read_csv(caminho_csv)

#Criando um objeto do tipo grafo
g = Grafo()

#Para cada linha do arquivo, adicionamos uma aresta que liga o vértice de origem ao de destino
for _, linha in df.iterrows():
    g.adicionar_aresta(linha['bairro_origem'], linha['bairro_destino'], linha['peso(distancia em km)'])

GRAFO = g
print(g.__str__())