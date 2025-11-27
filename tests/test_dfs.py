from src.graphs.algorithms import dfs, dfs_analise

def test_dfs_detecta_ciclo():
    grafo = {
        "A": {"B": [1], "C": [1,1]},
        "B": {"C": [1], "A": [1]},
        "C": {"A": [1,1], "C": [1]},  
    }

    resultado = dfs_analise(grafo, "A")

    assert resultado["tem_ciclo"] is True
    assert any(
        tipo == "back" for tipo in resultado["tipos_arestas"].values()
    )


def test_dfs_classificacao_sem_ciclo():
    grafo = {
        "A": {"B": [1, 6], "C":[1]},
        "B": {"D": [1]},   
        "C": {"D": [1]},   
        "D": {} 
    }

    resultado = dfs_analise(grafo, "A")

    assert resultado["tem_ciclo"] is False
    assert "back" not in resultado["tipos_arestas"].values()
    
def test_dfs_basico():
    grafo = {
        "A": {"B": [1,4], "C": [1]},
        "B": {"D":[1], "A":[1,4]},
        "C": {"D": [1], "A":[1]},
        "D": {"B": [1], "C":[1]}
    }
    ordem, iteracoes = dfs(grafo, "A")

    assert ordem[0] == "A"
    assert set(ordem) == {"A", "B", "C", "D"}
    assert ordem.index("A") < ordem.index("B")
    assert ordem.index("A") < ordem.index("C")

    #Se B for visitado antes de C, então D deve vir depois de B (profundidade)
    if ordem.index("B") < ordem.index("C"):
        assert ordem.index("B") < ordem.index("D")

    assert iteracoes >= len(ordem)
