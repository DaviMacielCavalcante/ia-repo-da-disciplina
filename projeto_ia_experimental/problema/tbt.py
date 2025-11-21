import numpy as np
from .problema_otimizacao import ProblemaOptimizacao

class TBTProblem(ProblemaOptimizacao):
    """
    Three Bar Truss Design Problem.
    
    Minimiza o volume de uma treliça de três barras sujeita a restrições
    de tensão.
    """
    def __init__(self):
        self.n_vars = 2
        self.n_constraints = 3
        self.lower_bounds = np.array([0, 0])
        self.upper_bounds = np.array([1, 1])

        # comprimento (cm)
        self.l = 100
        # carga aplicada (KN/cm²)
        self.P = 2
        # tensão máxima permitida (KN/cm²)
        self.sigma = 2

    def objective(self, x):
        x1 = x[0]
        x2 = x[1]

        # f(x) = (2√2·x₁ + x₂) × l
        f = (2 * np.sqrt(2)*x1 + x2) * self.l

        return f
        

    def constraints(self, x):
        x1, x2 = x[0], x[1]

        common = np.sqrt(2)*x1**2 + 2*x1 *x2

        r1 = ((np.sqrt(2)*x1 + x2) / common)*self.P - self.sigma

        r2 = (x2 / common)*self.P - self.sigma

        r3 = (1 / (x1 + np.sqrt(2)*x2))*self.P - self.sigma


        return np.array([r1,r2,r3])
        

    def evaluate(self, x):
        
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