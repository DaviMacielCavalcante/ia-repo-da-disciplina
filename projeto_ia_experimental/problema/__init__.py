"""
Módulo de problemas de otimização.
"""
from .problema_otimizacao import ProblemaOptimizacao
from .tbt import TBTProblem
from .himmel import HimmelblauHNO1,HimmelblauHNO2
from .mwtcs import SpringProblem
from .pressure import PressureVesselDPV1,PressureVesselDPV2
from .srd import SpeedReducerProblem
from .tcd import TabularColumnProblem
from .welded import WeldedBeamWBD1,WeldedBeamWBD2

__all__ = ['ProblemaOptimizacao', 'TBTProblem']