from projeto_ia_1_av.graph import Graph

def test_graph():
    # Criando o grafo
    g = Graph()
    
    # Adicionando arestas conforme a heurística definida (grafo da Romênia, por exemplo)
    # Estrutura de exemplo baseada nas heurísticas A-M
    g.add_edge('A', 'B', 10)
    g.add_edge('A', 'C', 15)
    g.add_edge('B', 'D', 12)
    g.add_edge('B', 'E', 15)
    g.add_edge('C', 'F', 10)
    g.add_edge('D', 'G', 8)
    g.add_edge('E', 'H', 7)
    g.add_edge('F', 'I', 9)
    g.add_edge('G', 'J', 10)
    g.add_edge('H', 'J', 6)
    g.add_edge('I', 'K', 5)
    g.add_edge('J', 'L', 4)
    g.add_edge('J', 'K', 8)
    g.add_edge('K', 'M', 6)
    g.add_edge('L', 'M', 7)
    
    print("=" * 60)
    print("ESTRUTURA DO GRAFO")
    print("=" * 60)
    g.print_graph()
    print()
    
    # Testando todas as buscas de A até M
    start = 'A'
    goal = 'M'
    
    print("=" * 60)
    print(f"TESTANDO BUSCAS: {start} -> {goal}")
    print("=" * 60)
    print()
    
    # Busca em Largura
    print("1. BUSCA EM LARGURA (BFS)")
    print("-" * 60)
    result = g.busca_largura(start, goal)
    if result:
        print(f"Caminho encontrado: {' -> '.join(result[0])}")
        print(f"Custo total: {result[1]}")
    else:
        print("Caminho não encontrado!")
    print()
    
    # Busca de Custo Uniforme
    print("2. BUSCA DE CUSTO UNIFORME (UCS)")
    print("-" * 60)
    result = g.busca_custo_uniforme(start, goal)
    if result:
        print(f"Caminho encontrado: {' -> '.join(result[0])}")
        print(f"Custo total: {result[1]}")
    else:
        print("Caminho não encontrado!")
    print()
    
    # Busca Gulosa
    print("3. BUSCA GULOSA (Greedy Best-First)")
    print("-" * 60)
    result = g.busca_gulosa(start, goal)
    if result:
        print(f"Caminho encontrado: {' -> '.join(result[0])}")
        print(f"Custo total: {result[1]}")
    else:
        print("Caminho não encontrado!")
    print()
    
    # Busca A*
    print("4. BUSCA A* (A-Star)")
    print("-" * 60)
    result = g.busca_a_estrela(start, goal)
    if result:
        print(f"Caminho encontrado: {' -> '.join(result[0])}")
        print(f"Custo total: {result[1]}")
    else:
        print("Caminho não encontrado!")
    print()
    
    # Busca Bidirecional
    print("5. BUSCA BIDIRECIONAL")
    print("-" * 60)
    result = g.busca_bidirecional(start, goal)
    if result:
        print(f"Caminho encontrado: {' -> '.join(result[0])}")
        print(f"Custo total: {result[1]}")
    else:
        print("Caminho não encontrado!")
    print()
    
    print("=" * 60)
    print("TESTE CONCLUÍDO")
    print("=" * 60)


if __name__ == "__main__":
    test_graph()