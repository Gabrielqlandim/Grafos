import pandas as pd

def distribuicao_graus(grafo):
    dados = []

    #percorre todos os vértices do grafo
    for v in grafo:
        grau = 0

        #percorre o dicionário interno (conexões)
        for vizinho, pesos in grafo[v].items():
            #Adiciona o tamanho da lista de conexões com cada vértice na contagem do grau
            grau += len(pesos)

        dados.append([v, grau])

    df = pd.DataFrame(columns=["cidade", "grau"], data=dados)
    df.to_csv('out/distribuicao_graus_parte2.csv', index=False)

    

