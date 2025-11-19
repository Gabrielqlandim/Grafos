from src.graphs.graph import Grafo
from src.graphs.io import criar_grafo
from src.graphs.algorithms import *
import time

g = criar_grafo('out/airlines_spicejet.csv')

#Parte de BFS e DFS
inicio_dfs = time.time()
ordem, iteracoes = dfs(g, 'Delhi')
fim_dfs = time.time()

inicio_bfs = time.time()
ordem_bfs, iteracoes_bfs = bfs(g, 'Mumbai')
fim_bfs = time.time()

inicio_bfs2 = time.time()
ordem_bfs2, iteracoes_bfs2 = bfs(g, 'Bangalore')
fim_bfs2 = time.time()

#Parte de Dijskra

pares_origem_destino = [
    ("Delhi", "Mumbai"),
    ("Delhi", "Hyderabad"),
    ("Mumbai", "Kolkata"),
    ("Bangalore", "Delhi"),
    ("Chennai", "Mumbai"),
]

for origem, destino in pares_origem_destino:
    inicio_dijskra = time.time()
    resultado = dijkstra(g, origem, destino)
    fim_dijskra= time.time()

    tempo_exec = fim_dijskra - inicio_dijskra