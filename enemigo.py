import pygame
from player import *
from constantes import *
from auxiliar import Auxiliar
from bullet import Bullet2
import random

class Enemy():
    
    def __init__(self,x,y,speed_walk,speed_run,gravity,jump_power,frame_rate_ms,move_rate_ms,jump_height,p_scale=0.24,interval_time_jump=100) -> None:
        self.walk_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/Run__00{0}.png",0,7,scale=p_scale)
        self.walk_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/Run__00{0}.png",0,7,flip=True,scale=p_scale)
        self.stay_r = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/IDLE_00{0}.png",0,7,scale=p_scale)
        self.stay_l = Auxiliar.getSurfaceFromSeparateFiles("images/caracters/enemies/IDLE_00{0}.png",0,7,flip=True,scale=p_scale)

        self.contador = 0
        self.frame = 0
        self.lives = 3
        self.score = 0
        self.move_x = 0
        self.move_y = 0
        self.speed_walk =  speed_walk
        self.speed_run =  speed_run
        self.gravity = gravity
        self.jump_power = jump_power
        self.animation = self.stay_r
        self.direction = DIRECTION_R
        self.image = self.animation[self.frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.collition_rect = pygame.Rect(x+self.rect.width/3,y,self.rect.width/3,self.rect.height)
        self.ground_collition_rect = pygame.Rect(self.collition_rect)
        self.ground_collition_rect.height = GROUND_COLLIDE_H
        self.ground_collition_rect.y = y + self.rect.height - GROUND_COLLIDE_H
        self.sonido_die = pygame.mixer.Sound(r"sounds\efectos\jump.wav")

        self.is_jump = False
        self.is_fall = False
        self.is_shoot = False
        self.is_knife = False

        self.tiempo_transcurrido_animation = 0
        self.frame_rate_ms = frame_rate_ms 
        self.tiempo_transcurrido_move = 0
        self.move_rate_ms = move_rate_ms
        self.y_start_jump = 0
        self.jump_height = jump_height

        self.tiempo_transcurrido = 0
        self.tiempo_last_jump = 0 # en base al tiempo transcurrido general
        self.interval_time_jump = interval_time_jump
        self.bullet_list = list()
   
    def change_x(self,delta_x):
        '''
        Actualiza la posición x del enemigo y sus rectángulos de colisión al moverlo horizontalmente.
        '''
        self.rect.x += delta_x
        self.collition_rect.x += delta_x
        self.ground_collition_rect.x += delta_x

    def change_y(self,delta_y):
        self.rect.y += delta_y
        self.collition_rect.y += delta_y
        self.ground_collition_rect.y += delta_y

    def do_movement(self,delta_ms,plataform_list):
        '''
        Gestiona el movimiento del enemigo. Cambia su dirección de movimiento de izquierda
        a derecha y viceversa después de un tiempo y hace que el enemigo caiga si no está
        en una plataforma.
        '''
        self.tiempo_transcurrido_move += delta_ms
        if self.tiempo_transcurrido_move >= self.move_rate_ms:
            self.tiempo_transcurrido_move = 0

            if not self.is_on_plataform(plataform_list):
                if self.move_y == 0:
                    self.is_fall = True
                    self.change_y(self.gravity)
            else:
                self.is_fall = False
                self.change_x(self.move_x)
                if self.contador <= 30:
                    self.move_x = -self.speed_walk
                    self.animation = self.walk_l
                    self.contador += 1
                elif self.contador <= 60:
                    self.move_x = self.speed_walk
                    self.animation = self.walk_r
                    self.contador += 1
                else:
                    self.contador = 0
    
    def is_on_plataform(self,plataform_list):
        '''
        Verifica si el enemigo está en una plataforma.
        '''
        retorno = False
        
        if(self.ground_collition_rect.bottom >= GROUND_LEVEL):
            retorno = True
        else:
            for plataforma in  plataform_list:
                if(self.ground_collition_rect.colliderect(plataforma.ground_collition_rect)):
                    retorno = True
                    break       
        return retorno          

    def do_animation(self,delta_ms):
        '''
        Controla la animación del enemigo, cambiando entre los cuadros de animación.
        '''
        self.tiempo_transcurrido_animation += delta_ms
        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            if(self.frame < len(self.animation) - 1):
                self.frame += 1 
            else: 
                self.frame = 0

    def update(self,delta_ms,plataform_list, lista_balas):
        '''
        Actualiza el enemigo, gestionando su movimiento y animación.
        '''
        self.do_movement(delta_ms, plataform_list)
        self.do_animation(delta_ms)
        self.tiempo_transcurrido += delta_ms
        if self.tiempo_transcurrido >= 1000:
            self.tiempo_transcurrido = 0
            self.shooting(lista_balas = lista_balas)

    def draw(self,screen):
        '''
        Dibuja el enemigo en la pantalla. Si DEBUG está habilitado, también
        dibuja rectángulos de colisión para fines de depuración.
        '''
        if(DEBUG):
            pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            pygame.draw.rect(screen,color=(255,255,0),rect=self.ground_collition_rect)
        
        self.image = self.animation[self.frame]
        screen.blit(self.image,self.rect)

    def receive_shoot(self):
        '''
        Reduce la vida del enemigo cuando recibe un disparo.
        '''
        self.lives -= 1
        if self.lives <= 1:
            self.sonido_die.play()
        
    def shooting(self, lista_balas):
        bullet_img = pygame.image.load(r'images\caracters\players\robot\Objects\Bullet_000.png').convert_alpha()
        bullet_img = pygame.transform.scale(bullet_img, (20, 20))
        
        if self.contador <= 40 :
            bullet = Bullet2(self.rect.centerx + (0.75 * self.rect.size[0] * -DIRECTION_R), self.rect.centery, -DIRECTION_R, bullet_img)
        else:
            bullet = Bullet2(self.rect.centerx + (0.75 * self.rect.size[0] * DIRECTION_R), self.rect.centery, DIRECTION_R, bullet_img)

        lista_balas.append(bullet)
        
    @staticmethod
    def generate_random_enemy():
        '''
        Un método estático que genera un enemigo con valores aleatorios para sus
        atributos, lo que permite crear enemigos aleatorios en el juego.
        '''
        x = random.randint(100, ANCHO_PANTALLA - 150)
        y = random.randint(0, 400)
        enemy= (Enemy(x=x,y=y,speed_walk=4,speed_run=5,gravity=14,jump_power=30,frame_rate_ms=150,move_rate_ms=50,jump_height=140,p_scale=0.24,interval_time_jump=300))
        return enemy

# fin enemigo