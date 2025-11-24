import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


class SpeedReducerProblem(ProblemaOptimizacao):
    """
    SRD — Speed Reducer Design Problem
    Benchmark clássico de otimização com 7 variáveis contínuas.
    Objetivo: minimizar o peso do conjunto.
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 7
        self.n_constraints = 11

        # Domínios padrão do problema
        self.lower_bounds = np.array([
            2.6,    # x1
            0.7,    # x2
            17.0,   # x3
            7.3,    # x4
            7.3,    # x5
            2.9,    # x6
            5.0     # x7
        ], dtype=float)

        self.upper_bounds = np.array([
            3.6,    # x1
            0.8,    # x2
            28.0,   # x3
            8.3,    # x4
            8.3,    # x5
            3.9,    # x6
            5.5     # x7
        ], dtype=float)

        self.optimization = "min"

    # -----------------------------------------------------
    #        Função objetivo (minimizar peso)
    # -----------------------------------------------------
    def objective(self, x):
        x1, x2, x3, x4, x5, x6, x7 = x

        return (
            0.7854 * x1 * x2**2 * (3.3333 * x3**2 + 14.9334 * x3 - 43.0934)
            - 1.508 * x1 * (x6**2 + x7**2)
            + 7.477 * (x6**3 + x7**3)
            + 0.7854 * (x4 * x6**2 + x5 * x7**2)
        )

    # -----------------------------------------------------
    #                 Restrições g(x) <= 0
    # -----------------------------------------------------
    def constraints(self, x):
        x1, x2, x3, x4, x5, x6, x7 = x

        g = np.zeros(11)

        g[0] = 27.0 / (x1 * x2**2 * x3) - 1.0
        g[1] = 397.5 / (x1 * x2**2 * x3**2) - 1.0
        g[2] = 1.93 * x4**3 / (x2 * x3 * x6**4) - 1.0
        g[3] = 1.93 * x5**3 / (x2 * x3 * x7**4) - 1.0
        g[4] = (np.sqrt( (745.0 * x4 / (x2 * x3))**2 + 16.9e6 ) / 1100.0) - 1.0
        g[5] = (np.sqrt( (745.0 * x5 / (x2 * x3))**2 + 157.5e6 ) / 850.0) - 1.0
        g[6] = (x2 * x3) / 40.0 - 1.0
        g[7] = (x4 / (x2 * x3)) - 12.0
        g[8] = (x5 / (x2 * x3)) - 12.0
        g[9] = 5.0 - (x2 / x1)
        g[10] = (x1 / x2) - 1.5

        return g
