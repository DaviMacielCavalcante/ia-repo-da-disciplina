from projeto_ia_1_av.comparador import comparar_algoritmos, exibir_estatisticas_finais
from projeto_ia_1_av.mapa_hyrule import construir_mapa_complexo


from projeto_ia_1_av.mapa_hyrule import construir_mapa_complexo
from projeto_ia_1_av.visualizador_mapa import VisualizadorMapa


def main():
    print("="*80)
    print(" VISUALIZADOR INTERATIVO - MAPA DE HYRULE")
    print("="*80)
    print("\nCarregando mapa e calculando rotas...")
    
    # Constrói o mapa
    mapa = construir_mapa_complexo()
    
    # Define origem e destino
    origem = "Castelo de Hyrule"
    destino = "Gerudo Town"
    
    print(f"\nBuscando rotas de '{origem}' para '{destino}'...\n")
    
    # Cria visualizador
    # Se você tiver uma imagem do mapa de Hyrule, passe o caminho aqui:
    # visualizador = VisualizadorMapa(imagem_mapa="caminho/para/hyrule_map.png")
    visualizador = VisualizadorMapa()
    
    # Carrega as rotas
    visualizador.carregar_rotas(mapa, origem, destino)
    
    print("Abrindo visualizador...")
    print("\nControles:")
    print("  • Arrastar mouse: Mover pelo mapa")
    print("  • Scroll: Zoom in/out")
    print("  • F: Mostrar/Ocultar caminho A* + Fuzzy")
    print("  • T: Mostrar/Ocultar caminho A* Tradicional")
    print("  • L: Mostrar/Ocultar labels dos nodos")
    print("  • ESC: Sair\n")
    
    # Executa visualizador
    visualizador.executar()


if __name__ == "__main__":
    main()

# def main():
#     print("=" * 80)
#     print(" COMPARAÇÃO: A* TRADICIONAL vs A* + LÓGICA FUZZY")
#     print("\n☀️ - O A* tradicional considera apenas a distância base.")
#     print("🌦️ - O A* + Fuzzy avalia clima e qualidade da estrada.\n")

#     # Cenários de teste escolhidos para destacar as diferenças
#     cenarios = [
#         (
#             "Castelo de Hyrule",
#             "Hateno Village",
#             "Leste: Rota curta perigosa vs rota longa segura",
#         ),
#         (
#             "Castelo de Hyrule",
#             "Goron City",
#             "Norte: Atalho arriscado vs caminho convencional",
#         ),
#         (
#             "Great Plateau",
#             "Gerudo Town",
#             "Deserto: Direto pelo deserto vs contorno pela costa",
#         ),
#         ("Rito Village", "Vila Akkala", "Travessia completa: múltiplas opções de rota"),
#     ]

#     for origem, destino, descricao in cenarios:
#         print(f"\n{'#' * 80}")
#         print(f"CENÁRIO: {descricao}")
#         mapa = construir_mapa_complexo()
#         comparar_algoritmos(mapa, origem, destino, num_simulacoes=1)

#         input("\nPressione ENTER para continuar para o próximo cenário...")

#     exibir_estatisticas_finais()


# if __name__ == "__main__":
#     main()
