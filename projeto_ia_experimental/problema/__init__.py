"""
Módulo de problemas de otimização.
"""
from .problema_otimizacao import ProblemaOptimizacao
from .tbt import TBTProblem
from .himmel import HimmelblauProblem
from .mwtcs import SpringProblem
from .pressure import PressureVesselProblem
from .srd import SpeedReducerProblem
from .tcd import TabularColumnProblem
from .welded import WeldedBeamProblem

__all__ = ['ProblemaOptimizacao', 'TBTProblem']