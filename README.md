# Projeto Grafos – 2ª Unidade

## Descrição
Este projeto consiste na construção e análise de grafos aplicados a dois contextos:  
1. **Bairros do Recife** – grafos ponderados representando bairros e ruas, permitindo cálculos de menor caminho, subgrafos, e métricas de conectividade.  
2. **Voos na Índia (SpiceJet)** – grafos ponderados e multigrafos representando cidades conectadas por voos, permitindo comparação de algoritmos e análise de desempenho.

---

## Integrantes
- Gabriel Landim
- Maria Fernanda Ordonho
- Pedro Sampaio
- Rafaela Vidal

## Estrutura do Projeto

```bash
project/
├── data/
│   ├── adjacencias_bairros.csv
│   ├── airlines_flights_data.csv
│   ├── airlines_spicejet.csv
│   ├── bairros_recife.csv
│   ├── bairros_unique.csv
│   └── enderecos.csv
│
├── out/
│   ├── .gitkeep
│   ├── arvore_percurso.png
│   ├── bfs_Boa Viagem.json
│   ├── dfs_Boa Viagem.json
│   ├── dist_Boa Viagem_to_Pina.json
│   ├── distancias_enderecos.csv
│   ├── distribuicao_graus_parte2.csv
│   ├── ego_bairro.csv
│   ├── ego_Boa Viagem.json
│   ├── grafo_interativo_parte1.html
│   ├── grafo_interativo_parte2.html
│   ├── grafo_interativo.html
│   ├── graus.csv
│   ├── histograma_graus.png
│   ├── mapa_cores.png
│   ├── microrregioes.json
│   ├── parte2_report.json
│   ├── percurso_nova_descoberta_setubal.json
│   ├── recife_global.json
│   └── subgrafo_top10.png
│
├── src/
│   │
│   ├── graphs/
│   │   ├── __init__.py
│   │   ├── algorithms.py
│   │   ├── graph.py
│   │   ├── histograma_graus.py
│   │   ├── io.py
│   │   ├── mapa_cores.py
│   │   ├── metrics.py
│   │   └── subgrafo_top10.py
│   │
│   ├── parte2/
│   │   ├── __init__.py
│   │   ├── distribuicao_graus_parte2.py
│   │   ├── filtrar_csv.py
│   │   └── main_2.py
|   |
│   ├── cli.py
│   ├── front_inicial.py
│   ├── front_part1.py
│   ├── front_part2.py
│   └── solve.py
│
├── tests/
│   ├── test_bellman_ford.py
│   ├── test_bfs.py
│   ├── test_dfs.py
│   └── test_dijkstra.py
│
├── .gitignore
├── README.md
└── requirements.txt


```
---

## Algoritmos Implementados
- **BFS** – Busca em largura  
- **DFS** – Busca em profundidade  
- **Dijkstra** – Menor caminho em grafos ponderados sem arestas negativas  
- **Bellman-Ford** – Menor caminho em grafos ponderados, permite arestas negativas e detecção de ciclos negativos  

---

## Arquivos Principais
- `adjacencias_bairros.csv` – Lista de adjacências dos bairros do Recife  
- `bairros_recife.csv` / `bairros_unique.csv` – Informações dos bairros e microrregiões  
- `enderecos.csv` – Endereços para cálculo de distâncias  
- `airlines_spicejet.csv` – Dados filtrados da SpiceJet para análise de grafos de voos  
- Saídas importantes: `out/graus.csv`, `out/ego_bairro.csv`, `out/subgrafo_top10.png`, `out/grafo_interativo.html`  

---

## Como Rodar

### Parte 1 – Bairros do Recife
```bash
# BFS
python -m src.cli --dataset data/adjacencias_bairros.csv --alg BFS --source "Boa Viagem"

# DFS
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DFS --source "Boa Viagem"

# Dijkstra
python -m src.cli --dataset data/adjacencias_bairros.csv --alg DIJKSTRA --source "Boa Viagem" --target "Pina"

# Métricas gerais
python -m src.cli --dataset data/adjacencias_bairros.csv --alg METRICAS

# Subgrafo top 10 bairros
python -m src.cli --alg SUBGRAFO_TOP10 --dataset data/adjacencias_bairros.csv --out out --k 10

```
### Parte 2 – Voos SpiceJet
```bash
python -m src.parte2.main_2
```
Testes
```bash
python -m pytest -q
```

## Visualização Interativa
O arquivo out/grafo_interativo.html funciona como menu para navegar entre:

- Grafo dos bairros do Recife
- Grafo de voos (Parte 2)

## Para abrir:

1. Instalar a extensão Live Server no VS Code

2. Clicar com o botão direito em grafo_interativo.html → Open with Live Server


