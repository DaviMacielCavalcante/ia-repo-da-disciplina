import numpy as np
from .problema_otimizacao import ProblemaOptimizacao

class HimmelblauProblem(ProblemaOptimizacao):
    """
    Himmelblau Nonlinear Optimization
    version=1 -> HNO1
    version=2 -> HNO2
    """

    def __init__(self, version: int = 1):
        super().__init__()

        self.n_vars = 5
        # 3 funções g, mas cada uma com limite inferior/superior -> 6 restrições
        self.n_constraints = 6

        # Domínio clássico do problema
        self.lower_bounds = np.array([78.0, 33.0, 27.0, 27.0, 27.0], dtype=float)
        self.upper_bounds = np.array([102.0, 45.0, 45.0, 45.0, 45.0], dtype=float)

        # Parâmetro V (muda entre HNO1 e HNO2)
        if version == 1:
            self.V = 0.0006262
        else:
            self.V = 0.0002600

        self.version = version
        self.optimization = "min"

    def objective(self, x: np.ndarray) -> float:
        x1, x2, x3, x4, x5 = x
        # f(x) = 5.3578547 x3² + 0.8356891 x1 x5 + 37.293239 x1 - 40792.141
        return (
            5.3578547 * x3**2
            + 0.8356891 * x1 * x5
            + 37.293239 * x1
            - 40792.141
        )

    def constraints(self, x: np.ndarray) -> np.ndarray:
        x1, x2, x3, x4, x5 = x

        g1 = (
            85.334407
            + 0.0056858 * x2 * x5
            + self.V * x1 * x4
            - 0.0022053 * x3 * x5
        )
        g2 = (
            80.51249
            + 0.0071317 * x2 * x5
            + 0.0029955 * x1 * x2
            - 0.0021813 * x3**2
        )
        g3 = (
            9.300961
            + 0.0047026 * x3 * x5
            + 0.0012547 * x1 * x3
            - 0.0019085 * x3 * x4
        )

        # Intervalos (formato g(x) <= 0):
        # 0   <= g1 <= 92
        # 90  <= g2 <= 110
        # 20  <= g3 <= 25
        c1_low  = 0.0   - g1      # g1 >= 0
        c1_high = g1    - 92.0    # g1 <= 92
        c2_low  = 90.0  - g2      # g2 >= 90
        c2_high = g2    - 110.0   # g2 <= 110
        c3_low  = 20.0  - g3      # g3 >= 20
        c3_high = g3    - 25.0    # g3 <= 25

        return np.array([c1_low, c1_high, c2_low, c2_high, c3_low, c3_high],
                        dtype=float)

