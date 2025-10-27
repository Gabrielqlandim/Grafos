def bfs(grafo, inicio):
    """
    Busca em largura a partir de 'inicio'.

    Retorna:
    - ordem: lista com a ordem de visita dos vértices
    - camadas: dict nivel(int) -> lista de vértices naquele nível
    """
    if inicio not in grafo:
        return [], {}

    visitados = set()
    ordem = []
    camadas = {}

    fila = [inicio]
    niveis = {inicio: 0}
    visitados.add(inicio)

    while fila:
        atual = fila.pop(0)
        ordem.append(atual)

        nivel_atual = niveis[atual]
        if nivel_atual not in camadas:
            camadas[nivel_atual] = []
        camadas[nivel_atual].append(atual)

        # Vizinho é a chave do dict interno; o peso é ignorado
        for vizinho in grafo.get(atual, {}):
            if vizinho not in visitados:
                visitados.add(vizinho)
                niveis[vizinho] = nivel_atual + 1
                fila.append(vizinho)

    return ordem, camadas


def dfs(grafo, inicio, visitados=None, ordem=None):
    """
    Busca em profundidade (recursiva) a partir de 'inicio'.

    Retorna a ordem de visita como uma lista.
    """
    if inicio not in grafo:
        return []

    if visitados is None:
        visitados = set()
    if ordem is None:
        ordem = []

    visitados.add(inicio)
    ordem.append(inicio)

    for vizinho in grafo.get(inicio, {}):
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados, ordem)

    return ordem
