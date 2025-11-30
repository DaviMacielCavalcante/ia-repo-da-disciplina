import numpy as np
from .problema_otimizacao import ProblemaOptimizacao


# =============================================================================
#  Base do Pressure Vessel (DPV1 / DPV2)
# =============================================================================

class _PressureVesselBase(ProblemaOptimizacao):
    """
    Pressure Vessel Design Problem Base (Real-valued version).

    Variáveis de decisão:
        x1 = espessura da casca (Ts)
        x2 = espessura do tampo (Th)
        x3 = raio interno        (R)
        x4 = comprimento cilíndrico do vaso (L)

    Função objetivo (minimização):
        f(x) = 0.6224 x1 x3 x4 + 1.7781 x2 x3² + 3.1661 x1² x4 + 19.84 x1² x3

    Restrições:
        g1(x) = -x1 + 0.0193 x3                      <= 0
        g2(x) = -x2 + 0.00954 x3                     <= 0
        g3(x) = -x3²·x4 - (4/3)π·x3³ + 1296000       <= 0
        g4(x) = x4 - 240                             <= 0  (igual para ambas versões - paper)
        *A diferença DPV1/DPV2 está SOMENTE nos bounds do domínio.*
    """

    def __init__(self, x4_max: float, name: str):
        super().__init__()

        # Esse problema tem 4 variáveis e 4 restrições
        self.n_vars = 4
        self.n_constraints = 4

        # Bounds globais do problema (na versão real-valued contínua do artigo)
        # DPV1: x4_max=200.0 → 10 ≤ x₄ ≤ 200 (domínio)
        # DPV2: x4_max=240.0 → 10 ≤ x₄ ≤ 240 (domínio)
        self.lower_bounds = np.array([0.0625, 0.0625, 10.0, 10.0], dtype=float)
        self.upper_bounds = np.array([6.1875, 6.1875, 200.0, x4_max], dtype=float)

        self.name = name
        self.optimization = "min"

    # ------------------------ Objetivo ------------------------

    def objective(self, x: np.ndarray) -> float:
        x1, x2, x3, x4 = x
        return (
            0.6224 * x1 * x3 * x4
            + 1.7781 * x2 * x3**2
            + 3.1661 * x1**2 * x4
            + 19.84  * x1**2 * x3
        )

    # ------------------------ Restrições ------------------------

    def constraints(self, x: np.ndarray) -> np.ndarray:
        x1, x2, x3, x4 = x

        g1 = -x1 + 0.0193  * x3
        g2 = -x2 + 0.00954 * x3
        g3 = -x3**2 * x4 - (4.0 / 3.0) * np.pi * x3**3 + 1296000.0
        g4 = x4 - 240.0  # ✅ exatamente como no artigo/paper para ambas as versões

        return np.array([g1, g2, g3, g4], dtype=float)


# =============================================================================
#  DPV1  (Pressure Vessel versão 1)
# =============================================================================

class PressureVesselDPV1(_PressureVesselBase):
    """
    Pressure Vessel Design - DPV1

    Bounds do domínio:
        0.0625 ≤ x1 ≤ 6.1875
        0.0625 ≤ x2 ≤ 6.1875
        10.0   ≤ x3 ≤ 200.0
        10.0   ≤ x4 ≤ 200.0  ✅
    """

    def __init__(self):
        super().__init__(x4_max=200.0, name="DPV1")


# =============================================================================
#  DPV2  (Pressure Vessel versão 2)
# =============================================================================

class PressureVesselDPV2(_PressureVesselBase):
    """
    Pressure Vessel Design - DPV2

    Bounds do domínio:
        0.0625 ≤ x1 ≤ 6.1875
        0.0625 ≤ x2 ≤ 6.1875
        10.0   ≤ x3 ≤ 200.0
        10.0   ≤ x4 ≤ 240.0  ✅
    """

    def __init__(self):
        super().__init__(x4_max=240.0, name="DPV2")
