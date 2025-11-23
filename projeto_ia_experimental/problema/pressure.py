import numpy as np
from .problema_otimizacao import ProblemaOptimizacao

class PressureVesselProblem(ProblemaOptimizacao):
    """
    Pressure Vessel Design (DPV1 / DPV2)
    version=1 -> DPV1 (x4 <= 200)
    version=2 -> DPV2 (x4 <= 240)
    """

    def __init__(self, version: int = 1):
        super().__init__()

        self.n_vars = 4
        self.n_constraints = 4

        # x1, x2 múltiplos de 0.0625; x3, x4 contínuos
        self.lower_bounds = np.array([0.0625, 0.0625, 10.0, 10.0], dtype=float)

        if version == 1:
            self.upper_bounds = np.array([6.1875, 6.1875, 200.0, 200.0], dtype=float)
        else:
            self.upper_bounds = np.array([6.1875, 6.1875, 200.0, 240.0], dtype=float)

        self.version = version
        self.optimization = "min"

    def objective(self, x: np.ndarray) -> float:
        x1, x2, x3, x4 = x
        # f(x) = 0.6224 x1 x3 x4 + 1.7781 x2 x3² + 3.1661 x1² x4 + 19.84 x1² x3
        return (
            0.6224 * x1 * x3 * x4
            + 1.7781 * x2 * x3**2
            + 3.1661 * x1**2 * x4
            + 19.84  * x1**2 * x3
        )

    def constraints(self, x: np.ndarray) -> np.ndarray:
        x1, x2, x3, x4 = x

        g1 = -x1 + 0.0193 * x3      # <= 0
        g2 = -x2 + 0.00954 * x3     # <= 0
        g3 = (
            -np.pi * x3**2 * x4
            - (4.0 / 3.0) * np.pi * x3**3
            + 1296000.0
        )                           # <= 0
        g4 = x4 - 240.0             # <= 0 (o bound de x4 já diferencia DPV1/DPV2)

        return np.array([g1, g2, g3, g4], dtype=float)
