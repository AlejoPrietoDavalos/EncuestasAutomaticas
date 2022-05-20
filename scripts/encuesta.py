from uuid import RESERVED_FUTURE
import pygame as pg
import os
from scripts.N_CarpetasYColumnas import *
from scripts.PossDimElementos import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scripts.Botones import *
from scripts.func_encuesta import *
from threading import Thread

class Encuesta():
    Lista_Excels = os.listdir("Excel Profesores")
    
    def __init__(self, win):
        self.win = win
        self.excel = None            # Acá vamos a cargar el excel segun la hoja de datos y el nombre
        self.HojaInstitutoDocente = None
        self.NombreHojaInstitutoDocente = "Instituto Docentes Encuestados"  ############ Ponerlo en un entrytext o pedirle a nico q lo ponga por default.
        self.Cuatrimestre = "Segundo Cuatrimestre 2021"                     ############ Ponerlo en un entrytext

        self.HojaInstitutoCarrera = None
        self.NombreHojaInstitutoCarrera = "Instituto de Carrera"


        self.TipoEncuesta = {
            "Por Docente" : False
        }


        self.N_Col = {          # Guardamos el nombre de la columna en versión corta.
            "DNI" : "DNI docentes",
            "Equipo Docente" : "equipo_doc",
            "Materia" : "Materia",
            "Cod" : "Cód_materia",
            "Cusaste Entera?" : "¿Cursaste la materia desde el principio hasta el final?",
            "Preg 1" : "¿Considerás que la forma en la cual el/la docente llevó adelante la materia fue adecuada para favorecer el aprendizaje?",
            "Preg 3" : "¿El/la docente desarrolló estrategias de enseñanza para que todos/as pudieran aprender?",
            "Preg 10" : "El/la profesor/a incluía material audiovisual que complementaba la bibliografía",
            "Preg 11" : "El/la profesor/a propuso  material de apoyo para comprender mejor la bibliografía (como guías de estudio, resúmenes, power points u otras lecturas complementarias)",
            "Preg 2" : "¿Hubo un seguimiento adecuado  de las necesidades educativas de los/as estudiantes  por parte del /la docente?",
            "Preg 12" : "Hubo canales para consultas y las mismas eran respondidas.",
            "Preg 4" : "¿Considerás que lo que fue evaluado fue acorde con lo que fue enseñado?",
            "Preg 5" : "¿Los criterios para evaluarte fueron claros?",
            "Preg 6" : "¿Se cumplió con el Régimen Académico de la UNAHUR (dos parciales como mínimo, recuperatorios, evaluación integradora)",
            "Preg 7" : "¿Se utilizó el campus virtual de UNAHUR?",
            "Preg 8" : "¿Se utilizaron otros entornos o herramientas digitales para desarrollar las clases? (Como por ejemplo: clases sincrónicas, encuentros de Zoom o meet,  laboratorios virtuales, entornos de programación o redes sociales)",
            "Preg 9.1" : "Si se utilizaron ¿Podrías indicar cuáles? - Opción: Redes sociales",
            "Preg 9.2" : "Si se utilizaron ¿Podrías indicar cuáles? - Opción: Clases o encuentros sincrónicas (zoom, meet, big blue botton)",
            "Preg 9.3" : "Si se utilizaron ¿Podrías indicar cuáles? - Opción: Laboratorios o simuladores virtuales",
            "Preg 9.4" : "Si se utilizaron ¿Podrías indicar cuáles? - Opción: Entornos de programación",
            "Preg 9.5" : "Si se utilizaron ¿Podrías indicar cuáles? - Opción: Whatsapp",
            "Preg 9.6" : "Si se utilizaron ¿Podrías indicar cuáles? - Opción: Otros",            
        }


        self.IndiceDocente = {}             # Vamos a guardar el DNI del docente como clave, y el índice donde aparece como valor en una lista.
        # Al empezar una nueva encuesta, tenemos que recorrer estos índices e ir guardando el valor de las respuestas.
        self.NombreDocente = {}             # Vamos a guardar el DNI del docente como clave, y el nombre de éste como valor.
        self.InstitutoDocente = {}          # Vamos a guardar el DNI del docente como clave, y el instituto al que pertenece el docente como valor.


        self.IndiceCarrera = {}             # Almacena el nombre de la carrera como clave, y el indice donde aparece como valor.
        self.InstitutoCarrera = {}          # Se almacena el instituto de cada carrera.


    def CalcularResEncuestaDocente(self, dni):     # Vamos a calcular el valor de cada una de las respuestas del docente.   
        ResEncuesta = [0]*42             # La posición de cada elemento esta definida en la hoja "Automatismo Alejo", estoy reciclando el codigo asi que esta medio feito.
        # Para hacer la encuesta necesito 42 variables que son todos los datos que se obtienen de la encuesta.
        MateriasDelDocente = []
        N_Filas = len(self.IndiceDocente[dni])

        ResEncuesta[0] = self.InstitutoDocente[dni]
        ResEncuesta[1] = self.NombreDocente[dni]
        ResEncuesta[2] = self.Cuatrimestre


        for i in self.IndiceDocente[dni]:   # Vamos a recorrer cada una de las filas donde aparece el docente.
            MateriasDelDocente.append(self.excel[self.N_Col["Materia"]][i])

            # Cuantos cursaron las materia de principio a fin.
            if self.excel[self.N_Col["Cusaste Entera?"]][i] == "Si":
                ResEncuesta[3] += 1
            else:
                ResEncuesta[4] += 1
            


            # Pregunta 1
            ResEncuesta[8] += self.excel[self.N_Col["Preg 1"]][i]    # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 1"]][i] < 4:
                ResEncuesta[5] += 1
            elif self.excel[self.N_Col["Preg 1"]][i] > 6:
                ResEncuesta[7] += 1
            else:
                ResEncuesta[6] += 1
            


            # Pregunta 3
            ResEncuesta[12] += self.excel[self.N_Col["Preg 3"]][i]   # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 3"]][i] < 4:
                ResEncuesta[9] += 1
            elif self.excel[self.N_Col["Preg 3"]][i] > 6:
                ResEncuesta[11] += 1
            else:
                ResEncuesta[10] += 1



            # Pregunta 10
            if self.excel[self.N_Col["Preg 10"]][i] == "Si":
                ResEncuesta[13] += 1
            else:
                ResEncuesta[14] += 1



            # Pregunta 11
            if self.excel[self.N_Col["Preg 11"]][i] == "Si":
                ResEncuesta[15] += 1
            else:
                ResEncuesta[16] += 1



            # Pregunta 2
            ResEncuesta[20] += self.excel[self.N_Col["Preg 2"]][i]   # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 2"]][i] < 4:
                ResEncuesta[17] += 1
            elif self.excel[self.N_Col["Preg 2"]][i] > 6:
                ResEncuesta[19] += 1
            else:
                ResEncuesta[18] += 1



            # Pregunta 12
            if self.excel[self.N_Col["Preg 12"]][i] == "Si":
                ResEncuesta[21] += 1
            else:
                ResEncuesta[22] += 1
            


            # Pregunta 4
            if self.excel[self.N_Col["Preg 4"]][i] == "Muy acorde":
                ResEncuesta[23] += 1
            elif self.excel[self.N_Col["Preg 4"]][i] == "Acorde":
                ResEncuesta[24] += 1
            else:
                ResEncuesta[25] += 1
            


            # Pregunta 5
            if self.excel[self.N_Col["Preg 5"]][i] == "Muy claro":
                ResEncuesta[26] += 1
            elif self.excel[self.N_Col["Preg 5"]][i] == "Claro":
                ResEncuesta[27] += 1
            else:
                ResEncuesta[28] += 1
            


            # Pregunta 6
            if self.excel[self.N_Col["Preg 6"]][i] == "Si":
                ResEncuesta[29] += 1
            else:
                ResEncuesta[30] += 1



            # Pregunta 7
            if self.excel[self.N_Col["Preg 7"]][i] == "Si, fue el entorno virtual donde se cursó la materia":
                ResEncuesta[31] += 1
            elif self.excel[self.N_Col["Preg 7"]][i] == "Se lo usó esporádicamente (cada tanto)":
                ResEncuesta[32] += 1
            else:
                ResEncuesta[33] += 1
            


            # Pregunta 8
            if self.excel[self.N_Col["Preg 8"]][i] == "Si":
                ResEncuesta[34] += 1
            else:
                ResEncuesta[35] += 1
            


            # Pregunta 9
            if self.excel[self.N_Col["Preg 9.1"]][i] != "":
                ResEncuesta[36] += 1
            if self.excel[self.N_Col["Preg 9.2"]][i] != "":
                ResEncuesta[37] += 1
            if self.excel[self.N_Col["Preg 9.3"]][i] != "":
                ResEncuesta[38] += 1
            if self.excel[self.N_Col["Preg 9.4"]][i] != "":
                ResEncuesta[39] += 1
            if self.excel[self.N_Col["Preg 9.5"]][i] != "":
                ResEncuesta[40] += 1
            if self.excel[self.N_Col["Preg 9.6"]][i] != "":
                ResEncuesta[41] += 1

        ResEncuesta[8] = ResEncuesta[8]/N_Filas
        ResEncuesta[12] = ResEncuesta[12]/N_Filas
        ResEncuesta[20] = ResEncuesta[20]/N_Filas

        return ResEncuesta, MateriasDelDocente


    def CrearEncuestasDocentes(self):
        Lista_Encuestas_No_Realizadas = []
        for dni in list(self.IndiceDocente.keys()):
            # Esta primera validación la hacemos por si el programa se cerró en plena ejecución, o tuvimos que hacerlo, y que no nos intente crear
            # de nuevo una encuesta que ya fue creada anteriormente.
            if not(f"{self.NombreDocente[dni]} - Encuesta {self.Cuatrimestre}.pdf" in os.listdir("PDF Profesores")):    # Si la encuesta no fue creada anteriormente, la crea.
                ResEncuesta, MateriasDelDocente = self.CalcularResEncuestaDocente(dni)
                HacerEncuesta(ResEncuesta, MateriasDelDocente)
        # Nos fijamos cuales no se hicieron
        if len(Lista_Encuestas_No_Realizadas)==0:
            print("\n- - - TODAS LAS ENCUESTAS FUERON CREADAS SIN ERRORES!!! - - -")
        else:
            print("\n--SE CREARON TODAS LAS ENCUESTAS A EXCEPCIÓN DE:")
            for i in range(len(Lista_Encuestas_No_Realizadas)):
                print(Lista_Encuestas_No_Realizadas[i])


    def CrearEncuestaCarrera(self):
        Lista_Encuestas_No_Realizadas = []
        for carrera in list(self.IndiceCarrera.keys()):
            ResEncuesta, MateriasDeLaCarrera = self.CalcularResEncuestaCarrera(carrera)
            HacerEncuesta(ResEncuesta, MateriasDeLaCarrera)


    def CalcularResEncuestaCarrera(self, carrera):
        ResEncuesta = [0]*42             # La posición de cada elemento esta definida en la hoja "Automatismo Alejo", estoy reciclando el codigo asi que esta medio feito.
        # Para hacer la encuesta necesito 42 variables que son todos los datos que se obtienen de la encuesta.
        MateriasDeLaCarrera = []
        N_Filas = len(self.IndiceCarrera[carrera])

        ResEncuesta[0] = self.InstitutoCarrera[carrera]
        ResEncuesta[1] = carrera
        ResEncuesta[2] = self.Cuatrimestre


        for i in self.IndiceCarrera[carrera]:   # Vamos a recorrer cada una de las filas donde aparece el docente.
            MateriasDeLaCarrera.append(self.excel[self.N_Col["Materia"]][i])

            # Cuantos cursaron las materia de principio a fin.
            if self.excel[self.N_Col["Cusaste Entera?"]][i] == "Si":
                ResEncuesta[3] += 1
            else:
                ResEncuesta[4] += 1
            


            # Pregunta 1
            ResEncuesta[8] += self.excel[self.N_Col["Preg 1"]][i]    # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 1"]][i] < 4:
                ResEncuesta[5] += 1
            elif self.excel[self.N_Col["Preg 1"]][i] > 6:
                ResEncuesta[7] += 1
            else:
                ResEncuesta[6] += 1
            


            # Pregunta 3
            ResEncuesta[12] += self.excel[self.N_Col["Preg 3"]][i]   # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 3"]][i] < 4:
                ResEncuesta[9] += 1
            elif self.excel[self.N_Col["Preg 3"]][i] > 6:
                ResEncuesta[11] += 1
            else:
                ResEncuesta[10] += 1



            # Pregunta 10
            if self.excel[self.N_Col["Preg 10"]][i] == "Si":
                ResEncuesta[13] += 1
            else:
                ResEncuesta[14] += 1



            # Pregunta 11
            if self.excel[self.N_Col["Preg 11"]][i] == "Si":
                ResEncuesta[15] += 1
            else:
                ResEncuesta[16] += 1



            # Pregunta 2
            ResEncuesta[20] += self.excel[self.N_Col["Preg 2"]][i]   # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 2"]][i] < 4:
                ResEncuesta[17] += 1
            elif self.excel[self.N_Col["Preg 2"]][i] > 6:
                ResEncuesta[19] += 1
            else:
                ResEncuesta[18] += 1



            # Pregunta 12
            if self.excel[self.N_Col["Preg 12"]][i] == "Si":
                ResEncuesta[21] += 1
            else:
                ResEncuesta[22] += 1
            


            # Pregunta 4
            if self.excel[self.N_Col["Preg 4"]][i] == "Muy acorde":
                ResEncuesta[23] += 1
            elif self.excel[self.N_Col["Preg 4"]][i] == "Acorde":
                ResEncuesta[24] += 1
            else:
                ResEncuesta[25] += 1
            


            # Pregunta 5
            if self.excel[self.N_Col["Preg 5"]][i] == "Muy claro":
                ResEncuesta[26] += 1
            elif self.excel[self.N_Col["Preg 5"]][i] == "Claro":
                ResEncuesta[27] += 1
            else:
                ResEncuesta[28] += 1
            


            # Pregunta 6
            if self.excel[self.N_Col["Preg 6"]][i] == "Si":
                ResEncuesta[29] += 1
            else:
                ResEncuesta[30] += 1



            # Pregunta 7
            if self.excel[self.N_Col["Preg 7"]][i] == "Si, fue el entorno virtual donde se cursó la materia":
                ResEncuesta[31] += 1
            elif self.excel[self.N_Col["Preg 7"]][i] == "Se lo usó esporádicamente (cada tanto)":
                ResEncuesta[32] += 1
            else:
                ResEncuesta[33] += 1
            


            # Pregunta 8
            if self.excel[self.N_Col["Preg 8"]][i] == "Si":
                ResEncuesta[34] += 1
            else:
                ResEncuesta[35] += 1
            


            # Pregunta 9
            if self.excel[self.N_Col["Preg 9.1"]][i] != "":
                ResEncuesta[36] += 1
            if self.excel[self.N_Col["Preg 9.2"]][i] != "":
                ResEncuesta[37] += 1
            if self.excel[self.N_Col["Preg 9.3"]][i] != "":
                ResEncuesta[38] += 1
            if self.excel[self.N_Col["Preg 9.4"]][i] != "":
                ResEncuesta[39] += 1
            if self.excel[self.N_Col["Preg 9.5"]][i] != "":
                ResEncuesta[40] += 1
            if self.excel[self.N_Col["Preg 9.6"]][i] != "":
                ResEncuesta[41] += 1

        ResEncuesta[8] = ResEncuesta[8]/N_Filas
        ResEncuesta[12] = ResEncuesta[12]/N_Filas
        ResEncuesta[20] = ResEncuesta[20]/N_Filas

        return ResEncuesta, MateriasDeLaCarrera


    def CrearEncuestaGeneral(self):
        Lista_Encuestas_No_Realizadas = []
        if not(f"Todos los Institutos - Encuesta {self.Cuatrimestre}.pdf" in os.listdir("PDF Profesores")):    # Si la encuesta no fue creada anteriormente, la crea.
            ResEncuesta, MateriasDelDocente = self.CalcularResEncuestaGeneral()
            HacerEncuesta(ResEncuesta, MateriasDelDocente)


    def CalcularResEncuestaGeneral(self):
        ResEncuesta = [0]*42             # La posición de cada elemento esta definida en la hoja "Automatismo Alejo", estoy reciclando el codigo asi que esta medio feito.
        # Para hacer la encuesta necesito 42 variables que son todos los datos que se obtienen de la encuesta.
        MateriasDelDocente = []
        N_Filas = len(self.excel["Instituto"])

        ResEncuesta[0] = "SA"
        ResEncuesta[1] = "Todos los Institutos"
        ResEncuesta[2] = self.Cuatrimestre


        for i in range(len(self.excel["Instituto"])):   # Vamos a recorrer cada una de las filas donde aparece el docente.
            MateriasDelDocente.append(self.excel[self.N_Col["Materia"]][i])

            # Cuantos cursaron las materia de principio a fin.
            if self.excel[self.N_Col["Cusaste Entera?"]][i] == "Si":
                ResEncuesta[3] += 1
            else:
                ResEncuesta[4] += 1
            


            # Pregunta 1
            ResEncuesta[8] += self.excel[self.N_Col["Preg 1"]][i]    # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 1"]][i] < 4:
                ResEncuesta[5] += 1
            elif self.excel[self.N_Col["Preg 1"]][i] > 6:
                ResEncuesta[7] += 1
            else:
                ResEncuesta[6] += 1
            


            # Pregunta 3
            ResEncuesta[12] += self.excel[self.N_Col["Preg 3"]][i]   # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 3"]][i] < 4:
                ResEncuesta[9] += 1
            elif self.excel[self.N_Col["Preg 3"]][i] > 6:
                ResEncuesta[11] += 1
            else:
                ResEncuesta[10] += 1



            # Pregunta 10
            if self.excel[self.N_Col["Preg 10"]][i] == "Si":
                ResEncuesta[13] += 1
            else:
                ResEncuesta[14] += 1



            # Pregunta 11
            if self.excel[self.N_Col["Preg 11"]][i] == "Si":
                ResEncuesta[15] += 1
            else:
                ResEncuesta[16] += 1



            # Pregunta 2
            ResEncuesta[20] += self.excel[self.N_Col["Preg 2"]][i]   # Este es un promedio, al final tengo q dividir por el N_Filas
            if self.excel[self.N_Col["Preg 2"]][i] < 4:
                ResEncuesta[17] += 1
            elif self.excel[self.N_Col["Preg 2"]][i] > 6:
                ResEncuesta[19] += 1
            else:
                ResEncuesta[18] += 1



            # Pregunta 12
            if self.excel[self.N_Col["Preg 12"]][i] == "Si":
                ResEncuesta[21] += 1
            else:
                ResEncuesta[22] += 1
            


            # Pregunta 4
            if self.excel[self.N_Col["Preg 4"]][i] == "Muy acorde":
                ResEncuesta[23] += 1
            elif self.excel[self.N_Col["Preg 4"]][i] == "Acorde":
                ResEncuesta[24] += 1
            else:
                ResEncuesta[25] += 1
            


            # Pregunta 5
            if self.excel[self.N_Col["Preg 5"]][i] == "Muy claro":
                ResEncuesta[26] += 1
            elif self.excel[self.N_Col["Preg 5"]][i] == "Claro":
                ResEncuesta[27] += 1
            else:
                ResEncuesta[28] += 1
            


            # Pregunta 6
            if self.excel[self.N_Col["Preg 6"]][i] == "Si":
                ResEncuesta[29] += 1
            else:
                ResEncuesta[30] += 1



            # Pregunta 7
            if self.excel[self.N_Col["Preg 7"]][i] == "Si, fue el entorno virtual donde se cursó la materia":
                ResEncuesta[31] += 1
            elif self.excel[self.N_Col["Preg 7"]][i] == "Se lo usó esporádicamente (cada tanto)":
                ResEncuesta[32] += 1
            else:
                ResEncuesta[33] += 1
            


            # Pregunta 8
            if self.excel[self.N_Col["Preg 8"]][i] == "Si":
                ResEncuesta[34] += 1
            else:
                ResEncuesta[35] += 1
            


            # Pregunta 9
            if self.excel[self.N_Col["Preg 9.1"]][i] != "":
                ResEncuesta[36] += 1
            if self.excel[self.N_Col["Preg 9.2"]][i] != "":
                ResEncuesta[37] += 1
            if self.excel[self.N_Col["Preg 9.3"]][i] != "":
                ResEncuesta[38] += 1
            if self.excel[self.N_Col["Preg 9.4"]][i] != "":
                ResEncuesta[39] += 1
            if self.excel[self.N_Col["Preg 9.5"]][i] != "":
                ResEncuesta[40] += 1
            if self.excel[self.N_Col["Preg 9.6"]][i] != "":
                ResEncuesta[41] += 1

        ResEncuesta[8] = ResEncuesta[8]/N_Filas
        ResEncuesta[12] = ResEncuesta[12]/N_Filas
        ResEncuesta[20] = ResEncuesta[20]/N_Filas

        return ResEncuesta, MateriasDelDocente


    def ResetearFiltroDocentes(self):
        self.IndiceDocente = {}
        self.NombreDocente = {}







class Button_SeleccionarExcelGeneral(Button_ListaDesplegable):
    def __init__(self, win, poss_boton, Listado, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, Listado, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR)
    
    def EventosListaDesplegable(self):      # Este evento hay que ponerlo dentro del evento "MOUSEBUTTONDOWN"
        if not(self.ListadoDesplegado):
            if self.mouse_up_contraido:
                self.ListadoDesplegado = True
        else:
            for i in range(len(self.Listado)):
                if self.mouse_up_desplegado[i] == True:
                    self.Valor = self.Listado[i]
                    self.ListadoDesplegado = False


class Button_CargarExcel(Button):
    def __init__(self, win, encuesta, poss_boton, text, tamaño_fuente, Boton_RecolectarHojasExcel, Boton_ElegirNombreHojaExcelGeneral, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR)
        self.encuesta = encuesta
        self.Boton_RecolectarHojasExcel = Boton_RecolectarHojasExcel
        self.Boton_ElegirNombreHojaExcelGeneral = Boton_ElegirNombreHojaExcelGeneral


    def Eventos_CargarExcel(self):
        if self.mouse_up:
            try:
                self.encuesta.excel = pd.read_excel("Excel Profesores/"+self.Boton_RecolectarHojasExcel.Valor, self.Boton_ElegirNombreHojaExcelGeneral.text, keep_default_na=(False))
                for columna in list(self.encuesta.excel.columns.values):     #Convierto todos los datos numéricos en strings.
                    try:    # Que convierta en entero todas las columnas que pueda, y si no, las vuelve string.
                        self.encuesta.excel[columna] = self.encuesta.excel[columna].apply(int)
                    except:
                        self.encuesta.excel[columna] = self.encuesta.excel[columna].apply(str)
                

                
                self.encuesta.HojaInstitutoDocente = pd.read_excel("Excel Profesores/"+self.Boton_RecolectarHojasExcel.Valor, self.encuesta.NombreHojaInstitutoDocente, keep_default_na=(False))
                for columna in list(self.encuesta.HojaInstitutoDocente.columns.values):
                    self.encuesta.HojaInstitutoDocente[columna] = self.encuesta.HojaInstitutoDocente[columna].apply(str)
                
                for i in range(len(self.encuesta.HojaInstitutoDocente["DNI UNICOS"])):
                    dni = self.encuesta.HojaInstitutoDocente["DNI UNICOS"][i]
                    instituto = self.encuesta.HojaInstitutoDocente["Instituto"][i]
                    self.encuesta.InstitutoDocente[dni] = instituto



                self.encuesta.HojaInstitutoCarrera = pd.read_excel("Excel Profesores/"+self.Boton_RecolectarHojasExcel.Valor, self.encuesta.NombreHojaInstitutoCarrera, keep_default_na=(False))
                for i in range(len(self.encuesta.HojaInstitutoCarrera["CARRERAS UNICAS"])):
                    carrera = self.encuesta.HojaInstitutoCarrera["CARRERAS UNICAS"][i]
                    instituto_carrera = self.encuesta.HojaInstitutoCarrera["Instituto"][i]
                    self.encuesta.InstitutoCarrera[carrera] = instituto_carrera
            except:
                print("---> Hiciste algo mal pibe, ponete las pilas")     ########## Poner cartelito


class Button_FiltrarDocentesEncuesta(Button):
    def __init__(self, win, encuesta, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR)
        self.encuesta = encuesta


    def Eventos_FiltrarDocentesEncuesta(self):
        if self.mouse_up:
            self.encuesta.ResetearFiltroDocentes()
            for i in range(len(self.encuesta.excel[self.encuesta.N_Col["DNI"]])):                # Recorremos cada índice del excel.
                equipo_doc = self.encuesta.excel[self.encuesta.N_Col["Equipo Docente"]][i].split("|")
                dni_doc = self.encuesta.excel[self.encuesta.N_Col["DNI"]][i].split("|")
                
                for j in range(len(dni_doc)):                                           # Recorremos la lista de dni y equipo. Si el DNI no se encuentra en guardado en las claves de indice, lo agregamos y tambien al de nombres.
                    if dni_doc[j] in list(self.encuesta.IndiceDocente.keys()):     # Si ya existía simplemente agregamos el indice.
                        self.encuesta.IndiceDocente[dni_doc[j]].append(i)
                    else:                                                               # Si no está lo agrego, primera aparición.
                        self.encuesta.IndiceDocente[dni_doc[j]] = [i]                   # Primer índice donde aparece, y es una lista, por q luego voy a agregar mas.
                        self.encuesta.NombreDocente[dni_doc[j]] = equipo_doc[j]         # El nombre del docente es guardado referenciado x su dni.


                carreras = self.encuesta.excel["Carrera"][i].split(",")
                for k in range(len(carreras)):
                    carreras[k] = carreras[k].strip()

                    if carreras[k] in list(self.encuesta.IndiceCarrera.keys()):
                        self.encuesta.IndiceCarrera[carreras[k]].append(i)
                    else:
                        self.encuesta.IndiceCarrera[carreras[k]] = [i]


class Button_CrearEncuestaDocente(Button):
    def __init__(self, win, encuesta, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR)
        self.encuesta = encuesta


    def Eventos_CrearEncuestaDocente(self):
        if self.mouse_up:
            HiloCrearEncuestaDocente = Thread(name="HiloEncuestaDocente", target=self.encuesta.CrearEncuestasDocentes)
            HiloCrearEncuestaDocente.start()
            
            
class Button_CrearEncuestaGeneral(Button):
    def __init__(self, win, encuesta, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR)
        self.encuesta = encuesta
    

    def Eventos_CrearEncuestaDocente(self):
        if self.mouse_up:
            HiloCrearEncuestaGeneral = Thread(name="HiloEncuestaGeneral", target=self.encuesta.CrearEncuestaGeneral)
            HiloCrearEncuestaGeneral.start()


class Button_CrearEncuestaCarrera(Button):
    def __init__(self, win, encuesta, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR):
        super().__init__(win, poss_boton, text, tamaño_fuente, color_texto_out=BLACK, color_texto_up=BLACK, color_boton_out=AZUL_UNAHUR, color_boton_up=VERDE_UNAHUR)
        self.encuesta = encuesta
    

    def Eventos_CrearEncuestaDocente(self):
        if self.mouse_up:
            HiloCrearEncuestaCarrera = Thread(name="HiloEncuestaCarrera", target=self.encuesta.CrearEncuestaCarrera)
            HiloCrearEncuestaCarrera.start()









