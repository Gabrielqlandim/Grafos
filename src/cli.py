from __future__ import annotations
import argparse
from pathlib import Path

from src.solve import solve_enderecos
from src.solve import executar_tarefa
from src.graphs.io import criar_grafo

from src.graphs.mapa_cores import (calcular_graus as calcular_graus_map,layout_circular as layout_circular_map,desenhar_mapa_cores,)
from src.graphs.histograma_graus import gerar_histograma
from src.graphs.subgrafo_top10 import (pegar_top10,subgrafo_induzido,desenhar_subgrafo,)

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

    if args.alg == "ENDERECOS":
        
        if args.enderecos is None:
            parser.error("--enderecos é obrigatório quando --alg ENDERECOS")
        
        solve_enderecos(adjacencias_csv=args.dataset,pares_enderecos_csv=args.enderecos,out_dir=args.out,)
        return 0
    
    #Graficos de cores
    if args.alg == "HIST_GRAUS":
        grafo = criar_grafo(str(args.dataset))
        graus = calcular_graus_map(grafo)

        fig_path = args.figout or (args.out / "histograma_graus.png")
        titulo = args.title or "Distribuição dos graus"

        gerar_histograma(graus=graus,caminho_saida=fig_path,titulo=titulo,)
        print(f"Histograma gerado")
        return 0

    if args.alg == "MAPA_CORES":
        grafo = criar_grafo(str(args.dataset))
        graus = calcular_graus_map(grafo)
        pos = layout_circular_map(grafo, raio=1.0) 

        fig_path = args.figout or (args.out / "mapa_cores_grau.png")
        titulo = args.title or "Mapa de cores por grau"

        desenhar_mapa_cores(grafo=grafo,graus=graus,posicoes=pos,caminho_saida=fig_path,titulo=titulo,)
        print(f"Mapa de cores gerado")
        return 0

    if args.alg == "SUBGRAFO_TOP10":
        grafo = criar_grafo(str(args.dataset))

        # grau no grafo completo -> top10
        graus_totais = calcular_graus_map(grafo)
        top10 = pegar_top10(graus_totais, args.k)

        # subgrafo induzido e graus dentro do subgrafo
        g_sub = subgrafo_induzido(grafo, top10)
        graus_sub = calcular_graus_map(g_sub)
        pos_sub = layout_circular_map(g_sub, raio=1.0)

        fig_path = args.figout or (args.out / f"subgrafo_top10.png")
        titulo = args.title or f"Subgrafo dos bairros com maior grau"

        desenhar_subgrafo(grafo=g_sub,pos=pos_sub,graus=graus_sub,caminho_saida=fig_path,titulo=titulo,)
        print(f"Subgrafo gerado")
        return 0

    return executar_tarefa(args)


if __name__ == "__main__":
    raise SystemExit(main())
