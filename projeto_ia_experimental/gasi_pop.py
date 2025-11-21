"""
GASI-POP: Genetic Algorithm with Social Interaction (Population-based)

Baseado no artigo: "Game Theory and Social Interaction for Selection 
and Crossover Pressure Control in Genetic Algorithms"
"""

import numpy as np
from projeto_ia_experimental.individuo import Individuo
from projeto_ia_experimental.populacao import criar_populacao_inicial
from projeto_ia_experimental.operadores import selecao_torneio, crossover_blx_alpha, mutacao_gaussiana
from projeto_ia_experimental.jogo_dilema import JogoDilema



class GASIPOP:
    """
    Algoritmo Genético com Interação Social (GASI-POP).
    
    O jogo social acontece ANTES da seleção, entre todos os 
    indivíduos da população (pares consecutivos).
    """
    
    def __init__(self, problem, config, crossover_operator=None):
        """
        Args:
            problem: Problema de otimização
            config: Dicionário de configuração
            crossover_operator: Operador de crossover (opcional)
        """


        self.problem = problem
        self.tamanho_populacao = config.get('tamanho_populacao', 100)
        self.num_geracoes = config.get('num_geracoes', 100)
        self.taxa_crossover = config.get('taxa_crossover', 0.9)
        self.taxa_mutacao = config.get('taxa_mutacao', 0.1)
        self.tamanho_torneio = config.get('tamanho_torneio', 3)
        self.num_elites = config.get('num_elites', 2)
        self.crossover_operator = crossover_operator
        self.num_rounds = config.get('num_rounds', 10)
        self.game_rate = config.get('game_rate', 0.6)
        self.alpha_start = config.get('alpha_start', 0.5)
        self.alpha_end = config.get('alpha_end', 1.0)
        self.beta_start = config.get('beta_start', 0.9)
        self.beta_end = config.get('beta_end', 0.3)
        self.jogo = JogoDilema(num_rounds=self.num_rounds)
        
    def _normalizar_fitness(self, pop):

        fitness_list = [ind.fitness for ind in pop]

        melhor = min(fitness_list)
        pior = max(fitness_list)

        fitness_list_normalizado = []

        if pior == melhor:
            return [1.0] * len(pop)

        for ind in pop:
            f_normalizado = (pior - ind.fitness) / (pior - melhor)
            fitness_list_normalizado.append(f_normalizado)

        return fitness_list_normalizado
    
    
    def _calcular_payoffs(self):
        """
        Calcula T, R, P, S do Dilema do Prisioneiro.
        
        Baseado nas Equations 5-8 do artigo.
        No GASI, os payoffs são fixos pois usam fitness normalizado.
            
        Returns:
            tuple: (T, R, P, S) - valores do payoff
        """
             
        T = 0.4 
        R = 0.3 
        P = 0.2 
        S = 0.1 

        return T, R, P, S
  
       