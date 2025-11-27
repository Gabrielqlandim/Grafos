from src.graphs.algorithms import bfs


def test_bfs():
    grafo = {
        "A": {"B": [1, 4], "C": [1]},
        "B": {"A": [1, 4], "D": [1]},
        "C": {"A": [1], "D": [1]},
        "D": {"B": [1], "C":[1]},
    }

    ordem, camadas = bfs(grafo, "A")

    assert set(camadas[0]) == {"A"}

    assert set(camadas[1]) == {"B", "C"}

    assert set(camadas[2]) == {"D"}

