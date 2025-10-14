import pygame
import sys
from projeto_ia_1_av.mapa_hyrule import construir_mapa_complexo
from projeto_ia_1_av.graph_comparacao import GraphComparacao


class VisualizadorMapa:
    def __init__(
        self, largura=1000, altura=1000, imagem_mapa="projeto_ia_1_av/base.png"
    ):
        pygame.init()

        # Configurações da janela
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Mapa de Hyrule - A* vs A* + Fuzzy")

        # Fonte
        self.fonte = pygame.font.Font(None, 16)
        self.fonte_pequena = pygame.font.Font(None, 12)
        self.fonte_grande = pygame.font.Font(None, 24)

        # Imagem de fundo (opcional)
        self.imagem_fundo = None
        if imagem_mapa:
            try:
                self.imagem_fundo = pygame.image.load(imagem_mapa)
                # O ideal é que a imagem base já tenha uma resolução boa.
                # Vamos ajustar a escala inicial aqui.
                self.imagem_fundo = pygame.transform.scale(
                    self.imagem_fundo, (1000, 1000)
                )
            except:
                print(f"Aviso: Não foi possível carregar a imagem {imagem_mapa}")

        # Controles de câmera
        self.offset_x = largura // 2
        self.offset_y = altura // 2
        self.zoom = 1.0
        self.arrastando = False
        self.ultima_pos_mouse = (0, 0)

        # Estado da visualização
        self.mapa = None
        self.caminho_fuzzy = None
        self.caminho_tradicional = None
        self.custo_fuzzy = 0
        self.custo_tradicional = 0
        self.mostrar_fuzzy = True
        self.mostrar_tradicional = True
        self.mostrar_labels = True

        # Cores
        # Sugestão: um fundo mais escuro pode combinar melhor com o mapa
        self.COR_FUNDO = (20, 20, 30)
        self.COR_NODE = (70, 130, 180)
        self.COR_NODE_DESTAQUE = (255, 140, 0)
        self.COR_ARESTA = (200, 200, 200)
        self.COR_CAMINHO_FUZZY = (34, 139, 34)  # Verde
        self.COR_CAMINHO_TRADICIONAL = (220, 20, 60)  # Vermelho
        self.COR_TEXTO = (50, 50, 50)
        self.COR_PAINEL = (255, 255, 255, 200)

        # Clock para FPS
        self.clock = pygame.time.Clock()

    def mundo_para_tela(self, x, y):
        """Converte coordenadas do mundo para coordenadas da tela"""
        tela_x = (x * self.zoom) + self.offset_x
        # CORREÇÃO AQUI: Invertemos o sinal de 'y' para alinhar com o eixo do Pygame
        tela_y = (-y * self.zoom) + self.offset_y
        return int(tela_x), int(tela_y)

    def desenhar_fundo(self):
        """Desenha o fundo (imagem ou cor sólida)"""
        if self.imagem_fundo:
            # Calcula posição e escala da imagem com zoom
            img_largura = int(self.imagem_fundo.get_width() * self.zoom)
            img_altura = int(self.imagem_fundo.get_height() * self.zoom)
            img_escalada = pygame.transform.scale(
                self.imagem_fundo, (img_largura, img_altura)
            )

            # Centraliza a imagem com base no offset
            pos_x = self.offset_x - (img_largura // 2)
            pos_y = self.offset_y - (img_altura // 2)

            self.tela.blit(img_escalada, (pos_x, pos_y))
        # O else foi removido porque a tela já é preenchida no loop principal

    def desenhar_arestas(self):
        """Desenha todas as arestas do grafo"""
        if not self.mapa:
            return

        desenhadas = set()
        for node_value, node in self.mapa.nodes.items():
            if node_value not in self.mapa.coordenadas:
                continue

            x1, y1 = self.mapa.coordenadas[node_value]
            pos1 = self.mundo_para_tela(x1, y1)

            for vizinho in node.neighbors.keys():
                if vizinho.value not in self.mapa.coordenadas:
                    continue

                # Evita desenhar aresta duplicada
                par = tuple(sorted([node_value, vizinho.value]))
                if par in desenhadas:
                    continue
                desenhadas.add(par)

                x2, y2 = self.mapa.coordenadas[vizinho.value]
                pos2 = self.mundo_para_tela(x2, y2)

                pygame.draw.line(self.tela, self.COR_ARESTA, pos1, pos2, 1)

    def desenhar_caminho(self, caminho, cor, largura=4, offset=0):
        """Desenha um caminho no mapa"""
        if not caminho or not self.mapa:
            return

        for i in range(len(caminho) - 1):
            if (
                caminho[i] not in self.mapa.coordenadas
                or caminho[i + 1] not in self.mapa.coordenadas
            ):
                continue

            x1, y1 = self.mapa.coordenadas[caminho[i]]
            x2, y2 = self.mapa.coordenadas[caminho[i + 1]]

            # Inverte o y para o cálculo do offset perpendicular
            y1, y2 = -y1, -y2

            # Aplica offset para separar visualmente os dois caminhos
            if offset != 0:
                dx = y2 - y1
                dy = x1 - x2
                comprimento = (dx**2 + dy**2) ** 0.5
                if comprimento > 0:
                    dx_offset = (dx / comprimento) * offset
                    dy_offset = (dy / comprimento) * offset
                    # Desfaz a inversão do y ao aplicar o offset
                    x1, y1 = x1 + dx_offset, -(y1 - dy_offset)
                    x2, y2 = x2 + dx_offset, -(y2 - dy_offset)
                else:
                    # Desfaz a inversão se não houve offset
                    y1, y2 = -y1, -y2
            else:
                y1, y2 = -y1, -y2

            pos1 = self.mundo_para_tela(x1, y1)
            pos2 = self.mundo_para_tela(x2, y2)

            pygame.draw.line(self.tela, cor, pos1, pos2, largura)

    def desenhar_nodes(self, destacar=None):
        """Desenha todos os nodos do grafo"""
        if not self.mapa:
            return

        for node_value, (x, y) in self.mapa.coordenadas.items():
            pos = self.mundo_para_tela(x, y)

            # Define cor e tamanho baseado se é destaque ou não
            if destacar and node_value in destacar:
                cor = self.COR_NODE_DESTAQUE
                raio = int(max(4, 8 * self.zoom))
            else:
                cor = self.COR_NODE
                raio = int(max(3, 5 * self.zoom))

            # Desenha círculo do nodo
            pygame.draw.circle(self.tela, cor, pos, raio)
            pygame.draw.circle(
                self.tela, (255, 255, 255), pos, raio, 1
            )  # Borda mais fina

            # Desenha label se zoom for adequado
            if self.mostrar_labels and self.zoom > 0.5:
                texto = self.fonte_pequena.render(node_value, True, self.COR_TEXTO)
                texto_rect = texto.get_rect(center=(pos[0], pos[1] - (raio + 10)))

                # Fundo branco semi-transparente para legibilidade
                fundo = pygame.Surface((texto_rect.width + 4, texto_rect.height + 2))
                fundo.set_alpha(180)
                fundo.fill((255, 255, 255))
                self.tela.blit(fundo, (texto_rect.x - 2, texto_rect.y - 1))
                self.tela.blit(texto, texto_rect)

    def desenhar_painel_info(self):
        """Desenha painel com informações e controles"""
        # Painel semi-transparente
        painel = pygame.Surface((300, 250))  # Reduzido para ser mais compacto
        painel.set_alpha(220)
        painel.fill((255, 255, 255))
        self.tela.blit(painel, (10, 10))

        y = 20

        # Título
        titulo = self.fonte_grande.render("Comparação A*", True, self.COR_TEXTO)
        self.tela.blit(titulo, (20, y))
        y += 40

        # Info do A* + Fuzzy
        if self.caminho_fuzzy:
            texto = f"A* + Fuzzy: {len(self.caminho_fuzzy)} nodos"
            cor_texto = (
                self.COR_CAMINHO_FUZZY if self.mostrar_fuzzy else (150, 150, 150)
            )
            label = self.fonte.render(texto, True, cor_texto)
            self.tela.blit(label, (20, y))
            y += 20

            custo_texto = f"  Custo: {self.custo_fuzzy:.2f}"
            label = self.fonte_pequena.render(custo_texto, True, cor_texto)
            self.tela.blit(label, (20, y))
            y += 25

        # Info do A* Tradicional
        if self.caminho_tradicional:
            texto = f"A* Tradicional: {len(self.caminho_tradicional)} nodos"
            cor_texto = (
                self.COR_CAMINHO_TRADICIONAL
                if self.mostrar_tradicional
                else (150, 150, 150)
            )
            label = self.fonte.render(texto, True, cor_texto)
            self.tela.blit(label, (20, y))
            y += 20

            custo_texto = f"  Custo: {self.custo_tradicional:.2f}"
            label = self.fonte_pequena.render(custo_texto, True, cor_texto)
            self.tela.blit(label, (20, y))
            y += 30

        # Controles
        controles = [
            "Controles:",
            "• Arrastar: Mover mapa",
            "• Scroll: Zoom",
            "• F: Toggle A* + Fuzzy",
            "• T: Toggle A* Tradicional",
            "• L: Toggle Labels",
            "• ESC: Sair",
        ]

        for linha in controles:
            label = self.fonte_pequena.render(linha, True, self.COR_TEXTO)
            self.tela.blit(label, (20, y))
            y += 15

    def processar_eventos(self):
        """Processa eventos do Pygame"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return False
                elif evento.key == pygame.K_f:
                    self.mostrar_fuzzy = not self.mostrar_fuzzy
                elif evento.key == pygame.K_t:
                    self.mostrar_tradicional = not self.mostrar_tradicional
                elif evento.key == pygame.K_l:
                    self.mostrar_labels = not self.mostrar_labels

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo
                    self.arrastando = True
                    self.ultima_pos_mouse = evento.pos
                elif evento.button == 4:  # Scroll up (zoom in)
                    self.zoom = min(3.0, self.zoom * 1.1)
                elif evento.button == 5:  # Scroll down (zoom out)
                    self.zoom = max(0.3, self.zoom * 0.9)

            elif evento.type == pygame.MOUSEBUTTONUP:
                if evento.button == 1:
                    self.arrastando = False

            elif evento.type == pygame.MOUSEMOTION:
                if self.arrastando:
                    dx = evento.pos[0] - self.ultima_pos_mouse[0]
                    dy = evento.pos[1] - self.ultima_pos_mouse[1]
                    self.offset_x += dx
                    self.offset_y += dy
                    self.ultima_pos_mouse = evento.pos

        return True

    def carregar_rotas(self, mapa, origem, destino):
        """Carrega e calcula as rotas dos dois algoritmos"""
        self.mapa = mapa

        # Calcula A* + Fuzzy
        resultado_fuzzy = mapa.busca_a_estrela(origem, destino)
        if resultado_fuzzy:
            self.caminho_fuzzy, self.custo_fuzzy = resultado_fuzzy

        # Calcula A* Tradicional
        resultado_trad = mapa.busca_a_estrela_tradicional(origem, destino)
        if resultado_trad:
            self.caminho_tradicional, self.custo_tradicional = resultado_trad

    def executar(self):
        """Loop principal do visualizador"""
        rodando = True

        while rodando:
            rodando = self.processar_eventos()

            # CORREÇÃO AQUI: Limpa a tela no início de cada quadro
            self.tela.fill(self.COR_FUNDO)

            # Desenha tudo
            self.desenhar_fundo()
            self.desenhar_arestas()

            # Desenha caminhos (com offset para separar visualmente)
            if self.mostrar_tradicional:
                self.desenhar_caminho(
                    self.caminho_tradicional,
                    self.COR_CAMINHO_TRADICIONAL,
                    largura=4,
                    offset=-3,
                )

            if self.mostrar_fuzzy:
                self.desenhar_caminho(
                    self.caminho_fuzzy, self.COR_CAMINHO_FUZZY, largura=4, offset=3
                )

            # Desenha nodos destacando origem e destino
            nodes_destaque = []
            if self.caminho_fuzzy:
                nodes_destaque = [self.caminho_fuzzy[0], self.caminho_fuzzy[-1]]

            self.desenhar_nodes(destacar=nodes_destaque)
            self.desenhar_painel_info()

            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS

        pygame.quit()
