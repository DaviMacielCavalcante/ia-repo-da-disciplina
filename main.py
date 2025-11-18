from projeto_ia_experimental.individuo import TBTProblem
from projeto_ia_experimental.populacao import criar_populacao_inicial
import numpy as np

np.random.seed(42)  # Para ter resultados reproduzíveis

problem = TBTProblem()
populacao = criar_populacao_inicial(problem, 10)

print(f"=== População Criada ===")
print(f"Tamanho: {len(populacao)} indivíduos\n")

print("=== Primeiros 3 (não avaliados) ===")
for i in range(3):
    print(f"{i+1}. {populacao[i]}")

# Avaliar todos
for ind in populacao:
    ind.evaluate()

print("\n=== Primeiros 3 (avaliados) ===")
for i in range(3):
    print(f"{i+1}. {populacao[i]}")

# Melhor
melhor = min(populacao)
print(f"\n=== Melhor ===")
print(melhor)