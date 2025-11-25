from src.graphs.graph import Grafo
from src.graphs.io import criar_grafo
from src.graphs.algorithms import *
import time
import json

g = criar_grafo('data/airlines_spicejet.csv')

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

resultados_dijkstra = []

for origem, destino in pares_origem_destino:
    inicio_dijkstra = time.time()
    resultado = dijkstra(g, origem, destino)
    fim_dijkstra = time.time()
    tempo_exec = fim_dijkstra - inicio_dijkstra

    custo = resultado["Distância"]
    caminho = resultado["Caminho"]

    resultados_dijkstra.append(
        {
            "source": origem,
            "target": destino,
            "tempo": tempo_exec,
            "custo": custo,
            "tamanho_caminho": len(caminho),
            "caminho": caminho,
        }
    )

#Parte bellman-ford

resultados_bellman = []

# Dataset grande (airlines) com alguns pesos negativos
inicio_bf_air = time.time()
res_bf_air = bellman_ford(g, "Delhi", "Mumbai")
fim_bf_air = time.time()

tempo_bf_air = fim_bf_air - inicio_bf_air
custo_bf_air = res_bf_air["Distância"]
caminho_bf_air = res_bf_air["Caminho"]

resultados_bellman.append(
    {
        "descricao": "Dataset airlines completo (com algumas durações negativas)",
        "source": "Delhi",
        "target": "Mumbai",
        "tempo": tempo_bf_air,
        "custo": custo_bf_air,
        "tamanho_caminho": len(caminho_bf_air),
        "caminho": caminho_bf_air,
        "tem_ciclo_negativo": res_bf_air["CicloNegativo"],
    }
)

# Subgrafo com pesos negativos, sem ciclo negativo
grafo_negativo_sem_ciclo = {
    "Delhi":   {"Mumbai": -2.17},
    "Mumbai":  {"Chennai": -15.42},
    "Chennai": {"Hyderabad": -10.08},
    "Hyderabad": {},
}

inicio_bf_neg = time.time()
res_bf_neg = bellman_ford(grafo_negativo_sem_ciclo, "Delhi", "Hyderabad")
fim_bf_neg = time.time()

tempo_bf_neg = fim_bf_neg - inicio_bf_neg
custo_bf_neg = res_bf_neg["Distância"]
caminho_bf_neg = res_bf_neg["Caminho"]

resultados_bellman.append(
    {
        "descricao": "Subgrafo airlines (pesos negativos, sem ciclo negativo)",
        "source": "Delhi",
        "target": "Hyderabad",
        "tempo": tempo_bf_neg,
        "custo": custo_bf_neg,
        "tamanho_caminho": len(caminho_bf_neg),
        "caminho": caminho_bf_neg,
        "tem_ciclo_negativo": res_bf_neg["CicloNegativo"],
    }
)

# Subgrafo do airlines com ciclo negativo
grafo_com_ciclo_negativo = {
    "Delhi":   {"Mumbai": -2.17},
    "Mumbai":  {"Chennai": -15.42},
    "Chennai": {"Hyderabad": -10.08},
    "Hyderabad": {"Bangalore": -1.25},
    "Bangalore": {"Delhi": -2.83},
}

inicio_bf_cycle = time.time()
res_bf_cycle = bellman_ford(grafo_com_ciclo_negativo, "Delhi")
fim_bf_cycle = time.time()

tempo_bf_cycle = fim_bf_cycle - inicio_bf_cycle

resultados_bellman.append(
    {
        "descricao": "Subgrafo airlines (ciclo negativo)",
        "source": "Delhi",
        "target": None,
        "tempo": tempo_bf_cycle,
        "custo": None,
        "tamanho_caminho": None,
        "caminho": None,
        "tem_ciclo_negativo": res_bf_cycle["CicloNegativo"],
    }
)


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
        },
    ],
    "DIJKSTRA": resultados_dijkstra,

    "BELLMAN-FORD": resultados_bellman,
}

#Local de exportação dos resultados para o Json parte2_report

caminho_json = "out/parte2_report.json"

with open(caminho_json, "w", encoding="utf-8") as a:
    json.dump(resultados_BFS_DFS_Dijskra_BellmanFord, a, ensure_ascii=False, indent=2)