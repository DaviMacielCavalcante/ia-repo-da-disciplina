from roleta_ag.individuo import Individuo
from roleta_ag.roleta import Roleta

pop = []

ind_a = Individuo("a", 30)
ind_b = Individuo("b", 22)
ind_c = Individuo("c", 45)
ind_d = Individuo("d", 53)
ind_e = Individuo("e", 21)
ind_f = Individuo("f", 109)

pop.append(ind_a)
pop.append(ind_b)
pop.append(ind_c)
pop.append(ind_d)
pop.append(ind_e)
pop.append(ind_f)

roleta = Roleta(pop)

if __name__ == "__main__":
    print("\n" + "="*80)
    print("ROLETA DE SELECAO - ALGORITMOS GENETICOS")
    print("="*80)
    
    fitness_total = sum(ind.fitness for ind in pop)
    intervalos = roleta.calcular_intervalos()
    
    print("\n=== ESTRUTURA DA ROLETA ===")
    print(f"Fitness Total: {fitness_total}\n")
    
    print(f"{'Individuo':<12} {'Fitness':<10} {'Intervalo':<20} {'Percentual'}")
    print("-" * 65)
    
    for ind in pop:
        inicio, fim = intervalos[ind.name]
        percentual = (ind.fitness / fitness_total) * 100
        intervalo_str = f"[{inicio}, {fim})"
        print(f"{ind.name:<12} {ind.fitness:<10} {intervalo_str:<20} {percentual:>5.2f}%")
    
    print("-" * 65)
    
    print("\nREPRESENTACAO VISUAL:")
    print("-" * 65)
    for ind in pop:
        percentual = (ind.fitness / fitness_total) * 100
        tamanho_barra = int((ind.fitness / fitness_total) * 50)
        barra = "█" * tamanho_barra
        print(f"{ind.name}: {barra} {percentual:.2f}%")
    print("-" * 65)
    
    print("\n=== TESTES COM VALORES DO SLIDE ===")
    print("Valores: [1, 61, 82, 21, 279, 6]\n")
    
    valores_slide = [1, 61, 82, 21, 279, 6]
    
    print(f"{'Sorteio':<10} {'Valor':<10} {'Intervalo':<20} {'Selecionado':<15} {'Fitness':<10} {'Percentual'}")
    print("-" * 90)
    
    for i, valor in enumerate(valores_slide, 1):
        selecionado = roleta.escolher(valor)
        
        if selecionado:
            inicio, fim = intervalos[selecionado.name]
            intervalo_str = f"[{inicio}, {fim})"
            percentual = (selecionado.fitness / fitness_total) * 100
            print(f"{i:<10} {valor:<10} {intervalo_str:<20} {selecionado.name:<15} {selecionado.fitness:<10} {percentual:>5.2f}%")
        else:
            print(f"{i:<10} {valor:<10} {'---':<20} {'ERRO':<15} {'---':<10} {'---'}")
    
    print("-" * 90)