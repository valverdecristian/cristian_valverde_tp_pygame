import pygame
from pygame.locals import*
from GUI_form import*
from GUI_textbox import*
from GUI_label import*
from GUI_button import*
from GUI_slider import*
from GUI_button_image import*
from GUI_form_menu_score import*
from GUI_forms_menu_play import*
from nivel import*
import sqlite3
from constantes import *


class FormPrincipal(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border = "Black", border_size = -1, active = True)->None:
        super().__init__( screen, x, y, w, h, color_background, color_border , border_size , active)

        self.volumen = 0.2
        self.flag_play = True
        self.flag_sql = True
        

        pygame.mixer.init()

        ############ CONTROLES ######
      
        self.txtbox = TextBox(self._slave,x,y,350,150,160,50,(70,59,59),"White","Black",(70,59,59),2,font= "Comic Sans",font_size=15,font_color="Black")
      
        self.btn_select_level = Button(self._slave,x,y,350,220,160,60,(70,59,59),"Blue",self.btn_jugar_click,"Nombre","SELECT LEVELS",font="Verdana",font_size=15,font_color="White")
        self.btn_ranking =Button(self._slave,x,y,350,320,100,60,(70,59,59),"Blue",self.btn_tabla_click,"Nombre","RANKING",font="Verdana",font_size=15,font_color="White")
        self.btn_sound = Button(self._slave,x,y,350,410,160,60,(70,59,59),"Blue",self.btn_play_click,"Nombre","Pause music",font="Verdana",font_size=15,font_color="White")
        
        self.slider_volumen = Slider(self._slave,x,y,200,490,500,15,self.volumen,(70,59,59),"White")
        self.label_volumen = Label(self._slave, 750, 470, 100, 50 ,"20%","Comic Sans",15,"White",r"images/menu/boton-de-volumen.png" )


        # AGRERGARLOS A LA LISTA
        self.lista_de_botones.append(self.txtbox)
        self.lista_de_botones.append(self.btn_sound)
        self.lista_de_botones.append(self.label_volumen)
        self.lista_de_botones.append(self.slider_volumen)
        self.lista_de_botones.append(self.btn_ranking)
        self.lista_de_botones.append(self.btn_select_level)
        
        # agregar sonido
        pygame.mixer.music.load(r"sounds/ambiente/ambiente.wav")
        pygame.mixer.music.set_volume(self.volumen)
        pygame.mixer.music.play(-1)

        self.render()

    def update(self,lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()

                for widget in self.lista_de_botones:
                    widget.update(lista_eventos)
            self.upadte_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)


    def render(self):
        if isinstance(self._color_background, str):
            self._slave.fill(pygame.Color(self._color_background))
        else:
            self._slave.blit(self._color_background, (0, 0))
            
        for widget in self.lista_de_botones:
            widget.draw()


    def btn_play_click(self,texto):
       
        if self.flag_play:
            pygame.mixer.music.pause()
            self.btn_sound._color_background = (105,87,87)
            self.btn_sound._font_color = "Red"
            self.btn_sound.set_text("Play music")
        else:
            pygame.mixer.music.unpause()
            self.btn_sound._color_background = "Red"
            self.btn_sound._font_color = "White"
            self.btn_sound.set_text("Pause music")

        self.flag_play = not self.flag_play

    def upadte_volumen(self,lista_eventos):
        self.volumen = self.slider_volumen.value
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)

    def btn_jugar_click(self,param):
        nombre = self.txtbox.get_text()

        

        if len(nombre) > 0:
            form_jugar = FormMenuPlay(screen=self._master,
                                    x= self._master.get_width() / 2 - 250,
                                    y= self._master.get_height() / 2 - 250,
                                    w= 500,
                                    h= 500,
                                    color_background= (220,0,220),
                                    color_border= (255,255,255),
                                    active= True,
                                    path_image= r'images\menu\levels.png')
            

            banderas = {
                "nivel_1": {
                    "terminado": False,
                    "reset": False
                },
                "nivel_2": {
                    "terminado": False,
                    "reset": False
                },
                "nivel_3": {
                    "terminado": False,
                    "reset": False
                }
            }

            crear_banderas(banderas)
            
            self.show_dialog(form_jugar)
        # CREAMOS BD
        if self.flag_sql == True:

            with sqlite3.connect("mi_base_de_datos.db") as conexion:
                # CREAR TABLA--------------------------
                try:
                    sentencia = 'CREATE TABLE Ranking (nombre text, score integer)'
                    conexion.execute(sentencia)
                    print("Tabla creada")

                except Exception as e:
                    print(f"Error en Base de datos {e}")


            self.flag_sql = False

    def btn_tabla_click(self,texto):
        nombre = self.txtbox.get_text() # insert nombre
        ultimo_score = list()
        
        # ACCEDO AL ULTIMO SCORE
        archivo = open("score.txt","r")
        for linea in archivo:
            ultimo_score.append(linea)
        archivo.close()
            
        # INSERTO EN BD
        with sqlite3.connect("mi_base_de_datos.db") as conexion:
            print("Conexión a la base de datos establecida")
            try:
                print("entre",nombre,ultimo_score[0])
                sentencia = 'insert into Ranking (nombre, score) values(?,?)'
                conexion.execute(sentencia, (nombre, ultimo_score[0]))
                conexion.commit()
                print("Sentencia ejecutada correctamente")  # Agrega esta línea para verificar la ejecución


            except Exception as e:
                print(f"Error en Base de datos {e}")


        dic_score = list()

        with sqlite3.connect("mi_base_de_datos.db") as conexion:
            try:
              
                sentencia = '''
                            select * from Ranking order by score desc limit 3
                            '''
                cursor = conexion.execute(sentencia)
                for fila in cursor:
                    print("select")
                    dic_score.append({"jugador" : f"{fila[0]}","Score":f"{fila[1]}"},)
                print("Tabla creada")
            except Exception as e:
                print(f"Error en Base de datos {e}")

        form_puntaje = FormMenuScore(self._master,300,50,500,500,(220,0,220),"white",True,r'images\API_forms2\Window.png',dic_score,100,10,10)
        self.show_dialog(form_puntaje)