# pantalla
ANCHO_PANTALLA = 1200
ALTO_PANTALLA = 650

GROUND_LEVEL = 600
FPS = 60

DIRECTION_L = 0
DIRECTION_R = 1
GROUND_COLLIDE_H = 8

DEBUG = False
def cambiar_modo():
    global DEBUG
    DEBUG = not DEBUG

def get_mode():
    return DEBUG

#defino los colores
ROJO = (255, 0, 0)
AZUL = (0,0,255)
AMARILLO = (255, 255, 0)
BLANCO = (255, 255, 255)
VERDE = (0, 255, 0)
NEGRO = (0, 0, 0)