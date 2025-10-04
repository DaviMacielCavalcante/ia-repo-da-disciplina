class Node:
    def __init__(self, value):
        self.value = value
        self.neighbors = {}  # {node: cost}

    def add_neighbor(self, neighbor, cost):
        self.neighbors[neighbor] = cost