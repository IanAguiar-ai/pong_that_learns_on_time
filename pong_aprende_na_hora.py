from random import random, randint, sample
from math import *
import pygame
from artificial_neural_network import *

class obj:
    def __init__(self,v):
        self.p_vel = v

        self.velocidade()

        #Posicao_inicial
        self.posicao()

        self.colorir()

        #Tudo para efeito voltar no tempo
        self.d = (self.p_vel*2)/100
        self.terminou = True

    def velocidade(self):
        self.vel = int(self.p_vel)

    def colorir(self):
        self.cor = (int(self.x % 255),
                    int(self.y % 255 ),
                    int((self.x + self.y) % 255))

    def posicao(self):
        self.x = int(tela.x/2)
        self.y = int(tela.y/2)
        self.angulo = int(random()*360)

    def andar(self):
        self.angulo = self.angulo % 360

        if self.angulo > 150 and self.angulo < 200:
            self.angulo += int(random()*30 - 15)
            
        if (self.x + int(cos(radians(self.angulo)) * self.vel)) > tela.x and self.angulo >= 0 and self.angulo < 90:
            self.angulo = 90 + (90 - self.angulo)
        if (self.x + int(cos(radians(self.angulo)) * self.vel)) < 0 and self.angulo >= 90 and self.angulo < 180:
            self.angulo = 90 + (90 - self.angulo)
        if (self.x + int(cos(radians(self.angulo)) * self.vel)) < 0 and self.angulo >= 180 and self.angulo < 270:
            self.angulo = 270 + (270 - self.angulo)
        if (self.x + int(cos(radians(self.angulo)) * self.vel)) > tela.x and self.angulo >= 270 and self.angulo < 360:
            self.angulo = 270 + (270 - self.angulo)
            
        self.x = (self.x + int(cos(radians(self.angulo)) * self.vel))
        self.y = (self.y + int(sin(radians(self.angulo)) * self.vel))

        if ((self.y + int(sin(radians(self.angulo)) * self.vel))) > tela.y:
            p.ponto_p2 += 1
            ia_2.mudar_cor()
            self.x = int(tela.x/2)
            self.y = int(tela.y/2)
            self.angulo = int(random()*360)
            self.vel = self.p_vel
        if ((self.y + int(sin(radians(self.angulo)) * self.vel))) < 0:
            p.ponto_p1 += 1
            ia_1.mudar_cor()
            self.x = int(tela.x/2)
            self.y = int(tela.y/2)
            self.angulo = int(random()*360)
            self.vel = self.p_vel

        self.voltar_tempo()
        
        pygame.draw.circle(screen, self.cor, (self.x, self.y), 10) #Coloca na tela

        #pygame.draw.line(screen,(255,255,255), (self.x,self.y),
        #                 ((self.x + int(cos(radians(self.angulo - 180)) * self.vel * 5)),
        #                  self.y + int(sin(radians(self.angulo - 180)) * self.vel * 5)))

    def voltar_tempo(self):
        if self.terminou == False:
            if self.vel != self.p_vel:
                self.vel += self.d

            if self.vel >= self.p_vel:
                self.terminou = True


class grafico:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class jogador:
    def __init__(self,p,l,a,vel_max):

        self.posicao(p)

        self.largura = l
        self.altura = a

        self.vl = vel_max

        self.mudar_cor()


    def posicao(self,p):
        self.x = int(tela.x/2)
        self.y = p

    def mudar_cor(self):
        self.cor = (int(p.ponto_p1*47 % 255),
                    int((self.y * 47)% 255),
                    int(p.ponto_p2*47 % 255))

    def andar(self, c):
        dif = int(self.largura/2)
        if bola.x > self.x + dif:
            self.x += self.vl
        if bola.x < self.x + dif:
            self.x -= self.vl

        self.colisao(c)

        pygame.draw.rect(screen, self.cor, pygame.Rect(self.x, self.y, self.largura, self.altura), 2) #Coloca na tela

    def andar_ia(self, c, rede):
        resp_ = dado(bola)
        resp_[15] = 1 - resp_[15]
        resp_[16] = (resp_[16] + 1) % 2
        resp = (rede == resp_)
        resp_max = resp.index(max([*resp[:15]])) * 100

        if resp_max > self.x:
            self.x += self.vl
        if resp_max < self.x:
            self.x -= self.vl

        self.colisao(c)

        pygame.draw.rect(screen, self.cor, pygame.Rect(self.x, self.y, self.largura, self.altura), 2) #Coloca na tela
        

    def controlar_1(self,c):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vl
        if keys[pygame.K_RIGHT]:
            self.x += self.vl

        if keys[pygame.K_KP5]:
            bola.angulo += 1
        if keys[pygame.K_KP4]:
            bola.angulo -= 1

        if keys[pygame.K_KP1]:
            self.x = bola.x - int(self.largura/2)
            
        if keys[pygame.K_KP2]:
            self.largura += 1

        if keys[pygame.K_KP3]:
            bola.vel -= .25
        if keys[pygame.K_KP6]:
            bola.vel += .25
            
        self.colisao(c)

        pygame.draw.rect(screen, self.cor, pygame.Rect(self.x, self.y, self.largura, self.altura), 2) #Coloca na tela

    def controlar_2(self,c):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x -= self.vl
        if keys[pygame.K_d]:
            self.x += self.vl
            
        self.colisao(c)

        pygame.draw.rect(screen, self.cor, pygame.Rect(self.x, self.y, self.largura, self.altura), 2) #Coloca na tela

    def secreto(self):
        self.x = bola.x - int(self.largura/2)
        self.colisao()

    def colisao(self,c):
        for i in range(len(c)):
            if self.y > int(tela.y/2):
                if c[i].x > self.x and c[i].x < self.x + self.largura and c[i].y > self.y - int(self.altura/4) and c[i].angulo > 0 and c[i].angulo <= 180:
                    c[i].angulo = 180 + (180 - c[i].angulo) + int(random()*30-15)
                    c[i].colorir()

            else:
                if c[i].x > self.x and c[i].x < self.x + self.largura and c[i].y < self.y + int(self.altura*1.3) and c[i].angulo > 180 and c[i].angulo <= 360:
                    c[i].angulo = 180 + (180 - c[i].angulo) + int(random()*30-15)
                    c[i].colorir()

class pontuacao:
    def __init__(self):
        self.ponto_p1 = 0
        self.ponto_p2 = 0

def mod(k):
    if k < 0:
        return -k
    return k

def dividir(p):
    a = 5
    b = 5
    c = 3
    d = 10
    return a, b, c, d

def update_fps(): ###
    fps = str(int(clock.get_fps()))
    return font.render(fps, 1, pygame.Color("coral"))

def potuacao():
    pnt = str(p.ponto_p1) + " - " + str(p.ponto_p2)
    return font.render(pnt, 1, pygame.Color("coral"))

def mod(k):
    if k < 0:
        return -k
    return k

class caixa_abilidade:
    def __init__(self):
        self.posicao()
        self.mudar()
        self.largura = 20
        self.altura = 20

    def mudar(self):
        tipo = ["velocidade","tempo","desviar","teletrasporte"]
        self.t = tipo[int(random()*len(tipo))]
        self.posicao()
        self.colorir()
        
    def posicao(self):
        self.x = int(random()*(tela.x))
        self.y = int(random()*(tela.y))

    def colorir(self):
        if self.t == "velocidade":
            self.cor = (255,70,70)
        if self.t == "tempo":
            self.cor = (90,90,90)
        if self.t == "desviar":
            self.cor = (220,220,50)
        if self.t == "teletrasporte":
            self.cor = (90,40,170)

    def colisao(self,c):
        for i in range(len(c)):
            if mod(self.x - c[i].x - 10) < 20 and mod(self.y - c[i].y) < 20:
                if self.t == "velocidade":
                    c[i].vel += int(c[i].vel/2)
                if self.t == "tempo":
                    c[i].angulo = (c[i].angulo + 180) % 360
                    c[i].vel = -c[i].vel
                    c[i].terminou = False
                if self.t == "desviar":
                    c[i].angulo = (c[i].angulo + random()*360) % 360
                if self.t == "teletrasporte":
                    c[i].x = int(random()*tela.x/2+tela.x/4)
                    c[i].y = int(random()*tela.y/2+tela.y/4)
                    c[i].angulo = (c[i].angulo + random()*180 - 90) % 360
                    
                self.mudar() #Muda a caixa a posição e a cor

        pygame.draw.rect(screen, self.cor, pygame.Rect(self.x, self.y, self.largura, self.altura)) #Coloca na tela        
        
def ativar_caixas(l,bolas):
    for i in range(len(l)):
        l[i].colisao(bolas)        

def ativar_bolas(bolas):
    for i in range(len(bolas)):
        bolas[i].andar()


def dado(p):
    if bola.angulo > 180:
        dir_1 = 1
    else:
        dir_1 = 0
    if 270 > bola.angulo > 90:
        dir_2 = 1
    else:
        dir_2 = 0
    
    a = int(p.x/100)
    r = [0, 0, 0, 0, 0,
         0, 0, 0, 0, 0,
         0, 0, 0, 0, 0,
         bola.y/900, dir_1, dir_2]
    try:
        r[a] = 1
    except:
        r[15] = 1
    return r

def limitar_tamanho_listas(lista1, lista2, tamanho_desejado = 300):
    # Verificar se as listas já têm o tamanho desejado
    if len(lista1) <= tamanho_desejado:
        return lista1, lista2

    # Determinar quantos elementos serão removidos
    num_elementos_a_remover = len(lista1) - tamanho_desejado

    # Criar cópias das listas originais
    lista1_copia = lista1.copy()
    lista2_copia = lista2.copy()

    # Obter os índices dos elementos a serem removidos
    indices_a_remover = sample(range(len(lista1_copia)), num_elementos_a_remover)
    indices_a_remover.sort(reverse=True)

    # Remover elementos dos mesmos índices em ambas as listas
    for indice in indices_a_remover:
        lista1_copia.pop(indice)
        lista2_copia.pop(indice)

    return lista1_copia, lista2_copia

if __name__ == "__main__":

    nome_rede = "imitando"

    rede = mlp([18, 30, 30, 18], learn = 0.1)

    try:
        rede.import_(nome_rede)
    except:
        pass

    rede.print_ = False
    
    #Inicia os objetos
    p = pontuacao()
    tela = grafico(1500,900)

    #Bolas
    bola = obj(6)
    bola_2 = obj(6)
    bolas = [bola]

    #Jogadores
    ia_1 = jogador(tela.y - 50, 100, 30, 5)
    ia_2 = jogador(25, 100, 30, 5)
    #ia_3 = jogador(tela.y - 50, 100, 30, 4)

    #Caixa abilidades
    caixas = []
    for i in range(0):
        caixas.append(caixa_abilidade())

    #Inicia tela
    pygame.init()
    screen = pygame.display.set_mode([tela.x, tela.y])

    #Clock
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    #Para treinamento:
    dados_infs_1 = []
    dados_infs_2 = []
    antigo_p1 = 0
    antigo_p2 = 0

    op = 0
    #Roda o jogo
    running = True
    while running:
        #Botão fechar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #Fundo
        screen.fill((0, 0, 0))
        screen.blit(update_fps(), (10,0))
        screen.blit(potuacao(), (tela.x - 50,int(tela.y/2) - 10))

        ativar_bolas(bolas)

        ia_1.controlar_1(bolas)
        ia_2.andar_ia(bolas, rede)
        #ia_3.secreto()

        ativar_caixas(caixas, bolas)

        clock.tick(60)

        #Treina:
        if op % 5 == 0:
            dados_infs_1.append(dado(bola))
            dados_infs_2.append(dado(ia_1))
        if p.ponto_p2 != antigo_p2:
            dados_infs_1, dados_infs_2 = dados_infs_1[:-30], dados_infs_2 [:-30] 
            dados_infs_1, dados_infs_2 = limitar_tamanho_listas(dados_infs_1, dados_infs_2)
            antigo_p2 = p.ponto_p2
            print("Sucess!")
            rede.export_(nome_rede)
        if p.ponto_p1 != antigo_p1:
            rede.train(dados_infs_1, dados_infs_2, times = 1)
            dados_infs_1, dados_infs_2 = limitar_tamanho_listas(dados_infs_1, dados_infs_2)
            antigo_p1 = p.ponto_p1
            print("Train!")
        op = (op + 1 ) % 10000

        #Tela
        pygame.display.flip()
                    

    #Para fechar
    pygame.quit()  

