"""
Módulo para o Jogo do Dilema do Prisioneiro.

Usado pelo GBX, GBX2 e GASI.
"""

import numpy as np


class JogoDilema:
    """
    Implementa o Dilema do Prisioneiro iterado.
    """
    
    def __init__(self, num_rounds=10):
        """
        Args:
            num_rounds: Número de rodadas do jogo iterado
        """
        self.num_rounds = num_rounds

    def _decidir_jogada(self, estrategia, ultima_jogada_oponente):
        """
        Decide se vai cooperar (C) ou desertar (D) baseado na estratégia.
        
        Args:
            estrategia: str - A estratégia do jogador
            ultima_jogada_oponente: str - 'C', 'D' ou None (primeira rodada)
            
        Returns:
            str: 'C' (cooperate) ou 'D' (defect)
        """

        if estrategia == "ALL_C":
                return "C"
        if estrategia == "ALL_D":
                return "D" 
        if estrategia == "TFT":
                if ultima_jogada_oponente == None:
                    return "C"
                else:
                    return ultima_jogada_oponente
        if estrategia == "RAND":
                return np.random.choice(["C", "D"])

    def _gerar_estrategia_aleatoria(self):
        """
        Sorteia uma estratégia aleatória para um jogador.
        
        Returns:
            str: Uma das 4 estratégias ('ALL_C', 'ALL_D', 'TFT', 'RAND')
        """

        return np.random.choice(["ALL_C", "ALL_D", "TFT", "RAND"])
    
    def _jogar_dilema(self, estrategia1, estrategia2, T, R, P, S):
        """
        Joga o Dilema do Prisioneiro iterado entre dois jogadores.
        
        Args:
            estrategia1: Estratégia do jogador 1
            estrategia2: Estratégia do jogador 2
            T, R, P, S: Valores do payoff (Temptation, Reward, Punishment, Sucker)
            
        Returns:
            float: Payoff total acumulado pelo jogador 1
        """
        
        payoff_total = 0
        ultima_jogada_jog1 = None
        ultima_jogada_jog2 = None 

        for _ in range(self.num_rounds):

            jogada1 = self._decidir_jogada(estrategia1, ultima_jogada_jog2)
            jogada2 = self._decidir_jogada(estrategia2, ultima_jogada_jog1)

            if jogada1 == "C" and jogada2 == "C":
                payoff_rodada = R
            elif jogada1 == "C" and jogada2 == "D":
                payoff_rodada = S
            elif jogada1 == "D" and jogada2 == "C":
                payoff_rodada = T
            elif jogada1 == "D" and jogada2 == "D":
                payoff_rodada = P

            payoff_total += payoff_rodada

            ultima_jogada_jog1 = jogada1
            ultima_jogada_jog2 = jogada2

        return payoff_total