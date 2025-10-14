<h1>📊 Grafos do Recife</h1>
  <p><strong>Projeto final da disciplina de Teoria dos Grafos — CESAR School</strong></p>

  <div class="card">
    <h2>🎯 Objetivo</h2>
    <p>Construir e analisar o <strong>grafo dos bairros do Recife</strong>, implementando algoritmos clássicos (BFS, DFS, Dijkstra e Bellman-Ford) sem o uso de bibliotecas prontas. O projeto gera métricas, visualizações e comparações de desempenho em um dataset ampliado.</p>
  </div>

  <div class="card">
    <h2>👥 Integrantes</h2>
    <ul>
      <li>👤 <a href="https://github.com/gabrielqlandim" target="_blank">Gabriel Landim</a> — Derretimento e dados</li>
      <li>⚙️ <a href="https://github.com/nandaord" target="_blank">Pedro Sampaio</a> — Algoritmos e testes</li>
      <li>📈 <a href="https://github.com/nandaord" target="_blank">Maria Fernanda Ordonho</a> — Estrutura e métricas</li>
      <li>🎨 <a href="https://github.com/rafabvidal" target="_blank">Rafaela Vidal</a> — Visualizações e Parte 2</li>
    </ul>
  </div>

  <div class="card">
    <h2>▶️ Instruções para executar</h2>
    <p>Instale as dependências (recomenda-se ambiente virtual):</p>
    <pre><code>pip install -r requirements.txt</code></pre>
    <p>Execute o projeto (exemplo):</p>
    <pre><code>python -m src.cli --dataset ./data/bairros_recife.csv --alg BFS --source "Boa Viagem"</code></pre>
  </div>

  <div class="card">
    <h2>📂 Estrutura do projeto</h2>
    <pre><code>projeto-grafos/
├─ data/
│  ├─ bairros_recife.csv
│  ├─ adjacencias_bairros.csv
│  └─ enderecos.csv
├─ src/
│  ├─ graphs/
│  │  ├─ io.py
│  │  ├─ graph.py
│  │  └─ algorithms.py
│  ├─ cli.py
│  └─ solve.py
├─ out/
└─ tests/</code></pre>
  </div>
</body>
</html>
