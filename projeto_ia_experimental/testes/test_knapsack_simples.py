"""
Teste simples do Problema da Mochila
"""

from projeto_ia_experimental.problema.knapsack import KnapsackProblem
import numpy as np

# Exemplo simples: 4 itens
weights = [2, 5, 3, 1]
values = [10, 20, 15, 5]
capacity = 8

problem = KnapsackProblem(weights, values, capacity)

print("=" * 60)
print("TESTE DO PROBLEMA DA MOCHILA")
print("=" * 60)
print(f"Itens: {len(weights)}")
print(f"Capacidade: {capacity}")
print(f"\nItens:")
for i in range(len(weights)):
    print(f"  Item {i}: peso={weights[i]}, valor={values[i]}")

# Teste 1: Todos com mesma prioridade
print("\n" + "-" * 60)
print("TESTE 1: Prioridades iguais [0.5, 0.5, 0.5, 0.5]")
genes1 = np.array([0.5, 0.5, 0.5, 0.5])
fitness1, viavel1, peso1 = problem.evaluate(genes1)
print(f"Valor total: {fitness1}")
print(f"Peso usado: {peso1}/{capacity}")

# Teste 2: Priorizar item 1 (maior valor)
print("\n" + "-" * 60)
print("TESTE 2: Priorizar item 1 [0.1, 0.9, 0.3, 0.2]")
genes2 = np.array([0.1, 0.9, 0.3, 0.2])
fitness2, viavel2, peso2 = problem.evaluate(genes2)
print(f"Valor total: {fitness2}")
print(f"Peso usado: {peso2}/{capacity}")

# Teste 3: Solução ótima (itens 0, 2, 3)
print("\n" + "-" * 60)
print("TESTE 3: Solução ótima [0.9, 0.1, 0.8, 0.7]")
genes3 = np.array([0.9, 0.1, 0.8, 0.7])
fitness3, viavel3, peso3 = problem.evaluate(genes3)
print(f"Valor total: {fitness3}")
print(f"Peso usado: {peso3}/{capacity}")
print(f"Esperado: valor=30 (itens 0+2+3)")

print("\n✅ Testes concluídos!")