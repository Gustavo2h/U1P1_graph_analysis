import networkx as nx
import matplotlib.pyplot as plt

# 1. Carrega o grafo geral a partir do arquivo "2010-2025.gexf"
arquivo_geral = "avaliacao_geral/2010-2025.gexf"
G = nx.read_gexf(arquivo_geral)
print(f"Grafo geral carregado com {G.number_of_nodes()} vértices e {G.number_of_edges()} arestas.")

# 2. Gerar o subgrafo contendo os vértices com grau ≥ 14
nodos_filtrados = [n for n, grau in G.degree() if grau >= 20]
G_sub = G.subgraph(nodos_filtrados)
print(f"Subgrafo gerado com {G_sub.number_of_nodes()} vértices e {G_sub.number_of_edges()} arestas (vértices com grau >= 14).")

# 3. Calcular a densidade do grafo geral e do subgrafo
densidade_geral = nx.density(G)
densidade_sub = nx.density(G_sub)

print(f"\nDensidade do grafo geral: {densidade_geral:.4f}")
print(f"Densidade do subgrafo: {densidade_sub:.4f}")

# 4. Visualização dos grafos

# (a) Visualização do grafo geral
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
pos_geral = nx.spring_layout(G, seed=42)  # Layout para melhor distribuição
nx.draw_networkx_nodes(G, pos_geral, node_size=20, node_color="lightblue", alpha=0.7)
nx.draw_networkx_edges(G, pos_geral, edge_color="gray", alpha=0.5)
plt.title("Grafo Geral (2010-2025)")
plt.axis("off")

# (b) Visualização do subgrafo (vértices com grau >= 14)
plt.subplot(1, 2, 2)
pos_sub = nx.spring_layout(G_sub, seed=42)
nx.draw_networkx_nodes(G_sub, pos_sub, node_size=50, node_color="orange", alpha=0.8)
nx.draw_networkx_edges(G_sub, pos_sub, edge_color="gray", alpha=0.7)
#nx.draw_networkx_labels(G_sub, pos_sub, font_size=8)
plt.title("Subgrafo (vértices com ≥ 20 vizinhos)")
plt.axis("off")
plt.tight_layout()
plt.show()

# 5. Selecionar o vértice com mais arestas e analisar sua rede ego

# Selecionar o vértice com maior grau
vertice_max, grau_max = max(G.degree(), key=lambda x: x[1])
print(f"\nVértice com mais arestas: '{vertice_max}' com grau {grau_max}")

# Gerar a rede ego do vértice selecionado
ego_G = nx.ego_graph(G, vertice_max)

# Visualização da rede ego
plt.figure(figsize=(8,8))
pos_ego = nx.spring_layout(ego_G, seed=42)
nx.draw_networkx_nodes(ego_G, pos_ego, node_size=100, node_color="lightgreen")
nx.draw_networkx_edges(ego_G, pos_ego, edge_color="blue")
#nx.draw_networkx_labels(ego_G, pos_ego, font_size=10)
plt.title(f"Ego Network do vértice '{vertice_max}'")
plt.axis("off")
plt.show()
