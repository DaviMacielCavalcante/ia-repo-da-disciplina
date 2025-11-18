import numpy as np
from .individuo import Individuo

def criar_populacao_inicial(problem, tamanho_populacao):
    """
    Cria população inicial com indivíduos aleatórios.
    
    Args:
        problem: instância de TBTProblem
        tamanho_populacao: número de indivíduos
        
    Returns:
        Lista de objetos Individuo
    """
    populacao = []
    
    for _ in range(tamanho_populacao):

        # Gera genes aleatórios dentro dos limites
        genes = np.random.uniform(
            low=problem.lower_bounds,
            high=problem.upper_bounds,
            size=problem.n_vars
        )
        

        individuo = Individuo(genes, problem)  
        

        populacao.append(individuo)  
    
    return populacao