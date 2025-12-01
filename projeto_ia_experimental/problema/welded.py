import numpy as np
from .problema_otimizacao import ProblemaOptimizacao

#  Welded Beam Design - Versão 1 (WBD1)

class WeldedBeamWBD1(ProblemaOptimizacao):
    """
    Welded Beam Design Problem - WBD1

    Vetor de decisão:
        x1 = espessura da solda      (h)
        x2 = comprimento da solda    (l)
        x3 = altura da viga          (t)
        x4 = espessura da viga       (b)

    f(x) = 1.10471 * x1^2 * x2 + 0.04811 * x3 * x4 * (14 + x2)

    Restrições (g_i(x) <= 0):
        g1: tau(x)   - tau_max   <= 0   (tensão de cisalhamento)
        g2: sigma(x) - sigma_max <= 0   (tensão normal)
        g3: x1 - x4            <= 0
        g4: 0.125 - x1         <= 0
        g5: delta(x) - delta_max <= 0   (deflexão)
        g6: P - Pc(x)          <= 0     (flambagem)
    """

    def __init__(self):
        super().__init__()

        self.n_vars = 4
        self.n_constraints = 6

        # Bounds do artigo
        self.lower_bounds = np.array([0.1, 0.1, 0.1, 0.1], dtype=float)
        self.upper_bounds = np.array([2.0, 10.0, 10.0, 2.0], dtype=float)

        # Constantes
        self.P = 6000.0        
        self.L = 14.0          
        self.tau_max = 13600.0 
        self.sigma_max = 30000.0 
        self.G = 12e6          
        self.E = 30e6          
        self.delta_max = 0.25  

        self.optimization = "min"

    # ------------------------ objetivo ------------------------

    def objective(self, x: np.ndarray) -> float:
        x1, x2, x3, x4 = x
        return 1.10471 * x1**2 * x2 + 0.04811 * x3 * x4 * (14.0 + x2)

    # ----------------------- restrições -----------------------

    def constraints(self, x: np.ndarray) -> np.ndarray:
        x1, x2, x3, x4 = x

        # Momento polar de inércia J(x) - WBD1 (eq. 93)
        J = self._J_wbd1(x1, x2, x3)

        # Tensão de cisalhamento total tau(x) (eq. 90–92)
        tau = self._tau_total(x1, x2, x3, J)

        # Tensão normal sigma(x) (eq. 95)
        sigma = self._sigma(x3, x4)

        # Deflexão delta(x) (eq. 96, caso WBD1)
        delta = self._delta_wbd1(x3, x4)

        # Carga crítica de flambagem Pc(x) (eq. 97, caso WBD1)
        Pc = self._Pc_wbd1(x3, x4)

        g1 = tau - self.tau_max
        g2 = sigma - self.sigma_max
        g3 = x1 - x4
        g4 = 0.125 - x1
        g5 = delta - self.delta_max
        g6 = self.P - Pc

        return np.array([g1, g2, g3, g4, g5, g6], dtype=float)

    # ------------------ funções auxiliares --------------------

    def _R(self, x1: float, x2: float, x3: float) -> float:
        """
        Momento sobre o centro de gravidade da solda (eq. 94):
        R = sqrt(0.25 * x2^2 + [0.5*(x1 + x3)]^2)
        """
        return np.sqrt(0.25 * x2**2 + (0.5 * (x1 + x3))**2)

    def _J_wbd1(self, x1: float, x2: float, x3: float) -> float:
        """
        Momento polar de inércia J(x) para WBD1 (eq. 93, primeira linha):
        J(x) = 2 * (x1*x2/√2) * [x2²/12 + ((x1+x3)/2)²]
        """
        return 2.0 * (x1 * x2 / np.sqrt(2.0)) * (
            x2**2 / 12.0 + ((x1 + x3) / 2.0)**2
        )

    def _tau1(self, x1: float, x2: float) -> float:
        """
        Tensão primária (eq. 90):
        tau1 = P / (sqrt(2) * x1 * x2)
        """
        return self.P / (np.sqrt(2.0) * x1 * x2)

    def _tau2(self, x1: float, x2: float, x3: float, J: float) -> float:
        """
        Tensão secundária (eq. 91):
        tau2 = [ R * P * (L + 0.5 x2) ] / J
        """
        R_val = self._R(x1, x2, x3)
        return R_val * self.P * (self.L + 0.5 * x2) / J

    def _tau_total(self, x1: float, x2: float, x3: float, J: float) -> float:
        """
        Tensão de cisalhamento resultante (eq. 92):
        tau = sqrt(tau1^2 + 2*tau1*tau2*(x2/(2R)) + tau2^2)
        """
        tau1 = self._tau1(x1, x2)
        tau2 = self._tau2(x1, x2, x3, J)
        R_val = self._R(x1, x2, x3)
        return np.sqrt(tau1**2 + 2.0 * tau1 * tau2 * (x2 / (2.0 * R_val)) + tau2**2)

    def _sigma(self, x3: float, x4: float) -> float:
        """
        Tensão normal na viga (eq. 95):
        sigma(x) = 6 P L / (x4 * x3^2)
        """
        return 6.0 * self.P * self.L / (x4 * x3**2)

    def _delta_wbd1(self, x3: float, x4: float) -> float:
        """
        Deflexão da ponta da viga - WBD1 (eq. 96, primeira linha):
        delta(x) = 4 P L^3 / (E x3^3 x4)
        """
        return 4.0 * self.P * self.L**3 / (self.E * x3**3 * x4)

    def _Pc_wbd1(self, x3: float, x4: float) -> float:
        """
        Carga crítica de flambagem - WBD1 (eq. 97, primeira linha):
        Pc(x) = (4.013/L²) * √(E*G*x3²*x4⁶/36) * [1 - (x3/(2L))*√(E/(4G))]
        """
        raiz = np.sqrt(self.E * self.G * x3**2 * x4**6 / 36.0)
        fator = 1.0 - x3 * np.sqrt(self.E / (4.0 * self.G)) / (2.0 * self.L)
        return 4.013 * raiz * fator / (self.L**2)



#  Welded Beam Design - Versão 2 (WBD2)


class WeldedBeamWBD2(WeldedBeamWBD1):
    """
    Welded Beam Design Problem - WBD2

    Mesma função objetivo do WBD1, mas:
      - Usa J(x), delta(x) e Pc(x) com fórmulas específicas de WBD2.
      - Adiciona a restrição extra g7(x) (eq. 89):
            g7(x) = 0.10471 x1^2 + 0.04811 x3 x4 (14 + x2) - 5 <= 0
    """

    def __init__(self):
        super().__init__()
        self.n_constraints = 7  # WBD2 tem 7 g(x) em vez de 6

    def constraints(self, x: np.ndarray) -> np.ndarray:
        x1, x2, x3, x4 = x

        # J(x), delta(x) e Pc(x) agora usam as fórmulas da WBD2
        J = self._J_wbd2(x1, x2, x3)
        tau = self._tau_total(x1, x2, x3, J)
        sigma = self._sigma(x3, x4)
        delta = self._delta_wbd2(x3, x4)
        Pc = self._Pc_wbd2(x3, x4)

        g1 = tau - self.tau_max
        g2 = sigma - self.sigma_max
        g3 = x1 - x4
        g4 = 0.125 - x1
        g5 = delta - self.delta_max
        g6 = self.P - Pc

        # Restrição extra g7 (eq. 89)
        g7 = 0.10471 * x1**2 + 0.04811 * x3 * x4 * (14.0 + x2) - 5.0

        return np.array([g1, g2, g3, g4, g5, g6, g7], dtype=float)

    # ----------------- auxiliares específicas de WBD2 -----------------

    def _J_wbd2(self, x1: float, x2: float, x3: float) -> float:
        """
        Momento polar de inércia J(x) para WBD2 (eq. 93, segunda linha):
        J(x) = 2 * (√2*x1*x2) * [x2²/4 + ((x1+x3)/2)²]
        """
        return 2.0 * (np.sqrt(2.0) * x1 * x2) * (
            x2**2 / 4.0 + ((x1 + x3) / 2.0)**2
        )

    def _delta_wbd2(self, x3: float, x4: float) -> float:
        """
        Deflexão da ponta da viga - WBD2 (eq. 96, segunda linha):
        delta(x) = 6 P L^3 / (E x3^3 x4)
        """
        return 6.0 * self.P * self.L**3 / (self.E * x3**3 * x4)

    def _Pc_wbd2(self, x3: float, x4: float) -> float:
        """
        Carga crítica de flambagem - WBD2 (eq. 97, segunda linha):
        Pc(x) = (4.013*E/L²) * √(x3²*x4⁶/36) * [1 - (x3/(2L))*√(E/(4G))]
        """
        raiz = np.sqrt(x3**2 * x4**6 / 36.0)
        fator = 1.0 - x3 * np.sqrt(self.E / (4.0 * self.G)) / (2.0 * self.L)
        return 4.013 * self.E * raiz * fator / (self.L**2)