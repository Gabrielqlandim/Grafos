# src/cli.py
from __future__ import annotations
import argparse
from pathlib import Path
from src.solve import executar_tarefa

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="projeto-grafos",
        description="CLI do Projeto: Grafos do Recife + Algoritmos"
    )
    p.add_argument(
        "--dataset",
        type=Path,
        required=True,
        help="Caminho do CSV de arestas (ex.: data/adjacencias_bairros.csv)."
    )
    p.add_argument(
        "--alg",
        type=str,
        required=True,
        choices=["BFS", "DFS", "DIJKSTRA", "METRICAS", "EGO", "GRAUS"],
        help="Ação/algoritmo a executar."
    )
    p.add_argument("--source", type=str, default=None, help="Nó/bairro de origem (quando aplicável).")
    p.add_argument("--target", type=str, default=None, help="Nó/bairro de destino (DIJKSTRA).")
    p.add_argument("--out", type=Path, default=Path("./out"), help="Diretório de saída (criado se não existir).")
    p.add_argument("--verbose", action="store_true", help="Mostra logs no stderr.")
    return p

def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return executar_tarefa(args)

if __name__ == "__main__":
    raise SystemExit(main())
