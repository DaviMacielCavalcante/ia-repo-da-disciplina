"""
Algoritmo Genético completo.
"""

import numpy as np
from .populacao import criar_populacao_inicial
from .operadores import selecao_torneio, crossover_blx_alpha, mutacao_gaussiana

class AlgoritmoGenetico:

    def __init__(self, problem, config, crossover_operator=None):
        """
        Args:
            problem: instância do problema (ex: TBTProblem)
            config: dicionário com parâmetros do AG
            crossover_operator: operador de crossover customizado (opcional)
                                Se None, usa BLX-alpha padrão
        """
        self.problem = problem

        self.crossover_operator = crossover_operator

        self.tamanho_populacao = config.get('tamanho_populacao', 50)
        self.num_geracoes = config.get('num_geracoes', 100)
        self.taxa_crossover = config.get('taxa_crossover', 0.9)
        self.taxa_mutacao = config.get('taxa_mutacao', 0.1)
        self.tamanho_torneio = config.get('tamanho_torneio', 3)
        self.num_elites = config.get('num_elites', 2)

        self.historico_melhor_fitness = []
        self.historico_fitness_medio = []
        self.historico_num_viaveis = []

    def executar(self):
        """
        Executa o algoritmo genético.
        
        Returns:
            dict: Resultado com melhor indivíduo e histórico
        """

        pops = criar_populacao_inicial(self.problem, self.tamanho_populacao)

        for ind in pops:
            ind.evaluate()

        for generation in range(self.num_geracoes):

            new_generation = []
            elites = sorted(pops)[:self.num_elites]

            for elite in elites:
                new_generation.append(elite.copy())

            while len(new_generation) < self.tamanho_populacao:

                pai = selecao_torneio(pops, self.tamanho_torneio)
                mae = selecao_torneio(pops, self.tamanho_torneio)

                if np.random.random() < self.taxa_crossover:
                    if self.crossover_operator:
                        filho1, filho2 = self.crossover_operator.apply(pai, mae)
                    else:
                        filho1, filho2 = crossover_blx_alpha(pai, mae)

                else:
                    filho1 = pai.copy()
                    filho2 = mae.copy()

                filho1 = mutacao_gaussiana(individuo=filho1, taxa_mutacao=self.taxa_mutacao)
                filho2 = mutacao_gaussiana(individuo=filho2, taxa_mutacao=self.taxa_mutacao)

                filho1.evaluate()
                filho2.evaluate()

                new_generation.append(filho1)
                if len(new_generation) < self.tamanho_populacao:
                    new_generation.append(filho2)

            pops = new_generation

            the_one = min(pops)

            fitness_values = [ind.fitness for ind in pops]

            mean_fitness = np.mean(fitness_values)

            n_viables = sum(1 for ind in pops if ind.is_feasible())

            self.historico_melhor_fitness.append(the_one.fitness)
            self.historico_fitness_medio.append(mean_fitness)
            self.historico_num_viaveis.append(n_viables)

            if (generation + 1) % 10 == 0:
                print(f"Geração: {generation + 1}/{self.num_geracoes} | "
                f"Melhor: {the_one.fitness:.4f} | "      
                f"Médio: {mean_fitness:.4f} | "      
                f"Viáveis: {n_viables}/{self.tamanho_populacao}")
        
        the_one = min(pops)

        return {
            "melhor_individuo": the_one,
            "populacao_final": pops,
            "historico_melhor": self.historico_melhor_fitness,
            "historico_medio": self.historico_fitness_medio,
            "historico_viaveis": self.historico_num_viaveis
        }