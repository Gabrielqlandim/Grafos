import pytest
from src.graphs.algorithms import dijkstra


def test_dijkstra_caminho_correto():
    grafo = {
        "A": {"B": 1, "C": 4},
        "B": {"C": 2, "D": 5},
        "C": {"D": 1},
        "D": {},
    }

    resultado = dijkstra(grafo, "A", "D")

    assert resultado["Distância"] == 4
    assert resultado["Caminho"] == ["A", "B", "C", "D"]


def test_dijkstra_recusa_peso_negativo():
    grafo = {
        "A": {"B": 1},
        "B": {"C": -2},
        "C": {},
    }

    with pytest.raises(ValueError):
        dijkstra(grafo, "A", "C")
