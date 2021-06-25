#Se importan las bibliotecas

from tkinter import *
import random
import time
import winsound
from threading import Thread
import os
import sys
from tkinter import messagebox

#Se definen globales
global crashtop
global points
global nivel

points = 0
nivel = 1
crash = 0

sys.setrecursionlimit(1000000000)

#Se crea la funcion que carga las imagenes
def CargaImagen(name):
    ruta = os.path.join('Imagenes del proyecto',name)
    imagen = PhotoImage(file=ruta)
    return imagen

#Se crea la funcion que carga la musica del juego
def MusicaJuego():

    winsound. PlaySound("musica juego.wav",winsound.SND_FILENAME | winsound.SND_ASYNC )

#Se crea la funcion que carga la musica del menu del juego
def MusicaMenu():

    winsound. PlaySound("musica menu.wav",winsound.SND_FILENAME | winsound.SND_ASYNC )

#Se crea la funcion que carga la musica de una colision
def MusicaChoque():

    winsound.PlaySound("choque.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

#Se crea la funcion que regresa al menu y resetea las variables
def BackMenu():

    global points
    global crash

    winsound.PlaySound(None, winsound.SND_ASYNC)

    musicamenu = Thread(target = MusicaMenu)
    musicamenu.start()

    crash = 0
    points = 0

    W_Game.destroy()
    windows.deiconify()


#Se crea la funcion que detecta si le quedan vidas al jugador y si no, elinima los enemigos de pantalla
def Choque(background,enemy,num):

    global crash
    global life
    global I_lifes

    background.delete(enemy)

    crash += num

    if crash >= 3:

        TheBestScore(Write2(name.get(),points, TakePoints(Read()), TakeNames(Read()), 7))
        
        Label.destroy(I_lifes)

        time.sleep(0)

        Fin= Label(W_Game, text = "¡Fin del Juego!", bg = "black", fg = "gold",font=("fixedsys", "30"))
        Fin.place(x=170,y=10)

        Menu = Button(W_Game, text = "Regresa al menu",bg= "black",fg = "gold",font=("fixedsys", "17"),command = BackMenu)
        Menu.place(x=220, y= 100)
    
    else:

        if crash > 2:
            
            Label.destroy(I_lifes)

        else:
            
            life = CargaImagen("life" + str(crash) + ".png")
            I_lifes.config(image = life)


#Se crea una clase para el carro enemigo
class Rojo:
    def __init__(self):
        pass

    def MoverRojo(self, background, rojo):

        if crash >= 3:
            return background.delete(rojo)

        if background.coords(rojo)[0] + 25 > posx and posx > background.coords(rojo)[0] - 18:

            if background.coords(rojo)[1] + 50 > posy and posy > background.coords(rojo)[1] - 50:
                return Choque(background, rojo, 1)

        if background.coords(rojo)[1] > 600:

            background.delete(rojo)

        else:

            background.move(rojo, 0, Velocidad())

            time.sleep(0.1)

            return self.MoverRojo(background, rojo)


#Se crea una clase para el obstaculo roca
class Roca:
    def __init__(self):
        pass

    def MoverRoca(self, background, roca):

        if crash >= 3:
            return background.delete(roca)

        if background.coords(roca)[0] + 40 > posx and posx > background.coords(roca)[0] - 33:

            if background.coords(roca)[1] + 40 > posy and posy > background.coords(roca)[1] - 40:
                return Choque(background, roca, 2)

        if background.coords(roca)[1] > 600:

            background.delete(roca)

        else:

            background.move(roca, 0, Velocidad())

            time.sleep(0.1)

            return self.MoverRoca(background, roca)


#Se crea una clase para el bonus estrella
class Estrella:
    def __init__(self):
        pass

    def MoverEstrella(self, background, estrella):

        global points
        global crash
        global life
        global I_lifes

        if crash >= 3:
            return background.delete(estrella)

        if background.coords(estrella)[0] + 40 > posx and posx > background.coords(estrella)[0] - 33:

            if background.coords(estrella)[1] + 40 > posy and posy > background.coords(estrella)[1] - 40:
                points += 500
                crash -= 1
                background.delete(estrella)
                return 0

        if background.coords(estrella)[1] > 600:

            background.delete(estrella)

        else:

            background.move(estrella, 0, vel)

            time.sleep(0.1)

            return self.MoverEstrella(background, estrella)


#Se crea una clase para el fondo o pista
class Fondo:
    def __init__(self):
        pass

    def MoveBackgroud(self, background, BG, BG2):

        if crash >= 3:

            return 0

        elif background.coords(BG)[1] == 600:

            background.move(BG, 0, -1200)

            time.sleep(0.01)

            return self.MoveBackgroud(background, BG, BG2)

        elif background.coords(BG2)[1] == 600:

            background.move(BG2, 0, -1200)

            time.sleep(0.01)

            return self.MoveBackgroud(background, BG, BG2)

        else:

            background.move(BG, 0, 5)
            background.move(BG2, 0, 5)
            time.sleep(0.01)

            return self.MoveBackgroud(background, BG, BG2)


#Se crean los objetos de las clases anteriores
Rojo_Obj = Rojo()
Roca_Obj = Roca()
Estrella_Obj = Estrella()
Fondo_Obj = Fondo()


#Se crea una funcion que crea enemigos y obstaculos y hace el cambio del puntaje
def Controlador(W_Game, background, C_cars, I_Points, photo_rojo, photo_roca, photo_estrella):

    global points

    I_Points.config(text=points)

    x = random.randint(155, 290)

    if crash >= 3:

        return 0

    elif C_cars % 7 == 0:

        roca = background.create_image(x, 0, image=photo_roca, anchor=NW)

        M_roca = Thread(target=Roca_Obj.MoverRoca, args=(background, roca))
        M_roca.start()

        points += 100

        time.sleep(2)

        return Controlador(W_Game, background, C_cars + 1, I_Points, photo_rojo, photo_roca, photo_estrella)

    elif C_cars % 10 == 0:

        estrella = background.create_image(x, 0, image=photo_estrella, anchor=NW)

        M_estrella = Thread(target=Estrella_Obj.MoverEstrella, args=(background, estrella))
        M_estrella.start()

        time.sleep(2)

        points += 100

        return Controlador(W_Game, background, C_cars + 1, I_Points, photo_rojo, photo_roca, photo_estrella)

    else:

        rojo = background.create_image(x, 0, image=photo_rojo, anchor=NW)

        M_rojo = Thread(target=Rojo_Obj.MoverRojo, args=(background, rojo))
        M_rojo.start()

        time.sleep(2)

        points += 100

        return Controlador(W_Game, background, C_cars + 1, I_Points, photo_rojo, photo_roca, photo_estrella)


#Se crea la funcion que maneja el juego en si, crea la ventana y muestra en pantalla ciertos datos
def Juego():

    windows.withdraw()
    
    global W_Game
    global life
    global I_lifes
    global km
    global posx
    global posy
    global I_Points

    posx = 250
    posy = 490

    km = 100
    
    W_Game = Toplevel()
    W_Game.title("It´s time for the win")
    W_Game.minsize(750,600)
    W_Game.resizable(width=NO,height=NO)
    W_Game.config( bg= "white")

    photo_player = CargaImagen("carro azul.png")
    photo_rojo = CargaImagen("carro rojo.png")
    photo_roca = CargaImagen("roca.png")
    photo_estrella = CargaImagen("estrella.png")
    photo_backgroud = CargaImagen("fondo " + str(varMap.get()) + ".png")
    photo_backgroud2 = CargaImagen("fondo " + str(varMap.get()) + ".png")

    background = Canvas(W_Game,width=570, height=600,bg= "black")
    background.place(x=0,y=0)

    BG = background.create_image(0,0,image = photo_backgroud,anchor = NW)
    BG2 = background.create_image(0,-595,image = photo_backgroud,anchor = NW)

    Player = background.create_image(250,490,image = photo_player,anchor = NW)

    stats = Canvas(W_Game, width = 190, height=600, bg = "blue")
    stats.place(x=570,y=0)

    I_life = Label(stats, text = "Life:", bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_life.place(x=35,y=10)

    I_Level= Label(stats, text = "Level:", bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_Level.place(x=35,y=90)

    I_Level= Label(stats, text = nivel, bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_Level.place(x=35,y=120)

    I_Name = Label(stats, text = "NamePlayer:", bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_Name.place(x=10,y=160)

    I_name = Label(stats,text = name.get(), bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_name.place(x=35,y=200)

    I_Point = Label(stats, text = "Points:", bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_Point.place(x=35,y=230)

    I_Points = Label(stats, bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_Points.place(x=35,y=270)

    I_Vel = Label(stats, text = "Km/h:", bg = "blue", fg = "gold",font=("fixedsys", "17"))
    I_Vel.place(x=35,y=325)

    KM = Label(stats, text = km, bg = "blue", fg = "gold",font=("fixedsys", "17"))
    KM.place(x=35,y=355)

    life = CargaImagen("life.png")

    car_g = CargaImagen("cargame.png")

    I_car= Label(stats, image = car_g,bg = "White")
    I_car.place(x=5,y=440)

    I_lifes= Label(stats, image = life,bg = "black")
    I_lifes.place(x=35,y=55)

    #Esta funcion aplica la movilidad del jugador
    def Mover(event):

        global km
        global posx
        global posy
        
        if event.keysym == "a":
            
            if background.coords(Player)[0] < 155:

                background.move(Player,0,0)
                
            else:
                
                background.move(Player,-10,0)
                
        elif event.keysym == "d":
            
            if background.coords(Player)[0] > 290:
                
                background.move(Player,0,0)
                
            else:
                
                background.move(Player,10,0)
                
        elif event.keysym == "w":

            km += 10
            
            if background.coords(Player)[1] < 3:

                background.move(Player,0,0)
                
            else:
                
                background.move(Player,0,-10)
                
        elif event.keysym == "s":

            km -= 10
            
            if background.coords(Player)[1] > 490:
                
                background.move(Player,0,0)

            else:
                
                background.move(Player,0,10)

        if km < 100:

            km = 100
            
        elif km > 600:

            km = 600

        posx = background.coords(Player)[0]
        posy = background.coords(Player)[1]

        KM.config(text = km)

        background.update()

    background.bind_all("<KeyPress-a>",Mover)
    background.bind_all("<KeyPress-d>",Mover)
    background.bind_all("<KeyPress-w>",Mover)
    background.bind_all("<KeyPress-s>",Mover)

    controler = Thread(target = Controlador, args =(W_Game,background,1,I_Points,photo_rojo,photo_roca,photo_estrella))
    controler.start()

    MoveBG = Thread(target = Fondo_Obj.MoveBackgroud, args = (background,BG,BG2))
    MoveBG.start()

    musica = Thread(target = MusicaJuego())
    musica.start()
 
    W_Game.mainloop()


#Se crea la funcion que valida el inicio del juego y que el usuario de un nombre y este listo
def Validar():

    global vel

    vel = varVel.get()

    if varMap.get() > 0:

        if name.get() != "":

            winsound.PlaySound(None, winsound.SND_ASYNC)

            return Juego()
        
        else:

            messagebox.showinfo("No se puede empezar","Agregar un Nombre")
            
    else:

        messagebox.showinfo("No se puede empezar", "Debes oprimir SI")


#Se crea una funcion que cambia la velocidad de los emenigos y obstaculos
def Velocidad():

    global vel
    global points
    global nivel

    if points < 2000:
        vel = 10
    elif points > 2000 and points < 4000:
        vel = 20
        nivel = 2
    else:
        vel = 30
        nivel = 3

    return vel


#Se crea una funcion que muestra los creditos
def F_Creditos():

    #Esta funcion regresa el menu
    def BackCreditos():

        Creditos.destroy()
        windows.deiconify()


    Creditos = Toplevel()
    Creditos.title("Creditos")
    Creditos.minsize(300,450)
    Creditos.resizable(width=NO,height=NO)
    Creditos.config( bg= "black")

    creditos_ = Label(Creditos,text = """

    País:
    Costa Rica

    Universidad y carrera:
    Instituto Tecnológico de Costa Rica
    Ingenieria en computadores

    Grupo y profesor:
    Taller de programacion, grupo 5
    Antonio Gonzales Torres

    Versión:
    1.0

    Desarrolladores:
    Grevin Carrillo
    Fabian Guevara
    Roger Solano

    Año de desarrollo:
    2021""", bg = "black", fg = "white")
    creditos_.place(x=50,y=0)

    Back = Button(Creditos, text = "BACK",bg= "black",fg = "white",font=("fixedsys"),command = BackCreditos)
    Back.place(x=140, y= 400)

    Creditos.mainloop()


#Se crea una funcion que muestra informacion del juego
def F_informacion():

    # Esta funcion regresa el menu
    def BackInformacion():

        Informacion.destroy()
        windows.deiconify()


    Informacion = Toplevel()
    Informacion.title("Informacion")
    Informacion.minsize(500,450)
    Informacion.resizable(width=NO,height=NO)
    Informacion.config( bg= "black")

    informacion_ = Label(Informacion,text = """

    PyDakarRace Información:
        

    Es un juego de carreras en el que permite competir dos o más jugadores
    El tiempo de juego es de 3 minutos

    Puntaje:
    En ver puntuaje aparecerán los 6 mejores jugadores
        
    Obstaculos:
    El juego cuenta con obstaculos en la pista

    Niveles:
    Cuenta con 3 niveles de velocidad de los enemigos

    
    Arquitectura:
    Cliente - Servidor """, bg = "black", fg = "white")
    informacion_.place(x=50,y=0)

    Back = Button(Informacion, text = "BACK",bg= "black",fg = "white",font=("fixedsys"),command = BackInformacion)
    Back.place(x=240, y= 400)

    Informacion.mainloop()


#Se crea una funcion que muestra las instrucciones del juego
def ComoJugar():

    # Esta funcion regresa el menu
    def BackJugar():

        h_play.destroy()
        windows.deiconify()


    h_play = Toplevel()
    h_play.title("Como Jugar")
    h_play.minsize(750,600)
    h_play.resizable(width=NO,height=NO)
    h_play.config( bg= "black")

    asdwhowplay = CargaImagen("asdw.png")

    howplay = Label(h_play, image = asdwhowplay,borderwidth=0)
    howplay.place(x=10,y=10)

    strhowplay = Label(h_play,text = """
    con "d" se mueve a la derecha
    
    con "a" se mueve a la izquierda
    
    con "w" acelera
    
    con "s" disminuye la velocidad
    
    """, bg = "black", fg = "white",font = ("fixedsys", "15"))
    strhowplay.place(x=430,y=100)


    strhowplay2 = Label(h_play,text = """
    * Debes de tener desactivado las mayusculas *

    Para tener mejor experiencia ponerse audifonos

    Pierdes cuando chocas 3 veces, la roca quita 2 vidas,
    el carro rojo 1 vida y la estrella otorga 1 vida.

    Ganas obteniendo la mayor cantidad de puntos. """, bg = "black", fg = "white",font = ("fixedsys", "15"))
    strhowplay2.place(x=100,y=300)

    Back = Button(h_play, text = "BACK",bg= "black",fg = "white",font=("fixedsys"),command = BackJugar)
    Back.place(x=350, y= 500)

    h_play.mainloop()


#Se crea una funcion que nos muestra los mejores puntajes
def TopPlayers():

    # Esta funcion regresa el menu
    def BackTop():

        TopPlayers.destroy()
        windows.deiconify()


    TopPlayers = Toplevel()
    TopPlayers.title("Top Players")
    TopPlayers.minsize(700,600)
    TopPlayers.resizable(width=NO,height=NO)
    TopPlayers.config(bg= "grey")

    listplayers = Read()

    Top = Label(TopPlayers,text = "TOP 6",bg="grey",fg = "black",font=("fixedsys","20"))
    Top.place(x=300,y = 50)

    CanvasGrid = Canvas(TopPlayers,width=500, height=600,bg= "grey",highlightbackground="grey")
    CanvasGrid.place(x=185,y=100)

    Position = Label(CanvasGrid,text = "Posicion",bg="grey",fg = "black",font=("fixedsys","20"))
    Position.grid(row=0,column=0,padx = 5, pady = 5)

    Score = Label(CanvasGrid,text = "Nombre/Puntaje",bg="grey",fg = "black",font=("fixedsys","20"))
    Score.grid(row=0,column=1,padx = 5, pady = 5)

    First = Label(CanvasGrid,text = "Primero:",bg="grey",fg = "black",font=("fixedsys","20"))
    First.grid(row=1,column=0,padx = 5, pady = 5)
    
    Second = Label(CanvasGrid,text = "Segundo:",bg="grey",fg = "black",font=("fixedsys","20"))
    Second.grid(row=2,column=0,padx = 5, pady = 5)

    Third = Label(CanvasGrid,text = "Tercero:",bg="grey",fg = "black",font=("fixedsys","20"))
    Third.grid(row=3,column=0,padx = 5, pady = 5)

    Fourth = Label(CanvasGrid,text = "Cuarto:",bg="grey",fg = "black",font=("fixedsys","20"))
    Fourth.grid(row=4,column=0,padx = 5, pady = 5)

    Fifth = Label(CanvasGrid,text = "Quinto:",bg="grey",fg = "black",font=("fixedsys","20"))
    Fifth.grid(row=5,column=0,padx = 5, pady = 5)

    Sixth = Label(CanvasGrid,text = "Sexto:",bg="grey",fg = "black",font=("fixedsys","20"))
    Sixth.grid(row=6,column=0,padx = 5, pady = 5)

    NameFirst = Label(CanvasGrid,text = listplayers[0],bg="grey",fg = "black",font=("fixedsys","20"))
    NameFirst.grid(row=1,column=1,padx = 5, pady = 5)
    
    NameSecond = Label(CanvasGrid,text = listplayers[1],bg="grey",fg = "black",font=("fixedsys","20"))
    NameSecond.grid(row=2,column=1,padx = 5, pady = 5)

    NameThird = Label(CanvasGrid,text = listplayers[2],bg="grey",fg = "black",font=("fixedsys","20"))
    NameThird.grid(row=3,column=1,padx = 5, pady = 5)

    NameFourth = Label(CanvasGrid,text = listplayers[3],bg="grey",fg = "black",font=("fixedsys","20"))
    NameFourth.grid(row=4,column=1,padx = 5, pady = 5)

    NameFifth = Label(CanvasGrid,text = listplayers[4],bg="grey",fg = "black",font=("fixedsys","20"))
    NameFifth.grid(row=5,column=1,padx = 5, pady = 5)

    NameSixth = Label(CanvasGrid,text = listplayers[5],bg="grey",fg = "black",font=("fixedsys","20"))
    NameSixth.grid(row=6,column=1,padx = 5, pady = 5)

    Back = Button(TopPlayers, text = "BACK",bg= "black",fg = "white",font=("fixedsys"),command = BackTop)
    Back.place(x=330, y= 550)


#Las siguientes funciones son para leer y escribir en un archivo .txt los puntajes
def Read():
    path= "scores.txt"
    file=open(path, "r")
    txt=file.readlines()
    file.close()
    return Delete(txt)

def Write(txt):
    path="scores.txt"
    file=open(path, "a")
    file.write(txt+"\n") 
    file.close()

def Write2(player, points, list_com, name, best):

    if best == 0:
        return []
    else:
        if points > int(list_com[0]):
            return [player + "," + str(points)] + Write2(player, -1, list_com, name, best - 1)
        else:
            return [name[0] + "," + list_com[0]] + Write2(player, points, list_com[1:], name[1:], best - 1)

def Delete(txt):
    if txt == []:
        return []
    else:
        leng = len(txt[0])
        return [txt[0][:leng - 1]] + Delete(txt[1:])
 
def TheBestScore(score):

    path="scores.txt"
    ScoreFile=open(path, "w")
    ScoreFile.write(str(score[0])+"\n")
    ScoreFile.write(str(score[1])+"\n")
    ScoreFile.write(str(score[2])+"\n")
    ScoreFile.write(str(score[3])+"\n")
    ScoreFile.write(str(score[4])+"\n")
    ScoreFile.write(str(score[5])+"\n")
    ScoreFile.close()

def TakeNames(txt):
    
    if txt == []:

        return []
    
    else:
        
        return [txt[0].split(",")[0]] + TakeNames(txt[1:])

def TakePoints(txt):
    
    if txt == []:
        
        return []
    
    else:
        
        return [txt[0].split(",")[1]] + TakePoints(txt[1:])


#Aplicacion del juego

#Donde se crea la ventana del menu
windows = Tk()
windows.title("PyDakarRace")
windows.minsize(750,600)
windows.resizable(width=NO,height=NO)
windows.config( bg= "grey")

#Texto de name
Nplayer = Label(windows, text = "Nombre:", bg = "black",fg = "white",font=("fixedsys", "17"))
Nplayer.place(x= 150, y = 410)

#Ingresar nombre de jugador
name = Entry(windows,bg = "white",fg = "black",font=("fixedsys"))
name.place(x=100,y=450)

#Boton de inicar el juego
Inicio = Button(windows,text = "Empezar!",bg = "black",fg = "white", command = Validar)
Inicio.place(x=145,y=490)

C_options = Canvas(windows, width=200, height=200,bg= "grey",highlightbackground="grey")
C_options.place(x= 350, y=410)

#Texto de PyDakar
PyDakar = Label(windows, text = "PyDakar",bg="grey",fg = "black",font=("fixedsys", "120"))
PyDakar.place(x = 170, y = 50)

#Texto de race
Race = Label(windows, text = "Race",bg="grey",fg = "black",font=("fixedsys", "120"))
Race.place(x = 300, y = 200)

varMap = IntVar()

varVel = IntVar()

#Texto y boton de estar listo
L_Map = Label(windows,text = "Estas listo??",bg="black",fg = "white",font=("fixedsys"))
L_Map.place(x= 340, y=415)

B1 = Radiobutton(C_options, text = "Si", variable = varMap, value = 1,bg= "black",fg = "white",font=("fixedsys"))
B1.grid(row = 0, column=1,pady = 30)

#Boton de creditos
Creditos = Button(windows, text = "Creditos",bg= "white",fg = "black",font=("fixedsys"),command = F_Creditos)
Creditos.place(x=540,y=400)

#Boton de informacion
Informacion = Button(windows, text = "Informacion", bg= "white", fg= "black", font=("fixedsys"), command = F_informacion)
Informacion.place(x=540, y= 450)

#Boton de how to play
Como = Button(windows, text = "Como jugar",bg= "white",fg = "black",font=("fixedsys"),command = ComoJugar)
Como.place(x=540, y= 500)

#Boton de top players
Top = Button(windows, text = "Top players",bg= "white",fg = "black",font=("fixedsys"), command = TopPlayers)
Top.place(x=540, y= 550)

musicamenu = Thread(target = MusicaMenu())
musicamenu.start()

windows.mainloop()
