import pytest
from src.graphs.algorithms import dijkstra


def test_dijkstra_caminho_correto():
    grafo = {
        "A": {"B": [1], "C": [4]},
        "B": {"C": [2], "D": [5]},
        "C": {"D": [1,9], "B": [2]},
        "D": {"C": [1,9], "B": [5]},
    }

    resultado = dijkstra(grafo, "A", "D")

    assert resultado["Distância"] == 4
    assert resultado["Caminho"] == ["A", "B", "C", "D"]


def test_dijkstra_recusa_peso_negativo():
    grafo = {
        "A": {"B": [1,4]},
        "B": {"C": [-2], "A": [1,4]},
        "C": {"B": [-2]},
    }

    with pytest.raises(ValueError):
        dijkstra(grafo, "A", "C")
