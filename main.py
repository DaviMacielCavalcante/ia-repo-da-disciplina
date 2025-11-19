"""
Teste completo do Algoritmo Genético para o problema TBT.
Executa múltiplas rodadas e coleta estatísticas.
"""

from projeto_ia_experimental.individuo import TBTProblem
from projeto_ia_experimental.ag import AlgoritmoGenetico
import numpy as np
import matplotlib.pyplot as plt
import time

# ==============================================================================
# CONFIGURAÇÃO DO EXPERIMENTO
# ==============================================================================

# Parâmetros do AG
config = {
    'tamanho_populacao': 150,
    'num_geracoes': 300,
    'taxa_crossover': 0.9,
    'taxa_mutacao': 0.25,   
    'tamanho_torneio': 2,
    'num_elites': 1
}
# Número de execuções independentes
num_execucoes = 20

# ==============================================================================
# EXECUÇÃO DO EXPERIMENTO
# ==============================================================================

print("=" * 80)
print(" EXPERIMENTO: Algoritmo Genético para Three Bar Truss Problem")
print("=" * 80)
print(f"\nParâmetros:")
print(f"  População: {config['tamanho_populacao']}")
print(f"  Gerações: {config['num_geracoes']}")
print(f"  Crossover: {config['taxa_crossover']}")
print(f"  Mutação: {config['taxa_mutacao']}")
print(f"  Torneio: {config['tamanho_torneio']}")
print(f"  Elites: {config['num_elites']}")
print(f"\nNúmero de execuções: {num_execucoes}")
print("\n" + "=" * 80)

# Criar problema
problem = TBTProblem()

# Armazenar resultados de todas as execuções
resultados = []
tempo_total = 0

# Executar múltiplas vezes
for i in range(num_execucoes):
    print(f"\n{'─' * 80}")
    print(f"EXECUÇÃO {i+1}/{num_execucoes}")
    print(f"{'─' * 80}")
    
    # Criar AG (sem seed para execuções diferentes)
    ag = AlgoritmoGenetico(problem, config)
    
    # Medir tempo
    inicio = time.time()
    resultado = ag.executar()
    fim = time.time()
    tempo_exec = fim - inicio
    tempo_total += tempo_exec
    
    # Extrair melhor solução
    melhor = resultado['melhor_individuo']
    
    # Armazenar informações
    resultados.append({
        'execucao': i + 1,
        'melhor_individuo': melhor,
        'fitness': melhor.fitness,
        'genes': melhor.genes.copy(),
        'viavel': melhor.is_feasible(),
        'violacoes': melhor.violation_sum,
        'historico_melhor': resultado['historico_melhor'],
        'historico_medio': resultado['historico_medio'],
        'historico_viaveis': resultado['historico_viaveis'],
        'tempo': tempo_exec
    })
    
    print(f"\n✓ Execução {i+1} concluída em {tempo_exec:.2f}s")
    print(f"  Melhor fitness: {melhor.fitness:.4f}")
    print(f"  Viável: {'SIM' if melhor.is_feasible() else 'NÃO'}")
    if not melhor.is_feasible():
        print(f"  Violações: {melhor.violation_sum:.4f}")

# ==============================================================================
# ANÁLISE ESTATÍSTICA
# ==============================================================================

print("\n" + "=" * 80)
print(" RESULTADOS ESTATÍSTICOS")
print("=" * 80)

# Separar viáveis e inviáveis
resultados_viaveis = [r for r in resultados if r['viavel']]
resultados_inviaveis = [r for r in resultados if not r['viavel']]

print(f"\nSoluções viáveis: {len(resultados_viaveis)}/{num_execucoes}")
print(f"Soluções inviáveis: {len(resultados_inviaveis)}/{num_execucoes}")

# Estatísticas das soluções viáveis
if resultados_viaveis:
    fitness_viaveis = [r['fitness'] for r in resultados_viaveis]
    
    print(f"\n--- SOLUÇÕES VIÁVEIS ---")
    print(f"Melhor fitness: {min(fitness_viaveis):.4f}")
    print(f"Pior fitness: {max(fitness_viaveis):.4f}")
    print(f"Média: {np.mean(fitness_viaveis):.4f}")
    print(f"Desvio padrão: {np.std(fitness_viaveis):.4f}")
    print(f"Mediana: {np.median(fitness_viaveis):.4f}")
    
    # Melhor solução global
    melhor_global = min(resultados_viaveis, key=lambda x: x['fitness'])
    print(f"\n--- MELHOR SOLUÇÃO GLOBAL ---")
    print(f"Execução: {melhor_global['execucao']}")
    print(f"Fitness: {melhor_global['fitness']:.4f}")
    print(f"Genes: {melhor_global['genes']}")
    print(f"Tempo: {melhor_global['tempo']:.2f}s")
else:
    print("\n⚠️ ATENÇÃO: Nenhuma solução viável encontrada!")
    print("Considere aumentar:")
    print("  - Número de gerações")
    print("  - Tamanho da população")
    print("  - Taxa de mutação")

# Estatísticas das soluções inviáveis
if resultados_inviaveis:
    violacoes = [r['violacoes'] for r in resultados_inviaveis]
    
    print(f"\n--- SOLUÇÕES INVIÁVEIS ---")
    print(f"Menor violação: {min(violacoes):.4f}")
    print(f"Maior violação: {max(violacoes):.4f}")
    print(f"Média de violações: {np.mean(violacoes):.4f}")

# Estatísticas de tempo
print(f"\n--- TEMPO DE EXECUÇÃO ---")
print(f"Tempo total: {tempo_total:.2f}s ({tempo_total/60:.2f} minutos)")
print(f"Tempo médio por execução: {tempo_total/num_execucoes:.2f}s")

# ==============================================================================
# VISUALIZAÇÃO DOS RESULTADOS
# ==============================================================================

print("\n" + "=" * 80)
print(" GERANDO GRÁFICOS")
print("=" * 80)

# Criar figura com múltiplos gráficos
fig = plt.figure(figsize=(16, 10))

# -------------------------
# Gráfico 1: Convergência de Todas as Execuções
# -------------------------
ax1 = plt.subplot(2, 3, 1)
for i, res in enumerate(resultados):
    cor = 'green' if res['viavel'] else 'red'
    alpha = 0.3 if not res['viavel'] else 0.7
    label = 'Viável' if i == 0 and res['viavel'] else ('Inviável' if i == 0 and not res['viavel'] else '')
    ax1.plot(res['historico_melhor'], color=cor, alpha=alpha, linewidth=1, label=label)

# Destacar melhor execução
if resultados_viaveis:
    melhor_exec = melhor_global
    ax1.plot(melhor_exec['historico_melhor'], color='blue', linewidth=2.5, 
             label=f"Melhor (f={melhor_exec['fitness']:.2f})")

ax1.set_xlabel('Geração')
ax1.set_ylabel('Fitness (volume cm³)')
ax1.set_title('Convergência de Todas as Execuções')
ax1.legend()
ax1.grid(True, alpha=0.3)

# -------------------------
# Gráfico 2: Box Plot dos Fitness Finais
# -------------------------
ax2 = plt.subplot(2, 3, 2)
fitness_finais = [r['fitness'] for r in resultados]
cores = ['green' if r['viavel'] else 'red' for r in resultados]

ax2.boxplot(fitness_finais, vert=True)
ax2.scatter([1]*len(fitness_finais), fitness_finais, c=cores, s=100, alpha=0.6, edgecolors='black')
ax2.set_ylabel('Fitness (volume cm³)')
ax2.set_title('Distribuição dos Fitness Finais')
ax2.set_xticks([1])
ax2.set_xticklabels(['Todas Execuções'])
ax2.grid(True, alpha=0.3, axis='y')

# -------------------------
# Gráfico 3: Soluções Viáveis ao Longo das Gerações
# -------------------------
ax3 = plt.subplot(2, 3, 3)
for i, res in enumerate(resultados):
    alpha = 0.3
    ax3.plot(res['historico_viaveis'], alpha=alpha, linewidth=1)

# Média de viáveis
historico_viaveis_medio = np.mean([r['historico_viaveis'] for r in resultados], axis=0)
ax3.plot(historico_viaveis_medio, color='blue', linewidth=2.5, label='Média')
ax3.axhline(y=config['tamanho_populacao'], color='red', linestyle='--', 
            alpha=0.5, label='População total')

ax3.set_xlabel('Geração')
ax3.set_ylabel('Nº Soluções Viáveis')
ax3.set_title('Evolução de Soluções Viáveis')
ax3.legend()
ax3.grid(True, alpha=0.3)

# -------------------------
# Gráfico 4: Espaço de Busca (Melhor Execução)
# -------------------------
if resultados_viaveis:
    ax4 = plt.subplot(2, 3, 4)
    
    # Plotar todas as soluções finais de todas as execuções
    for res in resultados:
        genes = res['genes']
        cor = 'green' if res['viavel'] else 'red'
        ax4.scatter(genes[0], genes[1], c=cor, s=80, alpha=0.4, edgecolors='black', linewidths=0.5)
    
    # Destacar melhor solução
    melhor_genes = melhor_global['genes']
    ax4.scatter(melhor_genes[0], melhor_genes[1], c='blue', s=400, 
                marker='*', edgecolors='black', linewidths=2, 
                label=f'Melhor (f={melhor_global["fitness"]:.2f})', zorder=10)
    
    ax4.set_xlabel('x₁ (Área da barra 1)')
    ax4.set_ylabel('x₂ (Área da barra 2)')
    ax4.set_title('Soluções Finais no Espaço de Busca')
    ax4.set_xlim(-0.05, 1.05)
    ax4.set_ylim(-0.05, 1.05)
    ax4.legend()
    ax4.grid(True, alpha=0.3)

# -------------------------
# Gráfico 5: Histograma de Fitness
# -------------------------
ax5 = plt.subplot(2, 3, 5)
if resultados_viaveis:
    fitness_viaveis = [r['fitness'] for r in resultados_viaveis]
    ax5.hist(fitness_viaveis, bins=10, color='green', alpha=0.7, edgecolor='black')
    ax5.axvline(melhor_global['fitness'], color='blue', linestyle='--', linewidth=2, 
                label=f"Melhor: {melhor_global['fitness']:.2f}")
if resultados_inviaveis:
    fitness_inviaveis = [r['fitness'] for r in resultados_inviaveis]
    ax5.hist(fitness_inviaveis, bins=10, color='red', alpha=0.5, edgecolor='black')

ax5.set_xlabel('Fitness (volume cm³)')
ax5.set_ylabel('Frequência')
ax5.set_title('Distribuição de Fitness Finais')
ax5.legend()
ax5.grid(True, alpha=0.3, axis='y')

# -------------------------
# Gráfico 6: Tempo de Execução
# -------------------------
ax6 = plt.subplot(2, 3, 6)
tempos = [r['tempo'] for r in resultados]
execucoes_num = [r['execucao'] for r in resultados]
cores = ['green' if r['viavel'] else 'red' for r in resultados]

ax6.bar(execucoes_num, tempos, color=cores, alpha=0.7, edgecolor='black')
ax6.axhline(y=np.mean(tempos), color='blue', linestyle='--', linewidth=2, 
            label=f'Média: {np.mean(tempos):.2f}s')
ax6.set_xlabel('Execução')
ax6.set_ylabel('Tempo (segundos)')
ax6.set_title('Tempo de Execução por Rodada')
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

# -------------------------
# Salvar e mostrar
# -------------------------
plt.tight_layout()
plt.savefig('resultado_experimento_completo.png', dpi=300, bbox_inches='tight')
print("\n✓ Gráficos salvos em 'resultado_experimento_completo.png'")
plt.show()

# ==============================================================================
# SALVAR RESULTADOS EM ARQUIVO
# ==============================================================================

print("\n" + "=" * 80)
print(" SALVANDO RESULTADOS")
print("=" * 80)

with open('resultados_experimento.txt', 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write(" RESULTADOS DO EXPERIMENTO - Three Bar Truss Problem\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("PARÂMETROS:\n")
    for key, value in config.items():
        f.write(f"  {key}: {value}\n")
    f.write(f"  num_execucoes: {num_execucoes}\n\n")
    
    f.write("RESULTADOS POR EXECUÇÃO:\n")
    f.write("-" * 80 + "\n")
    for res in resultados:
        f.write(f"Execução {res['execucao']}:\n")
        f.write(f"  Fitness: {res['fitness']:.4f}\n")
        f.write(f"  Genes: [{res['genes'][0]:.6f}, {res['genes'][1]:.6f}]\n")
        f.write(f"  Viável: {'SIM' if res['viavel'] else 'NÃO'}\n")
        if not res['viavel']:
            f.write(f"  Violações: {res['violacoes']:.4f}\n")
        f.write(f"  Tempo: {res['tempo']:.2f}s\n")
        f.write("-" * 80 + "\n")
    
    f.write("\nESTATÍSTICAS GERAIS:\n")
    f.write(f"Soluções viáveis: {len(resultados_viaveis)}/{num_execucoes}\n")
    
    if resultados_viaveis:
        fitness_viaveis = [r['fitness'] for r in resultados_viaveis]
        f.write(f"\nSOLUÇÕES VIÁVEIS:\n")
        f.write(f"  Melhor: {min(fitness_viaveis):.4f}\n")
        f.write(f"  Pior: {max(fitness_viaveis):.4f}\n")
        f.write(f"  Média: {np.mean(fitness_viaveis):.4f}\n")
        f.write(f"  Desvio padrão: {np.std(fitness_viaveis):.4f}\n")
        f.write(f"  Mediana: {np.median(fitness_viaveis):.4f}\n")
        
        f.write(f"\nMELHOR SOLUÇÃO GLOBAL:\n")
        f.write(f"  Execução: {melhor_global['execucao']}\n")
        f.write(f"  Fitness: {melhor_global['fitness']:.4f}\n")
        f.write(f"  Genes: [{melhor_global['genes'][0]:.6f}, {melhor_global['genes'][1]:.6f}]\n")
    
    f.write(f"\nTEMPO TOTAL: {tempo_total:.2f}s ({tempo_total/60:.2f} minutos)\n")
    f.write(f"TEMPO MÉDIO: {tempo_total/num_execucoes:.2f}s por execução\n")

print("✓ Resultados salvos em 'resultados_experimento.txt'")

print("\n" + "=" * 80)
print(" EXPERIMENTO CONCLUÍDO!")
print("=" * 80)