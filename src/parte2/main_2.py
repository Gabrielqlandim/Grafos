from src.graphs.graph import Grafo
from src.graphs.io import criar_grafo
from src.graphs.algorithms import *
import time
import json

g = criar_grafo('out/airlines_spicejet.csv')

#Parte de BFS e DFS
inicio_dfs = time.time()
ordem, iteracoes = dfs(g, 'Delhi')
fim_dfs = time.time()
tempo_exec_dfs =fim_dfs - inicio_dfs

print("DFS para Delhi")
for posicao,vertice in enumerate(ordem, start=1):
    print(f"A cidade {vertice} foi o {posicao}° da ordem de visita")

print("\n")
print(f"Houveram {iteracoes} ciclos nesse DFS")
print("\n")
print(f"O tempo de execução desse DFS foi de: {tempo_exec_dfs}")
print("\n")

inicio_bfs = time.time()
ordem_bfs, camadas_bfs = bfs(g, 'Mumbai')
fim_bfs = time.time()
tempo_exec_bfs =fim_bfs - inicio_bfs

print("BFS para Mumbai")
for posicao,vertice in enumerate(ordem, start=1):
    print(f"A cidade {vertice} foi o {posicao}° da ordem de visita")

print("\n")
print(f"Houveram {len(camadas_bfs)} camadas nesse BFS")
print("\n")
print(f"O tempo de execução desse DFS foi de: {tempo_exec_bfs}")
print("\n")

inicio_bfs2 = time.time()
ordem_bfs2, camadas_bfs2 = bfs(g, 'Bangalore')
fim_bfs2 = time.time()
tempo_exec_bfs2 = fim_bfs2 - inicio_bfs2

print("BFS para Bangalore")
for posicao,vertice in enumerate(ordem, start=1):
    print(f"A cidade {vertice} foi o {posicao}° da ordem de visita")

print("\n")
print(f"Houveram {len(camadas_bfs2)} camadas nesse BFS")
print("\n")
print(f"O tempo de execução desse DFS foi de: {tempo_exec_bfs2}")
print("\n")

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

#Dicionario que vou usar para armazenar os resultados de cada algoritmo
resultados_BFS_DFS_Dijskra_BellmanFord = {
    "BFS": [
        {
            "source BFS 1": "Mumbai",
            "tempo": tempo_exec_bfs,
            "camadas": camadas_bfs,
            "ordem": len(ordem_bfs),
        },
        {
            "source BFS 2": "Bangalore",
            "tempo": tempo_exec_bfs2,
            "camadas": camadas_bfs2,
            "ordem": len(ordem_bfs2),
        },
    ],
    "DFS": [
        {
            "source DFS": "Delhi",
            "tempo": tempo_exec_dfs,
            #"camadas": camadas_bfs2
            "ordem": len(ordem),
            "ciclos": iteracoes,
        }
    ]
}

#Local de exportação dos resultados para o Json parte2_report

caminho_json = "out/parte2_report.json"

with open(caminho_json, "w", encoding="utf-8") as a:
    json.dump(resultados_BFS_DFS_Dijskra_BellmanFord, a, ensure_ascii=False, indent=2)