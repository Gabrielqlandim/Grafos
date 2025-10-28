import os
import json
import pandas as pd
from collections import defaultdict

# Leitura dos dados
def carregar_bairros(caminho_bairros="./data/bairros_unique.csv"):
    df = pd.read_csv(caminho_bairros)
    df["bairro"] = df["bairro"].astype(str).str.strip()
    df["microrregiao"] = df["microrregiao"].astype(str).str.strip()
    return df


def carregar_arestas(caminho_arestas="./data/adjacencias_bairros.csv"):
    df = pd.read_csv(caminho_arestas)
    df["bairro_origem"] = df["bairro_origem"].astype(str).str.strip()
    df["bairro_destino"] = df["bairro_destino"].astype(str).str.strip()

    # remove laços e duplicatas (por ser um grafo NÃO-direcionado)
    pares = set()
    arestas = []
    for _, r in df.iterrows():
        u, v = r["bairro_origem"], r["bairro_destino"]
        if u == v:
            continue
        chave = tuple(sorted((u, v)))
        if chave in pares:
            continue
        pares.add(chave)
        arestas.append((u, v))
    return arestas


# transforma a lista de bairros e a lista de arestas em um dicionário de adjacência 
# para cada bairro, guarda um conjunto com seus vizinhos
def montar_grafo(conjunto_bairros, arestas):

    # dicionário: bairro -> conjunto de vizinhos
    grafo = defaultdict(set)

    # garante todos os bairros (inclusive isolados)
    for b in conjunto_bairros:
        _ = grafo[b]

    # adiciona arestas (não-direcionado)
    for u, v in arestas:
        grafo[u].add(v)
        grafo[v].add(u)
    return grafo


# Métricas
def calcular_ordem_tamanho(grafo):
    ordem = len(grafo) 
    tamanho = sum(len(vizinhos) for vizinhos in grafo.values()) // 2 
    return ordem, tamanho

def calcular_densidade(ordem, tamanho):
    if ordem < 2:
        return 0.0
    return (2 * tamanho) / (ordem * (ordem - 1))


# Saídas
def salvar_json(dados, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def salvar_csv(df, caminho):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    df.to_csv(caminho, index=False)


# 1) Métrica global
def gerar_global(caminho_bairros="./data/bairros_unique.csv",
                 caminho_arestas="./data/adjacencias_bairros.csv",
                 saida="./out/recife_global.json"):
    df_b = carregar_bairros(caminho_bairros)
    arestas = carregar_arestas(caminho_arestas)
    grafo = montar_grafo(set(df_b["bairro"]), arestas)
    ordem, tamanho = calcular_ordem_tamanho(grafo)
    densidade = calcular_densidade(ordem, tamanho)
    salvar_json({"ordem": ordem, "tamanho": tamanho, "densidade": densidade}, saida)


# 2) Microrregiões
def gerar_microrregioes(caminho_bairros="./data/bairros_unique.csv",
                        caminho_arestas="./data/adjacencias_bairros.csv",
                        saida="./out/microrregioes.json"):
    df_b = carregar_bairros(caminho_bairros)
    arestas = carregar_arestas(caminho_arestas)

    resultados = []
    for mic, grupo in df_b.groupby("microrregiao"):
        bairros_mic = set(grupo["bairro"])
        arestas_mic = [(u, v) for (u, v) in arestas if u in bairros_mic and v in bairros_mic]
        grafo_mic = montar_grafo(bairros_mic, arestas_mic)
        ordem, tamanho = calcular_ordem_tamanho(grafo_mic)
        densidade = calcular_densidade(ordem, tamanho)
        resultados.append({
            "microrregiao": mic,
            "ordem": ordem,
            "tamanho": tamanho,
            "densidade": densidade
        })

    df_out = pd.DataFrame(resultados).sort_values("microrregiao")
    os.makedirs(os.path.dirname(saida), exist_ok=True)
    df_out.to_json(saida, orient="records", indent=4, force_ascii=False)


# 3) Ego-subrede por bairro
def gerar_ego(caminho_bairros="./data/bairros_unique.csv",
              caminho_arestas="./data/adjacencias_bairros.csv",
              saida="./out/ego_bairro.csv"):
    df_b = carregar_bairros(caminho_bairros)
    arestas = carregar_arestas(caminho_arestas)
    grafo = montar_grafo(set(df_b["bairro"]), arestas)

    linhas = []
    for bairro, vizinhos in grafo.items():
        ego_nos = {bairro} | set(vizinhos)
        ego_arestas = [(u, v) for (u, v) in arestas if u in ego_nos and v in ego_nos]
        grafo_ego = montar_grafo(ego_nos, ego_arestas)
        ordem, tamanho = calcular_ordem_tamanho(grafo_ego)
        densidade = calcular_densidade(ordem, tamanho)
        linhas.append({
            "bairro": bairro,
            "grau": len(vizinhos),
            "ordem_ego": ordem,
            "tamanho_ego": tamanho,
            "densidade_ego": densidade
        })

    df_out = pd.DataFrame(linhas).sort_values("bairro")
    salvar_csv(df_out, saida)


# para executar tudo, rodar: python -m src.graphs.metrics
def gerar_todas_metricas(caminho_bairros="./data/bairros_unique.csv",
                         caminho_arestas="./data/adjacencias_bairros.csv",
                         pasta_saida="./out/"):
    gerar_global(caminho_bairros, caminho_arestas, os.path.join(pasta_saida, "recife_global.json"))
    gerar_microrregioes(caminho_bairros, caminho_arestas, os.path.join(pasta_saida, "microrregioes.json"))
    gerar_ego(caminho_bairros, caminho_arestas, os.path.join(pasta_saida, "ego_bairro.csv"))

if __name__ == "__main__":
    gerar_todas_metricas()
