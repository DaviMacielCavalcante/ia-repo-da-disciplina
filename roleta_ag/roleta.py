class Roleta:

    def __init__(self, pop):
        self.pop = pop

    def calcular_intervalos(self):
        acumulado = 0
        intervalos = {}

        for ind in self.pop:
            inicio = acumulado
            fim = acumulado + ind.fitness
            intervalos[ind.name] = (inicio, fim)
            acumulado = fim 

        return intervalos
    
    def total_fitness(self):

        total = 0

        for ind in self.pop:
            total += ind.fitness

        return total
    
    def escolher(self, valor):

        intervalos = self.calcular_intervalos()
        fitness_total = self.total_fitness()

        if valor >= fitness_total:
            valor = valor % fitness_total


        for ind in self.pop:
            inicio, fim = intervalos[ind.name]

            if valor >= inicio and valor < fim:
                return ind
            
        return None
    
    def mostrar_estrutura(self):
        fitness_total = self.calcular_fitness_total()
        intervalos = self.calcular_intervalos()
        
        print("=== ESTRUTURA DA ROLETA ===")
        print(f"Fitness Total: {fitness_total}\n")
        print(f"{'Indivíduo':<12} {'Fitness':<10} {'Intervalo':<20} {'Percentual'}")
        print("-" * 60)
        
        for ind in self.pop:
            inicio, fim = intervalos[ind.name]
            percentual = (ind.fitness / fitness_total) * 100
            print(f"{ind.name:<12} {ind.fitness:<10} [{inicio}, {fim}){' '*(20-len(f'[{inicio}, {fim})'))} {percentual:.2f}%")