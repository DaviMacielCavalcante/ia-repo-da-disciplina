import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


class SpeedReducerProblem(ProblemaOptimizacao):
    """
    SRD – Speed Reducer Design Problem
    Benchmark clássico de otimização com 7 variáveis contínuas.
    Objetivo: minimizar o peso do conjunto.
    
    Baseado nas Equações 58-69 do artigo:
    "Game Theory and Social Interaction for Selection and Crossover 
    Pressure Control in Genetic Algorithms"
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 7
        self.n_constraints = 11

        # Domínios padrão do problema (Seção VI-D)
        self.lower_bounds = np.array([
            2.6,    # x1: Face Width
            0.7,    # x2: Teeth Modulus
            17.0,   # x3: Number of teeth in pinion
            7.3,    # x4: Length of 1st shaft between bearings
            7.3,    # x5: Length of 2nd shaft between bearings
            2.9,    # x6: Diameter of 1st shaft
            5.0     # x7: Diameter of 2nd shaft
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
    #        Função objetivo (minimizar peso) - Eq. 58
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

        # g1 (Eq. 59)
        g[0] = 27.0 / (x1 * x2**2 * x3) - 1.0
        
        # g2 (Eq. 60)
        g[1] = 397.5 / (x1 * x2**2 * x3**2) - 1.0
        
        # g3 (Eq. 61)
        g[2] = 1.93 * x4**3 / (x2 * x3 * x6**4) - 1.0
        
        # g4 (Eq. 62)
        g[3] = 1.93 * x5**3 / (x2 * x3 * x7**4) - 1.0
        
        # g5 (Eq. 63) - CORRIGIDO
        termo1 = (745.0 * x4 / (x2 * x3))**2 + 1.69e6
        g[4] = np.sqrt(termo1) / (110.0 * x6**3) - 1.0
        
        # g6 (Eq. 64) - CORRIGIDO
        termo2 = (745.0 * x5 / (x2 * x3))**2 + 157.5e6
        g[5] = np.sqrt(termo2) / (85.0 * x7**3) - 1.0
        
        # g7 (Eq. 65)
        g[6] = (x2 * x3) / 40.0 - 1.0
        
        # g8 (Eq. 66) - CORRIGIDO
        g[7] = (5.0 * x2 / x1) - 1.0
        
        # g9 (Eq. 67) - CORRIGIDO
        g[8] = x1 / (12.0 * x2) - 1.0
        
        # g10 (Eq. 68) - CORRIGIDO
        g[9] = (1.5 * x6 + 1.9) / x4 - 1.0
        
        # g11 (Eq. 69) - CORRIGIDO
        g[10] = (1.1 * x7 + 1.9) / x5 - 1.0

        return g