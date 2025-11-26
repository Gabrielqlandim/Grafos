from src.graphs.algorithms import bellman_ford
import pytest

@pytest.fixture
def grafo_sem_ciclo():
    return{
        "A": {"B": 4, "C": 5},
        "B": {"D": -2},
        "C": {"D": 1},
        "D": {},
    }


@pytest.fixture
def grafo_com_ciclo():
    return {
        "A": {"B": 1},
        "B": {"C": -1},
        "C": {"A": -1},
    }

def test_sem_ciclo(grafo_sem_ciclo):
    resultado = bellman_ford(grafo_sem_ciclo, "A")

    distancia = resultado["Distâncias"]
    assert resultado["CicloNegativo"] is False
    assert distancia["C"] == 2

def test_com_ciclo(grafo_com_ciclo):
    resultado = bellman_ford(grafo_com_ciclo, "A")
    assert resultado["CicloNegativo"] is True