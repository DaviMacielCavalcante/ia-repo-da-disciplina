import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


class TabularColumnProblem(ProblemaOptimizacao):
    """
    TCD — Tabular Column Design
    Minimização do custo de uma coluna tubular.

    Variáveis:
        x1 = d  (diâmetro externo)
        x2 = t  (espessura da parede)

    Todas as restrições g(x) <= 0.
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 2
        self.n_constraints = 6

        # Domínio clássico
        self.lower_bounds = np.array([2.0, 0.2], dtype=float)
        self.upper_bounds = np.array([14.0, 0.8], dtype=float)

        # Parâmetros típicos
        self.P = 2500.0
        self.L = 250.0
        self.sigma_x = 500.0
        self.E = 0.85e6

        self.optimization = "min"

    def objective(self, x):
        d, t = x
        return 9.82 * d * t + 2.0 * d

    def constraints(self, x):
        d, t = x
        P = self.P
        L = self.L
        sigma_x = self.sigma_x
        E = self.E

        # Área e momento de inércia do tubo
        A = np.pi * (d**2 - (d - 2 * t)**2) / 4.0
        I = np.pi * (d**4 - (d - 2 * t)**4) / 64.0

        # Tensões e flambagem
        g1 = (P / A) / sigma_x - 1.0
        g2 = (P * L**2) / (np.pi**2 * E * I) - 1.0

        # Restrições geométricas padrões
        g3 = 0.5 - t / d
        g4 = t - 0.8
        g5 = 2.0 - d
        g6 = d - 14.0

        return np.array([g1, g2, g3, g4, g5, g6], dtype=float)
