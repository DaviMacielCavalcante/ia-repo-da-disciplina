"""
=================================================================================
TESTE COMPARATIVO COMPLETO - KNAPSACK (100 ITENS ALEATÓRIOS)
=================================================================================
Este arquivo executa todas as 9 combinações principais:
- Algoritmos: AG, GASI-POP, GASI-S
- Crossovers: BLX-α, GBX, GBX2

Gera:
1. Tabela comparativa (similar à Tabela 13 do artigo)
2. Plot de convergência média de cada configuração (similar à Figura 10 - página 21)
3. Box plots comparativos por algoritmo e crossover
=================================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd

# Importar classes do projeto
from projeto_ia_experimental.problema.knapsack import KnapsackProblem
from projeto_ia_experimental.ag import AlgoritmoGenetico
from projeto_ia_experimental.gasi_pop import GASIPOP
from projeto_ia_experimental.gasi_s import GASIS
from projeto_ia_experimental.gbx import GBXCrossover
from projeto_ia_experimental.gbx2 import GBX2Crossover

# ==============================================================================
# CONFIGURAÇÕES GERAIS
# ==============================================================================

# Parâmetros dos experimentos
CONFIG_GERAL = {
    'num_execucoes': 10,           # 30 execuções independentes (como no artigo)
    'tamanho_populacao': 500,
    'num_geracoes': 200,
    'taxa_crossover': 0.9,
    'taxa_mutacao': 0.15,
    'tamanho_torneio': 3,
    'num_elites': 2,
}

# Definição das configurações a serem testadas
CONFIGURACOES = [
    # AG com diferentes crossovers
    {'id': 'AG_BLX', 'algoritmo': 'AG', 'crossover': 'BLX', 'nome': 'AG BLX-α'},
    {'id': 'AG_GBX', 'algoritmo': 'AG', 'crossover': 'GBX', 'nome': 'AG GBX'},
    {'id': 'AG_GBX2', 'algoritmo': 'AG', 'crossover': 'GBX2', 'nome': 'AG GBX2'},
    
    # GASI-POP com diferentes crossovers
    {'id': 'GASI_POP_BLX', 'algoritmo': 'GASI-POP', 'crossover': 'BLX', 'nome': 'GASI-POP BLX-α'},
    {'id': 'GASI_POP_GBX', 'algoritmo': 'GASI-POP', 'crossover': 'GBX', 'nome': 'GASI-POP GBX'},
    {'id': 'GASI_POP_GBX2', 'algoritmo': 'GASI-POP', 'crossover': 'GBX2', 'nome': 'GASI-POP GBX2'},
    
    # GASI-S com diferentes crossovers
    {'id': 'GASI_S_BLX', 'algoritmo': 'GASI-S', 'crossover': 'BLX', 'nome': 'GASI-S BLX-α'},
    {'id': 'GASI_S_GBX', 'algoritmo': 'GASI-S', 'crossover': 'GBX', 'nome': 'GASI-S GBX'},
    {'id': 'GASI_S_GBX2', 'algoritmo': 'GASI-S', 'crossover': 'GBX2', 'nome': 'GASI-S GBX2'},
]

# ==============================================================================
# FUNÇÕES AUXILIARES
# ==============================================================================

def criar_operador_crossover(tipo_crossover, num_geracoes):
    """Cria o operador de crossover apropriado."""
    if tipo_crossover == 'BLX':
        return None  # BLX-α é o padrão, usa None
    elif tipo_crossover == 'GBX':
        return GBXCrossover(num_rounds=10)
    elif tipo_crossover == 'GBX2':
        return GBX2Crossover(num_rounds=10, max_iter=num_geracoes)
    else:
        raise ValueError(f"Crossover desconhecido: {tipo_crossover}")


def criar_algoritmo(tipo_algoritmo, problema, config, crossover_operator):
    """Cria a instância do algoritmo apropriado."""
    if tipo_algoritmo == 'AG':
        return AlgoritmoGenetico(problema, config, crossover_operator)
    elif tipo_algoritmo == 'GASI-POP':
        return GASIPOP(problema, config, crossover_operator)
    elif tipo_algoritmo == 'GASI-S':
        return GASIS(problema, config, crossover_operator)
    else:
        raise ValueError(f"Algoritmo desconhecido: {tipo_algoritmo}")


def executar_uma_rodada(tipo_algoritmo, tipo_crossover, config, problema):
    """
    Executa uma única rodada do algoritmo especificado.
    
    Returns:
        dict com resultados da execução
    """
    # Criar operador de crossover
    crossover_op = criar_operador_crossover(tipo_crossover, config['num_geracoes'])
    
    # Criar algoritmo
    algoritmo = criar_algoritmo(tipo_algoritmo, problema, config, crossover_op)
    
    # Executar
    resultado = algoritmo.executar()
    
    # Extrair informações
    melhor = resultado['melhor_individuo']
    
    return {
        'fitness': melhor.fitness,
        'genes': melhor.genes.copy(),
        'viavel': melhor.is_feasible(),
        'violacoes': melhor.violation_sum,
        'historico_melhor': resultado['historico_melhor'],
        'historico_medio': resultado['historico_medio'],
        'historico_viaveis': resultado['historico_viaveis']
    }


def executar_experimento(config_exp, config_geral, problema):
    """
    Executa um experimento completo (múltiplas execuções).
    
    Args:
        config_exp: dicionário com id, algoritmo, crossover
        config_geral: parâmetros gerais (população, gerações, etc)
        problema: instância do problema
    
    Returns:
        dict com resultados agregados
    """
    print(f"\n{'='*80}")
    print(f"Executando: {config_exp['nome']}")
    print(f"{'='*80}")
    
    resultados = []
    tempo_inicio = time.time()
    
    for exec_num in range(config_geral['num_execucoes']):
        print(f"  Execução {exec_num + 1}/{config_geral['num_execucoes']}...", end=' ', flush=True)
        
        inicio = time.time()
        resultado = executar_uma_rodada(
            config_exp['algoritmo'],
            config_exp['crossover'],
            config_geral,
            problema
        )
        fim = time.time()
        
        resultado['execucao'] = exec_num + 1
        resultado['tempo'] = fim - inicio
        resultados.append(resultado)
        
        print(f"✓ (fitness: {resultado['fitness']:.0f}, tempo: {resultado['tempo']:.1f}s)")
    
    tempo_total = time.time() - tempo_inicio
    
    # Para Knapsack, todas soluções são viáveis
    resultados_viaveis = resultados
    
    # Calcular estatísticas
    fitness_values = [r['fitness'] for r in resultados_viaveis]
    
    estatisticas = {
        'Mean': np.mean(fitness_values),
        'Median': np.median(fitness_values),
        'Std. Dev': np.std(fitness_values),
        'Best': np.max(fitness_values),  # Máximo porque é maximização
        'Worst': np.min(fitness_values),
        'Num_Viaveis': len(resultados_viaveis),
        'Taxa_Viabilidade': 1.0
    }
    
    print(f"\n✓ Concluído em {tempo_total:.1f}s")
    print(f"  Mean={estatisticas['Mean']:.0f}, Best={estatisticas['Best']:.0f}")
    
    return {
        'config': config_exp,
        'resultados': resultados,
        'estatisticas': estatisticas,
        'tempo_total': tempo_total
    }

# ==============================================================================
# MAIN - EXECUÇÃO DE TODOS OS EXPERIMENTOS
# ==============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*80)
    print("TESTE COMPARATIVO COMPLETO - KNAPSACK (100 ITENS)")
    print("="*80)
    
    # Gerar problema com 100 itens aleatórios (seed fixo para reprodutibilidade)
    # Capacidade suficiente para aproximadamente 10 itens de peso médio
    problema = KnapsackProblem.gerar_aleatorio(n_items=100, capacidade_n_itens=10, seed=42)
    
    print("\nInformações do problema:")
    problema.imprimir_info()
    
    print(f"\nParâmetros gerais:")
    print(f"  - Execuções por configuração: {CONFIG_GERAL['num_execucoes']}")
    print(f"  - População: {CONFIG_GERAL['tamanho_populacao']}")
    print(f"  - Gerações: {CONFIG_GERAL['num_geracoes']}")
    print(f"  - Taxa crossover: {CONFIG_GERAL['taxa_crossover']}")
    print(f"  - Taxa mutação: {CONFIG_GERAL['taxa_mutacao']}")
    print(f"  - Torneio: {CONFIG_GERAL['tamanho_torneio']}")
    print(f"  - Elites: {CONFIG_GERAL['num_elites']}")
    print(f"\n  - Total de testes: {len(CONFIGURACOES)}")
    print(f"  - Total de execuções: {len(CONFIGURACOES) * CONFIG_GERAL['num_execucoes']}")
    
    tempo_inicio_total = time.time()
    
    # Executar todos os experimentos
    resultados_todos = []
    
    for config in CONFIGURACOES:
        resultado_exp = executar_experimento(config, CONFIG_GERAL, problema)
        resultados_todos.append(resultado_exp)
    
    tempo_total = time.time() - tempo_inicio_total
    
    # ==============================================================================
    # GERAR TABELA COMPARATIVA
    # ==============================================================================
    
    print("\n" + "="*80)
    print("TABELA COMPARATIVA (SIMILAR À TABELA 13)")
    print("="*80)
    
    # Criar DataFrame
    dados_tabela = []
    for resultado in resultados_todos:
        linha = {
            'Algoritmo': resultado['config']['nome'],
            'Mean': resultado['estatisticas']['Mean'],
            'Median': resultado['estatisticas']['Median'],
            'Std. Dev': resultado['estatisticas']['Std. Dev'],
            'Best': resultado['estatisticas']['Best'],
            'Worst': resultado['estatisticas']['Worst'],
        }
        dados_tabela.append(linha)
    
    df_resultados = pd.DataFrame(dados_tabela)
    
    # Imprimir tabela formatada
    print("\n" + df_resultados.to_string(index=False))
    
    # Salvar em CSV
    df_resultados.to_csv('resultados_knapsack.csv', index=False)
    print("\n✓ Tabela salva em: resultados_knapsack.csv")
    
    # ==============================================================================
    # GERAR PLOT DE CONVERGÊNCIA (SIMILAR À FIGURA 10 - PÁGINA 21)
    # ==============================================================================
    
    print("\n" + "="*80)
    print("GERANDO PLOT DE CONVERGÊNCIA")
    print("="*80)
    
    # Criar figura única com todas as curvas de convergência média
    fig = plt.figure(figsize=(14, 8))
    ax = fig.add_subplot(111)
    
    # Definir cores e estilos para cada configuração
    cores = ['#1f77b4', '#ff7f0e', '#2ca02c',  # AG: azul, laranja, verde
             '#d62728', '#9467bd', '#8c564b',  # GASI-POP: vermelho, roxo, marrom
             '#e377c2', '#7f7f7f', '#bcbd22']  # GASI-S: rosa, cinza, amarelo-verde
    
    estilos = ['-', '--', ':']  # Sólido, tracejado, pontilhado
    
    # Plotar convergência média de cada configuração
    for idx, resultado in enumerate(resultados_todos):
        config = resultado['config']
        resultados_exp = resultado['resultados']
        
        # Calcular média das convergências de todas as execuções
        historico_medio = np.mean([r['historico_melhor'] for r in resultados_exp], axis=0)
        
        # Determinar estilo baseado no crossover
        if config['crossover'] == 'BLX':
            estilo = '-'
        elif config['crossover'] == 'GBX':
            estilo = '--'
        else:  # GBX2
            estilo = ':'
        
        # Plotar curva de convergência média
        ax.plot(historico_medio,
               color=cores[idx],
               linestyle=estilo,
               linewidth=2.5,
               label=f"{config['nome']} (média)",
               alpha=0.9)
    
    # Formatação do gráfico
    ax.set_xlabel('Gerações', fontsize=12, fontweight='bold')
    ax.set_ylabel('Valor Médio (Maximização)', fontsize=12, fontweight='bold')
    ax.set_title('Convergência Média - Knapsack (100 itens)',
                fontsize=14, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    
    # Legenda organizada e clara
    ax.legend(loc='lower right',  # Lower right porque é maximização
             fontsize=9,
             framealpha=0.95,
             edgecolor='black',
             ncol=1)
    
    # Adicionar informações adicionais
    info_text = f"Média de {CONFIG_GERAL['num_execucoes']} execuções\n" \
                f"Pop={CONFIG_GERAL['tamanho_populacao']}, " \
                f"Ger={CONFIG_GERAL['num_geracoes']}\n" \
                f"100 itens, Cap={problema.capacity}"
    ax.text(0.02, 0.98, info_text,
           transform=ax.transAxes,
           fontsize=9,
           verticalalignment='top',
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.6))
    
    plt.tight_layout()
    plt.savefig('convergencia_knapsack.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfico de convergência salvo em: convergencia_knapsack.png")
    
    # ==============================================================================
    # PLOT ADICIONAL: BOX PLOTS COMPARATIVOS
    # ==============================================================================
    
    print("\nGerando box plots comparativos...")
    
    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Box plot por algoritmo
    dados_por_algo = {
        'AG': [],
        'GASI-POP': [],
        'GASI-S': []
    }
    
    for resultado in resultados_todos:
        algo = resultado['config']['algoritmo']
        fitness_values = [r['fitness'] for r in resultado['resultados']]
        dados_por_algo[algo].extend(fitness_values)
    
    ax1.boxplot([dados_por_algo['AG'], dados_por_algo['GASI-POP'], dados_por_algo['GASI-S']],
                labels=['AG', 'GASI-POP', 'GASI-S'])
    ax1.set_ylabel('Valor Obtido', fontsize=12)
    ax1.set_title('Comparação por Algoritmo - Knapsack', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Box plot por crossover
    dados_por_cross = {
        'BLX': [],
        'GBX': [],
        'GBX2': []
    }
    
    for resultado in resultados_todos:
        cross = resultado['config']['crossover']
        fitness_values = [r['fitness'] for r in resultado['resultados']]
        dados_por_cross[cross].extend(fitness_values)
    
    ax2.boxplot([dados_por_cross['BLX'], dados_por_cross['GBX'], dados_por_cross['GBX2']],
                labels=['BLX-α', 'GBX', 'GBX2'])
    ax2.set_ylabel('Valor Obtido', fontsize=12)
    ax2.set_title('Comparação por Crossover - Knapsack', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('boxplots_knapsack.png', dpi=300, bbox_inches='tight')
    print("✓ Box plots salvos em: boxplots_knapsack.png")
    
    # ==============================================================================
    # SUMÁRIO FINAL
    # ==============================================================================
    
    print("\n" + "="*80)
    print("SUMÁRIO FINAL")
    print("="*80)
    
    print(f"\nTempo total de execução: {tempo_total:.2f}s ({tempo_total/60:.2f} minutos)")
    print(f"Tempo médio por configuração: {tempo_total/len(CONFIGURACOES):.2f}s")
    
    # Encontrar melhor configuração (maior Mean porque é maximização)
    melhor_config = max(resultados_todos, key=lambda x: x['estatisticas']['Mean'])
    
    print(f"\n🏆 MELHOR CONFIGURAÇÃO (Maior Mean - Maximização):")
    print(f"   {melhor_config['config']['nome']}")
    print(f"   Mean: {melhor_config['estatisticas']['Mean']:.2f}")
    print(f"   Best: {melhor_config['estatisticas']['Best']:.2f}")
    print(f"   Std: {melhor_config['estatisticas']['Std. Dev']:.2f}")
    
    print("\n" + "="*80)
    print("ARQUIVOS GERADOS:")
    print("="*80)
    print("  1. resultados_knapsack.csv      - Tabela de resultados estatísticos")
    print("  2. convergencia_knapsack.png    - Plot de convergência média")
    print("  3. boxplots_knapsack.png        - Box plots comparativos")
    
    print("\n✅ Teste comparativo Knapsack finalizado com sucesso!")
    print("="*80 + "\n")
    
    plt.show()