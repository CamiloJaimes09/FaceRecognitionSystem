from tkinter import *
import mediapipe as mp
import cv2
import face_recognition as fr
import numpy as np
from PIL  import Image, ImageTk
import imutils
import os

#Funcion LogBiometric

def LogBiometric():
    global pantalla2, conteo, parpadeo, img_info, step, cap, lblvideo

    #Verificar si hay videocaptura
    if cap is not None:
        ret, frame = cap.read()
        
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

#Variables

parpadeo = False
conteo = 0
muestra = 0
step = 0

#Offset

offsety = 30
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



