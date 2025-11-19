import numpy as np
#from itertools import permutations
import random 

class CaixeiroViajante:
    
    
    def __init__(self):
        self.num_cidades = 15
        # não tenho certeza se as rotas ficam aqui ou são armazenadas em outro local. já que precisam da população...
        #self.melhor_rota = []
        #self.rotas_salvas = []      
        self.nomes_cidades = [
				"A", "B", "C", "D", "E", "F", "G", "H",
				"I", "J", "K", "L", "M", "N", "O"
			]
        
        self.coordenadas_cidades = np.array([
				[7.4, 82.9],[15.2, 63.7],
                [91.6, 12.3],[48.9, 55.1],[33.5, 97.8],[6.8, 24.4],[72.1, 18.9],
                [59.3, 40.7],[84.6, 9.2],[21.7, 76.4],[66.2, 35.8],[98.4, 4.6],
                [53.1, 70.5],[29.8, 88.3],[11.9, 57.2]
			])
        
        self.matriz_distancias = self.calcular_matriz_distancias()
        
    def calcular_matriz_distancias(self):
        matriz_distancias = np.zeros((self.num_cidades, self.num_cidades))
        for i in range(self.num_cidades):
            for j in range(self.num_cidades):
                matriz_distancias[i,j] = np.linalg.norm(self.coordenadas_cidades[i] - self.coordenadas_cidades[j])
        return matriz_distancias

    
    # Tentei esse entretanto ele cria todas as rotas possiveis...
    #def criando_rotas(self):
        #return permutations(range(self.num_cidades), self.num_cidades)
    
    def criar_rota(self):
        return random.sample(range(self.num_cidades), self.num_cidades)
    