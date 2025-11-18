from __future__ import annotations
import argparse
from pathlib import Path

from src.solve import solve_enderecos
from src.solve import executar_tarefa
from src.graphs.io import criar_grafo

from src.graphs.mapa_cores import calcular_graus as calcular_graus_map,layout_circular as layout_circular_map,desenhar_mapa_cores
from src.graphs.histograma_graus import gerar_histograma
from src.graphs.subgrafo_top10 import pegar_top10,subgrafo_induzido,desenhar_subgrafo

#função que define o passe dos parametros para rodar os codigos no terminal
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="projeto-grafos",description="CLI do Projeto: Grafos do Recife + Algoritmos")
    
    p.add_argument("--dataset",type=Path,required=True,help="Caminho do CSV de arestas.")

    p.add_argument("--alg",type=str,required=True,choices=["BFS", "DFS", "DIJKSTRA", "METRICAS", "EGO", "GRAUS", "ENDERECOS","HIST_GRAUS", "MAPA_CORES", "SUBGRAFO_TOP10"],help="Ação/algoritmo a executar.")


    p.add_argument("--source", type=str, default=None, help="Nó/bairro de origem.")
    p.add_argument("--target", type=str, default=None, help="Nó/bairro de destino.")


    p.add_argument("--enderecos",type=Path,default=None,help="Caminho do CSV de pares de endereços — exigido no modo ENDERECOS.")

    p.add_argument("--out",type=Path,default=Path("./out"),help="Diretório de saída.")

    p.add_argument("--verbose", action="store_true", help="Mostra logs no stderr.")

    p.add_argument("--k", type=int, default=10, help="Top10 para SUBGRAFO_TOP10.")

    p.add_argument("--figout", type=Path, default=None,help="Arquivo PNG de saída da figura. Se não passar, será criado dentro de --out.")

    p.add_argument("--title", type=str, default=None, help="Título da figura.")

    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    return executar_tarefa(args)


if __name__ == "__main__":
    raise SystemExit(main())
