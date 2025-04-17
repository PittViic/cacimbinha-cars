import pygame
import random
import time
import sys

# Inicialização da biblioteca Pygame
pygame.init()
pygame.font.init()

#Fontes de Mensagens
fonte_fim_jogo = pygame.font.Font(None, 55)
fonte_mudanca_fase = pygame.font.Font(None, 25)

#Variavel fim de jogo
jogo_acabou = False

#Quantidade de Obstaculos
qtd_obstaculos = 0
fase_atual = 1

# Configurações de Tela (Resolução)
largura_tela = 500
altura_tela = 800
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Imposto's Fuga")

#Carregando Imagens
background_image = pygame.image.load('Highway.jpg')
end_game_image = pygame.image.load('perceba.jpg')
obstaculo = pygame.image.load('obstaculo.png')

#Inicializo o Mixer
pygame.mixer.init()

#Carregando audios
pygame.mixer.music.load('meu_pai_e_foda.mp3')
audio_batida = pygame.mixer.Sound('meuovo.mp3')

#Volume da musica
pygame.mixer.music.set_volume(0.5)
audio_batida.set_volume(1)

#Inicie a reprodução da música em um loop
pygame.mixer.music.play(-1)

# Cores
preto = (0, 0, 0)
branco = (255, 255, 255)

#Variaveis de tempo
fonte_tempo = pygame.font.SysFont(None, 25)
tempo_inicial = pygame.time.get_ticks()
tempo_passado_segundos = 0

# Aqui coloquei separado para ajustar as configurações do carro
carro_largura = 80
carro = pygame.image.load('pngegg.png')  
carro = pygame.transform.scale(carro, (carro_largura, 100))

# Posição inicial do carro
x = (largura_tela * 0.45)
y = (altura_tela * 0.8)

# Configurações dos obstáculos
obstaculo_largura = 50
obstaculo_altura = 100
obstaculo_cor = (255, 0, 0)  
obstaculo_velocidade = 7 
obstaculo_x = random.randrange(0, largura_tela)
obstaculo_y = -600

# Função para imagem de fundo
def background(background_image):
    size = pygame.transform.scale(background_image, (500, 800))
    tela.blit(size, (0, 0))
    
# Função para imagem de fim de jogo
def end_image(end_game_image):
    size = pygame.transform.scale(end_game_image, (500, 800))
    tela.blit(size, (0, 0))

# Desenhando os obstáculos 
def desenha_obstaculo(x, y, largura, altura, cor):
    pygame.draw.rect(tela, cor, [x, y, largura, altura])
    
# Função para verificar fase e alterar velocidade
def level(obstaculo_velocidade, fase_atual):
    # Contagem e mudança de fase
    if qtd_obstaculos > 0 and qtd_obstaculos % 10 == 0:
        if fase_atual < 3 and qtd_obstaculos // 10 == 1:  # Mudança de fase após 10 obstáculos
            fase_atual += 1
            obstaculo_velocidade += 1
            mensagem_fase = fonte_mudanca_fase.render(f'Nova fase alcançada! Fase {fase_atual}', True, branco)

# Redesenhando a tela 
def redesenhar_tela():
    background(background_image)
    tela.blit(carro, (x, y))
    desenha_obstaculo(obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura, obstaculo_cor)
        
    #Desenha um retangulo para o contador
    pygame.draw.rect(tela, preto, (0, 0, 120, 50))
    
    #Atualiza tempo do contador
    texto_tempo = fonte_tempo.render(f"Tempo: {int(tempo_passado_segundos)}s", True, branco)
    mensagem_fase = fonte_mudanca_fase.render(f'Fase: {fase_atual}', True, branco)
    tela.blit(texto_tempo, (10, 10))
    tela.blit(mensagem_fase, (10, 30))

    pygame.display.update()

# Função para verificar se ocorreu a colisão
def verifica_colisao(x_carro, y_carro, largura_carro, altura_carro, x_obstaculo, y_obstaculo, largura_obstaculo, altura_obstaculo):
    if x_carro < x_obstaculo + largura_obstaculo and x_carro + largura_carro > x_obstaculo \
            and y_carro < y_obstaculo + altura_obstaculo and y_carro + altura_carro > y_obstaculo:
        return True
    return False

# Parte principal do jogo 
jogo_ativo = True
clock = pygame.time.Clock()

while jogo_ativo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_ativo = False

    tempo_atual = pygame.time.get_ticks()
    tempo_passado_segundos = (tempo_atual - tempo_inicial) / 1000

    #if tempo_passado_segundos >= 3:
        #obstaculo_velocidade += 0.1
        #tempo_inicial = pygame.time.get_ticks() #Reinicia o tempo inicial
        #tempo_inicial = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= 5

        if x < 0:
            x = 0

    if keys[pygame.K_RIGHT]:
        x += 5

        if x > (500 - carro_largura):
            x = (500 - carro_largura)

    # Verifica colisão
    if verifica_colisao(x, y, carro_largura, 100, obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura):
        jogo_acabou = True
        qtd_obstaculos = 0

    obstaculo_y += obstaculo_velocidade
    if obstaculo_y > altura_tela:
        obstaculo_y = 0 - obstaculo_altura
        obstaculo_x = random.randrange(0, largura_tela)

    #Redesenha tela
    redesenhar_tela()

    background(background_image)
    tela.blit(carro, (x, y))
    desenha_obstaculo(obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura, obstaculo_cor)
    qtd_obstaculos += 1
    
    level(obstaculo_velocidade, fase_atual)

    if jogo_acabou:
        pygame.mixer.music.pause()
        audio_batida.play()
        end_image(end_game_image)
        mensagem_fim_jogo = fonte_fim_jogo.render(f'Fim de Jogo - {tempo_passado_segundos}', True, branco)
        tela.blit(mensagem_fim_jogo, (largura_tela // 3.2 - 70, altura_tela // 2))

        pygame.display.update()
        pygame.time.delay(2000)  # Aguarda 2 segundos
        jogo_ativo = False

    clock.tick(60)

pygame.quit()