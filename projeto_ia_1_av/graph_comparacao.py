from projeto_ia_1_av.graph import Graph
import heapq


class GraphComparacao(Graph):
    """
    Extensão da classe Graph original para incluir A* tradicional (sem fuzzy)
    """

    def busca_a_estrela_tradicional(self, start, goal):
        """
        A* tradicional que usa apenas o custo base, ignorando condições fuzzy.
        Implementação idêntica ao A* + Fuzzy, mas sem calcular custo real.
        """
        start_node = self.get_node(start)
        if not start_node:
            return None

        heap = []
        visitados = set()

        initial_g = 0
        initial_h = self.heuristic_calculated(start_node, goal)
        initial_f = initial_g + initial_h

        heapq.heappush(
            heap, (initial_f, next(self.counter), start_node, [start], initial_g)
        )

        while heap:
            initial_f, _, current_node, path, g = heapq.heappop(heap)

            if current_node.value in visitados:
                continue

            visitados.add(current_node.value)

            if current_node.value == goal:
                return (path, g)

            for neighbor, edge_data in current_node.neighbors.items():
                if neighbor.value not in visitados:
                    # USA APENAS O CUSTO BASE - não considera clima/qualidade
                    custo_base = edge_data["cost"]

                    new_g = g + custo_base
                    new_h = self.heuristic_calculated(neighbor, goal)
                    new_f = new_g + new_h
                    new_path = path + [neighbor.value]

                    heapq.heappush(
                        heap, (new_f, next(self.counter), neighbor, new_path, new_g)
                    )

        return None
