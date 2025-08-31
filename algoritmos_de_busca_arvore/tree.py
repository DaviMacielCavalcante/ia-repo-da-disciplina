from .node import Node
import heapq

class Tree:
    def __init__(self, root):
        self.root = Node(root, 0)

    def find_node(self, value):
        queue = [self.root]
        while queue:
            current_node = queue.pop(0)
            if current_node.value == value:
                return current_node
            for child in current_node.childs:
                queue.append(child)
        return None
            

    def add_child(self, father: str, child: str, cost: int):
        father_node = self.find_node(father)

        if father_node:
            new_child = Node(child, cost)
            father_node.add_child(new_child)
        

    def print_tree(self, node, level=0):
        indent = "  " * level
        print(f"{indent}- {node.value}-{node.cost}")
        for child in node.childs:
            self.print_tree(child, level + 1)


    def busca_largura(self, start, goal):

        start_node = self.find_node(start)
        
        path = []

        queue = [(start_node, [start], 0)] 

        while queue: 
            current_node, path, cost = queue.pop(0)

            if current_node.value == goal:
                return (path, cost)
            
            for child in current_node.childs:
                new_path = path + [child.value]
                new_cost = cost + child.cost
                queue.append((child, new_path, new_cost))

    def busca_custo_uniforme(self, start, goal):

        heap = []

        start_node = self.find_node(start)

        visitados = set()  

        heapq.heappush(heap, (0, start_node, [start]))

        while heap:

            current_cost, current_node, path = heapq.heappop(heap)

            if current_node in visitados:
                continue

            visitados.add(current_node)

            if current_node.value == goal:
                return (path, current_cost)
            
            for child in current_node.childs:
                if child.value not in visitados: 
                    new_cost = current_cost + child.cost
                    new_path = path + [child.value]
                    heapq.heappush(heap, (new_cost, child, new_path))

    def busca_gulosa(self, start, goal):
        
        heap = []

        visitados = set()

        start_node = self.find_node(start)

        heuristic = self.heuristic_calculated(start_node, goal)

        heapq.heappush(heap, (heuristic, start_node, [start], 0))

        while heap:

            (_, current_node, path, cost) = heapq.heappop(heap)

            if current_node in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, cost)
            
            for child in current_node.childs:
                if child.value not in visitados:
                    new_real_cost = cost + child.cost
                    new_path = path + [child.value]

                    new_heuristic = self.heuristic_calculated(child, goal)
                    heapq.heappush(heap, (new_heuristic, child, new_path, new_real_cost))

    def heuristic_calculated(self, node, goal):
        
        heuristics = {
        'A': 223, 'B': 222, 'C': 166, 'D': 192, 'E': 165,
        'F': 136, 'G': 122, 'H': 111, 'I': 100, 'J': 60,
        'K': 32, 'L': 102, 'M': 0
        }
        return heuristics.get(node.value, float('inf'))
    
    def busca_a_estrela(self, start, goal):
        
        heap = []

        visitados = set()

        initial_g = 0
        initial_h = self.heuristic_calculated(self.find_node(start), goal)
        initial_f = initial_g + initial_h

        heapq.heappush(heap, (initial_f, self.find_node(start), [start], initial_g))

        while heap:

            (current_f, current_node, path, g) = heapq.heappop(heap)

            if current_node in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, g)
            
            for child in current_node.childs:
                if child.value not in visitados:
                    new_g = g + child.cost
                    new_h = self.heuristic_calculated(child, goal)
                    new_f = new_g + new_h
                    new_path = path + [child.value]

                    heapq.heappush(heap, (new_f, child, new_path, new_g))