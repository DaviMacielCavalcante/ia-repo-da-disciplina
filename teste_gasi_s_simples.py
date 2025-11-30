"""
Teste simples do GASI-S
"""

from projeto_ia_experimental.problema import TBTProblem
from projeto_ia_experimental.gasi_s import GASIS

config = {
    'tamanho_populacao': 500,
    'num_geracoes': 200,
    'taxa_crossover': 0.9,
    'taxa_mutacao': 0.15,
    'tamanho_torneio': 3,  # Melhor ser potência de 2 para eliminação
    'num_elites': 2,
    'num_rounds': 60
}

problem = TBTProblem()

print("=" * 60)
print("TESTE DO GASI-S")
print("=" * 60)

gasi = GASIS(problem, config)
resultado = gasi.executar()

print(f"\nMelhor fitness: {resultado['melhor_individuo'].fitness:.4f}")
print(f"Genes: {resultado['melhor_individuo'].genes}")
print(f"Viável: {resultado['melhor_individuo'].is_feasible()}")

print("\n✅ GASI-S funcionou!")