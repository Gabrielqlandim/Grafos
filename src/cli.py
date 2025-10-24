# src/cli.py
from __future__ import annotations
import argparse
from pathlib import Path
from src.solve import run_task

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="projeto-grafos",
        description="CLI do Projeto: Grafos do Recife + Comparação de Algoritmos"
    )
    p.add_argument("--dataset", type=Path, required=True,
                   help="Caminho do CSV de bairros ou pasta do dataset (Parte 2).")
    p.add_argument("--alg", type=str, required=True,
                   choices=["BFS", "DFS", "DIJKSTRA", "BELLMAN_FORD",
                            "INTERACTIVE", "METRICAS", "EGO", "GRAUS"],
                   help="Algoritmo/ação a executar.")
    p.add_argument("--source", type=str, default=None,
                   help="Nó/bairro de origem (quando aplicável).")
    p.add_argument("--target", type=str, default=None,
                   help="Nó/bairro de destino (quando aplicável).")
    p.add_argument("--out", type=Path, default=Path("./out"),
                   help="Diretório de saída (será criado se não existir).")
    p.add_argument("--verbose", action="store_true",
                   help="Mostra logs detalhados.")
    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return run_task(args)

if __name__ == "__main__":
    raise SystemExit(main())
