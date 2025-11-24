import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


class WeldedBeamProblem(ProblemaOptimizacao):
    """
    WBD — Welded Beam Design Problem
    Minimização do custo total da viga soldada.

    Variáveis:
        x1 = h   (espessura da solda)
        x2 = l   (comprimento da solda)
        x3 = t   (espessura do reforço)
        x4 = b   (largura do reforço)
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 4
        self.n_constraints = 7

        self.lower_bounds = np.array([0.1, 0.1, 0.1, 0.1], dtype=float)
        self.upper_bounds = np.array([2.0, 10.0, 10.0, 2.0], dtype=float)

        # Parâmetros clássicos do problema
        self.P = 6000.0
        self.L = 14.0
        self.E = 30e6
        self.G = 12e6
        self.tau_max = 13600.0
        self.sigma_max = 30000.0
        self.delta_max = 0.25

        self.optimization = "min"

    # -----------------------------------------------------------
    #                   Função objetivo
    # -----------------------------------------------------------
    def objective(self, x):
        h, l, t, b = x
        # Custo (peso + solda)
        return 1.10471 * h**2 * l + 0.04811 * t * b * (14.0 + l)

    # -----------------------------------------------------------
    #                   Restrições g(x) <= 0
    # -----------------------------------------------------------
    def constraints(self, x):
        h, l, t, b = x

        P = self.P
        L = self.L
        E = self.E
        G = self.G
        tau_max = self.tau_max
        sigma_max = self.sigma_max
        delta_max = self.delta_max

        # Constantes
        M = P * (L + l/2)
        R = np.sqrt(l**2 + (2*h)**2) / 2
        J = 2 * (h * l) * (l**2 + 4*h**2) / 12

        # Tensões
        tau1 = P / (np.sqrt(2) * h * l)
        tau2 = M * R / J
        tau = np.sqrt(tau1**2 + 2 * tau1 * tau2 * l / (2*R) + tau2**2)

        sigma = 6 * P * L / (b * t**2)

        # Deflexão
        delta = 4 * P * L**3 / (E * t**3 * b)

        # Restrições
        g1 = tau - tau_max
        g2 = sigma - sigma_max
        g3 = h - b
        g4 = P - (b * t**2) * 6000
        g5 = delta - delta_max
        g6 = 0.10471 * h**2 + 0.04811 * t * b * (14.0 + l) - 5.0  # limite de custo parcial
        g7 = 0.125 - h

        return np.array([g1, g2, g3, g4, g5, g6, g7], dtype=float)
