from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import sys
import csv
import pandas as pd

from src.graphs.io import criar_grafo, ler_pares_enderecos, desenhar_grafo
from src.graphs.algorithms import bfs, dfs, dijkstra
from src.graphs.metrics import gerar_todas_metricas

from src.graphs.mapa_cores import calcular_graus as calcular_graus_map,layout_circular as layout_circular_map,desenhar_mapa_cores
from src.graphs.histograma_graus import gerar_histograma
from src.graphs.subgrafo_top10 import pegar_top10,subgrafo_induzido,desenhar_subgrafo


#Aqui armazena as variaveis que sao passadas nos codigos do terminal para rodar cada parte do projeto
@dataclass
class Args:
    dataset: Path        
    alg: str             
    source: str | None   
    target: str | None   
    out: Path            
    verbose: bool = False
    enderecos: Path | None = None
    k: int = 10
    figout: Path | None = None
    title: str | None = None




def _garantir_saida(pasta: Path):
    pasta.mkdir(parents=True, exist_ok=True)


def _escrever_json(caminho: Path, payload: dict):
    caminho.write_text(json.dumps(payload, ensure_ascii=False, indent=2))


def _inferir_bairros_csv_de_arestas(arestas_csv: Path) -> Path:
    #Tenta localizar bairros_unique.csv na mesma pasta do CSV de arestas
    return arestas_csv.parent / "bairros_unique.csv"


def _grau_por_bairro(grafo: dict[str, dict]) -> dict[str, int]:
    #grafo é um dicionario de dicionarios
    #grau = número de chaves do dicionario interno
    return {v: len(vizinhos) for v, vizinhos in grafo.items()}


def _escrever_graus_csv(out_csv: Path, graus: dict[str, int]) -> None:
    #Escreve bairro, grau ordenado por grau descendente e desempate por bairro ascendente
    linhas = sorted(graus.items(), key=lambda x: (-x[1], x[0]))
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["bairro", "grau"])
        w.writerows(linhas)



def _ler_linha_ego(ego_csv: Path, bairro: str) -> dict | None:
    #Lê uma linha específica do ego_bairro.csv para o bairro indicado
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
    
    #Gera o bairro com maior densidade a partir de ego_bairro.csv 
    
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
    #Função principal chamada pelo CLI
    args = Args(
        dataset=ns.dataset,
        alg=ns.alg.upper(),
        source=ns.source,
        target=ns.target,
        out=ns.out,
        verbose=ns.verbose,
        enderecos=getattr(ns, "enderecos", None),
        k=getattr(ns, "k", 10),
        figout=getattr(ns, "figout", None),
        title=getattr(ns, "title", None),
    )

    _garantir_saida(args.out)
    


    #Carrega grafo quando necessário
    if args.alg in {"BFS", "DFS", "DIJKSTRA", "GRAUS"}:
        grafo = criar_grafo(str(args.dataset))
        



    #Ações

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
        # Gera os arquivos recife_global.json, microrregioes.json, ego_bairro.csv na pasta out
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
            #se ainda não existe ai ele gera tudo de novo e tenta novamente
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

        #Ranking do maior grau
        if graus:
            bairro_max, grau_max = max(graus.items(), key=lambda x: (x[1], x[0]))
            print(f"graus.csv gerado em {args.out}/graus.csv")
            print(f"[Ranking] Bairro com maior grau: {bairro_max} (grau = {grau_max})")
        else:
            print("graus.csv gerado (grafo vazio)")

        #Ranking do bairro mais denso lido em ego_bairro.csv 
        try:
            ego_csv = args.out / "ego_bairro.csv"
            bairro_denso, dens = _obter_bairro_mais_denso(ego_csv, args.dataset)
            print(f"Bairro mais denso: {bairro_denso} e a é: densidade_ego = {dens:.6f}")
        except Exception as e:
            print(f"Não foi possível obter 'bairro mais denso': {e}")

        return 0
    if args.alg == "ENDERECOS":
        
        if args.enderecos is None:
            print("--enderecos é obrigatório quando --alg ENDERECOS")
            return 2
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

        fig_path = args.figout or (args.out / "mapa_cores.png")
        titulo = args.title or "Mapa de cores por grau"

        desenhar_mapa_cores(grafo=grafo,graus=graus,posicoes=pos,caminho_saida=fig_path,titulo=titulo,)
        print(f"Mapa de cores gerado")
        return 0

    if args.alg == "SUBGRAFO_TOP10":
        grafo = criar_grafo(str(args.dataset))

        #calcula o grau do grafo completo e pega os 10 maiores
        graus_totais = calcular_graus_map(grafo)
        top10 = pegar_top10(graus_totais, args.k)

        #gera o subgrafo induzido, recalcula os graus e posiciona eles na imagem
        g_sub = subgrafo_induzido(grafo, top10)
        graus_sub = calcular_graus_map(g_sub)
        pos_sub = layout_circular_map(g_sub, raio=1.0)

        fig_path = args.figout or (args.out / f"subgrafo_top10.png")
        titulo = args.title or f"Subgrafo dos bairros com maior grau"

        desenhar_subgrafo(grafo=g_sub,pos=pos_sub,graus=graus_sub,caminho_saida=fig_path,titulo=titulo,)
        print(f"Subgrafo gerado")
        return 0
    
    print(f"Ação desconhecida: {args.alg}", file=sys.stderr)
    return 2


#Distância entre endereços X e Y
def solve_enderecos(
    adjacencias_csv: Path,
    pares_enderecos_csv: Path,
    out_dir: Path,
) -> None:
    
        #Lê pares dos enderecos
        #Monta grafo que vem do arquivo adjacencias_bairros.csv
        #Roda Dijkstra para cada par
        #Gera:
        #distancias_enderecos.csv
        #percurso_nova_descoberta_setubal.json 
    
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    G = criar_grafo(adjacencias_csv)
    pares = ler_pares_enderecos(Path(pares_enderecos_csv))

    dist_csv = out_dir / "distancias_enderecos.csv"
    with dist_csv.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["X", "Y", "bairro_X", "bairro_Y", "custo", "caminho"])

        for p in pares:
            bx = p["bairro_X"]
            by = p["bairro_Y"]

            try:
                custo, caminho = dijkstra(G, bx, by)
                custo_str = f"{float(custo):.4f}"
                caminho_str = " > ".join(caminho)
            except Exception:
                custo_str = "NA"
                caminho = []
                caminho_str = ""

            writer.writerow([p["X"], p["Y"], bx, by, custo_str, caminho_str])

            #par obrigatório: Nova Descoberta até Boa Viagem(Setúbal)
            if bx == "Nova Descoberta" and by == "Boa Viagem(Setúbal)" and caminho:
                payload = {
                    "origem": p["X"],
                    "destino": p["Y"],
                    "bairro_origem": bx,
                    "bairro_destino": by,
                    "custo": float(custo),
                    "caminho_bairros": caminho
                }
                (out_dir / "percurso_nova_descoberta_setubal.json").write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8"
                )

                desenhar_grafo(G, caminho=caminho, titulo="Caminho Nova Descoberta - Setúbal")