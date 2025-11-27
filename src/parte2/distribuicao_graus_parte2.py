import pandas as pd

def distribuicao_graus(grafo):
    dados = []
    vertices = grafo.keys()

    for v in vertices:
        dados.append([v,len(grafo[v])])

    df = pd.DataFrame(columns=["cidade", "grau"], data= dados)

    df.to_csv('out/distribuicao_graus_parte2.csv', index= False)

    

