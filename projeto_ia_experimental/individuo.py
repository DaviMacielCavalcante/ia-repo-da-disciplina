import numpy as np

class TBTProblem:

    def __init__(self):
        self.n_vars = 2
        self.n_constraints = 3
        self.lower_bounds = np.array([0, 0])
        self.upper_bounds = np.array([1, 1])

        # comprimento (cm)
        self.l = 100
        # carga aplicada (KN/cm²)
        self.P = 2
        # tensão máxima permitida (KN/cm²)
        self.sigma = 2

    def objective(self, x):
        x1 = x[0]
        x2 = x[1]

        # f(x) = (2√2·x₁ + x₂) × l
        f = (2 * np.sqrt(2)*x1 + x2) * self.l

        return f
        

    def constraints(self, x):
        x1, x2 = x[0], x[1]

        common = np.sqrt(2)*x1**2 + 2*x1 *x2

        r1 = ((np.sqrt(2)*x1 + x2) / common)*self.P - self.sigma

        r2 = (x2 / common)*self.P - self.sigma

        r3 = (1 / (x1 + np.sqrt(2)*x2))*self.P - self.sigma


        return np.array([r1,r2,r3])
        

    def evaluate(self, x):
        
        objective = self.objective(x)
        constraints = self.constraints(x)

        violations = np.sum(constraints > 0)

        violations_sum = np.sum(constraints[constraints > 0])

        return {
            "objective": objective,
            "constraints": constraints,
            "n_violations": violations,
            "violation_sum": violations_sum
        }
    
def compare_solutions(sol1, sol2):
    """
    Compara duas soluções usando o método de Deb.
    
    Args:
        sol1, sol2: dicionários retornados por evaluate()
        
    Returns:
        1 se sol1 é melhor
        -1 se sol2 é melhor
        0 se são equivalentes
    """    

    viavel1 = sol1['n_violations'] == 0
    viavel2 = sol2['n_violations'] == 0

    if viavel1 and not viavel2:
        return 1
    
    if viavel2 and not viavel1:
        return -1
    
    if viavel1 and viavel2:
        if sol1['objective'] < sol2['objective']:
            return 1 
        elif sol1['objective'] > sol2['objective']:
            return -1
        else:
            return 0
        
    if sol1["violation_sum"] < sol2["violation_sum"]:
        return 1
    elif sol1["violation_sum"] > sol2["violation_sum"]:
        return -1
    else:
        return 0
    

class Individuo:

    def __init__(self, genes, problem):
        """
        Representa um indivíduo na população do AG.
        
        Args:
            genes: array numpy com os valores das variáveis [x1, x2, ...]
            problem: instância de TBTProblem
        """  

        self.genes = genes
        self.problem = problem

        self.fitness = None
        self.constraints = None 
        self.n_violations = None 
        self.violation_sum = None
        self.evaluated = False

    def evaluate(self):

        """Avalia o indivíduo usando o problema"""

        result = self.problem.evaluate(self.genes)

        self.fitness = result["objective"] 
        self.constraints = result["constraints"]
        self.n_violations = result["n_violations"]
        self.violation_sum = result["violation_sum"]
        self.evaluated = True 

    def is_feasible(self):
        if not self.evaluated:
            self.evaluate()

        return self.n_violations == 0 

    def __lt__(self, other):

        if not self.evaluated:
            self.evaluate()
        if not other.evaluated:
            other.evaluate()

        sol1 = {
            'objective': self.fitness,
            'n_violations': self.n_violations,
            'violation_sum': self.violation_sum
        }

        sol2 = {
            'objective': other.fitness,
            'n_violations': other.n_violations,
            'violation_sum': other.violation_sum
        }

        result = compare_solutions(sol1, sol2)

        return result == 1
    
    def __repr__(self):
        """Representação textual para print()"""
        # Se ainda não foi avaliado, mostra só os genes
        if not self.evaluated:
            return f"Individuo(genes={self.genes}, not evaluated)"
        
        # Se foi avaliado, mostra genes, fitness e se é viável
        status = "feasible" if self.is_feasible() else "infeasible"
        return f"Individuo(genes={self.genes}, fitness={self.fitness:.4f}, {status})"
    
    def copy(self):
        """Cria uma cópia profunda do indivíduo"""
        # Cria novo indivíduo com genes copiados (não referência!)
        new_ind = Individuo(self.genes.copy(), self.problem)
        
        # (evita reavaliar se não for necessário)
        if self.evaluated:
            new_ind.fitness = self.fitness
            new_ind.constraints = self.constraints.copy()
            new_ind.n_violations = self.n_violations
            new_ind.violation_sum = self.violation_sum
            new_ind.evaluated = True
        
        return new_ind