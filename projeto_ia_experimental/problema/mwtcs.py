import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


class SpringProblem(ProblemaOptimizacao):
    """
    MWTCS - Minimização do peso de uma mola de tração/compressão.

    Variáveis:
        x1 = D   (diâmetro médio da mola)
        x2 = d   (diâmetro do fio)
        x3 = N   (número de espiras ativas)

    Objetivo:
        Minimizar o peso (volume ~ (N + 2)*d*D^2).

    Todas as restrições estão no formato g(x) <= 0.
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 3
        self.n_constraints = 4

        # Limites clássicos do benchmark
        # 0.05 ≤ D ≤ 2.0
        # 0.25 ≤ d ≤ 1.3
        # 2 ≤ N ≤ 15
        self.lower_bounds = np.array([0.05, 0.25, 2.0], dtype=float)
        self.upper_bounds = np.array([2.0, 1.3, 15.0], dtype=float)

        # É um problema de minimização
        self.optimization = "min"

    # -----------------------------------------------------
    #                 Função objetivo
    # -----------------------------------------------------
    def objective(self, x: np.ndarray) -> float:
        D, d, N = x
        # f(x) = (N + 2) * d * D^2
        return (N + 2.0) * d * D**2

    # -----------------------------------------------------
    #                 Restrições g(x) <= 0
    # -----------------------------------------------------
    def constraints(self, x: np.ndarray) -> np.ndarray:
        D, d, N = x

        # Fórmulas clássicas do benchmark MWTCS
        # g1: tensão de cisalhamento
        g1 = 1.0 - (d**3 * N) / (71785.0 * D**4)

        # g2: limite de deflexão / geometria
        g2 = (
            (4.0 * d**2 - D * d)
            / (12566.0 * (d * D**3 - D**4 / 4.0))
            + 1.0 / (5108.0 * D**2)
            - 1.0
        )

        # g3: restrição de frequência / carga
        g3 = 1.0 - (140.45 * D) / (d**2 * N)

        # g4: limite geométrico de diâmetro máximo
        g4 = (D + d) / 1.5 - 1.0

        return np.array([g1, g2, g3, g4], dtype=float)
