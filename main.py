import os
import pygame as pg
from scripts.COLORES import *
from scripts.encuesta import *
from scripts.ventana import Ventana
from scripts.Botones import *
from scripts.func_encuesta import *


if __name__ == "__main__":
    # Revisemos si estas carpetas están creadas, si no lo están las creamos.
    if not("PDF Profesores" in os.listdir()):
        os.mkdir("PDF Profesores")
    if not("Plots Profesores" in os.listdir()):
        os.mkdir("Plots Profesores")




    win = Ventana()


    Boton_IrPorDocente = Button_CambiarVentana(win, [1050,150], "Encuesta por Docente", "Por Docente", 30)



    Boton_IrMenu = Button_CambiarVentana(win, [0,0], "Volver al Menu", "Menu", 30)

    Boton_RecolectarHojasExcel = Button_SeleccionarExcelGeneral(win, [0,40], ["--"]+Encuesta.Lista_Excels,15)
    Boton_ElegirNombreHojaExcelGeneral = EntryText(win, [Boton_RecolectarHojasExcel.dim_boton[0]+Boton_RecolectarHojasExcel.poss_botones[0][0] + 15,Boton_RecolectarHojasExcel.poss_botones[0][1]],100,20)



    encuesta = Encuesta(win)
    Boton_CargarExcel = Button_CargarExcel(win, encuesta, [Boton_ElegirNombreHojaExcelGeneral.poss_boton[0]+Boton_ElegirNombreHojaExcelGeneral.dim_boton[0],Boton_ElegirNombreHojaExcelGeneral.poss_boton[1]], "Cargar Excel", 20,Boton_RecolectarHojasExcel, Boton_ElegirNombreHojaExcelGeneral)
    Boton_FiltrarDocentesEncuesta = Button_FiltrarDocentesEncuesta(win, encuesta, [1000,200], "Filtrar Docentes Encuesta", 30)
    Boton_CrearEncuestaDocente = Button_CrearEncuestaDocente(win, encuesta, [1000,300], "Crear Encuesta Docentes", 30)
    Boton_CrearEncuestaGeneral = Button_CrearEncuestaGeneral(win, encuesta, [300,300], "Crear Encuesta General", 30)
    Boton_CrearEncuestaCarrera = Button_CrearEncuestaCarrera(win, encuesta, [200,200], "Crear Encuesta Carrera", 30)






    while win.run:
        while win.Ventanas_Posibles["Menu"] and win.run:
            win.ActualizarPulsacionControles()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    win.CerrarPrograma()
                if event.type == pg.MOUSEBUTTONDOWN:
                    Boton_IrPorDocente.EventosCambiarVentana()
                    Boton_CrearEncuestaGeneral.Eventos_CrearEncuestaDocente()
                    Boton_CrearEncuestaCarrera.Eventos_CrearEncuestaDocente()
                
            
            win.InsertarImgFondo()
            Boton_IrPorDocente.InsertarBoton()
            Boton_CrearEncuestaGeneral.InsertarBoton()
            Boton_CrearEncuestaCarrera.InsertarBoton()
            
            
            
            pg.display.update()
            win.RELOJ.tick(win.FPS)
        

        while win.Ventanas_Posibles["Por Docente"] and win.run:
            win.ActualizarPulsacionControles()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    win.CerrarPrograma()
                if event.type == pg.MOUSEBUTTONDOWN:
                    Boton_IrMenu.EventosCambiarVentana()
                    Boton_FiltrarDocentesEncuesta.Eventos_FiltrarDocentesEncuesta()
                    Boton_CrearEncuestaDocente.Eventos_CrearEncuestaDocente()
                    Boton_RecolectarHojasExcel.EventosListaDesplegable()
                    Boton_ElegirNombreHojaExcelGeneral.EventosClick_EntryText()
                    Boton_CargarExcel.Eventos_CargarExcel()
                if event.type == pg.KEYDOWN:
                    Boton_ElegirNombreHojaExcelGeneral.EventosTeclas_EntryText(event)
            
            win.InsertarImgFondo()

            Boton_IrMenu.InsertarBoton()
            Boton_FiltrarDocentesEncuesta.InsertarBoton()
            Boton_CrearEncuestaDocente.InsertarBoton()
            Boton_RecolectarHojasExcel.InsertarBoton()
            Boton_ElegirNombreHojaExcelGeneral.InsertarBoton()
            Boton_CargarExcel.InsertarBoton()
            pg.display.update()
            win.RELOJ.tick(win.FPS)


