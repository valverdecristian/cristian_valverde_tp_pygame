import pygame
from pygame.locals import *
from constantes import *
from player import Player
from enemigo import Enemy
from plataforma import Plataform
from background import Background
from bullet import Bullet
from botin import Objeto
from auxiliar import Auxiliar
from class_healthBar import HealthBar
from class_chronometer import Chronometer
from manejador_banderas import *

class Level1():
    def __init__(self,w,h):

        # --- GAME ELEMNTS --- 
        self.cronometro = Chronometer(tiempo_inicial=60)
        self.last_update_time = pygame.time.get_ticks()
        self.static_background = Background(x=0,y=0,width=w,height=h,path="images/locations/all.png")

        self.player = Player(x=100,y=200,speed_walk=6,speed_run=12,gravity=14,jump_power=30,frame_rate_ms=100,move_rate_ms=50,jump_height=140,p_scale=0.2,interval_time_jump=300)
        self.barra_salud = HealthBar(200, 10, self.player.lives, 5)
        self.datos_obtenidos = Auxiliar.leer_json(ruta="niveles.json")

        self.enemy_list = list()
        self.enemy_list.append (Enemy(x=650,y=200,speed_walk=4,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.enemy_list.append (Enemy(x=900,y=200,speed_walk=5,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.08,interval_time_jump=300))
        self.plataform_list = list()
        self.objeto_list = list()
        self.bullet_list = list()
        self.flagenemy = False
        
        for coordenada in self.datos_obtenidos["primer_nivel"]["plataformas"]:
            x,y,width,height,type=coordenada
            self.plataform_list.append(Plataform(x,y,width,height,type, path_img="images/tileset/plataforma1.png"))

            gema = Objeto(x=x, y=y-50, width=30, height=30, image_path="images/objetos/gema1.png", nombre="gema")
            self.objeto_list.append(gema)

        veneno = Objeto(x=800, y=550, width=30, height=30, image_path="images/objetos/veneno.png", nombre="veneno")
        self.objeto_list.append(veneno)

    def update(self,lista_eventos):
        delta_ms = pygame.time.get_ticks() - self.last_update_time
        self.last_update_time = pygame.time.get_ticks()

        for bullet in self.bullet_list:
            print("dispara")
            bullet.update(delta_ms,self.plataform_list,self.enemy_list,self.player)

        for enemy_element in self.enemy_list:
            if self.player.rect.colliderect(enemy_element.rect):
                print("colisiono con el enemigo")
                self.enemy_list.remove(enemy_element)
            enemy_element.update(delta_ms,self.plataform_list)
            
        if not self.enemy_list and self.flagenemy == False:
            print("aparece la llave")
            self.flagenemy = True
            llave = Objeto(x=1000, y=550, width=70, height=100, image_path="images/objetos/keyBlue.png", nombre="llave")
            self.objeto_list.append(llave)
            
        for objeto in self.objeto_list:
            if self.player.rect.colliderect(objeto.rect):
                if objeto.nombre == "gema":
                    self.player.score += 100  # Aumentar el puntaje del jugador
                elif objeto.nombre == "veneno":
                    print("tomo un veneno xd")
                    self.player.lives -=1 # Restar vida del jugador
                elif objeto.nombre == "llave":
                    self.guardar_partida()
                    modificar_banderas("nivel_1", "terminado", True)
                    modificar_banderas("nivel_1", "reset", True)
                self.objeto_list.remove(objeto)  # Elimina el objeto

        self.player.events(delta_ms,lista_eventos)
        self.player.update(delta_ms,self.plataform_list)
        self.cronometro.actualizar()
    
    def draw(self, pantalla): 
        if leer_bandera("nivel_1", "reset"):
            print("Gano")
            imagen = pygame.image.load(r'menu_1\win.jpg')
            imagen_escalada = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
            pantalla.blit(imagen_escalada, (0, 0))
        elif self.player.lives <= 0 or self.cronometro.tiempo_desendente <= 0 :
            print("juego terminado")
            imagen = pygame.image.load(r'menu_1\gameover.png')
            imagen_escalada = pygame.transform.scale(imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
            pantalla.blit(imagen_escalada, (0, 0))
        else:    
            self.static_background.draw(pantalla)

            for plataforma in self.plataform_list:
                plataforma.draw(pantalla)

            for enemy_element in self.enemy_list:
                enemy_element.draw(pantalla)
            
            self.player.draw(pantalla)
            self.barra_salud.draw(self.player.lives,pantalla)

            for bullet in self.bullet_list:
                bullet.draw(pantalla)
                
            for gema_element in self.objeto_list:
                gema_element.draw(pantalla)
                
            self.cronometro.mostrar_tiempo(pantalla)
            
    def guardar_partida(self):
        with open("score.txt","w") as archivo:
            archivo.write(str(self.player.score))
            
# fin del nivel