class Node:
    def __init__(self, value, cost):
        self.father = None
        self.value = value
        self.cost = cost
        self.childs = []

    def add_father(self, father):
        self.father = father

    def add_child(self, child):
        self.childs.append(child)
        child.add_father(self)