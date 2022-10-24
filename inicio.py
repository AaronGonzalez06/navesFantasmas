import pygame
import random
import math
from pygame import mixer
from modelo.Personaje import Personaje
from modelo.Vida import Vida
import os

#iniciar pygame
pygame.init()
#mostrar pantalla
pantalla = pygame.display.set_mode((800,600))
#musica
mixer.music.load('audio/audio.mp3')
mixer.music.play(-1)
#cambiar titulo
pygame.display.set_caption("halloween")
#cambiar icono
icono = pygame.image.load("img/calabaza.png")
pygame.display.set_icon(icono)
#cambiar imagen de fondo
fondo = pygame.image.load("img/fondo2.jpg")
#puntuacipon
puntuacion = 0
fuente = pygame.font.Font('freesansbold.ttf',32)
texto_x = 10
texto_y = 10

def mostrar_puntuacion (x, y):
    texto = fuente.render(f"Puntuacion {puntuacion}",True, (255,255,255))
    pantalla.blit(texto, (x,y))


#jugador
Jugador = Personaje(368,500,'img/jugador.png',0,0,True)
print(Jugador.img)
img_jugador = pygame.image.load(Jugador.img)

def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))

#enemigos
cantidad_enemigo = 12
Fantasmas = []
img_enemigo = pygame.image.load('img/fantasma.png')
auxx = 150
auxy = 70
for i, val in enumerate([70, 170, 270]):
    print(i, val)
    if val == 170:
        direccion = -0.3
    else:
        direccion = 0.3

    for z, val2 in enumerate([150, 300, 450, 600]):
        Fantasma = Personaje(val2, val, 'img/fantasma.png', direccion, 50, True)
        Fantasmas.append(Fantasma)

def enemigo(x, y):
    pantalla.blit(img_enemigo, (x,y))

#murcielago
Murcielago = Personaje(0,500,'img/murcielago.png',0,0.3,False)
img_murcielago = pygame.image.load(Murcielago.img)

def disparar_murcielago(x,y,Objeto):
    Objeto.visible = True
    pantalla.blit(img_murcielago,(x + 16,y + 10))

#tridente
Tridente = Personaje(0,0,'img/tridente.png',0,0.06,False)
img_tridente = pygame.image.load(Tridente.img)

def disparar_tridente(x,y,Objeto):
    print("entro en tridente")
    Objeto.visible = True
    pantalla.blit(img_tridente,(x,y))

#detectar colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_1 - y_1,2) + math.pow(x_2 - y_2,2))
    if distancia < 50:
        return True
    else:
        return False


#vidas
Vida1 = Vida(768,5,"img/vida.png",0)
Vida2 = Vida(735,5,"img/vida.png",0)
Vida3 = Vida(702,5,"img/vida.png",0)
Pocion = Vida(900,0,"img/pocion.png",0)
img_vida = pygame.image.load(Vida1.img)
img_pocion = pygame.image.load(Pocion.img)
vida = 3
numeros = [0,1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

#finaltexto
def texto_final():
    fuenteFinal = pygame.font.Font('fuente/CFHalloween-Regular.ttf',60)
    Fuente = fuenteFinal.render("FIN DEL JUEGO",True,(127,5,42))
    pantalla.blit(Fuente,(150, 170))
    for e in range(cantidad_enemigo):
        Fantasmas[e].coordenaday = -300
        Fantasmas[e].velocidad = 0

    Tridente.coordenaday = -500
    Tridente.velocidad = 0
    Pocion.coordenaday = -500
    Pocion.velocidad = 0
    Jugador.velocidad = 0
    Murcielago.coordenaday = -300
    Murcielago.velocidad = 0
    mixer.music.stop()


se_inicio = True
while se_inicio:
    pantalla.blit(fondo, (0, 0))
    pantalla.blit(img_vida,(Vida1.coordenadax, Vida1.coordenaday))
    pantalla.blit(img_vida,(Vida2.coordenadax, Vida2.coordenaday))
    pantalla.blit(img_vida,(Vida3.coordenadax, Vida3.coordenaday))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_inicio = False

        #evento cuando pulso una letra
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_a:
                Jugador.velocidad = -0.3
            if evento.key == pygame.K_d:
                Jugador.velocidad = 0.3
            if evento.key == pygame.K_SPACE and Murcielago.visible == False:
                sonidoMur = mixer.Sound('audio/sonidoMurcielago.mp3')
                sonidoMur.play()
                if not Murcielago.visible:
                    Murcielago.coordenadax = Jugador.coordenadax
                    disparar_murcielago(Murcielago.coordenadax,Murcielago.coordenaday,Murcielago)


    # modificacion de movimiento del jugador
    Jugador.coordenadax += Jugador.velocidad
    # control de bordes
    if Jugador.coordenadax <= 0:
        Jugador.coordenadax = 0
    elif Jugador.coordenadax >= 736:
        Jugador.coordenadax = 736

    # modificacion de movimiento del enemigo
    for e in range(cantidad_enemigo):

        #final juego
        if puntuacion == 12:
            texto_final()
            #se_inicio = False
        elif vida == 0:
            texto_final()


        Fantasmas[e].coordenadax += Fantasmas[e].puntos
    # control de bordes
        if Fantasmas[e].coordenadax <= 0:
            Fantasmas[e].puntos = 0.3
            #Fantasmas[e].coordenaday += Fantasmas[e].velocidad
        elif Fantasmas[e].coordenadax >= 736:
            Fantasmas[e].puntos = -0.3
            #Fantasmas[e].coordenaday += Fantasmas[e].velocidad

        #enemigo lanzados
        if not Tridente.visible:
            Tridente.visible = True
            #enemigoNun = random.randint(0, 11)
            enemigoNun = random.choice(numeros)
            Tridente.coordenadax = Fantasmas[enemigoNun].coordenadax
            Tridente.coordenaday = Fantasmas[enemigoNun].coordenaday

        pantalla.blit(img_tridente, (Tridente.coordenadax +15, Tridente.coordenaday +35))

        if Tridente.visible:
            Tridente.coordenaday += Tridente.velocidad

        if Tridente.coordenaday > 600:
            Tridente.visible = False

        # fin enemigo lanzados
    # colision
        colision = hay_colision(Fantasmas[e].coordenadax, Murcielago.coordenadax, Murcielago.coordenaday, Fantasmas[e].coordenaday)
        if colision and Murcielago.visible == True:
            Murcielago.coordenaday = 500
            Murcielago.visible = False
            puntuacion += 1
            #Fantasmas[e].coordenadax = random.randint(0, 736)
            #Fantasmas[e].coordenaday = random.randint(50, 200)
            Fantasmas[e].coordenadax = -300
            Fantasmas[e].coordenaday = -300
            Fantasmas[e].velocidad = 0
            Fantasmas[e].visible = False
            numeros.remove(e)
        enemigo(Fantasmas[e].coordenadax, Fantasmas[e].coordenaday)

    # colision con tridente
        colision = hay_colision(Jugador.coordenadax, Tridente.coordenadax, Tridente.coordenaday,Jugador.coordenaday)
        if colision:
            Tridente.visible = False
            print("me ha dado")
            vida -=1
            if vida == 2:
                Vida3.coordenadax = -30
                Pocion.coordenadax = random.randint(0, 760)
                Pocion.coordenaday = -1500
                Pocion.velocidad = 0.05
            elif vida == 1:
                Vida2.coordenadax = -30
            elif vida == 0:
                Vida1.coordenadax = -30

        Pocion.coordenaday += Pocion.velocidad
        pantalla.blit(img_pocion, (Pocion.coordenadax, Pocion.coordenaday))

    if Pocion.coordenaday > 600:
        Pocion.coordenadax = random.randint(0, 760)
        Pocion.coordenaday = -2000

    colisionPocion = hay_colision(Jugador.coordenadax, Pocion.coordenadax, Pocion.coordenaday, Jugador.coordenaday)
    if colisionPocion:
        if vida == 2:
            Pocion.coordenadax = 0
            Pocion.coordenaday = -2000
            Pocion.velocidad = 0
            vida += 1
            Vida3.coordenadax = 702
            Vida3.coordenaday = 5
        elif vida == 1:
            vida += 1
            Pocion.coordenaday = -2000
            Pocion.coordenadax = random.randint(0, 760)
            Vida2.coordenadax = 735
            Vida2.coordenaday = 5


    # movimiento murcielago
    if Murcielago.coordenaday <= -32:
        Murcielago.coordenaday = 500
        Murcielago.visible = False

    if Murcielago.visible:
        disparar_murcielago(Murcielago.coordenadax,Murcielago.coordenaday,Murcielago)
        Murcielago.coordenaday -= Murcielago.velocidad


    jugador(Jugador.coordenadax,Jugador.coordenaday)

    #mostrar_puntuacion(texto_x,texto_y)

    pygame.display.update()