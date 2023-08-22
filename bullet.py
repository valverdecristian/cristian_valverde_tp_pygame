from constantes import *

class Bullet2:
    def __init__(self, x, y, direction, image_bullet):
        '''
        Inicializa una instancia de la clase Bullet2.

        Parámetros:
        x (int): La coordenada x inicial de la bala.
        y (int): La coordenada y inicial de la bala.
        direction (int): Dirección de la bala (1 para derecha, -1 para izquierda).
        image_bullet (Surface): La imagen de la bala.

        Atributos:
        x (int): La coordenada x actual de la bala.
        y (int): La coordenada y actual de la bala.
        velocidad (int): La velocidad de movimiento de la bala.
        image (Surface): La imagen de la bala.
        rect (Rect): El rectángulo que rodea la imagen de la bala.
        direction (int): La dirección de la bala.
        '''
        self.x = x
        self.y = y
        self.velocidad = 10
        self.image = image_bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self, nivel_actual, player, enemy_list, bullet_list):
        '''
        Actualiza la posición y verifica colisiones de la bala.

        Parámetros:
        nivel_actual (Level): El nivel actual del juego.
        player (Player): El jugador en el juego.
        enemy_list (list): Lista de enemigos en el nivel.
        bullet_list (list): Lista de balas en el juego.
        '''
        self.x += (self.direction * self.velocidad)
        self.rect.x = self.x

        if self.x < 0 or self.x > ANCHO_PANTALLA:
            if self in bullet_list:
                bullet_list.remove(self)

        for obstacle in nivel_actual.plataform_list:
            if self.rect.colliderect(obstacle.rect) and self in bullet_list:
                 if self in bullet_list:
                    bullet_list.remove(self)

        for bullet in bullet_list:
            if bullet != self and self.rect.colliderect(bullet.rect):
                if self in bullet_list:
                    bullet_list.remove(self)

        if player.rect.colliderect(self.rect):
            if player.lives > 0:
                player.lives -= 1
                if self in bullet_list:
                    bullet_list.remove(self)

        for enemy in enemy_list:
            if enemy.rect.colliderect(self.rect):
                if enemy.lives > 0:
                    enemy.lives -= 1
                if enemy.lives == 0:
                    player.score += 200
                    enemy_list.remove(enemy)
                if self in bullet_list:
                    bullet_list.remove(self)

    def draw(self, pantalla):
        '''
        Dibuja la bala en la pantalla.

        Parámetros:
        pantalla (Surface): La superficie de la pantalla en la que se dibujará la bala.
        '''
        pantalla.blit(self.image, self.rect)