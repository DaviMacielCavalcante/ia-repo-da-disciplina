from .node import Node
from .fuzzy import fuzzy_config
import heapq
import itertools
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import random
import numpy as np

class Graph:
    def __init__(self):
        seed = random.randint(0, 2**32 - 2) # seed aleatória para sempre gerar vizinhos com custos diferentes
        self.simulador_fuzzy = self._iniciar_fuzzy()
        self.nodes = {}
        self.counter = itertools.count()  # Contador para desempate no heap
        self.coordenadas = {}
        self.rng = np.random.default_rng(seed)  # rng padrão com a seed gerada
        
    def _iniciar_fuzzy(self):
       sistema_fuzzy = ctrl.ControlSystem(fuzzy_config())
       simulador = ctrl.ControlSystemSimulation(sistema_fuzzy)
       return simulador

    def add_node(self, value, x=None, y=None):  
       # Coordenadas opcionais para os nodos
        if value not in self.nodes:
            self.nodes[value] = Node(value)  # Node continua simples
        
        # Armazena coordenadas separadamente para cálculos de distância euclidiana
        if x is not None and y is not None:
            self.coordenadas[value] = (x, y)
        
        return self.nodes[value]

    def add_edge(self, from_value, to_value, cost, clima=None, qualidade=None, bidirectional=True):
        # Adiciona aresta com custo base e condições fuzzy usando os seguintes argumentos:
        #     from_value: Nodo origem
        #     to_value: Nodo destino
        #     cost: Custo base da aresta
        #     clima: Condição climática (0-10), deixarmos None para gerar aleatoriamente
        #     qualidade: Qualidade da estrada (0-10), deixamos None para gerar aleatoriamente
        from_node = self.add_node(from_value)
        to_node = self.add_node(to_value)
        
        # Gera os valores aleatórios UMA VEZ para que a estrada de ida e de volta
        # tenham as mesmas condições no momento da criação.
        clima_final = clima if clima is not None else self.rng.uniform(0, 10)
        qualidade_final = qualidade if qualidade is not None else self.rng.uniform(0, 10)
        
        # Adiciona a aresta de ida
        from_node.add_neighbor(to_node, cost, clima=clima_final, qualidade=qualidade_final)
        
        # Se for bidirecional, adiciona a aresta de volta com os mesmos dados
        if bidirectional:
            to_node.add_neighbor(from_node, cost, clima=clima_final, qualidade=qualidade_final)

# ... (resto da sua classe Graph) ...
        

    def get_node(self, value):
        return self.nodes.get(value)
                    
    def calcular_custo_real(self, custo_base, clima, qualidade):
        # Calcula o custo real [g(n)] com base no custo base e condições do fuzzy
        self.simulador_fuzzy.input['clima'] = clima
        self.simulador_fuzzy.input['qualidade_estrada'] = qualidade
        self.simulador_fuzzy.compute()
        mult_de_ajuste = self.simulador_fuzzy.output['mult']
        return custo_base * mult_de_ajuste

    def heuristic_calculated(self, node, goal):
        # Usando a distância euclidiana para uma heurística mais adimissível do que valores fixos
        if node.value in self.coordenadas and goal in self.coordenadas:
            x1, y1 = self.coordenadas[node.value]
            x2, y2 = self.coordenadas[goal]
            custo = np.sqrt((x2-x1)**2 + (y2-y1)**2)
            
            # Multiplica pelo MENOR fator possível (esperando que o melhor caminho custará PELO MENOS este valor)
            MULT_MINIMO = 0.5
            return custo * MULT_MINIMO
        """
            Por que fazer isso?
            Este é o custo estimado [h(n)] que o A* utiliza na heurística, ele sempre deve ser menor que o custo real, pois queremos um algoritmo otimista! Quando somado ao custo real ficará claro qual o melhor caminho, e qual o pior.
        """
        
        # Fallback caso não houver coordenadas para os nodos (sempre admissível, mas menos informativa)
        return 0

    def busca_a_estrela(self, start, goal):
        # Busca A* com custos ajustados pela lógica fuzzy

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
                    # Dados fuzzy da aresta
                    custo_base = edge_data['cost']
                    clima_edge = edge_data['clima']
                    qualidade_edge = edge_data['qualidade']
                    
                    # Calculando custo real com o Fuzzy baseado em variáveis aleatórias
                    custo_real = self.calcular_custo_real(
                        custo_base, clima_edge, qualidade_edge
                    )
                    
                    # Usa o custo real para realizar a heurística
                    new_g = g + custo_real
                    new_h = self.heuristic_calculated(neighbor, goal)
                    new_f = new_g + new_h
                    new_path = path + [neighbor.value]
                    
                    heapq.heappush(
                        heap, (new_f, next(self.counter), neighbor, new_path, new_g)
                    )

        return None