import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


class TabularColumnProblem(ProblemaOptimizacao):
    """
    TCD — Tabular Column Design
    Minimização do custo de uma coluna tubular.

    Variáveis:
        x1 = d  (diâmetro médio da coluna)
        x2 = t  (espessura da parede)

    Todas as restrições g(x) <= 0.
    
    Referência: Equações (75)-(81) do artigo
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 2
        self.n_constraints = 6

        # Domínio: 2.0 ≤ d ≤ 14.0; 0.2 ≤ t ≤ 0.8
        self.lower_bounds = np.array([2.0, 0.2], dtype=float)
        self.upper_bounds = np.array([14.0, 0.8], dtype=float)

        # Parâmetros do problema
        self.P = 2500.0      # Carga de compressão (kgf)
        self.L = 250.0       # Comprimento da coluna (cm)
        self.sigma_x = 500.0 # Tensão de escoamento (kgf/cm²)
        self.E = 0.85e6      # Módulo de elasticidade (kgf/cm²)

        self.optimization = "min"

    def objective(self, x):
        """
        Equação (75): f(x) = 9.82dt + 2d
        """
        d, t = x
        return 9.82 * d * t + 2.0 * d

    def constraints(self, x):
        """
        Restrições (76)-(81) do artigo.
        Todas no formato g(x) <= 0.
        """
        d, t = x
        P = self.P
        L = self.L
        sigma_x = self.sigma_x
        E = self.E

        # g1(x) = P/(π·d·t·σx) - 1 ≤ 0  [Equação 76]
        g1 = P / (np.pi * d * t * sigma_x) - 1.0

        # g2(x) = 8PL²/(π³·E·d·t·(d² + t²)) - 1 ≤ 0  [Equação 77]
        g2 = (8.0 * P * L**2) / (np.pi**3 * E * d * t * (d**2 + t**2)) - 1.0

        # g3(x) = (d × 0.5)⁻¹ - 1 ≤ 0  →  2/d - 1 ≤ 0  [Equação 78]
        g3 = 2.0 / d - 1.0

        # g4(x) = (0.07142857142 × d) - 1 ≤ 0  →  d/14 - 1 ≤ 0  [Equação 79]
        g4 = (1.0 / 14.0) * d - 1.0

        # g5(x) = (t × 5)⁻¹ - 1 ≤ 0  →  1/(5t) - 1 ≤ 0  [Equação 80]
        g5 = 1.0 / (5.0 * t) - 1.0

        # g6(x) = (1.25 × t) - 1 ≤ 0  [Equação 81]
        g6 = 1.25 * t - 1.0

        return np.array([g1, g2, g3, g4, g5, g6], dtype=float)