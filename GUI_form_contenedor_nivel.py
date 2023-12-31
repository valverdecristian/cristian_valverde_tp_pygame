import pygame
from pygame.locals import*
from GUI_form import*
from GUI_button_image import*
from GUI_form_fin import*
from Manejador_niveles import*

class FormContenedorNivel(Form):
    '''
    Inicia una instancia de la clase FormContenedorNivel.

        Parámetros:
        pantalla (pygame.Surface): La superficie de pantalla en la que se dibujará el formulario.
        nivel (ManejadorNiveles): Una instancia del manejador de niveles.

        Atributos:
        nivel (ManejadorNiveles): Una instancia del manejador de niveles.
        _btn_home (Button_Image): Un botón de imagen que representa un botón de "inicio".
        form_jugar (FormFin): Un formulario para el juego.
        lista_de_botones (list): Una lista que contiene los botones en el formulario.
    '''
    def __init__(self,pantalla:pygame.Surface,nivel):
        super().__init__(pantalla,0,0,pantalla.get_width(),pantalla.get_height(),color_background="Black")
   
        nivel._slave = self._master
        self.nivel = nivel

        self._btn_home = Button_Image(screen=self._master,
                                      master_x=self._x,
                                      master_y=self._y,
                                      x=self._w - 100,
                                      y=self._h - 100,
                                      w=50,
                                      h=50,
                                      onclick=self.btn_home_click,
                                      onclick_param="",
                                      path_image=r"images\API_forms2\home.png")
        
        dic = [{"clave": "pepe","punot":"cdcd"}]

        self.form_jugar = FormFin(self._master,690,205,500,550,(220,0,220),
                                 "white",True,r"images\API_forms2\home.png",
                                 dic,100,10,10)
        
        self.lista_de_botones.append(self._btn_home)

    def update(self,lista_eventos):
        '''
        Actualiza el formulario y sus elementos.

        Parámetros:
        lista_eventos (list): Una lista de eventos de pygame.
        '''
        self.nivel.update(lista_eventos)     
        self.draw()
        for widget in self.lista_de_botones:
            widget.update(lista_eventos)

        
    def draw(self):
        '''Dibuja el formulario y el nivel en la superficie maestra.'''
        self.nivel.draw(self._master)

    def btn_home_click(self,param):
        '''Maneja el evento de clic en el botón "inicio".'''
        self.end_dialog()