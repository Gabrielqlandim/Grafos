# src/solve.py
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import json
import sys


from src.graphs.io import criar_grafo
from src.graphs.algorithms import bfs, dfs

@dataclass
class Args:
    dataset: Path
    alg: str
    source: str | None
    target: str | None
    out: Path
    verbose: bool = False

def _log(enabled: bool, *msg):
    if enabled:
        print("[LOG]", *msg, file=sys.stderr)

def _ensure_out(out: Path):
    out.mkdir(parents=True, exist_ok=True)

def _fake_graph_info(dataset: Path) -> dict:
    """Stub temporário para permitir testes de CLI antes do IO real."""
    # TODO: trocar por leitura real do CSV e construção do grafo.
    return {"dataset": str(dataset), "V": 10, "E": 15, "densidade": 2*15/(10*(10-1))}

def _write_json(path: Path, payload: dict):
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2))

def run_task(ns) -> int:
    # Transforma argparse.Namespace -> Args
    args = Args(dataset=ns.dataset, alg=ns.alg.upper(),
                source=ns.source, target=ns.target, out=ns.out, verbose=ns.verbose)

    _ensure_out(args.out)
    _log(args.verbose, f"Ação={args.alg} | Dataset={args.dataset}")

    # --- Rotas simples para teste ---
    if args.alg == "METRICAS":
        info = _fake_graph_info(args.dataset)
        _write_json(args.out / "recife_global.json", info)
        print("✔ Métricas globais salvas em out/recife_global.json")
        return 0

    if args.alg in {"BFS", "DFS"}:
        if not args.source:
            print("✖ Necessário --source para BFS/DFS", file=sys.stderr)
            return 2

        # Carrega grafo (dict de dicts) a partir do dataset
        grafo = criar_grafo(str(args.dataset))

        if args.alg == "BFS":
            ordem, camadas = bfs(grafo, args.source)
            payload = {
                "algoritmo": "BFS",
                "source": args.source,
                "ordem_visita": ordem,
                "camadas": {str(k): v for k, v in camadas.items()}
            }
        else:  # DFS
            ordem = dfs(grafo, args.source)
            payload = {
                "algoritmo": "DFS",
                "source": args.source,
                "ordem_visita": ordem
            }

        _write_json(args.out / f"{args.alg.lower()}_{args.source}.json", payload)
        print(f"✔ {args.alg} executado. Saída em out/{args.alg.lower()}_{args.source}.json")
        return 0

    if args.alg == "DIJKSTRA":
        if not args.source or not args.target:
            print("✖ Necessário --source e --target para Dijkstra", file=sys.stderr)
            return 2
        # TODO: chamar dijkstra real
        payload = {
            "algoritmo": "DIJKSTRA",
            "source": args.source,
            "target": args.target,
            "custo_stub": 7.5,
            "caminho_stub": [args.source, "X", "Y", args.target]
        }
        _write_json(args.out / f"dist_{args.source}_to_{args.target}.json", payload)
        print(f"✔ Dijkstra (stub) executado. Saída em out/dist_{args.source}_to_{args.target}.json")
        return 0

    if args.alg == "BELLMAN_FORD":
        if not args.source:
            print("✖ Necessário --source para Bellman-Ford", file=sys.stderr)
            return 2
        # TODO: chamar bellman_ford real
        payload = {
            "algoritmo": "BELLMAN_FORD",
            "source": args.source,
            "tem_ciclo_negativo_stub": False,
            "distancias_stub": {"A": 0, "B": 3, "C": 5}
        }
        _write_json(args.out / f"bellman_ford_{args.source}.json", payload)
        print(f"✔ Bellman-Ford (stub) executado. Saída em out/bellman_ford_{args.source}.json")
        return 0

    if args.alg == "EGO":
        if not args.source:
            print("✖ Necessário --source para EGO", file=sys.stderr)
            return 2
        # TODO: calcular ego-network real
        payload = {
            "bairro": args.source,
            "grau_stub": 5,
            "ordem_ego_stub": 6,
            "tamanho_ego_stub": 7,
            "densidade_ego_stub": 0.46
        }
        _write_json(args.out / f"ego_{args.source}.json", payload)
        print(f"✔ Ego-subrede (stub) salva em out/ego_{args.source}.json")
        return 0

    if args.alg == "GRAUS":
        # TODO: gerar graus reais
        (args.out / "graus.csv").write_text("bairro,grau\nBoa Viagem,7\nPina,5\n")
        print("✔ graus.csv (stub) gerado em out/graus.csv")
        return 0

    if args.alg == "INTERACTIVE":
        # Apenas um ping para validar que o modo existe.
        # Quando o viz.py estiver pronto, chamar a função que gera o HTML.
        html = args.out / "grafo_interativo.html"
        html.write_text("<html><body><h3>Grafo Interativo (stub)</h3></body></html>")
        print("✔ Interativo (stub) gerado em out/grafo_interativo.html")
        return 0

    print(f"✖ Ação desconhecida: {args.alg}", file=sys.stderr)
    return 2
