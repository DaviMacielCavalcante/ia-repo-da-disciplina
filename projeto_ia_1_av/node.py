class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = {}  

    # def add_neighbor(self, neighbor, cost):
    #     self.neighbors[neighbor] = cost

    def add_neighbor(self, neighbor, cost, clima=None, qualidade=None):
        self.neighbors[neighbor] = {
            "cost": cost,
            "clima": clima,
            "qualidade": qualidade
        }
