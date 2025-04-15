import os
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from joypy import joyplot

# 1) Ler os grafos e organizar os dados
anos = range(2010, 2026)

# Lista para armazenar dataframes individuais
lista_dfs = []
edges_dict = {}  # para mapear ano -> número de arestas

for ano in anos:
    nome_arquivo = f"anos/{ano}_authors_network.gexf"
    if not os.path.exists(nome_arquivo):
        print(f"[AVISO] Arquivo {nome_arquivo} não encontrado. Pulando...")
        continue

    # Ler o grafo
    G = nx.read_gexf(nome_arquivo)
    
    # Extrair graus (número de vizinhos) para cada nó
    graus = [d for _, d in G.degree()]  # G.degree() retorna tuplas (node, grau)
    
    # Salvar número de arestas
    edges_dict[ano] = G.number_of_edges()
    
    # Criar um DataFrame com (grau, ano, edges_ano)
    df_temp = pd.DataFrame({
        'degree': graus,
        'year': ano,
        'edges_year': edges_dict[ano]
    })
    lista_dfs.append(df_temp)

# Concatenar todos os dataframes
df = pd.concat(lista_dfs, ignore_index=True)

# 2) Preparar o mapeamento de cores
#    Vamos criar uma escala de cores do "mais claro" (poucas arestas) ao "mais escuro/vermelho" (mais arestas).
min_edges = df['edges_year'].min()
max_edges = df['edges_year'].max()

# Função para normalizar e mapear para uma colormap
# Aqui vamos usar, por exemplo, cmap="Reds".
cmap = plt.cm.Reds
norm = mcolors.Normalize(vmin=min_edges, vmax=max_edges)

def color_por_ano(ano):
    """Retorna uma cor baseada no número de arestas daquele ano."""
    e = edges_dict[ano]
    return cmap(norm(e))

# 3) Preparar os dados no formato que o joypy espera
#    Precisamos de colunas "year" para agrupar e "degree" para plotar a distribuição.
#    O joypy permite passar um DataFrame e dizer qual coluna é "by" e qual é "column".

# 4) Plotar o Joyplot (Ridgeline)
#    Parâmetros importantes:
#    - by='year': agrupar por ano
#    - column='degree': valor numérico para gerar as densidades
#    - overlap: controla a sobreposição vertical das curvas
#    - colormap: podemos passar None se formos definir as cores manualmente
#    - color: podemos usar um dict de {grupo: cor}, mas joypy facilita com "fade=True" etc.

# Para definir uma cor distinta para cada "year", usaremos um mapeamento
years_sorted = sorted(df['year'].unique())

# Vamos criar uma lista de cores, na mesma ordem dos anos
colors_for_years = [color_por_ano(ano) for ano in years_sorted]

# Criação do ridgeline chart
fig, axes = joyplot(
    data=df,
    by="year",
    column="degree",
    overlap=0.6,         # controla a sobreposição vertical (maior => mais sobreposto)
    linewidth=1,
    alpha=0.9,           # transparência das curvas
    range_style='own',   # cada curva ajusta seu próprio range
    kind='kde',          # usar Kernel Density Estimate (função de densidade)
    # Se quisermos as cores personalizadas, podemos passar `color` como lista no parâmetro `color`
    color=colors_for_years,
    legend=False,
    figsize=(10, 12)
)

# Ajustar rótulos e layout
plt.title("Distribuição do Grau dos Nós (Número de Vizinhos) - Ridgeline Chart")
plt.xlabel("Grau (Número de vizinhos)")

# Podemos customizar o eixo Y para mostrar somente alguns valores (ou o nome do ano).
# Por padrão, joypy já exibe os grupos no eixo Y. Mas podemos ajustá-lo:
plt.tight_layout()
plt.show()
