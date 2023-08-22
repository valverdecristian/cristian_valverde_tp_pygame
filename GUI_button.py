import pygame
from pygame.locals import *
from GUI_widget import Widget

class Button(Widget):
    '''
    Representa un botón interactivo con una imagen y texto en una interfaz gráfica.

    Parámetros:
    screen (Surface): La superficie de pantalla en la que se dibujará el botón.
    master_x (int): Coordenada x del widget principal que contiene el botón.
    master_y (int): Coordenada y del widget principal que contiene el botón.
    x (int): Coordenada x del botón en su widget principal.
    y (int): Coordenada y del botón en su widget principal.
    w (int): Ancho del botón.
    h (int): Altura del botón.
    path_image (str): Ruta de la imagen que se utilizará para el botón.
    onclick (function, opcional): Función que se ejecutará cuando se haga clic en el botón.
    onclick_param (object, opcional): Parámetro que se pasará a la función onclick.
    text (str, opcional): Texto que se mostrará en el botón.
    font (str, opcional): Fuente del texto.
    font_size (int, opcional): Tamaño de la fuente del texto.
    font_color (str o tuple, opcional): Color del texto en formato de cadena o tupla RGB.
    color_background (tuple, opcional): Color de fondo del botón en formato de tupla RGB.
    color_border (str o tuple, opcional): Color del borde del botón en formato de cadena o tupla RGB.
    border_size (int, opcional): Tamaño del borde del botón.

    Atributos:
    _onclick (function): Función que se ejecutará cuando se haga clic en el botón.
    _onclick_param (object): Parámetro que se pasará a la función onclick.
    _text (str): Texto que se mostrará en el botón.
    _font (Font): Fuente del texto.
    _font_color (str o tuple): Color del texto en formato de cadena o tupla RGB.
    _master_x (int): Coordenada x del widget principal que contiene el botón.
    _master_y (int): Coordenada y del widget principal que contiene el botón.
    _slave (Surface): Imagen que se utilizará como imagen principal del botón.
    isclicked (bool): Indica si el botón ha sido clicado.
    contador_click (int): Contador para controlar la velocidad de clics.
    '''
    def __init__(self, screen,master_x,master_y, x,y,w,h,color_background,color_border, onclick, onclick_param, text, font, font_size, font_color):
        super().__init__(screen, x,y,w,h,color_background,color_border)
        
        pygame.font.init()
        
        self._onclick = onclick
        self._onclick_param = onclick_param
        self._text = text
        self._font = pygame.font.SysFont(font,font_size)
        self._font_color = font_color
        self._master_x = master_x
        self._master_y = master_y
        
        self.isclicked = False
        
        self.render()

    def render(self):
        '''
        Renderiza el botón con la imagen y el texto.
        '''
        image_text = self._font.render(self._text, True, self._font_color, self._color_background)
        
        self._slave = pygame.surface.Surface((self._w,self._h))#superficie que se adapte a la del boton
        self.slave_rect = self._slave.get_rect()
        
        self.slave_rect.x = self._x
        self.slave_rect.y = self._y
        
        self.slave_rect_collide = pygame.Rect(self.slave_rect)
        self.slave_rect_collide.x += self._master_x
        self.slave_rect_collide.y += self._master_y 
        
        
        self._slave.fill(self._color_background)
        
        media_texto_horizontal = image_text.get_width() / 2
        media_texto_vertical = image_text.get_height() / 2

        media_horizontal = self._w / 2
        media_vertical = self._h / 2

        diferencia_horizontal = media_horizontal - media_texto_horizontal 
        diferencia_vertical = media_vertical - media_texto_vertical
        
        self._slave.blit(image_text,(diferencia_horizontal,diferencia_vertical))
    
    def update(self, lista_eventos):
        '''
        Actualiza el estado del botón en función de los eventos.
        '''
        self.isclicked = False
        for evento in lista_eventos:
           if evento.type == pygame.MOUSEBUTTONDOWN:
               if self.slave_rect_collide.collidepoint(evento.pos):
                   self.isclicked = True
                   self._onclick(self._onclick_param)
                   break
        self.draw()
                    
    def set_text(self, text):
        self._text = text
        self.render()
