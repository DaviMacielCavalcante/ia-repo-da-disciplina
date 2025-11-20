"""
Classe base abstrata para definição de problemas de otimização.
"""

from abc import ABC, abstractmethod
import numpy as np

class ProblemaOptimizacao(ABC):
    """
    Classe abstrata que define a interface de um problema de otimização.
    """

    def __init__(self):
        self.n_vars = None 
        self.n_constraints = None 
        self.lower_bounds = None 
        self.upper_bounds = None 

    @abstractmethod
    def objective(self, x):
        """
        Calcula o valor da função objetivo.
        
        Args:
            x: array numpy com os valores das variáveis
            
        Returns:
            float: valor da função objetivo
        """
        pass

    @abstractmethod
    def constraints(self, x):
        """
        Calcula os valores das restrições.
        
        Args:
            x: array numpy com os valores das variáveis
            
        Returns:
            array numpy: valores das restrições (≤ 0 para satisfeitas)
        """
        pass
    
    def evaluate(self, x):
        """
        Avalia uma solução completa (objetivo + restrições).
        
        Args:
            x: array numpy com os valores das variáveis
            
        Returns:
            dict: dicionário com objective, constraints, n_violations, violation_sum
        """
        objective = self.objective(x)
        constraints = self.constraints(x)
        
        violations = np.sum(constraints > 0)
        violations_sum = np.sum(constraints[constraints > 0])
        
        return {
            "objective": objective,
            "constraints": constraints,
            "n_violations": violations,
            "violation_sum": violations_sum
        }