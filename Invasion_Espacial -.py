'''Codigo básico para realizar un juego usando la libreria externa Pygame, parte de formaciones realizadas
en mi proceso de aprendizaje de programación usando el lenguaje Python'''

#Importacion de las librerías a usar
import pygame
import random
import math
from pygame import mixer
import io


#Inicializar pygame
pygame.init()

#cargar imagen de fondo, colocar la imagen en la misma carpta del ejecutable
fondo=pygame.image.load("FONDO.png")

#configurar el tamano de la pantalla
pantalla=pygame.display.set_mode((800,600))

#Configuraciones para el titulo e icono
pygame.display.set_caption("Invasión Espacial")
icono=pygame.image.load("ovni.png")
pygame.display.set_icon(icono)

#Para agregar la musica de fondo
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

#cargar nave espacial, imagen en el directorio del ejecutable
img_jugador=pygame.image.load("cohete.png")
#configirar posicion del jugador
jugador_x=368
jugador_y=500
jugador_x_cambio=0

#Agregar enemigos
img_enemigo=[]
enemigo_x=[]
enemigo_y=[]
enemigo_x_cambio=[]
enemigo_y_cambio=[]
cantidad_enemigos=8 #coloque 8 podria colocar los que quiera

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("enemigo.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.3)
    enemigo_y_cambio.append(50)

#Configurar las balas que disparará la nave a los enemigos
img_bala=pygame.image.load("bala.png")
bala_x=0 #en equis por ahora en cero
bala_y=500 #la bala en y debe estar a la altura de la nave o jugador que es 500
bala_x_cambio=0
bala_y_cambio=3
bala_visible=False

#Configurar puntaje cada vez que se elimina un enemigo
puntaje=0

#Funcion para convertir el ejecutable .py a un .exe
def fuente_bytes(fuente):
    #abre el archivo en formato ttf (formato que usa para el texto) en modo lectura binaria
    with open(fuente, "rb") as f:
        #lee todos los bytes del archivo y los almacena en una variable
        ttf_bytes=f.read()
        #crea un oibjeto BytesIO a partir de los bytes del archivo ttf
    return io.BytesIO(ttf_bytes)

fuente_como_bytes= fuente_bytes("freesansbold.ttf")
fuente=pygame.font.Font(fuente_como_bytes,32)
texto_x=10
texto_y=10

#texto de final de juego
fuente_final=pygame.font.Font(fuente_como_bytes,40)

def texto_final():
    mi_fuente_final=fuente_final.render("JUEGO TERMINADO",True,(255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))

#Función para mostrar puntaje
def mostrar_puntaje(x,y):
    texto=fuente.render(f"Puntaje: {puntaje}",True,(255,255,255))
    pantalla.blit(texto, (x,y))

#Función para lanzar al jugagor o la nave a la pantalla
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))

#Función para lanzar en pantalla al enemigo
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))

#Función para disparar balas
def disparar_bala(x,y):
    global bala_visible #global se usa para que aplique a todo, leer mas mejor
    bala_visible=True
    pantalla.blit(img_bala,(x+16,y+10))

#Función para determinar si hay colisión entre la nave y los enemigos
def hay_colision(x_1,y_1,x_2,y_2):
    distancia=math.sqrt(math.pow(x_2-x_1,2)+math.pow(y_2-y_1,2)) #math.pow es exponente y el 2 indica que es el cuadrado
    if distancia < 27: #se coloca 27 porque si la distancia entre el enemigo y la bala es menor se considerara colision
        return True
    else:
        return False

#Creación del loop del juego
se_ejecuta= True
while se_ejecuta:
    for evento in pygame.event.get():
        if evento.type==pygame.QUIT:
            se_ejecuta=False
        #Para controlar los movimientos
        if evento.type==pygame.KEYDOWN:
            if evento.key==pygame.K_LEFT:
                jugador_x_cambio=-2.5
            if evento.key==pygame.K_RIGHT:
                jugador_x_cambio= 2.5
            if evento.key==pygame.K_SPACE:
                #Agregar efecto de sonido
                sonido_bala=mixer.Sound("disparo.mp3")
                sonido_bala.play()
                if bala_visible==False:
                    bala_x=jugador_x
                    disparar_bala(bala_x,bala_y)
        if evento.type==pygame.KEYUP:
            if evento.key==pygame.K_LEFT or evento.key==pygame.K_RIGHT:
                jugador_x_cambio= 0


    pantalla.blit(fondo,(0,0))
    jugador_x+=jugador_x_cambio
    if jugador_x <= 0:
        jugador_x=0
    elif jugador_x >= 736:
        jugador_x=736

    for e in range(cantidad_enemigos):
        if enemigo_y[e]>500:
            for k in range(cantidad_enemigos):
                enemigo_y[k]=1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1.5
            enemigo_y[e]+=enemigo_y_cambio[e]
        elif enemigo_x[e] >= 768:
            enemigo_x_cambio[e] = -1.5
            enemigo_y[e] +=enemigo_y_cambio[e]
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision == True:
            #agregar sonido a las colisiones
            sonido_colision=mixer.Sound("Golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1  # le sumo 1 al puntaje cada vez que haya una colision

            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)
        enemigo(enemigo_x[e], enemigo_y[e],e)

    if bala_y <= -32:
        bala_y=500
        bala_visible=False
    if bala_visible==True:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio


    jugador(jugador_x,jugador_y)

    mostrar_puntaje(texto_x,texto_y)

    pygame.display.update()

