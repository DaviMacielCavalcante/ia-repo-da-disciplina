"""
Operadores genéticos: seleção, crossover e mutação.
"""

import numpy as np
from .individuo import Individuo

def selecao_torneio(populacao, tamanho_torneio=3):
    """
    Seleciona um indivíduo por torneio.
    
    Args:
        populacao: lista de objetos Individuo
        tamanho_torneio: número de competidores (default=3)
        
    Returns:
        Individuo: O melhor indivíduo do torneio
    """

    list_indx = np.random.choice(range(len(populacao)), size=tamanho_torneio, replace=False)

    pops = [populacao[i] for i in list_indx]

    return min(pops)

def crossover_blx_alpha(pai, mae, alpha=0.5):
    """
    Crossover BLX-α (Blend Crossover Alpha).
    
    Args:
        pai: Individuo (pai)
        mae: Individuo (mae)
        alpha: parâmetro de expansão (default=0.5)
        
    Returns:
        tuple: (filho1, filho2) - dois novos Individuos
    """    

    problem = pai.problem
    n_vars = problem.n_vars

    genes_filho_1 = np.zeros(n_vars)
    genes_filho_2 = np.zeros(n_vars)

    for i in range(n_vars):

        gene_pai = pai.genes[i]
        gene_mae = mae.genes[i]

        min_value = min(gene_pai, gene_mae)
        max_value = max(gene_pai, gene_mae)

        gene_range = max_value - min_value

        lower = min_value - alpha * gene_range
        upper = max_value + alpha * gene_range

        lower = max(lower, problem.lower_bounds[i])
        upper = min(upper, problem.upper_bounds[i])

        genes_filho_1[i] = np.random.uniform(lower, upper)
        genes_filho_2[i] = np.random.uniform(lower, upper)

    filho1 = Individuo(genes_filho_1, problem)
    filho2 = Individuo(genes_filho_2, problem)

    return filho1, filho2

def mutacao_gaussiana(individuo, taxa_mutacao=0.1, sigma=0.1):
    """
    Mutação gaussiana.
    
    Args:
        individuo: Individuo a ser mutado
        taxa_mutacao: probabilidade de mutar cada gene (default=0.1)
        sigma: desvio padrão da distribuição normal (default=0.1)
        
    Returns:
        Individuo: Novo indivíduo mutado
    """    

    problem = individuo.problem
    n_vars = problem.n_vars

    x_genes = individuo.genes.copy()

    for i in range(n_vars):
        if np.random.random() < taxa_mutacao:

            gene_range = problem.upper_bounds[i] - problem.lower_bounds[i]

            noise = np.random.normal(0, sigma) * gene_range 

            x_genes[i] = x_genes[i] + noise 

            x_genes[i] = np.clip(
                x_genes[i],
                problem.lower_bounds[i],
                problem.upper_bounds[i]
            )

    return Individuo(x_genes, problem)