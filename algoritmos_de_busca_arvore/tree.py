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

    def busca_bidirecional(self, start, goal):
    
        queue_start = [(self.find_node(start), [start], 0)]
        queue_goal = [(self.find_node(goal), [goal], 0)]

        visited_start = {start: (0, [start])}
        visited_goal = {goal: (0, [goal])}

        while queue_start or queue_goal:
            
            if queue_start:
                current_node_start, path_start, cost_start = queue_start.pop(0)

                if current_node_start.value in visited_goal:
                    path_goal_reversed = list(reversed(visited_goal[current_node_start.value][1]))
                    final_path = path_start + path_goal_reversed[1:]  
                    total_cost = cost_start + visited_goal[current_node_start.value][0]
                    return (final_path, total_cost)
                
                for child in current_node_start.childs:
                    if child.value not in visited_start:
                        new_cost = cost_start + child.cost
                        new_path = path_start + [child.value]
                        queue_start.append((child, new_path, new_cost))
                        visited_start[child.value] = (new_cost, new_path)

            if queue_goal:
                current_node_goal, path_goal, cost_goal = queue_goal.pop(0)

                if current_node_goal.value in visited_start:
                    path_goal_reversed = list(reversed(path_goal))
                    final_path = visited_start[current_node_goal.value][1] + path_goal_reversed[1:]  
                    total_cost = cost_goal + visited_start[current_node_goal.value][0]
                    return (final_path, total_cost)
                
                if current_node_goal.father:
                    father = current_node_goal.father
                    if father.value not in visited_goal:
                        new_cost = cost_goal + current_node_goal.cost
                        new_path = path_goal + [father.value]  
                        queue_goal.append((father, new_path, new_cost))
                        visited_goal[father.value] = (new_cost, new_path)