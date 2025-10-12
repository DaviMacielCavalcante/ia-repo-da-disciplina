from projeto_ia_1_av.graph import Graph # Assumindo que seu projeto está numa pasta 'meu_projeto'

def construir_mapa_hyrule_expandido():
    """
    Função que cria e retorna uma instância do mapa de Hyrule com mais locais e rotas.
    """
    mapa = Graph()

    # --- Adicionando locais ---
    # Locais Originais
    mapa.add_node("Hateno Village", x=300, y=-180)
    mapa.add_node("Kakariko Village", x=180, y=-110)
    mapa.add_node("Great Plateau", x=0, y=-200)
    mapa.add_node("Zora's Domain", x=320, y=150)
    mapa.add_node("Goron City", x=100, y=300)
    mapa.add_node("Rito Village", x=-350, y=220)
    mapa.add_node("Gerudo Town", x=-400, y=-350)
    mapa.add_node("Lurelin Village", x=400, y=-400)
    mapa.add_node("Central Hyrule", x=0, y=0)
    
    # Novos Locais
    mapa.add_node("Posto dos Picos Gêmeos", x=100, y=-140) # Hub entre Kakariko e Hateno
    mapa.add_node("Floresta Korok", x=0, y=250)           # Norte do castelo, difícil acesso
    mapa.add_node("Vila Akkala", x=400, y=250)          # Extremo nordeste

    # --- Adicionando rotas (bidirecionais por padrão) ---
    
    # Rotas Centrais
    mapa.add_edge("Great Plateau", "Central Hyrule", cost=150)
    mapa.add_edge("Central Hyrule", "Posto dos Picos Gêmeos", cost=90)
    mapa.add_edge("Posto dos Picos Gêmos", "Great Plateau", cost=70)
    
    # Rotas de Kakariko e Hateno (agora com o Posto no meio)
    mapa.add_edge("Kakariko Village", "Posto dos Picos Gêmeos", cost=50, qualidade=9.0) # Caminho seguro
    mapa.add_edge("Hateno Village", "Posto dos Picos Gêmeos", cost=100)
    mapa.add_edge("Hateno Village", "Lurelin Village", cost=150, clima=4.5)
    mapa.add_edge("Lurelin Village", "Posto dos Picos Gêmos", cost=180, clima=4.5)
    
    # Rotas para Zora's Domain
    mapa.add_edge("Posto dos Picos Gêmeos", "Zora's Domain", cost=200, clima=4.0, qualidade=5.0) # Caminho longo e chuvoso
    mapa.add_edge("Vila Akkala", "Zora's Domain", cost=180, qualidade=6.0) # Conexão de Akkala
    mapa.add_edge("Vila Akkala", "Central Hyrule", cost=280, qualidade=8.0)

    # Rotas para Goron City e Floresta Korok
    mapa.add_edge("Central Hyrule", "Floresta Korok", cost=150, qualidade=1.0, clima=2.0) # A rota das Florestas
    mapa.add_edge("Central Hyrule", "Goron City", cost=250, clima=1.0, qualidade=1.5)
    mapa.add_edge("Goron City", "Floresta Korok", cost=120, qualidade=3.5) # Atalho pelas montanhas

    # Rotas do Oeste
    mapa.add_edge("Central Hyrule", "Rito Village", cost=320, clima=2.5)
    mapa.add_edge("Central Hyrule", "Gerudo Town", cost=380, qualidade=3.0)
    mapa.add_edge("Great Plateau", "Gerudo Town", cost=300, qualidade=3.0)
    mapa.add_edge("Rito Village", "Gerudo Town", cost=450) # Travessia perigosa
    
    return mapa

def main():
    # Lista de viagens para simular
    viagens = [
        ("Hateno Village", "Rito Village", "Jornada de leste a oeste"),
        ("Gerudo Town", "Vila Akkala", "Atravessando a maior distância do mapa"),
        ("Kakariko Village", "Floresta Korok", "Caminho das Florestas (condições melhores)")
    ]

    for origem, destino, descricao in viagens:
        print("=========================================================")
        print(f"INICIANDO SIMULAÇÃO: {descricao}")
        print(f"Buscando a rota mais segura e rápida de '{origem}' para '{destino}'...\n")

        for i in range(5):
            print(f"--- Tentativa de Viagem {i + 1} ---")

            # A cada simulação, construímos um mapa novo para ter aleatoriedade
            mapa_simulacao = construir_mapa_hyrule_expandido()

            resultado = mapa_simulacao.busca_a_estrela(origem, destino)

            if resultado:
                caminho, custo_total = resultado
                print(f"Rota sugerida pela Sheikah Slate: {' -> '.join(caminho)}")
                print(f"Custo total da viagem (considerando perigos): {custo_total:.2f}\n")
            else:
                print("Não foi possível encontrar uma rota.\n")
        
        print("=========================================================\n")


if __name__ == "__main__":
    main()