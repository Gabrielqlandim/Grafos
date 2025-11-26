from src.graphs.algorithms import bellman_ford

def test_sem_ciclo():
    grafo_sem_ciclo = {
        "A": {"B": 4, "C": 5},
        "B": {"D": -2},
        "C": {"D": 1},
        "D": {},
    }

    resultado = bellman_ford(grafo_sem_ciclo, "A")

    distancias = resultado["Distâncias"]
    assert resultado["CicloNegativo"] is False
    
    assert distancias["D"] == 2

def test_com_ciclo():
    grafo_com_ciclo = {
        "A": {"B": 1},
        "B": {"C": -1},
        "C": {"A": -1},
    }

    resultado = bellman_ford(grafo_com_ciclo, "A")
    assert resultado["CicloNegativo"] is True