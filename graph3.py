import os
import networkx as nx
import matplotlib.pyplot as plt

# Lista dos períodos que possuem um arquivo de grafo (formato: "2010-2012.gexf", etc.)
periodos = ["2010-2012", "2013-2016", "2017-2020", "2021-2024"]

# Loop para processar cada período individualmente
for periodo in periodos:
    nome_arquivo = f"avaliacao_geral/{periodo}.gexf"
    if not os.path.exists(nome_arquivo):
        print(f"[AVISO] Arquivo {nome_arquivo} não encontrado. Pulando este período.")
        continue
    
    # Ler o grafo
    G = nx.read_gexf(nome_arquivo)
    
    # Cálculo do grau de cada nó (número de vizinhos)
    degrees = dict(G.degree())
    
    # Identificar os top 5 nós com maior número de vizinhos
    top_5 = sorted(degrees, key=degrees.get, reverse=True)[:5]
    
    # Definir o tamanho dos nós proporcional ao grau.
    # Ajuste o fator multiplicador conforme necessário para uma visualização adequada.
    factor_node = 50  
    node_sizes = [degrees[n] * factor_node for n in G.nodes()]
    
    # Ajustar o layout para evitar que os nós fiquem amontoados.
    # Uma sugestão é usar o spring_layout com um parâmetro 'k' dependente do número de nós.
    n_nodes = G.number_of_nodes()
    k_value = 1.0 / (n_nodes ** 0.5) if n_nodes > 0 else 0.2  # quanto menor 'n_nodes', menor 'k'
    pos = nx.spring_layout(G, k=k_value, seed=42)
    
    # Preparar as configurações para as arestas:
    # - Cor: "red" se ambos os nós conectados possuem is_permanent == True, caso contrário "black".
    # - Largura: proporcional à média das citações dos nós (propriedade "citation_num").
    edge_colors = []
    edge_widths = []
    
    for u, v in G.edges():
        # Verifica a propriedade "is_permanent" nos nós u e v.
        is_perm_u = G.nodes[u].get("is_permanent", False)
        is_perm_v = G.nodes[v].get("is_permanent", False)
        if is_perm_u and is_perm_v:
            edge_colors.append("red")
        else:
            edge_colors.append("black")
        
        # Obter as citações; caso a propriedade não exista, assume 0.
        citation_u = G.nodes[u].get("citation_num", 0)
        citation_v = G.nodes[v].get("citation_num", 0)
        media_citacoes = (citation_u + citation_v) / 2.0
        
        # Define a largura; ajuste o fator divisor para que os valores fiquem visualmente proporcionais.
        largura = 0.5 + media_citacoes / 20.0
        edge_widths.append(largura)
    
    # Criar uma nova figura para este grafo
    plt.figure(figsize=(12, 10))
    plt.title(f"Grafo do período {periodo}", fontsize=16)
    
    # Desenha as arestas
    nx.draw_networkx_edges(G, pos,
                           edge_color=edge_colors,
                           width=edge_widths)
    
    # Desenha todos os nós (com tamanho proporcional ao grau)
    nx.draw_networkx_nodes(G, pos,
                           node_size=node_sizes,
                           node_color="lightblue",
                           edgecolors="black")
    
    # Destaca os top 5 nós:
    # - Usa uma cor diferenciada ("orange") e um tamanho maior.
    factor_top = 50  # fator para aumentar o tamanho dos nós destacados
    nx.draw_networkx_nodes(G, pos,
                           nodelist=top_5,
                           node_color="orange",
                           node_size=[degrees[n] * factor_top for n in top_5],
                           edgecolors="red")
    
    # Adiciona labels apenas para os top 5 (pode ser o ID ou outra propriedade)
    labels_top5 = {n: n for n in top_5}
    nx.draw_networkx_labels(G, pos,
                            labels=labels_top5,
                            font_color="white",
                            font_size=12,
                            font_weight="bold")
    
    plt.axis("off")
    plt.tight_layout()
    plt.show()
