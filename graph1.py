import os
import networkx as nx
import matplotlib.pyplot as plt

# Definindo os anos de interesse e os anos marcados para avaliação
anos = list(range(2010, 2026))  # 2010 a 2025
anos_marcos = [2012, 2016, 2020, 2024]

# Listas para armazenar as métricas
densidades = []
num_vertices = []
num_arestas = []
media_vizinhos = []

# Loop sobre cada ano para ler o arquivo e extrair as métricas
for ano in anos:
    # Formato do nome do arquivo: "ano_authors_network.gexf"
    nome_arquivo = f"anos/{ano}_authors_network.gexf"
    
    if not os.path.exists(nome_arquivo):
        print(f"Aviso: Arquivo {nome_arquivo} não encontrado. Pulando este ano.")
        densidades.append(None)
        num_vertices.append(None)
        num_arestas.append(None)
        media_vizinhos.append(None)
        continue

    # Ler o grafo do arquivo GEXF
    G = nx.read_gexf(nome_arquivo)
    
    # Calculando as métricas
    dens = nx.density(G)
    n_vertices = G.number_of_nodes()
    n_arestas = G.number_of_edges()
    # Média de vizinhos = média do grau dos nós (se o grafo for não direcionado,
    # a média é dada por 2 * num_arestas / num_vertices)
    media_deg = (2 * n_arestas / n_vertices) if n_vertices > 0 else 0

    # Armazenando as métricas
    densidades.append(dens)
    num_vertices.append(n_vertices)
    num_arestas.append(n_arestas)
    media_vizinhos.append(media_deg)

# Converter os dados para visualização (removendo pontos onde não houve arquivo, se necessário)
# Aqui, assumindo que os arquivos existem para todos os anos.

# Criação do gráfico com 4 subplots
fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle("Comportamento das Métricas dos Grafos (2010-2025)", fontsize=16)

# Plot para densidade
axs[0, 0].plot(anos, densidades, marker='o', linestyle='-', color='b')
axs[0, 0].set_title("Densidade da Rede")
axs[0, 0].set_xlabel("Ano")
axs[0, 0].set_ylabel("Densidade")
# Adiciona linhas tracejadas nos anos de avaliação
for ano_marco in anos_marcos:
    axs[0, 0].axvline(x=ano_marco, color='gray', linestyle='--')

# Plot para número de vértices
axs[0, 1].plot(anos, num_vertices, marker='o', linestyle='-', color='g')
axs[0, 1].set_title("Número de Vértices")
axs[0, 1].set_xlabel("Ano")
axs[0, 1].set_ylabel("Vértices")
for ano_marco in anos_marcos:
    axs[0, 1].axvline(x=ano_marco, color='gray', linestyle='--')

# Plot para número de arestas
axs[1, 0].plot(anos, num_arestas, marker='o', linestyle='-', color='r')
axs[1, 0].set_title("Número de Arestas")
axs[1, 0].set_xlabel("Ano")
axs[1, 0].set_ylabel("Arestas")
for ano_marco in anos_marcos:
    axs[1, 0].axvline(x=ano_marco, color='gray', linestyle='--')

# Plot para número médio de vizinhos (grau médio)
axs[1, 1].plot(anos, media_vizinhos, marker='o', linestyle='-', color='m')
axs[1, 1].set_title("Número Médio de Vizinhos")
axs[1, 1].set_xlabel("Ano")
axs[1, 1].set_ylabel("Grau Médio")
for ano_marco in anos_marcos:
    axs[1, 1].axvline(x=ano_marco, color='gray', linestyle='--')

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
