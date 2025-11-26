import pytest
from src.graphs.algorithms import bfs


@pytest.fixture
def grafo():
    return {
        "A": {"B": 1, "C": 1},
        "B": {"A": 1, "D": 1},
        "C": {"A": 1, "D": 1},
        "D": {"B": 1, "C": 1},
    }

def test_bfs(grafo):
    camada = bfs(grafo, "A")

    assert set(camada[0]) == {"A"}
    assert set(camada[1]) == {"B", "C"}
    assert set(camada[2]) == {"D"}