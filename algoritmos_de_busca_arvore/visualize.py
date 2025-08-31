import plotly.graph_objects as go
import plotly.figure_factory as ff
from algoritmos_de_busca_arvore.tree import Tree
import math

def tree_to_plotly_data(tree):
    """
    Converte a estrutura de árvore para dados do Plotly
    """
    nodes = []
    edges = []
    edge_weights = []
    
    def collect_data(node, parent=None, level=0):
        nodes.append({
            'id': node.value,
            'level': level,
            'parent': parent.value if parent else None
        })
        
        if parent:
            edges.append((parent.value, node.value))
            edge_weights.append(node.cost)
        
        for child in node.childs:
            collect_data(child, node, level + 1)
    
    collect_data(tree.root)
    return nodes, edges, edge_weights

def calculate_tree_positions(nodes):
    """
    Calcula posições para os nós usando um layout de árvore hierárquico melhorado
    """
    # Organiza nós por nível
    levels = {}
    for node in nodes:
        level = node['level']
        if level not in levels:
            levels[level] = []
        levels[level].append(node)
    
    positions = {}
    
    # Função recursiva para calcular largura da subárvore
    def calculate_subtree_width(node_id, nodes):
        children = [n for n in nodes if n['parent'] == node_id]
        if not children:
            return 1
        
        total_width = 0
        for child in children:
            total_width += calculate_subtree_width(child['id'], nodes)
        
        return max(total_width, 1)
    
    # Posiciona os nós nível por nível
    max_level = max(levels.keys()) if levels else 0
    
    for level in range(max_level + 1):
        nodes_at_level = levels[level]
        y = max_level - level  # Y decresce conforme nível aumenta
        
        if level == 0:
            # Raiz no centro
            positions[nodes_at_level[0]['id']] = (0, y)
        else:
            # Agrupa nós por pai
            parent_groups = {}
            for node in nodes_at_level:
                parent_id = node['parent']
                if parent_id not in parent_groups:
                    parent_groups[parent_id] = []
                parent_groups[parent_id].append(node)
            
            for parent_id, children in parent_groups.items():
                if parent_id in positions:
                    parent_x = positions[parent_id][0]
                    num_children = len(children)
                    
                    if num_children == 1:
                        # Filho único fica diretamente abaixo do pai
                        positions[children[0]['id']] = (parent_x, y)
                    else:
                        # Múltiplos filhos: distribui com espaçamento maior
                        spacing = 4  # Aumentado de 2 para 4
                        total_width = (num_children - 1) * spacing
                        start_x = parent_x - total_width / 2
                        
                        for i, child in enumerate(children):
                            x = start_x + i * spacing
                            positions[child['id']] = (x, y)
    
    # Segunda passada: ajusta posições para evitar sobreposições
    # Separa mais os ramos principais (filhos da raiz)
    root_children = [n for n in nodes if n['level'] == 1]
    if len(root_children) > 1:
        # Aumenta espaçamento entre ramos principais
        main_spacing = 8  # Espaçamento maior entre ramos principais
        total_width = (len(root_children) - 1) * main_spacing
        start_x = -total_width / 2
        
        for i, child in enumerate(root_children):
            old_x = positions[child['id']][0]
            new_x = start_x + i * main_spacing
            offset = new_x - old_x
            
            # Move toda a subárvore
            def move_subtree(node_id, offset):
                if node_id in positions:
                    x, y = positions[node_id]
                    positions[node_id] = (x + offset, y)
                
                # Move recursivamente todos os descendentes
                descendants = [n for n in nodes if n['parent'] == node_id]
                for desc in descendants:
                    move_subtree(desc['id'], offset)
            
            move_subtree(child['id'], offset)
    
    return positions

def visualize_tree_plotly(tree, caminho_encontrado=None):
    """
    Visualiza a árvore usando Plotly
    """
    nodes, edges, edge_weights = tree_to_plotly_data(tree)
    positions = calculate_tree_positions(nodes)
    
    # Identifica elementos do caminho
    path_nodes = set(caminho_encontrado) if caminho_encontrado else set()
    path_edges = set()
    if caminho_encontrado:
        for i in range(len(caminho_encontrado) - 1):
            path_edges.add((caminho_encontrado[i], caminho_encontrado[i + 1]))
    
    # Prepara dados para plotagem
    edge_x = []
    edge_y = []
    edge_colors = []
    edge_widths = []
    
    for i, (start, end) in enumerate(edges):
        x0, y0 = positions[start]
        x1, y1 = positions[end]
        
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Define cor e largura baseado se está no caminho
        if (start, end) in path_edges:
            edge_colors.extend(['darkgreen', 'darkgreen', 'darkgreen'])
            edge_widths.append(4)
        else:
            edge_colors.extend(['lightgray', 'lightgray', 'lightgray'])
            edge_widths.append(1)
    
    # Cria figura
    fig = go.Figure()
    
    # Adiciona arestas
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        mode='lines',
        line=dict(color='lightgray', width=1),
        hoverinfo='none',
        showlegend=False,
        name='Arestas'
    ))
    
    # Adiciona arestas do caminho separadamente (mais grossas)
    if path_edges:
        path_edge_x = []
        path_edge_y = []
        
        for start, end in path_edges:
            x0, y0 = positions[start]
            x1, y1 = positions[end]
            path_edge_x.extend([x0, x1, None])
            path_edge_y.extend([y0, y1, None])
        
        fig.add_trace(go.Scatter(
            x=path_edge_x,
            y=path_edge_y,
            mode='lines',
            line=dict(color='darkgreen', width=4),
            hoverinfo='none',
            showlegend=False,
            name='Caminho'
        ))
    
    # Adiciona nós
    node_x = []
    node_y = []
    node_text = []
    node_colors = []
    
    for node in nodes:
        x, y = positions[node['id']]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node['id'])
        
        # Define cor baseado se está no caminho
        if node['id'] in path_nodes:
            node_colors.append('lightgreen')
        else:
            node_colors.append('lightgray')
    
    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(
            size=40,
            color=node_colors,
            line=dict(width=2, color='black')
        ),
        text=node_text,
        textposition='middle center',
        textfont=dict(size=14, color='black'),
        hoverinfo='text',
        hovertext=node_text,
        showlegend=False,
        name='Nós'
    ))
    
    # Adiciona rótulos de peso nas arestas
    for i, (start, end) in enumerate(edges):
        x0, y0 = positions[start]
        x1, y1 = positions[end]
        mid_x = (x0 + x1) / 2
        mid_y = (y0 + y1) / 2
        
        fig.add_annotation(
            x=mid_x,
            y=mid_y,
            text=str(edge_weights[i]),
            showarrow=False,
            font=dict(color='red', size=12),
            bgcolor='white',
            bordercolor='red',
            borderwidth=1
        )
    
    # Configura layout
    title = "Árvore de Busca"
    if caminho_encontrado:
        caminho_str = ' → '.join(caminho_encontrado)
        title += f"<br>Caminho: {caminho_str}"
    
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16),
            x=0.5
        ),
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='white',
        width=800,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Salva como HTML e tenta abrir
    try:
        fig.show()
    except ValueError:
        # Se der erro, salva como arquivo HTML
        filename = "tree_visualization.html"
        fig.write_html(filename)
        print(f"Visualização salva como '{filename}'. Abra o arquivo no navegador para ver.")
        
        # Tenta abrir automaticamente no navegador
        import webbrowser
        try:
            webbrowser.open(filename)
        except:
            print("Não foi possível abrir automaticamente. Abra manualmente o arquivo no navegador.")
