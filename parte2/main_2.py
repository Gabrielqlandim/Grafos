from src.graphs.graph import Grafo
from src.graphs.io import criar_grafo
from src.graphs.algorithms import *
import time

g = criar_grafo('out/airlines_spicejet.csv')

inicio_dfs = time.time()
ordem, iteracoes = dfs(g, 'Delhi')
fim_dfs = time.time()

inicio_bfs = time.time()
ordem_bfs, iteracoes_bfs = bfs(g, 'Delhi')
fim_bfs = time.time