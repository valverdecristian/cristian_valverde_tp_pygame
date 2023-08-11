from player import *
from constantes import *
from auxiliar import Auxiliar
from enemigo import Enemy
import math

class Bullet():
    '''
    Representa una bala en el juego que puede ser disparada por diferentes entidades.

    Args:
        owner: La entidad propietaria que dispara la bala.
        x_init (int): La coordenada x inicial de la bala.
        y_init (int): La coordenada y inicial de la bala.
        x_end (int): La coordenada x final de la bala.
        y_end (int): La coordenada y final de la bala.
        speed (int): La velocidad de la bala.
        path (str): La ruta de la imagen de la bala.
        frame_rate_ms (int): La tasa de cuadro de la animación de la bala.
        move_rate_ms (int): La tasa de movimiento de la bala.
        width (int, opcional): El ancho de la imagen de la bala. Por defecto es 5.
        height (int, opcional): El alto de la imagen de la bala. Por defecto es 5.
    '''
    def __init__(self,owner,x_init,y_init,x_end,y_end,speed,path,frame_rate_ms,move_rate_ms,width=5,height=5) -> None:
        self.tiempo_transcurrido_move = 0
        self.tiempo_transcurrido_animation = 0
        self.image = pygame.image.load(path).convert()
        self.image = pygame.transform.scale(self.image,(width,height))
        self.rect = self.image.get_rect()
        self.x = x_init
        self.y = y_init
        self.owner = owner
        self.rect.x = x_init
        self.rect.y = y_init
        self.frame_rate_ms = frame_rate_ms
        self.move_rate_ms = move_rate_ms
        angle = math.atan2(y_end - y_init, x_end - x_init) #Obtengo el angulo en radianes
        print('El angulo engrados es:', int(angle*180/math.pi))

        self.move_x = math.cos(angle)*speed
        self.move_y = math.sin(angle)*speed
        
        self.is_active = True 
   
    def change_x(self,delta_x):
        '''
        Cambia la coordenada x de la bala.

        Args:
            delta_x (int): Cambio en la coordenada x.
        '''
        self.x = self.x + delta_x
        self.rect.x = int(self.x)   

    def change_y(self,delta_y):
        '''
        Cambia la coordenada y de la bala.

        Args:
            delta_y (int): Cambio en la coordenada y.
        '''
        self.y = self.y + delta_y
        self.rect.y = int(self.y)

    def do_movement(self,delta_ms,plataform_list,enemy_list,player):
        '''
        Realiza el movimiento de la bala en función de su velocidad.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
            plataform_list (list): Lista de plataformas en el juego.
            enemy_list (list): Lista de enemigos en el juego.
            player (Player): Jugador en el juego.
        '''
        self.tiempo_transcurrido_move += delta_ms
        if(self.tiempo_transcurrido_move >= self.move_rate_ms):
            self.tiempo_transcurrido_move = 0
            self.change_x(self.move_x)
            self.change_y(self.move_y)
            self.check_impact(plataform_list,enemy_list,player)

    def do_animation(self,delta_ms):
        '''
        Realiza la animación de la bala en función de la tasa de cuadro.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
        '''
        self.tiempo_transcurrido_animation += delta_ms
        if(self.tiempo_transcurrido_animation >= self.frame_rate_ms):
            self.tiempo_transcurrido_animation = 0
            pass
    
    def check_impact(self, plataform_list, enemy_list, player):
        '''
        Verifica si la bala colisiona con plataformas, enemigos o el jugador.

        Args:
            plataform_list (list): Lista de plataformas en el juego.
            enemy_list (list): Lista de enemigos en el juego.
            player (Player): Jugador en el juego.
        '''
        if self.is_active and self.owner != player and self.rect.colliderect(player.rect):
            print("IMPACTO PLAYER")
            player.receive_shoot()
            self.is_active = False
        for aux_enemy in enemy_list:
            if self.is_active and self.owner != aux_enemy and self.rect.colliderect(aux_enemy.rect):
                print("IMPACTO ENEMY")
                self.is_active = False
                new_enemy = Enemy.generate_random_enemy()
                enemy_list.append(new_enemy)

    def update(self,delta_ms,plataform_list,enemy_list,player):
        '''
        Actualiza el movimiento, animación y colisión de la bala.

        Args:
            delta_ms (int): Tiempo transcurrido desde la última actualización en milisegundos.
            plataform_list (list): Lista de plataformas en el juego.
            enemy_list (list): Lista de enemigos en el juego.
            player (Player): Jugador en el juego.
        '''
        self.do_movement(delta_ms,plataform_list,enemy_list,player)
        
        self.do_animation(delta_ms) 

    def draw(self,screen):
        '''
        Dibuja la bala en la pantalla si está activa.

        Args:
            screen: Superficie de la pantalla donde se dibujará la bala.
        '''
        if(self.is_active):
            if(DEBUG):
                pygame.draw.rect(screen,color=(255,0 ,0),rect=self.collition_rect)
            screen.blit(self.image,self.rect)