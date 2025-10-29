from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import sys
import csv
import pandas as pd

from src.graphs.io import criar_grafo
from src.graphs.algorithms import bfs, dfs, dijkstra
from src.graphs.metrics import gerar_todas_metricas


@dataclass
class Args:
    dataset: Path        # caminho para data/adjacencias_bairros.csv
    alg: str             # BFS | DFS | DIJKSTRA | METRICAS | EGO | GRAUS
    source: str | None   # nó origem (quando aplicável)
    target: str | None   # nó destino (DIJKSTRA)
    out: Path            # pasta out/
    verbose: bool = False


def _registrar_log(habilitado: bool, *msg):
    if habilitado:
        print("[LOG]", *msg, file=sys.stderr)


def _garantir_saida(pasta: Path):
    pasta.mkdir(parents=True, exist_ok=True)


def _escrever_json(caminho: Path, payload: dict):
    caminho.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def _inferir_bairros_csv_de_arestas(arestas_csv: Path) -> Path:
    """Tenta localizar bairros_unique.csv na mesma pasta do CSV de arestas."""
    return arestas_csv.parent / "bairros_unique.csv"


def _grau_por_bairro(grafo: dict[str, dict]) -> dict[str, int]:
    """grafo é dict de dicts; grau = número de chaves do dict interno."""
    return {v: len(vizinhos) for v, vizinhos in grafo.items()}


def _escrever_graus_csv(out_csv: Path, graus: dict[str, int]) -> None:
    """Escreve bairro,grau ordenado por grau desc e desempate por bairro asc."""
    linhas = sorted(graus.items(), key=lambda x: (-x[1], x[0]))
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bairro", "grau"])
        w.writerows(linhas)



def _ler_linha_ego(ego_csv: Path, bairro: str) -> dict | None:
    """Lê uma linha específica do out/ego_bairro.csv para o bairro indicado."""
    if not ego_csv.exists():
        return None
    df = pd.read_csv(ego_csv)
    colunas_necessarias = {"bairro", "grau", "ordem_ego", "tamanho_ego", "densidade_ego"}
    faltando = colunas_necessarias - set(df.columns)
    if faltando:
        raise ValueError(f"Colunas ausentes em {ego_csv.name}: {faltando}")
    linha = df.loc[df["bairro"].astype(str).str.strip() == str(bairro).strip()]
    if linha.empty:
        return None
    r = linha.iloc[0]
    return {
        "bairro": str(r["bairro"]),
        "grau": int(r["grau"]),
        "ordem_ego": int(r["ordem_ego"]),
        "tamanho_ego": int(r["tamanho_ego"]),
        "densidade_ego": float(r["densidade_ego"]),
    }



def _obter_bairro_mais_denso(ego_csv: Path, arestas_csv: Path) -> tuple[str, float]:
    """
    Garante out/ego_bairro.csv e retorna (bairro_com_maior_densidade_ego, valor).
    Se o arquivo não existir, gera as métricas primeiro.
    """
    if not ego_csv.exists():
        bairros_csv = _inferir_bairros_csv_de_arestas(arestas_csv)
        gerar_todas_metricas(
            caminho_bairros=str(bairros_csv),
            caminho_arestas=str(arestas_csv),
            pasta_saida=str(ego_csv.parent),
        )

    df = pd.read_csv(ego_csv)
    if "bairro" not in df.columns or "densidade_ego" not in df.columns:
        raise ValueError("ego_bairro.csv precisa das colunas 'bairro' e 'densidade_ego'.")
    idx = df["densidade_ego"].astype(float).idxmax()
    return str(df.loc[idx, "bairro"]), float(df.loc[idx, "densidade_ego"])


def executar_tarefa(ns) -> int:
    """Função principal chamada pelo CLI."""
    args = Args(
        dataset=ns.dataset,
        alg=ns.alg.upper(),
        source=ns.source,
        target=ns.target,
        out=ns.out,
        verbose=ns.verbose,
    )

    _garantir_saida(args.out)
    _registrar_log(args.verbose, f"Ação={args.alg} | Dataset(arestas)={args.dataset}")


    # Carrega grafo quando necessário
    if args.alg in {"BFS", "DFS", "DIJKSTRA", "GRAUS"}:
        grafo = criar_grafo(str(args.dataset))
        _registrar_log(args.verbose, f"Vértices={len(grafo)}")



    # Ações

    if args.alg == "BFS":
        if not args.source:
            print("Erro de uso: Necessário --source para BFS", file=sys.stderr)
            return 2
        ordem, camadas = bfs(grafo, args.source)
        payload = {
            "algoritmo": "BFS",
            "source": args.source,
            "ordem_visita": ordem,
            "camadas": {str(k): v for k, v in camadas.items()},
        }
        _escrever_json(args.out / f"bfs_{args.source}.json", payload)
        print(f"BFS executado. Saída em {args.out}/bfs_{args.source}.json")
        return 0


    if args.alg == "DFS":
        if not args.source:
            print("Erro de uso: Necessário --source para DFS", file=sys.stderr)
            return 2
        ordem = dfs(grafo, args.source)
        payload = {
            "algoritmo": "DFS",
            "source": args.source,
            "ordem_visita": ordem,
        }
        _escrever_json(args.out / f"dfs_{args.source}.json", payload)
        print(f"DFS executado. Saída em {args.out}/dfs_{args.source}.json")
        return 0


    if args.alg == "DIJKSTRA":
        if not args.source or not args.target:
            print("Erro de uso: Necessário --source e --target para Dijkstra", file=sys.stderr)
            return 2
        dist = dijkstra(grafo, args.source)
        custo = dist.get(args.target, float("inf"))
        payload = {
            "algoritmo": "DIJKSTRA",
            "source": args.source,
            "target": args.target,
            "custo": None if custo == float("inf") else custo,
            "distancias": dist,
        }
        _escrever_json(args.out / f"dist_{args.source}_to_{args.target}.json", payload)
        print(f"Dijkstra executado. Saída em {args.out}/dist_{args.source}_to_{args.target}.json")
        return 0


    if args.alg == "METRICAS":
        # Gera: out/recife_global.json, out/microrregioes.json, out/ego_bairro.csv
        bairros_csv = _inferir_bairros_csv_de_arestas(args.dataset)
        gerar_todas_metricas(
            caminho_bairros=str(bairros_csv),
            caminho_arestas=str(args.dataset),
            pasta_saida=str(args.out),
        )
        print("Métricas geradas: recife_global.json, microrregioes.json e ego_bairro.csv em", args.out)
        return 0


    if args.alg == "EGO":
        if not args.source:
            print("Erro de uso: Necessário --source para EGO", file=sys.stderr)
            return 2
        ego_csv = args.out / "ego_bairro.csv"
        info = _ler_linha_ego(ego_csv, args.source)
        if info is None:
            # se ainda não existe, gera tudo e tenta novamente
            bairros_csv = _inferir_bairros_csv_de_arestas(args.dataset)
            gerar_todas_metricas(
                caminho_bairros=str(bairros_csv),
                caminho_arestas=str(args.dataset),
                pasta_saida=str(args.out),
            )
            info = _ler_linha_ego(ego_csv, args.source)
        if info is None:
            print(f"Erro de uso: Bairro '{args.source}' não encontrado em ego_bairro.csv", file=sys.stderr)
            return 3

        _escrever_json(args.out / f"ego_{args.source}.json", info)
        print(f"Ego-subrede salva em {args.out}/ego_{args.source}.json")
        return 0


    if args.alg == "GRAUS":
        graus = _grau_por_bairro(grafo)
        _escrever_graus_csv(args.out / "graus.csv", graus)

        # Ranking: maior grau
        if graus:
            bairro_max, grau_max = max(graus.items(), key=lambda x: (x[1], x[0]))
            print(f"graus.csv gerado em {args.out}/graus.csv")
            print(f"[Ranking] Bairro com maior grau: {bairro_max} (grau = {grau_max})")
        else:
            print("graus.csv gerado (grafo vazio)")

        # Ranking: bairro mais denso (ego) — lido de out/ego_bairro.csv (gera se não existir)
        try:
            ego_csv = args.out / "ego_bairro.csv"
            bairro_denso, dens = _obter_bairro_mais_denso(ego_csv, args.dataset)
            print(f"[Ranking] Bairro mais denso (ego): {bairro_denso} (densidade_ego = {dens:.6f})")
        except Exception as e:
            _registrar_log(args.verbose, f"Não foi possível obter 'bairro mais denso': {e}")

        return 0

    print(f"Ação desconhecida: {args.alg}", file=sys.stderr)
    return 2
