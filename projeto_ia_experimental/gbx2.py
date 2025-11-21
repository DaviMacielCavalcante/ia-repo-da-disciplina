"""
GBX2 - Game-Based Crossover
Operador de crossover baseado em teoria dos jogos.
"""

import numpy as np
from .individuo import Individuo
from projeto_ia_experimental.jogo_dilema import JogoDilema

class GBX2Crossover:
    """
    Game-Based Crossover (GBX) - Versão 2
    """   

    def __init__(self, num_rounds=10, phi_min=0.8, phi_max=1.2, dollar_start=1.0, dollar_end=0.5, current_iter=0, max_iter=200):
        """
        Args:
            num_rounds: Número de rodadas do jogo iterado
            phi_min, phi_max: Range do fator de perturbação φ
            dollar_start: Valor inicial da função $ (default=0.6)
            dollar_end: Valor final da função $ (default=1.0)
            current_iter: Iteração/geração atual (default=0)
            max_iter: Total de iterações/gerações (default=200)
        """

        self.num_rounds = num_rounds
        self.phi_min = phi_min 
        self.phi_max = phi_max
        self.dollar_start = dollar_start
        self.dollar_end = dollar_end
        self.current_iter = current_iter
        self.max_iter = max_iter
        self.jogo = JogoDilema(num_rounds=self.num_rounds)
 
    def _calcular_payoffs(self, min_val, max_val):
        """
        Calcula T, R, P, S do Dilema do Prisioneiro.
        
        Baseado nas Equations 13-16 do artigo.
        
        Args:
            min_val: Limite inferior da busca
            max_val: Limite superior da busca
            
        Returns:
            tuple: (T, R, P, S) - valores do payoff
        """
             
        phi = np.random.normal(0, 1)
        diff = abs(max_val - min_val)

        T = phi * (diff*0.4) / self.num_rounds
        R = phi * (diff*0.3) / self.num_rounds
        P = phi * (diff*0.2) / self.num_rounds
        S = phi * (diff*0.1) / self.num_rounds

        return T, R, P, S
    
    def _calcular_limites(self, lower_bound, upper_bound):
        """
        Calcula Min e Max baseado na direção de busca.
        
        Baseado nas Equations 18-19 do artigo.
        
        Args:
            gene_pai: Valor do gene do pai
            direcao: +1 (crescente) ou -1 (decrescente)
            lower_bound: Limite inferior da variável
            upper_bound: Limite superior da variável
            
        Returns:
            tuple: (min_val, max_val) 
        """
  
        return lower_bound, upper_bound

    def _gerar_gene(self, gene_pai, z, direcao, lower_bound, upper_bound):
        """
        Gera o gene do filho baseado no payoff acumulado.
        
        Baseado na Equation 23 do artigo.
        
        Args:
            gene_pai: Valor do gene do pai
            Z: Payoff total acumulado no jogo
            direcao: +1 (crescente) ou -1 (decrescente)
            lower_bound: Limite inferior da variável
            upper_bound: Limite superior da variável
            
        Returns:
            float: Valor do gene do filho
        """

        dollar = self.dollar_start - ((self.dollar_start - self.dollar_end) * self.current_iter / self.max_iter )

        if direcao == -1:
            novo_gene = gene_pai - dollar * abs(z)
        else:
            novo_gene = gene_pai + dollar * abs(z)

        novo_gene = np.clip(novo_gene, lower_bound, upper_bound)

        return novo_gene

    def apply(self, pai, mae):
        """
        Aplica o crossover GBX2 entre dois pais.
        
        Args:
            pai: Individuo (pai)
            mae: Individuo (mae)
            
        Returns:
            tuple: (filho1, filho2) - dois novos Individuos
        """

        problem = pai.problem
        n_vars = problem.n_vars

        genes_filho1 = np.zeros(n_vars)
        genes_filho2 = np.zeros(n_vars)

        estrategia_pai = self.jogo._gerar_estrategia_aleatoria()
        estrategia_mae = self.jogo._gerar_estrategia_aleatoria()

        for j in range(n_vars):

            min_pai, max_pai = self._calcular_limites(
                problem.lower_bounds[j], problem.upper_bounds[j]
            )

            min_mae, max_mae = self._calcular_limites(
                problem.lower_bounds[j], problem.upper_bounds[j]
            )

            t_pai, r_pai, p_pai, s_pai = self._calcular_payoffs(min_pai, max_pai)

            t_mae, r_mae, p_mae, s_mae = self._calcular_payoffs(min_mae, max_mae)

            z_pai = self.jogo._jogar_dilema(
                estrategia_pai, estrategia_mae,
                t_pai, r_pai, p_pai, s_pai
            )

            z_mae = self.jogo._jogar_dilema(
                estrategia_mae, estrategia_pai,
                t_mae, r_mae, p_mae, s_mae
            )

            direcao_pai = 1 if z_pai >= 0 else -1
            direcao_mae = 1 if z_mae >= 0 else -1

            genes_filho1[j] = self._gerar_gene(
                pai.genes[j], z_pai, direcao_pai,
                problem.lower_bounds[j], problem.upper_bounds[j]
            )

            genes_filho2[j] = self._gerar_gene(
                mae.genes[j], z_mae, direcao_mae,
                problem.lower_bounds[j], problem.upper_bounds[j]
            )

        filho1 = Individuo(genes_filho1, problem)
        filho2 = Individuo(genes_filho2, problem)

        return filho1, filho2