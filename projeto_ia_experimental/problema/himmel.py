import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


# =============================================================================
#  Himmelblau Nonlinear Optimization - Base
# =============================================================================

class _HimmelblauBase(ProblemaOptimizacao):
    """
    Base para os problemas de Himmelblau (HNO1 / HNO2).

    Vetor de decisão:
        x1, x2, x3, x4, x5

    Objetivo:
        f(x) = 5.3578547 x3² + 0.8356891 x1 x5 + 37.293239 x1 - 40792.141

    Restrições (intervalares):
        0   <= g1(x) <= 92
        90  <= g2(x) <= 110
        20  <= g3(x) <= 25

    No código, isso vira 6 desigualdades g_i(x) <= 0.
    """

    def __init__(self, V: float, name: str):
        super().__init__()

        self.n_vars = 5
        # 3 funções com limite inferior/superior -> 6 restrições
        self.n_constraints = 6

        self.lower_bounds = np.array([78.0, 33.0, 27.0, 27.0, 27.0], dtype=float)
        self.upper_bounds = np.array([102.0, 45.0, 45.0, 45.0, 45.0], dtype=float)

        # parâmetro que muda entre HNO1 e HNO2
        self.V = V
        self.name = name

        self.optimization = "min"

    # ------------------------ objetivo ------------------------

    def objective(self, x: np.ndarray) -> float:
        x1, x2, x3, x4, x5 = x
        return (
            5.3578547 * x3**2
            + 0.8356891 * x1 * x5
            + 37.293239 * x1
            - 40792.141
        )

    # ----------------------- restrições -----------------------

    def constraints(self, x: np.ndarray) -> np.ndarray:
        x1, x2, x3, x4, x5 = x

        # Equações g1, g2, g3 do problema clássico de Himmelblau
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

        # Transformando intervalos em g(x) <= 0
        # 0   <= g1 <= 92   →  0 - g1 <= 0  e  g1 - 92 <= 0
        # 90  <= g2 <= 110  →  90 - g2 <= 0 e  g2 - 110 <= 0
        # 20  <= g3 <= 25   →  20 - g3 <= 0 e  g3 - 25 <= 0

        c1_low  = 0.0   - g1
        c1_high = g1    - 92.0

        c2_low  = 90.0  - g2
        c2_high = g2    - 110.0

        c3_low  = 20.0  - g3
        c3_high = g3    - 25.0

        return np.array(
            [c1_low, c1_high, c2_low, c2_high, c3_low, c3_high], dtype=float
        )


# =============================================================================
#  HNO1  (Himmelblau versão 1)
# =============================================================================

class HimmelblauHNO1(_HimmelblauBase):
    """
    Himmelblau Nonlinear Optimization - HNO1
    Usa V = 0.0006262 na equação g1.
    """

    def __init__(self):
        super().__init__(V=0.0006262, name="HNO1")


# =============================================================================
#  HNO2  (Himmelblau versão 2)
# =============================================================================

class HimmelblauHNO2(_HimmelblauBase):
    """
    Himmelblau Nonlinear Optimization - HNO2
    Usa outro valor de V (mais restritivo), por exemplo V = 0.0002600.
    Ajuste esse valor se o artigo especificar outro.
    """

    def __init__(self):
        super().__init__(V=0.0002600, name="HNO2")
