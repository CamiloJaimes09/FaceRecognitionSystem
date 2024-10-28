from tkinter import *
import mediapipe as mp
import cv2
import face_recognition as fr
import numpy as np
from PIL  import Image, ImageTk
import imutils
import os
import math

#Funcion LogBiometric

# Face Code
def Code_Face(images):
    listacod = []

    # Iteramos
    for img in images:
        # Correccion de color
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # Codificamos la imagen
        cod = fr.face_encodings(img)[0]
        # Almacenamos
        listacod.append(cod)

    return listacod

# Close Windows LogBiometric
def Close_Windows():
    global step, conteo
    # Reset Variables
    conteo = 0
    step = 0
    pantalla2.destroy()

# Close Windows SignBiometric
def Close_Windows2():
    global step, conteo
    # Reset Variables
    conteo = 0
    step = 0
    #pantalla3.destroy()

def LogBiometric():
    global pantalla2, conteo, parpadeo, img_info, step, cap, lblvideo, img_check, RegUser

    #Verificar si hay videocaptura
    if cap is not None:
        ret, frame = cap.read()

        frameSave = frame.copy()
        
        #Reslize
        frame = imutils.resize(frame, width=1280)

        #RGB

        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        


        #Mostrar frame
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        if ret == True:
            #Inferencia de la malla facial
            res = FaceMesh.process(frameRGB)

            #Result list
            px=[]
            py=[]
            lista_coordenadas = []
            if res.multi_face_landmarks:
                #Extraer las detecciones
                for rostros in res.multi_face_landmarks:
                    mpDraw.draw_landmarks(frame, rostros, FacemeshObject.FACEMESH_CONTOURS, configdraw, configdraw )

                    #Extraer los Key Points
                    #Face mesh nos entrega 468 puntos clave del rostro

                    for id, puntos in enumerate(rostros.landmark):
                        #info img

                        al, an, c = frame.shape
                        x, y = int(puntos.x * an), int(puntos.y*al)
                        px.append(x)
                        py.append(y)
                        lista_coordenadas.append([id,x,y])
                        
                        #468 puntos
                        if len(lista_coordenadas) == 468:
                            #ojo derecho
                            x1,y1 = lista_coordenadas[145][1:]
                            x2,y2 = lista_coordenadas[159][1:]
                            longitud1 = math.hypot(x2-x1, y2-y1)

                            #ojo izquierdo
                            x3,y3 = lista_coordenadas[374][1:]
                            x4,y4 = lista_coordenadas[386][1:]
                            longitud2 = math.hypot(x4-x3, y4-y3)
                            
                            #Parietal Derecho
                            x5,y5 = lista_coordenadas[139][1:]

                            #Parietal Izquierdo
                            x6,y6 = lista_coordenadas[368][1:]

                            #Ceja Derecha
                            x7,y7 = lista_coordenadas[70][1:]
                            
                            #Ceja Izquierda 
                            x8,y8 = lista_coordenadas[300][1:]

                            

                            #Face detect
                            faces = detector.process(frameRGB)
                            if faces.detections is not None:
                                for face in faces.detections:

                                    #Bbox: "ID, BBOX, SCORE"
                                    score = face.score
                                    score = score[0]
                                    bbox = face.location_data.relative_bounding_box

                                    #Treshold
                                    if score > confThreshold:
                                        #Convertir a pixeles

                                        xi, yi, anc, alt = bbox.xmin, bbox.ymin, bbox.width, bbox.height
                                        xi, yi, anc, alt = int(xi*an), int(yi*al), int(anc*an), int(alt*al)

                                        #offset

                                        offsetan = (offsetx /100)*anc
                                        xi = int(xi-int(offsetan/2))
                                        anc = int(anc+offsetan)
                                        xf = xi + anc

                                        #offset en y

                                        offsetal = (offsety/100)*alt
                                        yi = int(yi-offsetal)
                                        alt = int(alt + offsetal)
                                        yf = yi + alt

                                        #Quitar error de la mascara - Error

                                        if xi < 0 : xi = 0
                                        if yi < 0 : yi = 0
                                        if anc < 0 : anc = 0
                                        if alt < 0 : alt = 0

                                        #Steps
                                        if step == 0:
                                            #Draw
                                            cv2.rectangle(frame,(xi,yi,anc,alt), (100,150,255),2)

                                            #IMG Step0
                                            als0,ans0,c = img_step0.shape
                                            frame[50:50 + als0, 50:50 +ans0] = img_step0

                                            #IMG Step1
                                            als1,ans1,c = img_step1.shape
                                            frame[50:50 + als1, 1030:1030 +ans1] = img_step1

                                            #IMG Step2
                                            als2,ans2,c = img_step2.shape
                                            frame[270:270 + als2, 1030:1030 +ans2] = img_step2

                                            #Face Center
                                            if x7 > x5 and x8 < x6:
                                                #IMG CHECK
                                                alch,anch,c = img_check.shape
                                                frame[165:165 + alch, 1105:1105 +anch] = img_check

                                                #Conteo parpadeos
                                                if longitud1<= 10 and longitud2 <= 10 and parpadeo == False:
                                                    conteo += 1
                                                    parpadeo = True
                                                elif longitud1 > 10 and longitud2 > 10 and parpadeo == True:
                                                    parpadeo = False
                                                cv2.putText(frame, f'Parpadeos: {int(conteo)}', (1070,375), cv2.FONT_HERSHEY_COMPLEX,0.5, (255,255,255),1)

                                                #Condicion
                                                if conteo >= 3:
                                                    #IMG Check
                                                    alch,anch,c = img_check.shape
                                                    frame[385:385 + alch, 1105:1105 +anch] = img_check

                                                    #Ojos abiertos toma foto
                                                    if longitud1 > 14 and longitud2 > 14:
                                                        cut = frameSave[yi:yf , xi:xf]

                                                        #Guardar la cara
                                                        cv2.imwrite(f"{OutFolderPathFace}/{RegUser}.png", cut)

                                                        step = 1

                                                    

                                            else:
                                                conteo = 0
                                        if step == 1:

                                             #Draw
                                            cv2.rectangle(frame,(xi,yi,anc,alt), (0,255,0),2)

                                            #IMG Check Liveness
                                            alli,anlli,c = img_liche.shape
                                            frame[50:50 + alli, 50:50 +anlli] = img_liche




                            #Circle
                            cv2.circle(frame, (x7,y7), 2, (255,0,0), cv2.FILLED)
                            cv2.circle(frame, (x8,y8), 2, (255,0,0), cv2.FILLED)




        
        #Convertir el video
        im = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=im)

        #Mostrar video
        lblvideo.configure(image=img)
        lblvideo.image = img
        lblvideo.after(10, LogBiometric)
    else:
        cap.release()




#Function Sign
def Sign():
    print("Sing")

#Function Log

def Log():
    global RegName, Reguser, RegPass, InputNameReg, InputUserReg, InputPassReg, cap, lblvideo, pantalla2
    #Extract Name -User-Password

    RegName, RegUser, RegPass = InputNameReg.get(), InputUserReg.get(), InputPassReg.get()

    #Formularios incpmpletos

    if len(RegName) == 0 or len (RegUser) ==0 or len(RegPass) == 0:
        print("Formulario Incompleto")
    else:
        #Check Users
        UserList = os.listdir(PathUserCheck)
        #Name users

        UserName = []

        #verificar la lista de usuarios
        for users in UserList:
            #sacar usuario
            User = users
            User = User.split(',')
            #guardar usuario
            UserName.append(User[0])

        #verificar existencia de usuario
        if RegUser in UserName:
            print("El usuario ya se encuentra registrado")
        else:
            #guardar informacion
            info.append(RegName)
            info.append(RegUser)
            info.append(RegPass)
            #exportar info

            f = open(f"{OutFolderPathUser}/{RegUser}.txt","w")
            f.write(RegName + ',')
            f.write(RegUser + ',')
            f.write(RegPass)
            f.close

            #Limpiar
            InputNameReg.delete(0,END)
            InputUserReg.delete(0,END)
            InputPassReg.delete(0, END)

            #Nueva Pantalla
            pantalla2 = Toplevel(pantalla)
            pantalla2.title("LOGIN BIOMETRIC")
            pantalla2.geometry("1280x720")

            #Label de video
            lblvideo = Label(pantalla2)
            lblvideo.place(x=0, y=0)

            #Crear videocaptura
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            cap.set(3,1280)
            cap.set(4,720)
            LogBiometric ()





#Path

OutFolderPathUser = 'C:/Users/Usuario/Desktop/Face Recognition System/DataBase/Users'
PathUserCheck = 'C:/Users/Usuario/Desktop/Face Recognition System/DataBase/Users/'
OutFolderPathFace = 'C:/Users/Usuario/Desktop/Face Recognition System/DataBase/Faces'

#Leer imagenes
img_info = cv2.imread("C:/Users/Usuario/Desktop/Face Recognition System/Setup/Info.png")
img_check = cv2.imread("C:/Users/Usuario/Desktop/Face Recognition System/Setup/Check.png")
img_step0 = cv2.imread("C:/Users/Usuario/Desktop/Face Recognition System/Setup/Step0.png")
img_step1 = cv2.imread("C:/Users/Usuario/Desktop/Face Recognition System/Setup/Step1.png")
img_step2 = cv2.imread("C:/Users/Usuario/Desktop/Face Recognition System/Setup/Step2.png")
img_liche = cv2.imread("C:/Users/Usuario/Desktop/Face Recognition System/Setup/Liveness.png")
#Variables

parpadeo = False
conteo = 0
muestra = 0
step = 0

#Offset

offsety = 40
offsetx = 30

#Treshold

confThreshold = 0.5

#Tooldraw

mpDraw = mp.solutions.drawing_utils
configdraw = mpDraw.DrawingSpec(thickness =1, circle_radius=1)

#Object Face Mash

FacemeshObject = mp.solutions.face_mesh
FaceMesh = FacemeshObject.FaceMesh(max_num_faces=1)

#Object Face Detect

FaceObject = mp.solutions.face_detection
detector = FaceObject.FaceDetection(min_detection_confidence=0.5, model_selection=1)


#Lista de informacion
info = []

#Interfaz

#Ventana principal

pantalla = Tk()
pantalla.title("FACE RECOGNITION SYSTEM")
pantalla.geometry("1280x720")

#Fondo

imagenF = PhotoImage(file="C:/Users/Usuario/Desktop/Face Recognition System/Setup/Inicio.png")
background = Label(image=imagenF, text="Inicio")
background.place(x=0, y=0, relheight=1, relwidth=1)

#Input text  Login

#Name
InputNameReg = Entry(pantalla)
InputNameReg.place(x=155,y=315)

#User
InputUserReg = Entry(pantalla)
InputUserReg.place(x=155,y=415)

#Pass
InputPassReg = Entry(pantalla)
InputPassReg.place(x=155,y=515)

#Input Text SignUp

#User
InputUserLog = Entry(pantalla)
InputUserLog.place(x=740, y=390)

#Pass
InputPassLog = Entry(pantalla)
InputPassLog.place(x=740, y=500)

#Buttoms

#Log
ImagenBR = PhotoImage(file= "C:/Users/Usuario/Desktop/Face Recognition System/Setup/Login.png" )
Btreg = Button(pantalla, text="Registro", image=ImagenBR,height=40,width=200,command=Log)
Btreg.place(x=360, y=550)

#Sign
ImagenBL = PhotoImage(file= "C:/Users/Usuario/Desktop/Face Recognition System/Setup/Signup.png" )
BtSign = Button(pantalla, text="Registro", image=ImagenBL,height=40,width=200,command=Sign)
BtSign.place(x=920, y=550)
pantalla.mainloop()



