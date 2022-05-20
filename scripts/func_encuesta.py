import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from fpdf import FPDF
from scripts.N_CarpetasYColumnas import *
from scripts.PossDimElementos import *

def Conv(Long_Pix):     #Hace la conversión entre [píxeles] y [mm]
    Long_mm = (Long_Pix*T_Hojax)/Ancho_Img_Pix
    return Long_mm


def Sacar_Repetidos(Lista_Vieja):
    Lista_Nueva=[]
    for r in range(len(Lista_Vieja)):
        if r==0:
            Lista_Nueva.append(Lista_Vieja[r])
        else:
            flag=True
            l=0
            while flag:     #Vamos a recorrer la Lista_Nueva para ver si Lista_Vieja[r] está en la lista nueva.
                if l==len(Lista_Nueva)-1:
                    if Lista_Vieja[r]!=Lista_Nueva[l]:
                        Lista_Nueva.append(Lista_Vieja[r])
                    flag=False
                elif Lista_Vieja[r]==Lista_Nueva[l]:
                    flag=False
                l=l+1    
    return Lista_Nueva


def Elegir_Color(Instituto):    #Si quiero otros colores tengo que modificar acá
    if Instituto=="IEDU":
        Color2=["#D42121", "#E97272"]
        Color3=["#D42121", "#E97272", "#A81A1A"]
        Color6=["#D42121", "#E97272", "#A81A1A", "#F09E9E", "#7C1313", "#F7CACA"]
    elif Instituto=="ITI":
        Color2=["#EE9607", "#FABF60"]
        Color3=["#EE9607", "#FABF60", "#BC7606"]
        Color6=["#EE9607", "#FABF60", "#BC7606", "#FCD391", "#8A5704", "#FDE7C2"]
    elif Instituto=="IBIO":
        Color2=["#1365E2","#68A0F2"]
        Color3=["#1365E2","#68A0F2","#0F51B3"]
        Color6=["#1365E2","#68A0F2","#0F51B3","#97BDF6","#0B3B84","#C6DBFA"]
    elif Instituto=="ISC":
        Color2=["#0DCEC1", "#31EDE0"]
        Color3=["#0DCEC1", "#31EDE0", "#1B968D"]
        Color6=["#0DCEC1", "#31EDE0", "#1B968D", "#04EFDE", "#157E76", "#88D4CE"]
    elif Instituto=="SA":
        Color2=["#0E4B09", "#1E7D17"]
        Color3=["#0E4B09", "#1E7D17", "#2AA521"]
        Color6=["#0E4B09", "#1E7D17", "#2AA521", "#30BD25", "#3DDB32", "#4CF340"]
    return Color2, Color3, Color6


def Grafico_Torta(datos, Color, Leyenda, Nro_Plot, Nombre, Promedio="no tiene"):
    Color_Fondo = "#ffffff"
    h=4
    des=0
    if len(Leyenda)==6:
        h=5
        des=-0.05
    Leyenda_Aux=[]
    #Agrego porcentaje al final en la leyenda
    for u in range(len(Leyenda)):
        if datos[u]==0:
            Leyenda_Aux.append("")
        else:
            Leyenda_Aux.append(str(round((datos[u]*100)/(np.sum(datos)),1))+"%")
        Leyenda[u]=Leyenda[u]+" ["+str(round((datos[u]*100)/(np.sum(datos)),1))+"%]"
        
    plt.figure(dpi=200, figsize=[4,h], facecolor=Color_Fondo)
    plt.pie(datos, colors=Color, labels=Leyenda_Aux, labeldistance=0.5)
    plt.legend(loc="center", labels=Leyenda, bbox_to_anchor=(0.5, des), shadow=True)
    if Promedio!="no tiene":
        plt.title(f"Promedio de las respuestas entre 1 y 10:  {round(Promedio,1)}")
    plt.savefig("Plots Profesores/"+Nombre+" Plots/"+Nombre+" - "+Nro_Plot)
    plt.close('all')


def Grafico_Hist_Horizontal(datos, Color, Leyenda, Nro_Plot, Nombre, Promedio="no tiene"):
    Color_Fondo = "#ffffff"
    datos=np.array(datos)
    datos=(datos*100)/np.sum(datos)
    
    plt.figure(dpi=200, figsize=[8,4], facecolor=Color_Fondo)
    plt.barh(range(len(Leyenda)), datos, color=Color, edgecolor="black")
    plt.yticks(range(len(Leyenda)), Leyenda, rotation=60)
    plt.xlabel("Frecuencia [%]")
    if Promedio!="no tiene":
        plt.title(f"Promedio de las respuestas entre 1 y 10:  {round(Promedio,1)}")
    plt.savefig("Plots Profesores/"+Nombre+" Plots/"+Nombre+" - "+Nro_Plot)
    plt.close('all')
    

def InsertarTexto(pdf, pos_x, pos_y, text, tamaño, negrita="",fuente="Arial"):
    pdf.set_font(fuente, negrita, tamaño)
    pdf.text(x=pos_x, y=pos_y, txt=text)


def HacerEncuesta(ResEncuesta, MateriasDelDocente):
    try:
        Col_Materias = Sacar_Repetidos(MateriasDelDocente)   #Pasa una lista con todas las materias que da el docente sin repetir
        
        aux = ResEncuesta[1]+" Plots"
        if not(aux in os.listdir("Plots Profesores")):  #Compruebo si este directorio existe, en caso negativo lo creo
            os.mkdir("Plots Profesores/"+ResEncuesta[1]+" Plots")  #Creamos un directorio para poner los Plots de este profesor
        
        
        
        #-----Elijo el color de los gráficos en función de su instituto
        Color_2, Color_3, Color_6 = Elegir_Color(ResEncuesta[0])
        #-----Elijo el color de los gráficos en función de su instituto
        
        
        
        pdf = FPDF(orientation = "L", unit = "mm", format = "A4")   #CREAMOS EL PDF
        
        #----------------------------Hoja 1----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 1.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)   #Agrego la primer imagen, notar que va a buscar al archivo a la posición donde esta especificado el instituto en el excel
        
        #--------Hoja 1 - Texto 1
        InsertarTexto(pdf, Px+Conv(Poss_Text1[0]), Py+Conv(Poss_Text1[1]), ResEncuesta[2], 25, negrita="B")
        
        #--------Hoja 1 - Texto 2
        InsertarTexto(pdf, Px+Conv(Poss_Text2[0]), Py+Conv(Poss_Text2[1]), ResEncuesta[1], 25)
        
        #--------Hoja 1 - Texto 3
        if len(Col_Materias)<=4:
            Tamaño_Letra=18
            Espaciado_Entre_Lineas=8
            u=0
        else:
            Tamaño_Letra=10
            Espaciado_Entre_Lineas=5
            u=3
        for j in range(len(Col_Materias)):
            InsertarTexto(pdf, Px+Conv(Poss_Text3[0]), Py+Conv(Poss_Text3[1])+Espaciado_Entre_Lineas*j-u, "- "+str(Col_Materias[j]), Tamaño_Letra)

        #----------------------------Hoja 1----------------------------
        
        
        
        
        #----------------------------Hoja 2----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 2.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        
        #--------Hoja 2 - Plot 1
        Leyenda_Plot1=[f'Cursada Completa: {ResEncuesta[3]}',f'Cursada Incompleta: {ResEncuesta[4]}']
        Datos_Plot1=[ResEncuesta[3], ResEncuesta[4]]
        Grafico_Torta(Datos_Plot1, Color_2, Leyenda_Plot1, "Plot 1", ResEncuesta[1])
        
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 1.png", x=Px+Conv(Dim_Plot1[0]), y=Py+Conv(Dim_Plot1[1]), w=Conv(Dim_Plot1[2]), h=Conv(Dim_Plot1[3]))
        
        
        #--------Hoja 2 - Texto 4
        InsertarTexto(pdf, Px+Conv(Poss_Text4[0]), Py+Conv(Poss_Text4[1]), "De las "+str(ResEncuesta[3]+ResEncuesta[4])+" encuestas respondidas el", 15)
        
        #--------Hoja 2 - Texto 5
        InsertarTexto(pdf, Px+Conv(Poss_Text5[0]), Py+Conv(Poss_Text5[1]), str(round((ResEncuesta[3]*100)/(ResEncuesta[3]+ResEncuesta[4]),1))+"%", 30, "B")
        
        #--------Hoja 2 - Texto 6
        InsertarTexto(pdf, Px+Conv(Poss_Text6[0]), Py+Conv(Poss_Text6[1]), "Mientras que el "+str(round((ResEncuesta[4]*100)/(ResEncuesta[3]+ResEncuesta[4]),1))+"% fué respondida por", 13)
        
        #--------Hoja 2 - Texto 7
        InsertarTexto(pdf, Px+Conv(Poss_Text7[0]), Py+Conv(Poss_Text7[1]), ResEncuesta[2], 12)
        #----------------------------Hoja 2----------------------------
        
        
        
        
        #----------------------------Hoja 3----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 3.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        
        #--------Hoja 3 - Plot 2
        Leyenda_Plot2 = [f"Entre 1 y 3:   {ResEncuesta[5]}", f"Entre 4 y 6:   {ResEncuesta[6]}", f"Entre 7 y 10:   {ResEncuesta[7]}"]
        Datos_Plot2 = [ResEncuesta[5], ResEncuesta[6], ResEncuesta[7]]
        Promedio_Plot2 = ResEncuesta[8]
        Grafico_Hist_Horizontal(Datos_Plot2, Color_3, Leyenda_Plot2, "Plot 2", ResEncuesta[1], Promedio_Plot2)
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 2.png", x=Px+Conv(Dim_Plot2[0]), y=Py+Conv(Dim_Plot2[1]), w=Conv(Dim_Plot2[2]), h=Conv(Dim_Plot2[3]))
        
        #--------Hoja 3 - Plot 3
        Leyenda_Plot3 = [f"Entre 1 y 3:   {ResEncuesta[9]}", f"Entre 4 y 6:   {ResEncuesta[10]}", f"Entre 7 y 10:   {ResEncuesta[11]}"]
        Datos_Plot3 = [ResEncuesta[9], ResEncuesta[10], ResEncuesta[11]]
        Promedio_Plot3 = ResEncuesta[12]
        Grafico_Hist_Horizontal(Datos_Plot3, Color_3, Leyenda_Plot3, "Plot 3", ResEncuesta[1], Promedio_Plot3)
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 3.png", x=Px+Conv(Dim_Plot3[0]), y=Py+Conv(Dim_Plot3[1]), w=Conv(Dim_Plot3[2]), h=Conv(Dim_Plot3[3]))
        
        #--------Hoja 3 - Plot 4
        Leyenda_Plot4 = [f"SI: {ResEncuesta[13]}", f"NO: {ResEncuesta[14]}"]
        Datos_Plot4 = [ResEncuesta[13], ResEncuesta[14]]
        Grafico_Hist_Horizontal(Datos_Plot4, Color_2, Leyenda_Plot4, "Plot 4", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 4.png", x=Px+Conv(Dim_Plot4[0]), y=Py+Conv(Dim_Plot4[1]), w=Conv(Dim_Plot4[2]), h=Conv(Dim_Plot4[3]))
        
        #--------Hoja 3 - Plot 5
        Leyenda_Plot5 = [f"SI: {ResEncuesta[15]}", f"NO: {ResEncuesta[16]}"]
        Datos_Plot5 = [ResEncuesta[15], ResEncuesta[16]]
        Grafico_Hist_Horizontal(Datos_Plot5, Color_2, Leyenda_Plot5, "Plot 5", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 5.png", x=Px+Conv(Dim_Plot5[0]), y=Py+Conv(Dim_Plot5[1]), w=Conv(Dim_Plot5[2]), h=Conv(Dim_Plot5[3]))
        
        #--------Hoja 3 - Texto 8
        pdf.set_font("Arial", "", 12)
        pdf.text(x=Px+Conv(Poss_Text8[0]), y=Py+Conv(Poss_Text8[1]), txt=ResEncuesta[2])
        #----------------------------Hoja 3----------------------------
        

        
                        
        #----------------------------Hoja 4----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 4.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        
        #--------Hoja 4 - Plot 6
        Leyenda_Plot6 = [f"Entre 1 y 3:   {ResEncuesta[17]}", f"Entre 4 y 6:   {ResEncuesta[18]}", f"Entre 7 y 10:   {ResEncuesta[19]}"]
        Datos_Plot6 = [ResEncuesta[17], ResEncuesta[18], ResEncuesta[19]]
        Promedio_Plot6 = ResEncuesta[20]
        Grafico_Torta(Datos_Plot6, Color_3, Leyenda_Plot6, "Plot 6", ResEncuesta[1], Promedio_Plot6)
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 6.png", x=Px+Conv(Dim_Plot6[0]), y=Py+Conv(Dim_Plot6[1]), w=Conv(Dim_Plot6[2]), h=Conv(Dim_Plot6[3]))
        
        #--------Hoja 4 - Plot 7
        Leyenda_Plot7 = [f"SI: {ResEncuesta[21]}", f"NO: {ResEncuesta[22]}"]
        Datos_Plot7 = [ResEncuesta[21], ResEncuesta[22]]
        Grafico_Hist_Horizontal(Datos_Plot7, Color_2, Leyenda_Plot7, "Plot 7", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 7.png", x=Px+Conv(Dim_Plot7[0]), y=Py+Conv(Dim_Plot7[1]), w=Conv(Dim_Plot7[2]), h=Conv(Dim_Plot7[3]))
        
        #--------Hoja 4 - Texto 9
        InsertarTexto(pdf, Px+Conv(Poss_Text9[0]), Py+Conv(Poss_Text9[1]), ResEncuesta[2], 12)
        #----------------------------Hoja 4----------------------------
        
        
        
        
        #----------------------------Hoja 5----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 5.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        
        #--------Hoja 5 - Plot 8
        Leyenda_Plot8 = [f"Muy Acorde:   {ResEncuesta[23]}", f"Acorde:   {ResEncuesta[24]}", f"Poco Acorde:   {ResEncuesta[25]}"]
        Datos_Plot8 = [ResEncuesta[23], ResEncuesta[24], ResEncuesta[25]]
        Grafico_Torta(Datos_Plot8, Color_3, Leyenda_Plot8, "Plot 8", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 8.png", x=Px+Conv(Dim_Plot8[0]), y=Py+Conv(Dim_Plot8[1]), w=Conv(Dim_Plot8[2]), h=Conv(Dim_Plot8[3]))
        
        #--------Hoja 5 - Plot 9
        Leyenda_Plot9 = [f"Muy Claro:   {ResEncuesta[26]}", f"Claro:   {ResEncuesta[27]}", f"Poco Claro:   {ResEncuesta[28]}"]
        Datos_Plot9 = [ResEncuesta[26], ResEncuesta[27], ResEncuesta[28]]
        Grafico_Torta(Datos_Plot9, Color_3, Leyenda_Plot9, "Plot 9", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 9.png", x=Px+Conv(Dim_Plot9[0]), y=Py+Conv(Dim_Plot9[1]), w=Conv(Dim_Plot9[2]), h=Conv(Dim_Plot9[3]))
        
        #--------Hoja 5 - Plot 10
        Leyenda_Plot10 = [f"SI: {ResEncuesta[29]}", f"NO: {ResEncuesta[30]}"]
        Datos_Plot10 = [ResEncuesta[29], ResEncuesta[30]]
        Grafico_Hist_Horizontal(Datos_Plot10, Color_2, Leyenda_Plot10, "Plot 10", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 10.png", x=Px+Conv(Dim_Plot10[0]), y=Py+Conv(Dim_Plot10[1]), w=Conv(Dim_Plot10[2]), h=Conv(Dim_Plot10[3]))
        
        #--------Hoja 5 - Texto 10
        InsertarTexto(pdf, Px+Conv(Poss_Text10[0]), Py+Conv(Poss_Text10[1]), ResEncuesta[2], 12)
        #----------------------------Hoja 5----------------------------
        
        
        
        
        #----------------------------Hoja 6----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 6.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        
        #--------Hoja 6 - Plot 11
        Leyenda_Plot11 = [f"SI:   {ResEncuesta[31]}", f"Esporádicamente:   {ResEncuesta[32]}", f"NO:   {ResEncuesta[33]}"]
        Datos_Plot11 = [ResEncuesta[31], ResEncuesta[32], ResEncuesta[33]]
        Grafico_Torta(Datos_Plot11, Color_3, Leyenda_Plot11, "Plot 11", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 11.png", x=Px+Conv(Dim_Plot11[0]), y=Py+Conv(Dim_Plot11[1]), w=Conv(Dim_Plot11[2]), h=Conv(Dim_Plot11[3]))
        
        #--------Hoja 6 - Plot 12
        Leyenda_Plot12 = [f"SI: {ResEncuesta[34]}", f"NO: {ResEncuesta[35]}"]
        Datos_Plot12 = [ResEncuesta[34], ResEncuesta[35]]
        Grafico_Hist_Horizontal(Datos_Plot12, Color_2, Leyenda_Plot12, "Plot 12", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 12.png", x=Px+Conv(Dim_Plot12[0]), y=Py+Conv(Dim_Plot12[1]), w=Conv(Dim_Plot12[2]), h=Conv(Dim_Plot12[3]))
        
        #--------Hoja 6 - Texto 11
        InsertarTexto(pdf, Px+Conv(Poss_Text11[0]), Py+Conv(Poss_Text11[1]), ResEncuesta[2], 12)
        #----------------------------Hoja 6----------------------------
        
        
        
        
        #----------------------------Hoja 7----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 7.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        
        #--------Hoja 6 - Plot 13
        Leyenda_Plot13 = [f"Redes Sociales:   {ResEncuesta[36]}", f"Clases Sincrónicas (Zoom, Meet,...):   {ResEncuesta[37]}", f"Laboratorios o Simuladores Virtuales:   {ResEncuesta[38]}", f"Entornos de Programación:   {ResEncuesta[39]}", f"Whatsapp:   {ResEncuesta[40]}", f"Otros:   {ResEncuesta[41]}"]
        Datos_Plot13 = [ResEncuesta[36],ResEncuesta[37], ResEncuesta[38], ResEncuesta[39], ResEncuesta[40], ResEncuesta[41]]
        Grafico_Torta(Datos_Plot13, Color_6, Leyenda_Plot13, "Plot 13", ResEncuesta[1])
        pdf.image("Plots Profesores/"+ResEncuesta[1]+" Plots/"+ResEncuesta[1]+" - Plot 13.png", x=Px+Conv(Dim_Plot13[0]), y=Py+Conv(Dim_Plot13[1]), w=Conv(Dim_Plot13[2]), h=Conv(Dim_Plot13[3]))
        
        #--------Hoja 6 - Texto 12
        pdf.set_font("Arial", "", 12)
        pdf.text(x=Px+Conv(Poss_Text12[0]), y=Py+Conv(Poss_Text12[1]), txt=ResEncuesta[2])
        #----------------------------Hoja 7----------------------------
        
        
        
        
        #----------------------------Hoja 8----------------------------
        pdf.add_page()
        pdf.image("Modelos/"+ResEncuesta[0]+" Modelo/"+ResEncuesta[0]+" - Hoja 8.PNG", x=Px, y=Py, w=Ancho_Img, h=Alto_Img)
        #----------------------------Hoja 8----------------------------
        
        
        
        
        #--------------------------CREAMOS EL PDF--------------------------
        pdf.output("PDF Profesores/"+ResEncuesta[1]+" - Encuesta "+ResEncuesta[2]+".pdf")     #Tiro como output el PDF del docente
        print(f"{ResEncuesta[1]} - ENCUESTA CREADA")
    
    except:
        Lista_Encuestas_No_Realizadas.append(ResEncuesta[1])    # Agrego el nombre del docente.
