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
    
    @staticmethod
    def gerar_aleatorio(n_items=100, capacidade_n_itens=10, seed=None):
        """
        Gera uma instância aleatória do problema da mochila.
        
        Args:
            n_items: número de itens (default=100)
            capacidade_n_itens: capacidade suficiente para N itens de peso médio (default=10)
            seed: seed para reprodutibilidade (default=None)
        
        Returns:
            KnapsackProblem: instância do problema com itens aleatórios
        """
        if seed is not None:
            np.random.seed(seed)
        
        # Gerar pesos aleatórios entre 1 e 50
        weights = np.random.randint(1, 51, size=n_items)
        
        # Gerar valores monetários FLUTUANTES entre 10.0 e 1000.0
        # Isso cria uma distribuição mais realista de preços
        values = np.random.uniform(10.0, 1000.0, size=n_items)
        
        # Arredondar para 2 casas decimais (centavos)
        values = np.round(values, 2)
        
        # Calcular capacidade como: peso_médio * capacidade_n_itens
        # Isso garante que caibam aproximadamente N itens de peso médio
        peso_medio = np.mean(weights)
        capacity = int(peso_medio * capacidade_n_itens)
        
        return KnapsackProblem(weights, values, capacity)
    
    def evaluate(self, genes):
        """
        Avalia uma solução (genes = prioridades).
        
        Returns:
            dict: resultado da avaliação
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
    
    def get_itens_selecionados(self, genes):
        """
        Retorna os índices dos itens selecionados na solução.
        
        Args:
            genes: array de prioridades
            
        Returns:
            tuple: (itens_selecionados, peso_usado, valor_usado)
        """
        indices_ordenados = np.argsort(-genes)
        
        peso_usado = 0
        valor_usado = 0
        itens_selecionados = []
        
        for idx in indices_ordenados:
            if peso_usado + self.weights[idx] <= self.capacity:
                itens_selecionados.append(idx)
                peso_usado += self.weights[idx]
                valor_usado += self.values[idx]
        
        return itens_selecionados, peso_usado, valor_usado
    
    def imprimir_info(self):
        """Imprime informações sobre o problema."""
        print(f"Número de itens: {self.n_vars}")
        print(f"Capacidade da mochila: {self.capacity}")
        print(f"Peso total dos itens: {np.sum(self.weights)}")
        print(f"Valor total dos itens: R$ {np.sum(self.values):.2f}")
        print(f"Peso médio: {np.mean(self.weights):.2f}")
        print(f"Valor médio: R$ {np.mean(self.values):.2f}")
        print(f"Razão valor/peso média: R$ {np.mean(self.values / self.weights):.2f} por unidade de peso")