"""
Teste simples do GASI-POP
"""

from projeto_ia_experimental.problema import TBTProblem
from projeto_ia_experimental.gasi_pop import GASIPOP

# Configuração
config = {
    'tamanho_populacao': 50,
    'num_geracoes': 20,
    'taxa_crossover': 0.9,
    'taxa_mutacao': 0.15,
    'tamanho_torneio': 3,
    'num_elites': 2,
    'num_rounds': 10
}

problem = TBTProblem()

print("=" * 60)
print("TESTE DO GASI-POP")
print("=" * 60)

gasi = GASIPOP(problem, config)
resultado = gasi.executar()

print(f"\nMelhor fitness: {resultado['melhor_individuo'].fitness:.4f}")
print(f"Genes: {resultado['melhor_individuo'].genes}")
print(f"Viável: {resultado['melhor_individuo'].is_feasible()}")
print(f"\nGerações: {len(resultado['historico_melhor'])}")
print(f"Primeiro fitness: {resultado['historico_melhor'][0]:.4f}")
print(f"Último fitness: {resultado['historico_melhor'][-1]:.4f}")

print("\n✅ GASI-POP funcionou!")