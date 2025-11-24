def bfs(grafo, inicio):

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


def dfs(grafo, inicio, visitados=None, ordem=None, iteracoes=0):

    #Caso o vértice não esteja  no grafo, retorna vazio
    if inicio not in grafo:
        return []

    #Inicia a lista de visitados
    if visitados is None:
        visitados = set()
    
    #Cria a lista com a ordem dos vértices visitados
    if ordem is None:
        ordem = []

    iteracoes += 1

    visitados.add(inicio)
    ordem.append(inicio)

    for vizinho in grafo.get(inicio, {}):
        if vizinho not in visitados:
            a, iteracoes = dfs(grafo, vizinho, visitados, ordem, iteracoes)

    return ordem, iteracoes

def dijkstra(grafo, inicio, destino = None):

    #Distâncias mínimas acumuladas
    #Inicia as distâncias como infinito
    dist = {v: float('inf') for v in grafo}
    dist[inicio] = 0

    #Dicionário para armazenar o antecessor de cada vértice
    anterior = {v: None for v in grafo}

    #Vértices visitados
    visitados = set()

    while len(visitados) < len(grafo):
        # Seleciona o vértice com menor distância ainda não visitado
        atual = None
        menor_dist = float('inf')

        #Percorre os vértices do grafo
        for v in grafo:

            #Caso o vértice ainda não tenha sido visitado e sua distância seja menor que a menor distância registrada, escolhe ele como o atual
            if v not in visitados and dist[v] < menor_dist:
                atual = v
                menor_dist = dist[v]

        #Caso não encontre um vértice atual, encerra o algorítmo
        if atual is None:  
            break
        
        #Encerra caso o destino seja encontrado antes do fim do algorítmo
        if atual == destino:
            break

        #Marca o vértice atual como visitado
        visitados.add(atual)

        #Atualiza distâncias dos vizinhos
        for vizinho, peso in grafo[atual].items():

            #Caso o vértice vizinho não tenha sido fechado, atualiza a distância dele
            if vizinho not in visitados:
                nova_dist = dist[atual] + peso
                if nova_dist < dist[vizinho]:
                    dist[vizinho] = nova_dist
                    anterior[vizinho] = atual

    #Caso não seja passado um destino, retorna tudo
    if destino is None:
        return dist

    #Reconstrói o caminho do início até o destino
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = anterior[atual]

    return {"Distância":dist[destino], "Caminho": caminho}


def bellman_ford(grafo, inicio, destino=None):
    # Inicializa as distâncias
    dist = {v: float('inf') for v in grafo}
    dist[inicio] = 0

    # Dicionário com o antecessor de cada vértice
    anterior = {v: None for v in grafo}

    # Lista de arestas (origem, destino, peso)
    arestas = []
    for u in grafo:
        for v, peso in grafo[u].items():
            arestas.append((u, v, peso))

    n = len(grafo)

    # Relaxa todas as arestas |V|-1 vezes
    for _ in range(n - 1):
        mudou = False

        # Para cada aresta, tenta relaxar
        for u, v, peso in arestas:
            # Só tenta relaxar se a distância de u já não for infinita
            if dist[u] != float('inf') and dist[u] + peso < dist[v]:
                dist[v] = dist[u] + peso
                anterior[v] = u
                mudou = True

        # Se nenhuma distância mudou, pode parar
        if not mudou:
            break

    # Verificação de ciclo negativo
    ciclo_negativo = False
    for u, v, peso in arestas:
        if dist[u] != float('inf') and dist[u] + peso < dist[v]:
            ciclo_negativo = True
            break

    # Se não tiver destino definido, retorna apenas distâncias e flags
    if destino is None:
        return {
            "Distâncias": dist,
            "Anterior": anterior,
            "CicloNegativo": ciclo_negativo
        }

    # Reconstrói o caminho do início até o destino
    caminho = []
    atual = destino
    while atual is not None:
        caminho.insert(0, atual)
        atual = anterior[atual]

    return {
        "Distância": dist[destino],
        "Caminho": caminho,
        "CicloNegativo": ciclo_negativo
    }
