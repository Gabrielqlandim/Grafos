import pytest
from src.graphs.algorithms import dfs

@pytest.fixture
def grafo_simples():
    return {
        "A": {"B": 1, "C": 1},
        "B": {"D": 1},
        "C": {"D": 1},
        "D": {}
    }

def test_dfs_basico(grafo_simples):
    ordem, iteracoes = dfs(grafo_simples, "A")

    assert ordem[0] == "A"
    assert set(ordem) == {"A", "B", "C", "D"}
    assert ordem.index("A") < ordem.index("B")
    assert ordem.index("A") < ordem.index("C")

    #Se B for visitado antes de C, então D deve vir depois de B (profundidade)
    if ordem.index("B") < ordem.index("C"):
        assert ordem.index("B") < ordem.index("D")

    assert iteracoes >= len(ordem)
