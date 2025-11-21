"""
Teste simples do GBX - verificar se funciona basicamente.
"""

from projeto_ia_experimental.problema import TBTProblem
from projeto_ia_experimental.individuo import Individuo
from projeto_ia_experimental.gbx import GBXCrossover
import numpy as np

# Criar problema
problem = TBTProblem()

# Criar dois pais manualmente
pai = Individuo(np.array([0.3, 0.7]), problem)
mae = Individuo(np.array([0.5, 0.4]), problem)

print("=" * 60)
print("TESTE DO GBX CROSSOVER")
print("=" * 60)
print(f"\nPai:  genes = {pai.genes}")
print(f"Mãe:  genes = {mae.genes}")

# Criar operador GBX
gbx = GBXCrossover(num_rounds=10)

# Aplicar crossover
filho1, filho2 = gbx.apply(pai, mae)

print(f"\nFilho1: genes = {filho1.genes}")
print(f"Filho2: genes = {filho2.genes}")

# Verificar se os genes estão dentro dos limites
print("\n" + "=" * 60)
print("VERIFICAÇÃO DE LIMITES")
print("=" * 60)
print(f"Lower bounds: {problem.lower_bounds}")
print(f"Upper bounds: {problem.upper_bounds}")

dentro_limites1 = np.all(filho1.genes >= problem.lower_bounds) and \
                  np.all(filho1.genes <= problem.upper_bounds)
dentro_limites2 = np.all(filho2.genes >= problem.lower_bounds) and \
                  np.all(filho2.genes <= problem.upper_bounds)

print(f"\nFilho1 dentro dos limites? {dentro_limites1}")
print(f"Filho2 dentro dos limites? {dentro_limites2}")

# Avaliar os filhos
filho1.evaluate()
filho2.evaluate()

print("\n" + "=" * 60)
print("AVALIAÇÃO DOS FILHOS")
print("=" * 60)
print(f"Filho1: fitness = {filho1.fitness:.4f}, viável = {filho1.is_feasible()}")
print(f"Filho2: fitness = {filho2.fitness:.4f}, viável = {filho2.is_feasible()}")

print("\n✅ GBX funcionou corretamente!")