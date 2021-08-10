import pygame
from pygame.locals import *
import random
import copy

LARGURA = 600
ALTURA = 400
SOBRALATERAL = 140
FPS = 30
ELEMENTOS = 3
PILHAS = 3


class Jogo:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.pilhadeestados = []
        self.telainicial = pygame.display.set_mode((LARGURA, ALTURA))
        self.estado_final = Estado("_ABC_", True)
        self.estado_inicial = Estado()
        while self.estado_inicial.to_string() == self.estado_final.to_string():
            self.estado_inicial = Estado()
        self.pilhadeestados.append(self.estado_inicial.to_string())

        # self.inteligencia_profundidade()
        # self.inteligencia_largura()
        self.run()

    def gera_filhos(self, estado):
        pai = estado.to_string()
        lista_filhos = []
        resultado = []

        for i in range(3):
            for j in range(2):
                estado_auxiliar = copy.deepcopy(estado)
                if j == 0:
                    estado_auxiliar.derrubar('E', i + 1)
                if j == 1:
                    estado_auxiliar.derrubar('D', i + 1)
                if estado_auxiliar.to_string not in lista_filhos:
                    lista_filhos.append(estado_auxiliar.to_string())

        for i in lista_filhos:
            if pai != i:
                resultado.append((pai, i))
        return resultado

    def inteligencia_profundidade(self):
        abertos = []
        fechados = []
        abertos_e = []
        fechados_e = []
        abertos.append((None, self.estado_inicial.to_string()))
        abertos_e.append(self.estado_inicial.to_string())
        terminado = False
        while not terminado:
            if len(abertos) > 0:
                x = abertos.pop()
                x_e = abertos_e.pop()
                fechados.append(x)
                fechados_e.append(x_e)
                if x_e == self.estado_final.to_string():
                    terminado = True
                    print("SUCESSO")
                    caminho = []
                    fechados.reverse()
                    elemento = fechados[0]
                    pai = elemento[0]
                    caminho.append(elemento)

                    for i in range(len(fechados)):
                        if fechados[i][1] == pai:
                            pai = fechados[i][0]
                            caminho.append(fechados[i])
                    caminho.reverse()
                    print(f"Total de estados do vetor Fechados: {len(fechados) - 1}")
                    print(f"Total de estados do caminho para o final: {len(caminho) - 1}")
                    self.end_game(caminho, True)
                else:
                    filhos = self.gera_filhos(Estado(x_e))
                    for filho in filhos:
                        if filho[1] not in abertos_e and filho[1] not in fechados_e:
                            abertos.append(filho)
                            abertos_e.append(filho[1])
            elif len(abertos) == 0:
                terminado = True
                print("NÃO FOI POSSIVEL RESOLVER ESSE PROBLEMA")

    def inteligencia_largura(self):
        abertos = []
        fechados = []
        abertos_e = []
        fechados_e = []
        abertos.append((None, self.estado_inicial.to_string()))
        abertos_e.append(self.estado_inicial.to_string())
        terminado = False
        while not terminado:
            if len(abertos) > 0:
                x = abertos.pop(0)
                x_e = abertos_e.pop(0)
                fechados.append(x)
                fechados_e.append(x_e)
                if x_e == self.estado_final.to_string():
                    terminado = True
                    print("SUCESSO")
                    caminho = []
                    fechados.reverse()
                    elemento = fechados[0]
                    pai = elemento[0]
                    caminho.append(elemento)

                    for i in range(len(fechados)):
                        if fechados[i][1] == pai:
                            pai = fechados[i][0]
                            caminho.append(fechados[i])
                    caminho.reverse()
                    print(f"Total de estados do vetor Fechados: {len(fechados) - 1}")
                    print(f"Total de estados do caminho para o final: {len(caminho) - 1}")
                    self.end_game(caminho, True)
                else:
                    filhos = self.gera_filhos(Estado(x_e))
                    for filho in filhos:
                        if filho[1] not in abertos_e and filho[1] not in fechados_e:
                            abertos.append(filho)
                            abertos_e.append(filho[1])
            elif len(abertos) == 0:
                terminado = True
                print("NÃO FOI POSSIVEL RESOLVER ESSE PROBLEMA")

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    posicao = pygame.mouse.get_pos()
                    coisa = self.estado_inicial.collision(posicao)
                    if coisa is not None:
                        if coisa[0].centerx > posicao[0]:
                            if posicao[0] > (LARGURA / 2) + 50:
                                coluna = 3
                            else:
                                coluna = 2

                            self.estado_inicial.derrubar('E', coluna)
                            # if self.estado_inicial.print() not in self.pilhadeestados:
                            self.pilhadeestados.append(self.estado_inicial.to_string())
                            if self.estado_inicial.to_string() == self.estado_final.to_string():
                                print("SUCESSSSSSSO!")
                                print(f"Foram usadas {len(self.pilhadeestados) - 1} jogadas:")
                                for i in self.pilhadeestados:
                                    print(i)
                                running = False
                                self.end_game()
                        else:
                            if posicao[0] < (LARGURA / 2) - 50:
                                coluna = 1
                            else:
                                coluna = 2

                            self.estado_inicial.derrubar('D', coluna)
                            # if self.estado_inicial.print() not in self.pilhadeestados:
                            self.pilhadeestados.append(self.estado_inicial.to_string())
                            if self.estado_inicial.to_string() == self.estado_final.to_string():
                                print("SUCESSSSSSSO!")
                                print(f"Foram usadas {len(self.pilhadeestados) - 1} jogadas:")
                                for i in self.pilhadeestados:
                                    print(i)
                                running = False
                                self.end_game()

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

            self.draw()

    def end_game(self, fechados=None, ia=False):
        running = True
        clock = pygame.time.Clock()
        num = 0

        while running:
            clock.tick(FPS)
            if not ia:
                # if num >= len(self.pilhadeestados) - 1:
                #     running = False

                for event in pygame.event.get():
                    if event.type == QUIT:
                        running = False
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            print(num)
                            num += 1
                            if fechados is not None and num >= len(fechados) - 1:
                                running = False
                if running:
                    self.telainicial.fill(pygame.Color("black"))
                    floor = pygame.Rect((0, ALTURA - 20), (LARGURA, 20))
                    pygame.draw.rect(self.telainicial, pygame.Color("brown"), floor)
                    try:
                        Estado(self.pilhadeestados[num]).draw(self.telainicial)
                    except IndexError:
                        running = False
                    pygame.display.flip()
            else:
                if fechados is not None:
                    # if num >= len(fechados) - 1:
                    #     running = False
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            running = False
                        if event.type == KEYDOWN:
                            if event.key == K_SPACE:
                                try:
                                    print(Estado(fechados[num + 1][1]).to_string())
                                except IndexError:
                                    pass
                                if num >= len(fechados) - 1:
                                    running = False
                                num += 1
                    if running:
                        self.telainicial.fill(pygame.Color("black"))
                        floor = pygame.Rect((0, ALTURA - 20), (LARGURA, 20))
                        pygame.draw.rect(self.telainicial, pygame.Color("brown"), floor)
                        Estado(fechados[num][1]).draw(self.telainicial)
                        pygame.display.flip()

    def draw(self):
        self.telainicial.fill(pygame.Color("black"))
        # Desenhando o CHÃO
        floor = pygame.Rect((0, ALTURA - 20), (LARGURA, 20))
        pygame.draw.rect(self.telainicial, pygame.Color("brown"), floor)
        self.estado_inicial.draw(self.telainicial)
        # self.estado_final.draw(self.telainicial)
        pygame.display.flip()


class Estado:
    def __init__(self, text=None, final=False, elementos=ELEMENTOS, qtde_pilhas=PILHAS):
        self.final = final
        if text is not None:
            self.text = text
        else:
            self.text = self.criar_random(elementos, qtde_pilhas)
            print(self.text)
        self.espacamento = (LARGURA - qtde_pilhas * 50 - 2 * SOBRALATERAL) / (qtde_pilhas - 1)
        self.pilha = []
        self.qtde_pilhas = qtde_pilhas
        for i in range(self.qtde_pilhas):
            self.pilha.append([])

        self.retangulos = []
        contador = 0

        for i in range(len(self.text)):
            if self.text[i] == '_':
                contador += 1
            else:
                self.pilha[contador].append(self.text[i])

    def draw(self, tela_principal):
        # Desenhando os BLOCOS
        font = pygame.font.SysFont("monospace", 50)
        if self.final:
            for i in range(len(self.pilha)):
                for j in range(len(self.pilha[i])):
                    menor = 5
                    if self.pilha[i][j] == 'A':
                        teste = ord('A')
                        print(f"{ord(self.pilha[i][j]) - teste}, A")
                        retangulo = [pygame.Rect((SOBRALATERAL + i * (50 + self.espacamento) + menor,
                                                  (ALTURA - 20) - (j + 1) * 50 + menor), (40, 40)),
                                     pygame.Color("orange"), 'A']
                        self.retangulos.append(retangulo)

                        pygame.draw.rect(tela_principal, retangulo[1], retangulo[0])
                        label = font.render(self.pilha[i][j], True, pygame.Color("black"))
                        tela_principal.blit(label, (retangulo[0].centerx - 15, retangulo[0].centery - 30))

                    elif self.pilha[i][j] == 'B':
                        teste = ord('A')
                        print(f"{ord(self.pilha[i][j]) - teste}, B")
                        retangulo = [pygame.Rect((SOBRALATERAL + i * (50 + self.espacamento) + menor,
                                                  (ALTURA - 20) - (j + 1) * 50 + menor), (40, 40)),
                                     pygame.Color("gray"), 'B']
                        self.retangulos.append(retangulo)
                        pygame.draw.rect(tela_principal, retangulo[1], retangulo[0])
                        label = font.render(self.pilha[i][j], True, pygame.Color("black"))
                        tela_principal.blit(label, (retangulo[0].centerx - 15, retangulo[0].centery - 30))
                    elif self.pilha[i][j] == 'C':
                        teste = ord('A')
                        print(f"{ord(self.pilha[i][j]) - teste}, C")
                        retangulo = [pygame.Rect((SOBRALATERAL + i * (50 + self.espacamento) + menor,
                                                  (ALTURA - 20) - (j + 1) * 50 + menor), (40, 40)),
                                     pygame.Color("blue"), 'C']
                        self.retangulos.append(retangulo)

                        pygame.draw.rect(tela_principal, retangulo[1], retangulo[0])
                        label = font.render(self.pilha[i][j], True, pygame.Color("black"))
                        tela_principal.blit(label, (retangulo[0].centerx - 15, retangulo[0].centery - 30))
        else:
            for i in range(len(self.pilha)):
                for j in range(len(self.pilha[i])):
                    if self.pilha[i][j] == 'A':
                        retangulo = [pygame.Rect((SOBRALATERAL + i * (50 + self.espacamento),
                                                  (ALTURA - 20) - (j + 1) * 50), (50, 50)), pygame.Color("yellow"), 'A']
                        self.retangulos.append(retangulo)

                        pygame.draw.rect(tela_principal, retangulo[1], retangulo[0])
                        label = font.render(self.pilha[i][j], True, pygame.Color("black"))
                        tela_principal.blit(label, (retangulo[0].centerx - 15, retangulo[0].centery - 30))
                    elif self.pilha[i][j] == 'B':
                        retangulo = [pygame.Rect((SOBRALATERAL + i * (50 + self.espacamento),
                                                  (ALTURA - 20) - (j + 1) * 50), (50, 50)), pygame.Color("white"), 'B']
                        self.retangulos.append(retangulo)

                        pygame.draw.rect(tela_principal, retangulo[1], retangulo[0])
                        label = font.render(self.pilha[i][j], True, pygame.Color("black"))
                        tela_principal.blit(label, (retangulo[0].centerx - 15, retangulo[0].centery - 30))
                    elif self.pilha[i][j] == 'C':
                        retangulo = [pygame.Rect((SOBRALATERAL + i * (50 + self.espacamento),
                                                  (ALTURA - 20) - (j + 1) * 50), (50, 50)), pygame.Color("cyan"), 'C']
                        self.retangulos.append(retangulo)

                        pygame.draw.rect(tela_principal, retangulo[1], retangulo[0])
                        label = font.render(self.pilha[i][j], True, pygame.Color("black"))
                        tela_principal.blit(label, (retangulo[0].centerx - 15, retangulo[0].centery - 30))

    def collision(self, pos):
        x, y = pos
        for rect in self.retangulos:
            if rect[0].collidepoint(x, y):
                return rect
        return None

    def criar_random(self, elementos, pilhas):
        letra0 = 'A'
        num = ord(letra0)
        resultado = []
        for i in range(pilhas - 1):
            resultado.append('_')
        for i in range(elementos):
            resultado.append(chr(num + i))
        random.shuffle(resultado)
        result = ''
        for i in resultado:
            result += i
        return result

    def derrubar(self, direcao, coluna):
        colunacerta = coluna - 1
        if direcao == 'D':
            if colunacerta < 2:
                if len(self.pilha[colunacerta]) != 0:
                    self.pilha[colunacerta + 1].append(self.pilha[colunacerta].pop())
        if direcao == 'E':
            if colunacerta > 0:
                if len(self.pilha[colunacerta]) != 0:
                    self.pilha[colunacerta - 1].append(self.pilha[colunacerta].pop())

    def to_string(self):
        saida = ""
        if len(self.pilha[0]) == 0:
            saida += '_'
        else:
            for i in self.pilha[0]:
                saida += i
            saida += '_'

        if len(self.pilha[1]) == 0:
            saida += '_'
        else:
            for i in self.pilha[1]:
                saida += i
            saida += '_'

        if len(self.pilha[2]) != 0:
            for i in self.pilha[2]:
                saida += i

        return saida


Jogo()
