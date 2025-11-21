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
        self.historico_melhor_fitness = []
        self.historico_fitness_medio = []
        self.historico_num_viaveis = []
        
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
    
    def _interacao_social(self, pop):
        """
        Executa a interação social entre pares de indivíduos.
        
        Args:
            pop: Lista de indivíduos
            
        Returns:
            list: Fitness social de cada indivíduo
        """
        
        t, r, p, s = self._calcular_payoffs()
        
        # Lista para guardar o fitness social de cada indivíduo
        fitness_social = [0.0] * len(pop)
        
        # Iterar pelos pares (0 vs 1, 2 vs 3, etc.)
        for i in range(0, len(pop) - 1, 2):

            

            if np.random.random() < self.game_rate:
                
                estrategia1 = self.jogo._gerar_estrategia_aleatoria()
                estrategia2 = self.jogo._gerar_estrategia_aleatoria()

                payoff1 = self.jogo._jogar_dilema(estrategia1, estrategia2, t, r, p ,s)
                payoff2 = self.jogo._jogar_dilema(estrategia2, estrategia1, t, r, p ,s)

                fitness_social[i] = payoff1
                fitness_social[i+1] = payoff2
        
        return fitness_social
    
    def _calcular_fitness_total(self, f_normalizado, f_social, iteracao):
        """
        Calcula o fitness total combinando fitness normalizado e social.
        
        Baseado na Equação 11 do artigo.
        
        Args:
            f_normalizado: Lista de fitness normalizados
            f_social: Lista de fitness sociais
            iteracao: Iteração atual
            
        Returns:
            list: Fitness total de cada indivíduo
        """
        
        # Calcular α 
        alpha = self.alpha_start - ((self.alpha_start - self.alpha_end) * iteracao / self.num_geracoes )
        
        # Calcular β 
        beta = self.beta_start - ((self.beta_start - self.beta_end) * iteracao / self.num_geracoes)
        
        # Calcular fitness total para cada indivíduo
        f_total = []
        for i in range(len(f_normalizado)):

            # Para minimização: f_total = (α × f_norm) - (β × f_social)

            total = (alpha * f_normalizado[i]) - (beta * f_social[i])
            f_total.append(total)
        
        return f_total
    
    def _selecao_torneio(self, pop):
        """
        Seleção por torneio usando fitness total e regra de Deb.
        """
        
        indices = np.random.choice(len(pop), size=self.tamanho_torneio, replace=False)
        competidores = [pop[i] for i in indices]
        
        # Encontrar o melhor usando regra de Deb + fitness total
        melhor = competidores[0]
        
        for ind in competidores[1:]:
            # Comparar 'ind' com 'melhor'
            
            if ind.is_feasible() and not melhor.is_feasible():
                # ind é viável, melhor não é → ind vence
                melhor = ind
            elif not ind.is_feasible() and melhor.is_feasible():
                # ind não é viável, melhor é → melhor continua
                pass
            elif ind.is_feasible() and melhor.is_feasible():
                # Ambos viáveis → maior fitness_total vence
                if ind.fitness_total > melhor.fitness_total:
                    melhor = ind
            else:
                # Ambos inviáveis → menor violação vence
                if ind.violation_sum < melhor.violation_sum:
                    melhor = ind
        
        return melhor
    
    def executar(self):
        """
        Executa o algoritmo GASI-POP.
        
        Returns:
            dict: Resultado com melhor indivíduo e histórico
        """

        pops = criar_populacao_inicial(self.problem, self.tamanho_populacao)

        for ind in pops:
            ind.evaluate()

        for generation in range(self.num_geracoes):

            if self.crossover_operator and hasattr(self.crossover_operator, "current_iter"):
                self.crossover_operator.current_iter = generation

            new_generation = []
            elites = sorted(pops)[:self.num_elites]

            for elite in elites:
                new_generation.append(elite.copy())

            f_normalizado = self._normalizar_fitness(pops)

            f_social = self._interacao_social(pops)

            f_total = self._calcular_fitness_total(f_normalizado, f_social, generation)

            # Guardar fitness total em cada indivíduo
            for i, ind in enumerate(pops):
                ind.fitness_total = f_total[i]

            while len(new_generation) < self.tamanho_populacao:

                pai = self._selecao_torneio(pops)
                mae = self._selecao_torneio(pops)

                
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

            if (generation + 1) % 10 == 0:
                print(f"Geração: {generation + 1}/{self.num_geracoes} | "
                f"Melhor: {the_one.fitness:.4f} | "      
                f"Médio: {mean_fitness:.4f} | "      
                f"Viáveis: {n_viables}/{self.tamanho_populacao}")


            pops = new_generation

            the_one = min(pops)

            fitness_values = [ind.fitness for ind in pops]

            mean_fitness = np.mean(fitness_values)

            n_viables = sum(1 for ind in pops if ind.is_feasible())

            self.historico_melhor_fitness.append(the_one.fitness)
            self.historico_fitness_medio.append(mean_fitness)
            self.historico_num_viaveis.append(n_viables)

        the_one = min(pops)

        return {
            "melhor_individuo": the_one,
            "populacao_final": pops,
            "historico_melhor": self.historico_melhor_fitness,
            "historico_medio": self.historico_fitness_medio,
            "historico_viaveis": self.historico_num_viaveis
        }