from projeto_ia_experimental.individuo import TBTProblem
import numpy as np

problem = TBTProblem()
x_test = np.array([0.5, 0.5])
result = problem.evaluate(x_test)

print("=== Teste 1: x = [0.5, 0.5] ===")
print(f"Objetivo: {result['objective']:.4f}")
print(f"Restrições: {result['constraints']}")
print(f"N° Violações: {result['n_violations']}")
print(f"Soma Violações: {result['violation_sum']:.4f}")

# Teste 2: Solução nos limites
x_test2 = np.array([0.788675, 0.408248])  # Uma solução conhecida
result2 = problem.evaluate(x_test2)

print("\n=== Teste 2: x = [0.788675, 0.408248] ===")
print(f"Objetivo: {result2['objective']:.4f}")
print(f"Restrições: {result2['constraints']}")
print(f"N° Violações: {result2['n_violations']}")

def comapre_solutions(sol1, sol2):
    """
    Compara duas soluções usando o método de Deb.
    
    Args:
        sol1, sol2: dicionários retornados por evaluate()
        
    Returns:
        1 se sol1 é melhor
        -1 se sol2 é melhor
        0 se são equivalentes
    """    