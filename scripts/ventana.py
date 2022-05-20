import pygame as pg
import sys, os, time

class Ventana():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.ventana = pg.display.set_mode((1366,768))
        pg.display.set_caption("Encuestas Automáticas UNAHUR - Asuntos Docentes")
        self.IMG_FONDO = pg.image.load("fondoUNAHUR.jpg").convert()
        self.FPS = 30
        self.RELOJ = pg.time.Clock()


        self.run = True
        self.Ventanas_Posibles = {
            "Menu" : True,
            "Por Docente" : False
        }

        self.mouse = None   
    

    def InsertarImgFondo(self):
        self.ventana.blit(self.IMG_FONDO, (0,0))
    

    def CerrarPrograma(self):
        self.run = False
        try:    # Para tener una salida épica.
            sound = pg.mixer.Sound("Audio Fin Ejecucion/You Shall Not Pass.mp3")
            sound.play()
            time.sleep(5)
        except:
            pass
        
        pg.quit()
        sys.exit()


    def CambiarDeVentana(self, Nueva_Ventana):
        for key in list(self.Ventanas_Posibles.keys()):
            self.Ventanas_Posibles[key] = False
        self.Ventanas_Posibles[Nueva_Ventana] = True
    
    
    def ActualizarPulsacionControles(self):  # Esto se va a encargar de actualizar todas las variables que afectan a los eventos del juego.
        self.mouse = pg.mouse.get_pos()