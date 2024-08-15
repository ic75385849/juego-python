import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Carreras con Obstáculos")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# FPS
RELOJ = pygame.time.Clock()
FPS = 60

# Cargar imágenes
imagen_vehiculo = pygame.image.load('motoooo.png')  # Imagen del vehículo
imagen_obstaculo = pygame.image.load('poliiiiiiii.png')  # Imagen de obstáculos
imagen_fondo = pygame.image.load('fondo2.png')  # Imagen de fondo

# Redimensionar imágenes
imagen_vehiculo = pygame.transform.scale(imagen_vehiculo, (100, 80))
imagen_obstaculo = pygame.transform.scale(imagen_obstaculo, (100, 80))
imagen_fondo = pygame.transform.scale(imagen_fondo, (ANCHO, ALTO))

# Estados del juego
ESTADO_MENU = "menu"
ESTADO_JUGANDO = "jugando"
ESTADO_JUEGO_TERMINADO = "juego_terminado"
estado_juego = ESTADO_MENU

# Puntuación
puntuacion = 0

# Clase para el Vehículo
class Vehiculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagen_vehiculo
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 2, ALTO - 50)
        self.velocidad = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            self.rect.x += self.velocidad

        # Limitar el movimiento del vehículo a la ventana
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO

# Clase para los Obstáculos
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = imagen_obstaculo
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-150, -self.rect.height)
        self.velocidad = 5

    def update(self):
        self.rect.y += self.velocidad
        if self.rect.y > ALTO:
            self.kill()

# Función para iniciar el juego
def iniciar_juego():
    global puntuacion, todos_sprites, obstaculos, vehiculo
    puntuacion = 0
    vehiculo = Vehiculo()
    todos_sprites = pygame.sprite.Group()
    todos_sprites.add(vehiculo)
    obstaculos = pygame.sprite.Group()

# Función para generar obstáculos
def generar_obstaculo():
    if random.random() < 0.04:
        obstaculo = Obstaculo()
        todos_sprites.add(obstaculo)
        obstaculos.add(obstaculo)

# Función para verificar colisiones
def verificar_colisiones():
    if pygame.sprite.spritecollideany(vehiculo, obstaculos):
        return True
    return False

# Función para dibujar la puntuación
def dibujar_puntuacion():
    fuente = pygame.font.SysFont(None, 36)
    texto = fuente.render(f'Puntuación: {puntuacion}', True, BLANCO)
    VENTANA.blit(texto, (10, 10))

# Función para mostrar la pantalla de "Juego Terminado"
def pantalla_juego_terminado():
    fuente = pygame.font.SysFont(None, 72)
    texto_juego_terminado = fuente.render('JUEGO TERMINADO', True, ROJO)
    texto_puntuacion = fuente.render(f'Puntuación: {puntuacion}', True, BLANCO)
    texto_reinicio = pygame.font.SysFont(None, 36).render('Presiona ESPACIO para reiniciar', True, BLANCO)
    VENTANA.blit(texto_juego_terminado, (ANCHO//2 - texto_juego_terminado.get_width()//2, ALTO//2 - 50))
    VENTANA.blit(texto_puntuacion, (ANCHO//2 - texto_puntuacion.get_width()//2, ALTO//2))
    VENTANA.blit(texto_reinicio, (ANCHO//2 - texto_reinicio.get_width()//2, ALTO//2 + 50))

# Función para mostrar la pantalla de inicio
def pantalla_inicio():
    VENTANA.fill(NEGRO)
    fuente = pygame.font.SysFont(None, 72)
    texto_titulo = fuente.render('Carrera con Obstáculos', True, BLANCO)
    texto_inicio = pygame.font.SysFont(None, 36).render('Presiona ENTER para comenzar', True, BLANCO)
    VENTANA.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, ALTO//2 - 50))
    VENTANA.blit(texto_inicio, (ANCHO//2 - texto_inicio.get_width()//2, ALTO//2 + 50))
    pygame.display.flip()

# Bucle principal del juego
ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.KEYDOWN:
            if estado_juego == ESTADO_MENU and evento.key == pygame.K_RETURN:
                estado_juego = ESTADO_JUGANDO
                iniciar_juego()
            elif estado_juego == ESTADO_JUEGO_TERMINADO and evento.key == pygame.K_SPACE:
                estado_juego = ESTADO_MENU

    if estado_juego == ESTADO_JUGANDO:
        # Actualizar
        todos_sprites.update()
        generar_obstaculo()

        # Verificar colisiones
        if verificar_colisiones():
            estado_juego = ESTADO_JUEGO_TERMINADO

        # Incrementar puntuación
        puntuacion += 1

        # Dibujar
        VENTANA.blit(imagen_fondo, (0, 0))
        todos_sprites.draw(VENTANA)
        dibujar_puntuacion()
        pygame.display.flip()
        RELOJ.tick(FPS)

    elif estado_juego == ESTADO_JUEGO_TERMINADO:
        VENTANA.fill(NEGRO)
        pantalla_juego_terminado()
        pygame.display.flip()

    elif estado_juego == ESTADO_MENU:
        pantalla_inicio()

pygame.quit()
