"""
Teste do AG no Problema da Mochila
"""

from projeto_ia_experimental.problema.knapsack import KnapsackProblem
from projeto_ia_experimental.ag import AlgoritmoGenetico

# Problema simples
weights = [2, 5, 3, 1, 4, 6, 2, 3]
values = [10, 20, 15, 5, 12, 25, 8, 14]
capacity = 15

problem = KnapsackProblem(weights, values, capacity)

config = {
    'tamanho_populacao': 50,
    'num_geracoes': 50,
    'taxa_crossover': 0.9,
    'taxa_mutacao': 0.15,
    'tamanho_torneio': 3,
    'num_elites': 2
}

print("=" * 60)
print("TESTE: AG NO PROBLEMA DA MOCHILA")
print("=" * 60)
print(f"Itens: {len(weights)}")
print(f"Capacidade: {capacity}")
print(f"\nItens disponíveis:")
for i in range(len(weights)):
    print(f"  Item {i}: peso={weights[i]}, valor={values[i]}")

print("\nExecutando AG...")
ag = AlgoritmoGenetico(problem, config)
resultado = ag.executar()

melhor = resultado['melhor_individuo']



# Mostrar quais itens foram selecionados
indices_ordenados = melhor.genes.argsort()[::-1]
peso_usado = 0
valor_usado = 0
itens_selecionados = []

for idx in indices_ordenados:
    if peso_usado + weights[idx] <= capacity:
        itens_selecionados.append(idx)
        peso_usado += weights[idx]
        valor_usado += values[idx]

print("\nItens selecionados:")
for idx in itens_selecionados:
    print(f"  Item {idx}: peso={weights[idx]}, valor={values[idx]}")

print("\n" + "-" * 60)
print("RESUMO:")
print(f"  Total de itens: {len(itens_selecionados)}/{len(weights)}")
print(f"  Peso usado: {peso_usado}/{capacity} ({100*peso_usado/capacity:.1f}%)")
print(f"  Valor obtido: {valor_usado}")
print(f"  Capacidade restante: {capacity - peso_usado}")

print("\n" + "=" * 60)
print("RESULTADO")
print("=" * 60)
print(f"Melhor valor total: {melhor.fitness}")
print(f"Peso total usado: {peso_usado}/{capacity}")


print("\n✅ Teste concluído!")