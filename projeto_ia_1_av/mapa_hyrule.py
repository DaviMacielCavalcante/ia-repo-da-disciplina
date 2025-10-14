from projeto_ia_1_av.graph_comparacao import GraphComparacao

def construir_mapa_complexo():
    """
    Cria um mapa expandido com situações que evidenciam a diferença entre
    A* tradicional e A* + Fuzzy.
    As coordenadas foram ajustadas para corresponder ao mapa de Breath of the Wild.
    """
    mapa = GraphComparacao()

    # ===== REGIÃO CENTRAL =====
    # O Castelo de Hyrule é o nosso ponto de origem (0,0)
    mapa.add_node("Castelo de Hyrule", x=0, y=0) 
    mapa.add_node("Posto da Torre Central", x=20, y=-60)
    
    # ===== REGIÃO SUL =====
    mapa.add_node("Great Plateau", x=-80, y=-250)
    mapa.add_node("Lago Hylia", x=-140, y=-200)

    # ===== REGIÃO LESTE =====
    mapa.add_node("Posto dos Picos Gêmeos", x=180, y=-140)
    mapa.add_node("Kakariko Village", x=230, y=-90)
    mapa.add_node("Hateno Village", x=380, y=-180)
    mapa.add_node("Floresta de Necluda", x=150, y=-80) # Ponto representativo da região
    
    # ===== REGIÃO SUDESTE =====
    mapa.add_node("Praia de Necluda", x=350, y=-350)
    mapa.add_node("Lurelin Village", x=420, y=-420)

    # ===== REGIÃO NORDESTE =====
    mapa.add_node("Zora's Domain", x=330, y=150)
    mapa.add_node("Vila Akkala", x=450, y=280)
    mapa.add_node("Citadela de Akkala", x=350, y=360)

    # ===== REGIÃO NORTE (DEATH MOUNTAIN & KOROK FOREST) =====
    mapa.add_node("Mina do Sul", x=140, y=260)
    mapa.add_node("Goron City", x=180, y=340)
    mapa.add_node("Floresta Korok", x=-50, y=200)
    mapa.add_node("Bosque Perdido", x=-90, y=230)

    # ===== REGIÃO OESTE =====
    mapa.add_node("Posto da Fronteira Oeste", x=-300, y=80)
    mapa.add_node("Rito Village", x=-380, y=220)
    
    # ===== REGIÃO SUDOESTE (DESERTO) =====
    mapa.add_node("Deserto Gerudo", x=-320, y=-350) # Ponto representativo da região
    mapa.add_node("Gerudo Town", x=-420, y=-380)

    # ===== CONEXÕES CENTRAIS =====
    mapa.add_edge(
        "Castelo de Hyrule", "Posto da Torre Central", cost=40, qualidade=9.0, clima=8.0
    )
    mapa.add_edge(
        "Castelo de Hyrule", "Great Plateau", cost=180, qualidade=7.0, clima=7.5
    )
    mapa.add_edge(
        "Castelo de Hyrule", "Floresta Korok", cost=200, qualidade=2.0, clima=3.0
    )
    mapa.add_edge(
        "Castelo de Hyrule",
        "Posto da Fronteira Oeste",
        cost=220,
        qualidade=6.0,
        clima=6.5,
    )

    # ===== ROTAS LESTE (com armadilhas para A* tradicional) =====
    # Rota aparentemente curta, mas com condições péssimas
    mapa.add_edge(
        "Posto da Torre Central",
        "Floresta de Necluda",
        cost=180,
        qualidade=1.5,
        clima=2.0,
    )
    mapa.add_edge(
        "Floresta de Necluda", "Hateno Village", cost=80, qualidade=2.0, clima=2.5
    )

    # Rota mais longa, mas com excelentes condições
    mapa.add_edge(
        "Posto da Torre Central",
        "Posto dos Picos Gêmeos",
        cost=120,
        qualidade=9.0,
        clima=8.5,
    )
    mapa.add_edge(
        "Posto dos Picos Gêmeos", "Kakariko Village", cost=60, qualidade=9.5, clima=9.0
    )
    mapa.add_edge(
        "Kakariko Village", "Hateno Village", cost=140, qualidade=8.5, clima=8.0
    )

    # Conexões adicionais
    mapa.add_edge(
        "Floresta de Necluda", "Kakariko Village", cost=100, qualidade=4.0, clima=5.0
    )
    mapa.add_edge(
        "Floresta de Necluda", "Zora's Domain", cost=150, qualidade=3.0, clima=2.5
    )

    # ===== ROTAS NORDESTE =====
    mapa.add_edge("Zora's Domain", "Vila Akkala", cost=160, qualidade=6.0, clima=4.0)
    mapa.add_edge(
        "Vila Akkala", "Citadela de Akkala", cost=90, qualidade=5.0, clima=5.5
    )
    mapa.add_edge("Zora's Domain", "Mina do Sul", cost=200, qualidade=4.5, clima=4.0)

    # ===== ROTAS NORTE (caminhos perigosos vs seguros) =====
    # Atalho perigoso pelo norte
    mapa.add_edge("Floresta Korok", "Bosque Perdido", cost=70, qualidade=1.0, clima=1.5)
    mapa.add_edge("Bosque Perdido", "Goron City", cost=150, qualidade=1.5, clima=1.0)

    # Rota segura mas mais longa
    mapa.add_edge("Floresta Korok", "Mina do Sul", cost=100, qualidade=7.0, clima=7.5)
    mapa.add_edge("Mina do Sul", "Goron City", cost=120, qualidade=8.0, clima=8.0)

    mapa.add_edge(
        "Goron City", "Citadela de Akkala", cost=200, qualidade=5.0, clima=5.0
    )

    # ===== ROTAS OESTE =====
    mapa.add_edge(
        "Posto da Fronteira Oeste", "Rito Village", cost=180, qualidade=6.5, clima=3.0
    )
    mapa.add_edge(
        "Posto da Fronteira Oeste", "Lago Hylia", cost=140, qualidade=8.0, clima=8.0
    )
    mapa.add_edge("Lago Hylia", "Great Plateau", cost=80, qualidade=7.5, clima=7.0)

    # ===== ROTAS SUL (grande diferença entre custos base e reais) =====
    # Caminho direto pelo deserto - curto mas extremo
    mapa.add_edge("Great Plateau", "Deserto Gerudo", cost=200, qualidade=1.0, clima=0.5)
    mapa.add_edge("Deserto Gerudo", "Gerudo Town", cost=120, qualidade=1.5, clima=1.0)

    # Caminho seguro pela costa - mais longo mas muito melhor
    mapa.add_edge("Great Plateau", "Lago Hylia", cost=100, qualidade=8.0, clima=8.0)
    mapa.add_edge("Lago Hylia", "Deserto Gerudo", cost=180, qualidade=7.0, clima=6.5)

    # Conexão com Lurelin
    mapa.add_edge(
        "Hateno Village", "Praia de Necluda", cost=100, qualidade=7.0, clima=6.0
    )
    mapa.add_edge(
        "Praia de Necluda", "Lurelin Village", cost=90, qualidade=6.5, clima=5.5
    )
    mapa.add_edge("Lurelin Village", "Gerudo Town", cost=350, qualidade=3.0, clima=3.5)

    return mapa