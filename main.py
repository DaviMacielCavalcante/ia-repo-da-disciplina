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

def compare_solutions(sol1, sol2):
    """
    Compara duas soluções usando o método de Deb.
    
    Args:
        sol1, sol2: dicionários retornados por evaluate()
        
    Returns:
        1 se sol1 é melhor
        -1 se sol2 é melhor
        0 se são equivalentes
    """    

    viavel1 = sol1['n_violations'] == 0
    viavel2 = sol2['n_violations'] == 0

    if viavel1 and not viavel2:
        return 1
    
    if viavel2 and not viavel1:
        return -1
    
    if viavel1 and viavel2:
        if sol1['objective'] < sol2['objective']:
            return 1 
        elif sol1['objective'] > sol2['objective']:
            return -1
        else:
            return 0
        
    if sol1["violation_sum"] < sol2["violation_sum"]:
        return 1
    elif sol1["violation_sum"] > sol2["violation_sum"]:
        return -1
    else:
        return 0
    
# Teste 1: Viável vs Inviável
sol_viavel = {'objective': 300, 'n_violations': 0, 'violation_sum': 0}
sol_inviavel = {'objective': 100, 'n_violations': 2, 'violation_sum': 1.5}

print(compare_solutions(sol_viavel, sol_inviavel))  # Deve retornar 1

# Teste 2: Ambas viáveis, objetivos diferentes
sol_a = {'objective': 200, 'n_violations': 0, 'violation_sum': 0}
sol_b = {'objective': 250, 'n_violations': 0, 'violation_sum': 0}

print(compare_solutions(sol_a, sol_b))  # Deve retornar 1

# Teste 3: Ambas inviáveis, violações diferentes
sol_c = {'objective': 200, 'n_violations': 2, 'violation_sum': 0.5}
sol_d = {'objective': 180, 'n_violations': 3, 'violation_sum': 1.2}

print(compare_solutions(sol_c, sol_d))  # Deve retornar 1