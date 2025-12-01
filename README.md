# Replicação de Experimento: Game Theory and Social Interaction in Genetic Algorithms

**Disciplina:** Inteligência Artificial / Inteligência Computacional  
**Instituição:** CESUPA - Centro Universitário do Pará  
**Professora:** Polyana Santos Fonseca Nascimento  
**Período:** 2025

---

## Contexto do Artigo Base

### Referência

**Título:** Game Theory and Social Interaction for Selection and Crossover Pressure Control in Genetic Algorithms

**Autores:** R. Lisbôa Pereira, et al.

**Publicação:** IEEE Access, Volume 8, 2020

**DOI/Link:** [IEEE Access - Volume 8, 2020](https://ieeexplore.ieee.org/document/9165284)

### Problema Estudado

O artigo propõe uma abordagem inovadora que integra conceitos de Teoria dos Jogos (especificamente o Dilema do Prisioneiro) aos Algoritmos Genéticos para controlar a pressão seletiva e melhorar o desempenho em problemas de otimização com restrições. A metodologia investiga como interações sociais baseadas em jogos podem influenciar a seleção de indivíduos e a aplicação de operadores de crossover.

### Objetivos

- Avaliar o impacto da interação social (baseada no Dilema do Prisioneiro) no desempenho de Algoritmos Genéticos
- Comparar três variantes algorítmicas: AG padrão, GASI-POP e GASI-S
- Analisar a eficácia de diferentes operadores de crossover: BLX-α, GBX e GBX2
- Validar os resultados em problemas clássicos de otimização com restrições

### Metodologia Aplicada

O artigo implementa três variantes principais de algoritmos:

1. **AG (Algoritmo Genético Padrão)**: Implementação clássica sem interação social
2. **GASI-POP (Genetic Algorithm with Social Interaction - Population)**: Interação social aplicada a toda população antes da seleção
3. **GASI-S (Genetic Algorithm with Social Interaction - Selection)**: Interação social integrada ao processo de seleção por torneio

Cada variante é testada com três operadores de crossover:
- **BLX-α** (Blend Crossover)
- **GBX** (Game-Based Crossover)
- **GBX2** (Game-Based Crossover 2)

Totalizando **9 combinações algorítmicas** testadas em múltiplos problemas de benchmark.

---

## Implementação

### Principais Componentes

#### 1. Algoritmos Implementados

**AG (Algoritmo Genético):**
- Seleção por torneio
- Crossover (BLX-α, GBX ou GBX2)
- Mutação gaussiana
- Elitismo
- Tratamento de restrições pelo método de Deb

**GASI-POP:**
- Interação social em toda população antes da seleção
- Quatro estratégias comportamentais: ALL_C, ALL_D, TFT, RAND
- Fitness social derivado do Dilema do Prisioneiro
- Combinação de fitness normalizado e fitness social

**GASI-S:**
- Interação social integrada ao torneio
- Jogos realizados entre candidatos do torneio
- Seleção baseada em fitness combinado

#### 2. Operadores de Crossover

**BLX-α (Blend Crossover):**
- α = 0.5 (padrão do artigo)
- Gera descendentes por interpolação e extrapolação

**GBX (Game-Based Crossover):**
- Taxa de crossover adaptativa baseada no fitness social
- Penaliza comportamentos não cooperativos

**GBX2 (Game-Based Crossover 2):**
- Variante do GBX com função exponencial
- Maior sensibilidade às diferenças de fitness social

#### 3. Problemas de Otimização Implementados

**Three Bar Truss (TBT):**
- 2 variáveis de decisão (áreas das barras)
- 3 restrições de tensão
- Minimização de volume

**Tabular Column Design (TCD):**
- 2 variáveis de decisão (diâmetro médio e espessura)
- 6 restrições (tensão, flambagem e limites geométricos)
- Minimização de custo da coluna

**Welded Beam Design (WBD1):**
- 4 variáveis de decisão (dimensões da solda e da viga)
- 6 restrições para WBD1
- Minimização de custo de fabricação
- Duas versões com diferentes formulações de cálculo

**Knapsack Problem:**
- Representação por chaves aleatórias (random keys)
- Restrição de capacidade da mochila
- Maximização de valor dos itens selecionados

### Parâmetros Experimentais

Seguindo o artigo original:

```python
PARAMETROS = {
    'tamanho_populacao': 500,
    'num_geracoes': 200,
    'taxa_mutacao': 0.15,
    'taxa_crossover': 0.9,
    'tamanho_torneio': 3,
    'num_elites': 2,
    'alpha_blx': 0.5,
    'num_execucoes': 60  # Para análise estatística
}
```

### Adaptações Implementadas

1. **Método de Deb para Restrições:** Soluções viáveis sempre têm prioridade sobre inviáveis
2. **Normalização de Fitness:** Implementada para combinar adequadamente fitness objetivo e social
3. **Estratégias do Dilema do Prisioneiro:**
   - ALL_C: Sempre coopera
   - ALL_D: Sempre deserta
   - TFT (Tit-for-Tat): Coopera inicialmente, depois copia oponente
   - RAND: Escolha aleatória

---

## Instruções de Execução

### Requisitos

- Python 3.8 ou superior
- Bibliotecas necessárias:
  ```bash
  pip install numpy matplotlib pandas scipy
  ```

### Clonando o Repositório

```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_REPOSITORIO]
```

### Executando os Testes

Os testes comparativos estão disponíveis para cada problema implementado. Cada arquivo de teste executa todas as 9 combinações de algoritmo-crossover.

#### Configuração dos Testes:

- 60 execuções independentes por configuração algorítmica
- Coleta de estatísticas: média, mediana, desvio padrão, melhor e pior resultado
- Geração automática de tabelas comparativas e visualizações gráficas

---

## Resumo de Resultados

### Problemas Validados

Os seguintes problemas foram implementados e testados:

- **Three Bar Truss (TBT)** - Validado contra resultados do artigo
- **Tabular Column Design (TCD)** - Implementado conforme o artigo
- **Welded Beam Design (WBD1)** - Implementadas ambas variantes 
- **Knapsack Problem** - Implementado com representação por chaves aleatórias

### Comparação com o Artigo Original

Os resultados obtidos foram comparados com as tabelas do artigo IEEE Access 2020:

**Tabelas de referência:**
- Tabela 9: Welded Beam Design (WBD1)
- Tabela 10: Tabular Column Design (TCD)
- Tabela 13: Three Bar Truss (TBT)

**Observações principais:**
- Convergência compatível com os resultados reportados no artigo
- Validação da metodologia GASI para controle de pressão seletiva
- GBX e GBX2 demonstram efetividade no controle adaptativo de crossover
- GASI-S frequentemente apresenta desempenho superior em problemas com muitas restrições
