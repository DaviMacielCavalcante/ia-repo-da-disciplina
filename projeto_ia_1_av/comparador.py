import numpy as np
from projeto_ia_1_av.mapa_hyrule import construir_mapa_complexo


def comparar_algoritmos(mapa, origem, destino, num_simulacoes=1):
    """
    Compara os dois algoritmos em múltiplas simulações
    """
    print(f"\n{'=' * 80}")
    print(f"COMPARAÇÃO: {origem} → {destino}")

    resultados_fuzzy = []
    resultados_tradicional = []

    for i in range(num_simulacoes):
        print(f"--- Simulação {i + 1} ---")

        # Reconstrói o mapa para nova aleatoriedade
        mapa_sim = construir_mapa_complexo()

        # A* + Fuzzy
        resultado_fuzzy = mapa_sim.busca_a_estrela(origem, destino)

        # A* Tradicional
        resultado_trad = mapa_sim.busca_a_estrela_tradicional(origem, destino)

        if resultado_fuzzy and resultado_trad:
            caminho_fuzzy, custo_fuzzy = resultado_fuzzy
            caminho_trad, custo_trad = resultado_trad

            resultados_fuzzy.append(custo_fuzzy)
            resultados_tradicional.append(custo_trad)

            print(f"\n🍂 A* + FUZZY:")
            print(f"   Caminho: {' → '.join(caminho_fuzzy)}")
            print(f"   Custo real: {custo_fuzzy:.2f}")

            print(f"\n🍃 A* TRADICIONAL:")
            print(f"   Caminho: {' → '.join(caminho_trad)}")
            print(f"   Custo base: {custo_trad:.2f}")

            # Destaca quando os caminhos são diferentes
            if caminho_fuzzy != caminho_trad:
                print(f"\n   ⚠️  CAMINHOS DIFERENTES!")
                diferenca = custo_fuzzy - custo_trad
                if diferenca < 0:
                    print(
                        f"   ✅ Fuzzy encontrou rota {abs(diferenca):.2f} mais barata!"
                    )
                else:
                    print(
                        f"   ⚠️  Fuzzy evitou rota perigosa (+{diferenca:.2f} de custo)"
                    )
            else:
                print(f"\n   ✓ Mesmo caminho escolhido")

        print()

    # Estatísticas finais
    if resultados_fuzzy and resultados_tradicional:
        print(f"\n{'─' * 80}")
        print("ESTATÍSTICAS GERAIS:")
        print(
            f"🍂 A* + Fuzzy     - Custo médio: {np.mean(resultados_fuzzy):.2f} "
            f"(σ={np.std(resultados_fuzzy):.2f})"
        )
        print(
            f"🍃 A* Tradicional - Custo médio: {np.mean(resultados_tradicional):.2f} "
            f"(σ={np.std(resultados_tradicional):.2f})"
        )

        diferenca_media = np.mean(resultados_fuzzy) - np.mean(resultados_tradicional)
        print(f"\nDiferença média: {diferenca_media:+.2f}")

        if diferenca_media > 0:
            print(
                "➡️ O Fuzzy prefere rotas mais seguras, mesmo que ligeiramente mais longas"
            )
        else:
            print("➡️ O Fuzzy encontrou rotas mais eficientes considerando as condições")


def exibir_estatisticas_finais():
    """
    Exibe as conclusões da comparação
    """
    print(f"\n{'=' * 80}")
    print("CONCLUSÃO:")
    print(f"{'=' * 80}")
    print("""
O A* + Fuzzy demonstra comportamento mais inteligente ao:
1. Evitar rotas com clima/qualidade ruins, mesmo que mais curtas
2. Preferir caminhos seguros quando a diferença de distância é pequena
3. Adaptar-se dinamicamente às condições de cada simulação

O A* tradicional é mais "ingênuo", sempre priorizando distância,
ignorando perigos que aumentariam significativamente o custo real.
    """)
