from algoritmos_de_busca_arvore.tree import Tree
from algoritmos_de_busca_arvore.visualize import *

tree = Tree('A')


tree.add_child('A', 'B', 36)
tree.add_child('A', 'C', 61)
tree.add_child('B', 'D', 31)
tree.add_child('C', 'F', 31)
tree.add_child('C', 'L', 80)
tree.add_child('D', 'E', 52)
tree.add_child('F', 'E', 31)
tree.add_child('F', 'K', 112)
tree.add_child('L', 'M', 102)
tree.add_child('E', 'G', 43)
tree.add_child('K', 'M', 32)
tree.add_child('K', 'J', 36)
tree.add_child('G', 'H', 20)
tree.add_child('J', 'I', 45)
tree.add_child('H', 'I', 40)


#caminho, custo = tree.busca_largura('A', 'M')
#caminho, custo = tree.busca_custo_uniforme('A', 'M')
#caminho, custo = tree.busca_gulosa('A', 'M')
#caminho, custo = tree.busca_a_estrela('A', 'M')
caminho, custo = tree.busca_bidirecional('A', 'M')

print(f"Caminho encontrado: {caminho} com custo total: {custo}")



visualize_tree_plotly(tree, caminho_encontrado=caminho)