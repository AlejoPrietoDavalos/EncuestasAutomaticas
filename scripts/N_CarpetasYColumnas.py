import os

#Con la función os.listdir("direccion") me devuelve una lista con todos los archivos que estan en esa carpeta.
#Para poner la dirección tengo que usar la barra "/" no la invertida

#Creo una lista con todos los Excels que tengo que hacer la encuesta
Carpeta_Excels = "Excel Profesores"
Lista_Excels = os.listdir(Carpeta_Excels)
if "readme.txt" in os.listdir(Carpeta_Excels):
    Lista_Excels.pop(Lista_Excels.index("readme.txt"))
Lista_Encuestas_No_Realizadas = []
Nombre_Hoja_Datos = "Hoja1"    #El nombre de la hoja donde estan todos los datos en crudo que armó Nico
Nombre_Hoja_Automatismo = "Automatismo Alejo"   #El nombre de la hoja donde estan todos los datos que me sirven a mi para armar el automatismo
Institutos_Existentes = ["ITI", "IEDU", "IBIO", "ISC","SA"]
Nombre_Col_Materias = "Materia"
Nombre_Col_Datos_Encuesta = "Datos Encuesta"

