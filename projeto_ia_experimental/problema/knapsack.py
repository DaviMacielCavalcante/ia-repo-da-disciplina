"""
Problema da Mochila (Knapsack Problem)
"""

import numpy as np


class KnapsackProblem:
    """
    Problema da Mochila usando representação Random Keys.
    """
    
    def __init__(self, weights, values, capacity):
        """
        Args:
            weights: lista de pesos dos itens
            values: lista de valores dos itens
            capacity: capacidade máxima da mochila
        """
        
        self.weights = np.array(weights)
        self.values = np.array(values)
        self.capacity = capacity
        self.n_vars = len(self.weights)
        self.lower_bounds = np.zeros(self.n_vars)
        self.upper_bounds = np.ones(self.n_vars)
        self.optimization = 'max'
    
    def evaluate(self, genes):
        """
        Avalia uma solução (genes = prioridades).
        
        Returns:
            tuple: (fitness, is_feasible, peso_total)
        """
        indices_ordenados = np.argsort(-genes)

        peso_atual = 0
        valor_total = 0

        for idx in indices_ordenados:
            if peso_atual + self.weights[idx] <= self.capacity:
                peso_atual += self.weights[idx]
                valor_total += self.values[idx]

        return {
            "objective": valor_total,
            "constraints": [],
            "n_violations": 0,      
            "violation_sum": 0,    
            "peso_usado": peso_atual
        }