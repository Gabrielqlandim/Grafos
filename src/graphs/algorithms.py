
def dfs(grafo, inicio, visitados=None):

    #Cria uma lista para marcar os vértices já visitados
    if visitados is None:
        visitados = set()  #Usei o Set ao invés de lista pois ele não permite duplicatas por padrão
    
    #Adiciona o vértice analisado
    visitados.add(inicio)
    print(inicio)
    
    #Percorre todos os vértices adjacentes ao analisado
    for vizinho in grafo[inicio]:

        #Caso o vértice não esteja nos visitados, chama a função recursivamente
        if vizinho not in visitados:
            dfs(grafo, vizinho, visitados)
    
    #Retorna a lista dos vértices visitados
    return visitados
