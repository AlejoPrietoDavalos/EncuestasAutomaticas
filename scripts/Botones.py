import pygame as pg
from scripts.COLORES import *

class Button:
    def __init__(self, win, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):    #poss va a ser una lista, en la posición 0 es la X y en la 1 es la Y.
        self.win = win

        self.poss_boton = poss_boton    #poss_boton = [poss_boton_x, poss_boton_y]
        self.text = text        #Texto que va a contener el botón
        self.fuente = pg.font.SysFont("Arial", tamaño_fuente)
        self.dim_texto = self.fuente.size(self.text)    # Calculamos la cantidad de pixeles que va a ocupar el texto 
        margen = 5          #Margen entre el texto y los bordes del boton


        self.poss_texto = [poss_boton[0] + margen, poss_boton[1] + margen]
        self.dim_boton = [self.dim_texto[0] + 2*margen, self.dim_texto[1] + 2*margen]      #dim = Lo voy a calcular como el Ancho y alto del texto, agregando algunos pixeles de margen
        
        
        
        self.color_texto_out = color_texto_out  #Color del texto cuando el mouse está FUERA del botón
        self.color_texto_up = color_texto_up    #Color del texto cuando el mouse está ENCIMA del botón
        self.color_boton_out = color_boton_out  #Color del boton cuando el mouse está FUERA del botón
        self.color_boton_up = color_boton_up    #Color del boton cuando el mouse está ENCIMA del botón

        self.mouse_up = False   # Con esto vamos a saber si la persona tiene el mouse arriba del botón o no.

    def InsertarBoton(self):
        self.MouseUp()
        texto = self.fuente.render(self.text , True , self.color_texto_out)
        if self.mouse_up:
            pg.draw.rect(self.win.ventana, self.color_boton_up, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]])
        else:
            pg.draw.rect(self.win.ventana, self.color_boton_out, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]])
        self.win.ventana.blit(texto, (self.poss_texto[0], self.poss_texto[1]))

    def MouseUp(self):
        '''Devuelve True si el mouse está arriba del botón.
        Devuelve False si el mouse está fuera del botón.'''

        if self.poss_boton[0] <= self.win.mouse[0] <= self.poss_boton[0]+self.dim_boton[0] and self.poss_boton[1] <= self.win.mouse[1] <= self.poss_boton[1]+self.dim_boton[1]: 
            self.mouse_up = True
        else:
            self.mouse_up = False


class Button_CambiarVentana(Button):
    def __init__(self, win, poss_boton, text, NuevaVentana, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, text, tamaño_fuente, color_texto_out, color_texto_up, color_boton_out, color_boton_up)
        self.NuevaVentana = NuevaVentana
    

    def EventosCambiarVentana(self):
        if self.mouse_up:
            self.win.CambiarDeVentana(self.NuevaVentana)


class Button_ListaDesplegable():
    def __init__(self, win, poss_boton, Listado, tamaño_fuente, color_texto_out=GRIS_CLARO, color_texto_up=WHITE, color_boton_out=VIOLETA_OSCURO, color_boton_up=VIOLETA_CLARO):
        self.win = win
        self.Listado = Listado
        
        self.fuente = pg.font.SysFont("Arial", tamaño_fuente)
        Ancho_Max = 0
        Alto_Max = 0
        margen = 5
        self.mouse_up_contraido = False
        self.mouse_up_desplegado = []
        self.poss_botones = []
        self.poss_textos = []
        for i in range(len(self.Listado)):
            if self.fuente.size(Listado[i])[0]>Ancho_Max:
                Ancho_Max = self.fuente.size(Listado[i])[0]
            if self.fuente.size(Listado[i])[1]>Alto_Max:
                Alto_Max = self.fuente.size(Listado[i])[1]
            self.mouse_up_desplegado.append(False)

        
        self.dim_texto = [Ancho_Max, Alto_Max]
        self.dim_boton = [Ancho_Max + 2*margen, Alto_Max + 2*margen]    # La lista desplegable van a ser N botones, uno abajo del otro 

        for i in range(len(self.Listado)):
            self.poss_botones.append([poss_boton[0], poss_boton[1] + i*self.dim_boton[1]])
            self.poss_textos.append([poss_boton[0]+margen, poss_boton[1]+margen + i*self.dim_boton[1]])


        self.color_texto_out = color_texto_out
        self.color_texto_up = color_texto_up
        self.color_boton_out = color_boton_out
        self.color_boton_up = color_boton_up

        self.ListadoDesplegado = False  # Cuando sea True, se despliega el listado, y cuando es False se muestra el valor seleccionado en 1 solo botón.
        self.Valor = Listado[0]

        
    def EventosListaDesplegable(self):      # Este evento hay que ponerlo dentro del evento "MOUSEBUTTONDOWN"
        if not(self.ListadoDesplegado):
            if self.mouse_up_contraido:
                self.ListadoDesplegado = True
        else:
            for i in range(len(self.Listado)):
                if self.mouse_up_desplegado[i] == True:
                    self.Valor = self.Listado[i]
                    self.ListadoDesplegado = False
                    

    def InsertarBoton(self):
        self.MouseUp()
        if not(self.ListadoDesplegado):     # Cuando no esté el listado desplegado, tenemos que renderizar un botón con la opción seleccionada
            if self.mouse_up_contraido:
                texto = self.fuente.render(self.Valor, True, self.color_texto_up)
                pg.draw.rect(self.win.ventana, self.color_boton_up, [self.poss_botones[0][0], self.poss_botones[0][1], self.dim_boton[0], self.dim_boton[1]])
            else:
                texto = self.fuente.render(self.Valor, True, self.color_texto_out)
                pg.draw.rect(self.win.ventana, self.color_boton_out, [self.poss_botones[0][0], self.poss_botones[0][1], self.dim_boton[0], self.dim_boton[1]])
            self.win.ventana.blit(texto, (self.poss_textos[0][0], self.poss_textos[0][1]))
        else:
            for i in range(len(self.Listado)):
                if self.mouse_up_desplegado[i]:
                    texto = self.fuente.render(self.Listado[i], True, self.color_texto_up)
                    btn = pg.draw.rect(self.win.ventana, self.color_boton_up, [self.poss_botones[i][0], self.poss_botones[i][1], self.dim_boton[0], self.dim_boton[1]])
                else:
                    texto = self.fuente.render(self.Listado[i], True, self.color_texto_out)
                    btn = pg.draw.rect(self.win.ventana, self.color_boton_out, [self.poss_botones[i][0], self.poss_botones[i][1], self.dim_boton[0], self.dim_boton[1]])
                self.win.ventana.blit(texto, (self.poss_textos[i][0], self.poss_textos[i][1]))


    def MouseUp(self):
        if not(self.ListadoDesplegado):
            if self.poss_botones[0][0] <= self.win.mouse[0] <= self.poss_botones[0][0]+self.dim_boton[0] and self.poss_botones[0][1] <= self.win.mouse[1] <= self.poss_botones[0][1]+self.dim_boton[1]:
                self.mouse_up_contraido = True
            else:
                self.mouse_up_contraido = False
        else:
            for i in range(len(self.Listado)):
                if self.poss_botones[i][0] <= self.win.mouse[0] <= self.poss_botones[i][0]+self.dim_boton[0] and self.poss_botones[i][1] <= self.win.mouse[1] <= self.poss_botones[i][1]+self.dim_boton[1]:
                    self.mouse_up_desplegado[i] = True
                else:
                    self.mouse_up_desplegado[i] = False


class EntryText():
    def __init__(self, win, poss_boton, ancho_boton, tamaño_fuente, color_texto_sin_escribir=BLACK, color_texto_escribiendo=BLACK, color_boton_sin_escribir=VERDE_UNAHUR, color_boton_escribiendo=VERDE_UNAHUR_CLARO):
        self.win = win
        self.poss_boton = poss_boton
        self.ancho_boton = ancho_boton      # El ancho va a ser fijo, por que es cuanto texto voy a querer yo mostrar.
        margen = 5                          # Margen entre el texto y los bordes del boton.
        self.poss_texto = [poss_boton[0] + margen, poss_boton[1] + margen]
        self.dim_boton = [ancho_boton, tamaño_fuente + margen]
        

        self.color_texto_sin_escribir = color_texto_sin_escribir  # Color del texto cuando no está escribiendo.
        self.color_texto_escribiendo = color_texto_escribiendo    # Color del texto cuando está escribiendo.
        self.color_boton_sin_escribir = color_boton_sin_escribir  # Color del texto cuando no está escribiendo.
        self.color_boton_escribiendo = color_boton_escribiendo    # Color del texto cuando está escribiendo.

        self.fuente = pg.font.SysFont("Arial", tamaño_fuente)
        self.text = ""                      # Texto que va a contener el botón

        self.mouse_up = False
        self.esta_escribiendo = False


    def InsertarBoton(self):
        if not(self.esta_escribiendo):
            texto = self.fuente.render(self.text , True , self.color_texto_sin_escribir)
            pg.draw.rect(self.win.ventana, self.color_boton_sin_escribir, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]])
        else:
            texto = self.fuente.render(self.text , True , self.color_texto_escribiendo)
            pg.draw.rect(self.win.ventana, self.color_boton_escribiendo, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]])
        self.win.ventana.blit(texto, (self.poss_texto[0], self.poss_texto[1]))


    def EventosClick_EntryText(self):   # Poner dentro del "if" cuando hay un evento de click.
        self.MouseUp()
        if self.mouse_up and not(self.esta_escribiendo):    # Si el mouse está arriba y no está escribiendo.
            self.esta_escribiendo = True
        elif self.esta_escribiendo:
            self.esta_escribiendo = False


    def EventosTeclas_EntryText(self, event):
        if self.esta_escribiendo and event.key == pg.K_RETURN:
            self.esta_escribiendo = False
        elif self.esta_escribiendo and event.key == pg.K_BACKSPACE:
            self.text = self.text[:-1]      # Le borro el último caracter
        elif self.esta_escribiendo:
            self.text += event.unicode


    def MouseUp(self):
        if self.poss_boton[0] <= self.win.mouse[0] <= self.poss_boton[0]+self.dim_boton[0] and self.poss_boton[1] <= self.win.mouse[1] <= self.poss_boton[1]+self.dim_boton[1]: 
            self.mouse_up = True
        else:
            self.mouse_up = False




'''
class Button_CheckButton(Button):
    def __init__(self, win, poss_boton, text, Valor_True, Valor_False, Valor_Inicial, Color_Borde_True=WHITE, color_texto_out=GRIS_CLARO, color_texto_up=WHITE, color_boton_out=VIOLETA_OSCURO, color_boton_up=VIOLETA_CLARO, tipo_fuente=FUENTE_MINECRAFT, tamaño_fuente=15):
        super().__init__(win, poss_boton, text, color_texto_out, color_texto_up, color_boton_out, color_boton_up, tipo_fuente, tamaño_fuente)
        self.Valores_Posibles = {
            True : Valor_True,
            False : Valor_False
            }
        
        self.color_borde_true = Color_Borde_True
        self.Valor = Valor_Inicial   # Esto va a almacenar el valor booleano que va a tener, y si quisiera el valor tendría que buscarlo del diccionario.
    

    def EventosCheckButton(self):
        if self.mouse_up:
            self.CambiarValor()


    def InsertarBoton(self):
        self.MouseUp()
        if self.mouse_up:
            texto = self.fuente.render(self.text , True , self.color_texto_up)
            pg.draw.rect(self.win.ventana, self.color_boton_up, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]])
        else:
            texto = self.fuente.render(self.text , True , self.color_texto_out)
            pg.draw.rect(self.win.ventana, self.color_boton_out, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]])
        
        if self.Valor == True:  # Si el botón está marcado que dibuje un borde.
            pg.draw.rect(self.win.ventana, self.color_borde_true, [self.poss_boton[0], self.poss_boton[1], self.dim_boton[0], self.dim_boton[1]], 3)
        
        self.win.ventana.blit(texto, (self.poss_texto[0], self.poss_texto[1]))


    def CambiarValor(self):          # Esta función va a cambiar el valor del booleano, para asi acceder al otro elemento del diccionario.
        self.Valor = not(self.Valor)
        ############## HACER ALGO CON LA ANIMACIÓN QUE SE MUESTRA DEL BOTON CUANDO ESTÁ EN TRUE
    
    
    def GetValue(self):
        return self.Valores_Posibles[self.Valor]


class Button_RadioButton():     # Vamos a hacerla de cero copiando algunas funcionalidades, por q tenemos q trabajar con un grupo de objetos.
    #poss_boton, y text van a ser listas, una para cada botón. Luego el resto de propiedades como, dim_texto, poss_texto, dim_boton, mouse_up también lo serán.
    #El texto que van a almacenar cuando sean oprimidos estos botones, es el contenido del texto de cada botón.
    #Cuando se quiera crear un conjunto de radiobuttons, crear una sub-clase de ésta para que Lista_Objetos sea única de ese conjunto de objetos.

    def __init__(self, win, poss_boton, text, Indice_Inicial, color_borde_true=RED, color_texto_out=GRIS_CLARO, color_texto_up=WHITE, color_boton_out=VIOLETA_OSCURO, color_boton_up=VIOLETA_CLARO, tipo_fuente=FUENTE_MINECRAFT, tamaño_fuente=15):
        self.win = win

        self.color_borde_true = color_borde_true
        self.poss_boton = poss_boton    #poss_boton = [[poss_boton_x_1, poss_boton_y_1] ,[poss_boton_x_2, poss_boton_y_2], ....., [poss_boton_x_n, poss_boton_y_n]] 
        self.text = text                #text = [text_1, text_2, ....., text_n]
        
        self.fuente = pg.font.Font(tipo_fuente, tamaño_fuente)  #La misma fuente para todos.
        

        margen = 5          #Margen entre el texto y los bordes del boton

        
        # Calculamos la cantidad de pixeles que va a ocupar el texto.
        self.dim_texto = []
        self.poss_texto = []
        self.dim_boton = []
        self.mouse_up = []
        
        for i in range(len(self.text)):
            self.dim_texto.append(self.fuente.size(self.text[i]))
            self.poss_texto.append( [poss_boton[i][0] + margen, poss_boton[i][1] + margen])
            self.dim_boton.append( [self.dim_texto[i][0] + 2*margen, self.dim_texto[i][1] + 2*margen] )      #dim = Lo voy a calcular como el Ancho y alto del texto, agregando algunos pixeles de margen
            self.mouse_up.append(False)     # Con esto vamos a saber si la persona tiene el mouse arriba del botón o no.
            
        


        self.color_texto_out = color_texto_out  #Color del texto cuando el mouse está FUERA del botón
        self.color_texto_up = color_texto_up    #Color del texto cuando el mouse está ENCIMA del botón
        self.color_boton_out = color_boton_out  #Color del boton cuando el mouse está FUERA del botón
        self.color_boton_up = color_boton_up    #Color del boton cuando el mouse está ENCIMA del botón

        self.Indice_Valor = Indice_Inicial
        self.Valor = self.text[self.Indice_Valor]


    def EventosRadioButtons(self):          # Este evento hay que ponerlo dentro del evento "MOUSEBUTTONDOWN"
        for i in range(len(self.text)):
            if self.mouse_up[i]:
                self.CambiarValor(i)


    def InsertarBoton(self):
        self.MouseUp()
        for i in range(len(self.text)):
            if self.mouse_up[i]:
                texto = self.fuente.render(self.text[i] , True , self.color_texto_up)
                pg.draw.rect(self.win.ventana, self.color_boton_up, [self.poss_boton[i][0], self.poss_boton[i][1], self.dim_boton[i][0], self.dim_boton[i][1]])
            else:
                texto = self.fuente.render(self.text[i] , True , self.color_texto_out)
                pg.draw.rect(self.win.ventana, self.color_boton_out, [self.poss_boton[i][0], self.poss_boton[i][1], self.dim_boton[i][0], self.dim_boton[i][1]])
            
            if self.Indice_Valor == i:  # Si el botón está marcado que dibuje un borde.
                pg.draw.rect(self.win.ventana, self.color_borde_true, [self.poss_boton[i][0], self.poss_boton[i][1], self.dim_boton[i][0], self.dim_boton[i][1]], 3)

            self.win.ventana.blit(texto, (self.poss_texto[i][0], self.poss_texto[i][1]))


    def MouseUp(self):
        #Devuelve True si el mouse está arriba del botón.
        #Devuelve False si el mouse está fuera del botón.
        for i in range(len(self.text)):
            if self.poss_boton[i][0] <= self.win.mouse[0] <= self.poss_boton[i][0]+self.dim_boton[i][0] and self.poss_boton[i][1] <= self.win.mouse[1] <= self.poss_boton[i][1]+self.dim_boton[i][1]: 
                self.mouse_up[i] = True
            else:
                self.mouse_up[i] = False
    




    def CambiarValor(self, i):
        self.Indice_Valor = i
        self.Valor = self.text[self.Indice_Valor]




class Button_Sprite():      # Es una imágen botón, cuando se presiona hará algo.
    def __init__(self, win, poss_boton, dir_img_clara, dir_img_oscura):
        self.win = win
        self.poss_boton = poss_boton
        self.dir_img_clara = dir_img_clara
        self.dir_img_oscura = dir_img_oscura
        
        self.img_boton_clara = pg.image.load(self.dir_img_clara)
        self.img_boton_oscura = pg.image.load(self.dir_img_oscura)
        
        self.dim_boton = [self.img_boton_clara.get_width(), self.img_boton_clara.get_height()]

        self.mouse_up = False
    
    
    def InsertarBoton(self):
        self.MouseUp()
        if self.mouse_up:
            self.win.ventana.blit(self.img_boton_clara, (self.poss_boton[0],self.poss_boton[1]))   #La introdusco en el origen de coordenadas.
        else:
            self.win.ventana.blit(self.img_boton_oscura, (self.poss_boton[0],self.poss_boton[1]))   #La introdusco en el origen de coordenadas.

    def MouseUp(self):
        if self.poss_boton[0] <= self.win.mouse[0] <= self.poss_boton[0]+self.dim_boton[0] and self.poss_boton[1] <= self.win.mouse[1] <= self.poss_boton[1]+self.dim_boton[1]: 
            self.mouse_up = True
        else:
            self.mouse_up = False


class Button_SpriteCambiarVentana(Button_Sprite):
    def __init__(self,win, poss_boton, dir_img_clara, dir_img_oscura, NuevaVentana):
        super().__init__(win, poss_boton, dir_img_clara, dir_img_oscura)
        self.NuevaVentana = NuevaVentana
    
    def EventosCambiarVentana(self):
        if self.mouse_up:
            self.win.CambiarDeVentana(self.NuevaVentana)






'''


