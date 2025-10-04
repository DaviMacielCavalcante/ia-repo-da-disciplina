from .node import Node
import heapq
import itertools

class Graph:
    def __init__(self):
        self.nodes = {}
        self.counter = itertools.count()  # Contador para desempate no heap

    def add_node(self, value):
        if value not in self.nodes:
            self.nodes[value] = Node(value)
        return self.nodes[value]

    def add_edge(self, from_value, to_value, cost, bidirectional=True):
        # Cria os nós se não existirem
        from_node = self.add_node(from_value)
        to_node = self.add_node(to_value)
        
        # Adiciona a aresta
        from_node.add_neighbor(to_node, cost)
        
        # Se for bidirecional, adiciona a aresta reversa
        if bidirectional:
            to_node.add_neighbor(from_node, cost)

    def get_node(self, value):
        return self.nodes.get(value)

    def print_graph(self):
        for value, node in self.nodes.items():
            neighbors = [f"{n.value}({c})" for n, c in node.neighbors.items()]
            print(f"{value}: {', '.join(neighbors)}")

    def heuristic_calculated(self, node, goal):
        heuristics = {
            'A': 223, 'B': 222, 'C': 166, 'D': 192, 'E': 165,
            'F': 136, 'G': 122, 'H': 111, 'I': 100, 'J': 60,
            'K': 32, 'L': 102, 'M': 0
        }
        return heuristics.get(node.value, float('inf'))

    def busca_largura(self, start, goal):
        start_node = self.get_node(start)
        if not start_node:
            return None

        visitados = set()
        queue = [(start_node, [start], 0)]

        while queue:
            current_node, path, cost = queue.pop(0)

            if current_node.value in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, cost)

            for neighbor, edge_cost in current_node.neighbors.items():
                if neighbor.value not in visitados:
                    new_path = path + [neighbor.value]
                    new_cost = cost + edge_cost
                    queue.append((neighbor, new_path, new_cost))

        return None

    def busca_custo_uniforme(self, start, goal):
        start_node = self.get_node(start)
        if not start_node:
            return None

        heap = []
        visitados = set()

        heapq.heappush(heap, (0, next(self.counter), start_node, [start]))

        while heap:
            current_cost, _, current_node, path = heapq.heappop(heap)

            if current_node.value in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, current_cost)

            for neighbor, edge_cost in current_node.neighbors.items():
                if neighbor.value not in visitados:
                    new_cost = current_cost + edge_cost
                    new_path = path + [neighbor.value]
                    heapq.heappush(heap, (new_cost, next(self.counter), neighbor, new_path))

        return None

    def busca_gulosa(self, start, goal):
        start_node = self.get_node(start)
        if not start_node:
            return None

        heap = []
        visitados = set()

        initial_h = self.heuristic_calculated(start_node, goal)
        heapq.heappush(heap, (initial_h, next(self.counter), start_node, [start], 0))

        while heap:
            _, _, current_node, path, cost = heapq.heappop(heap)

            if current_node.value in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, cost)

            for neighbor, edge_cost in current_node.neighbors.items():
                if neighbor.value not in visitados:
                    new_cost = cost + edge_cost
                    new_path = path + [neighbor.value]
                    new_h = self.heuristic_calculated(neighbor, goal)
                    heapq.heappush(heap, (new_h, next(self.counter), neighbor, new_path, new_cost))

        return None

    def busca_a_estrela(self, start, goal):
        start_node = self.get_node(start)
        if not start_node:
            return None

        heap = []
        visitados = set()

        initial_g = 0
        initial_h = self.heuristic_calculated(start_node, goal)
        initial_f = initial_g + initial_h

        heapq.heappush(heap, (initial_f, next(self.counter), start_node, [start], initial_g))

        while heap:
            current_f, _, current_node, path, g = heapq.heappop(heap)

            if current_node.value in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, g)

            for neighbor, edge_cost in current_node.neighbors.items():
                if neighbor.value not in visitados:
                    new_g = g + edge_cost
                    new_h = self.heuristic_calculated(neighbor, goal)
                    new_f = new_g + new_h
                    new_path = path + [neighbor.value]
                    heapq.heappush(heap, (new_f, next(self.counter), neighbor, new_path, new_g))

        return None

    def busca_bidirecional(self, start, goal):
        start_node = self.get_node(start)
        goal_node = self.get_node(goal)
        
        if not start_node or not goal_node:
            return None

        queue_start = [(start_node, [start], 0)]
        queue_goal = [(goal_node, [goal], 0)]

        visited_start = {start: (0, [start])}
        visited_goal = {goal: (0, [goal])}

        while queue_start or queue_goal:
            # Expansão a partir do início
            if queue_start:
                current_node, path, cost = queue_start.pop(0)

                if current_node.value in visited_goal:
                    path_goal_reversed = list(reversed(visited_goal[current_node.value][1]))
                    final_path = path + path_goal_reversed[1:]
                    total_cost = cost + visited_goal[current_node.value][0]
                    return (final_path, total_cost)

                for neighbor, edge_cost in current_node.neighbors.items():
                    if neighbor.value not in visited_start:
                        new_cost = cost + edge_cost
                        new_path = path + [neighbor.value]
                        queue_start.append((neighbor, new_path, new_cost))
                        visited_start[neighbor.value] = (new_cost, new_path)

            # Expansão a partir do objetivo
            if queue_goal:
                current_node, path, cost = queue_goal.pop(0)

                if current_node.value in visited_start:
                    path_goal_reversed = list(reversed(path))
                    final_path = visited_start[current_node.value][1] + path_goal_reversed[1:]
                    total_cost = cost + visited_start[current_node.value][0]
                    return (final_path, total_cost)

                for neighbor, edge_cost in current_node.neighbors.items():
                    if neighbor.value not in visited_goal:
                        new_cost = cost + edge_cost
                        new_path = path + [neighbor.value]
                        queue_goal.append((neighbor, new_path, new_cost))
                        visited_goal[neighbor.value] = (new_cost, new_path)

        return None