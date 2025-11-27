from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

def gerar_histograma_csv(caminho_csv, coluna, caminho_saida, titulo):
    # lê o CSV
    df = pd.read_csv(caminho_csv)
    
    # pega os valores da coluna 'duration'
    valores = df[coluna].dropna().tolist()
    
    # prepara para salvar o arquivo sem dar erro
    caminho_saida = Path(caminho_saida)
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    
    # como os valores vão ser agrupados
    minimo = int(min(valores))
    maximo = int(max(valores))
    bins = range(minimo, maximo + 2)  
    
    # cria a imagem
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.hist(valores, bins=bins, edgecolor="black", align="left")
    ax.set_xlabel(coluna)
    ax.set_ylabel("Quantidade de voos")
    ax.set_title(titulo)
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    
    # salva a imagem
    fig.tight_layout()
    fig.savefig(caminho_saida, dpi=300, bbox_inches="tight")
    plt.close(fig)

gerar_histograma_csv(
    caminho_csv="data/airlines_spicejet.csv",
    coluna="duration",
    caminho_saida="out/histograma_duração.png",
    titulo="Distribuição da Duração dos Voos"
)
