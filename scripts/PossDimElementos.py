# Vamos a guardar la posición de todas las imágenes, texto y sus dimenciones

'''
------------Cosas a tener en cuenta------------
Una hoja A4 horizontal tiene dimenciones de 297x210 mm. Siendo la primera medida el ancho, y la segunda el alto.
Si quiero insertar una imagen que tenga un cierto ancho deseado, y queremos saber cual tiene que ser la altura para que
no se deforme, entonces tenemos que tomar la relación.

--Calculos importantes--
Todas las imagenes van a tener 1313x735 pixeles de tamaño
Entonces para calcular cuanto tiene que ser la altura de la imagen para poder tener un ancho de 297mm, sería..
w=297
h=(735/1313)*297

Luego llamamos P, al punto de arriba a la izquierda de la imagen, dicho punto está puesto de forma que la imagen esté centrada.
Px = 0 y Py = (210 - Alto_Img)/2
'''

#-------------------Datos iniciales importantes---------------
T_Hojax = 297 #[mm]
T_Hojay = 210 #[mm]
Ancho_Img_Pix = 1313 #[pixels]
Alto_Img_Pix = 735 #[pixels]

Ancho_Img = T_Hojax
Alto_Img = (Alto_Img_Pix/Ancho_Img_Pix)*T_Hojax
Px = 0
Py = (T_Hojay-Alto_Img)/2

#--------Posición de los textos--------
#Posisión en X e Y
Poss_Text1=[455,200]
Poss_Text2=[455,256]
Poss_Text3=[20,410]
Poss_Text4=[150,240]
Poss_Text5=[280,340]
Poss_Text6=[155,480]
Poss_Text7=[291,688]
Poss_Text8=[291,688]
Poss_Text9=[291,688]
Poss_Text10=[291,690]
Poss_Text11=[291,690]
Poss_Text12=[291,690]
#--------Posición de los textos--------

#--------Dimensiones de los plots--------
#Posición en [Poss_X, Poss_Y, Ancho, Alto]
Dim_Plot1=[680,185,320,320]
Dim_Plot2=[45,350,278,230]
Dim_Plot3=[355,350,278,230]
Dim_Plot4=[665,350,278,230]
Dim_Plot5=[970,350,278,230]
Dim_Plot6=[160,310,290,290]
Dim_Plot7=[630,310,600,290]
Dim_Plot8=[95,350,270,270]
Dim_Plot9=[525,350,270,270]
Dim_Plot10=[890,350,400,270]
Dim_Plot11=[400,220,340,340]
Dim_Plot12=[810,300,460,250]
Dim_Plot13=[610,180,375,385]
#--------Dimensiones de los plots--------
#-------------------Datos iniciales importantes---------------




