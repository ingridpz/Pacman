# A00826973 Ingrid Giselle Paz Ramírez
# A00827533 Leo Abraham Puente Rangel
# Programa que recrea el famoso juego PACMAN
# Fecha de entrega: 28/10/2020

# Utilizamos bibliotecas para llamar funciones útiles
from random import choice # Elegir aleatoriamente una palabra
from turtle import *
from freegames import floor, vector # Tablero y animaciones

state = {'score': 0} # Puntaje
path = Turtle(visible=False) # Camino
writer = Turtle(visible=False) # Escribe vectores
aim = vector(5, 0) # Dirección
pacman = vector(-40, -80)# Posición de Pacman
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
] # Posición de fantasmas
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
] # Tablero con 1's = camino y 0's = paredes/espacios vacios

def square(x, y): # Características del tablero
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill() # Rellenado

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill() # Ayuda a definir el camino (cambios de color)

def offset(point):
    # Hallar el índice para el tablero (establecer ubicaciones)
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20 # Media/centro
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
     # Verificar que los movimientos no sean fuera de la pantalla
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
     # Dibujar el tablero
    "Draw world using path."
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)): # Donde colocar el camino
        tile = tiles[index]

        if tile > 0: # Características
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white') # Puntos = comida

def move(): # Movimiento de Pacman y los fantasmas
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score']) # Puntaje
    clear() # Se revalida cada que avanza

    if valid(pacman + aim):
        # Si el movimiento es válido, pacman se mueve
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1: # Cando pasa por un cuadro con dot
        tiles[index] = 2
        state['score'] += 1 # Aumentar puntaje
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10) 
    dot(20, 'yellow')
    # Color y tamaño de Pacman
    
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
            # Verificar que el movimiento sea posible
        else:
            # Si no es válido cambiar la dirección al azar
            options = [
                vector(8, 0),
                vector(-8, 0),
                vector(0, -8),
                vector(0, 8),
            ] # Distancia que recorren fantasmas (velocidad relativa)
            plan = choice(options)
            # Moverse en la nueva dirección
            course.x = plan.x
            course.y = plan.y
            
        if abs(pacman-point)<10:
            goto(pacman)
        if abs(pacman-point)<10:
            goto(pacman)
       # Los fantasmas siguen a Pacman
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')
        
            
    update()

    for point, course in ghosts:
        if abs(pacman-point)<10:
           return

    ontimer(move, 50) # Velocidad a la que sucede todo 

def change(x, y):
    # Cambio de dirección de Pacman 
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0) # Talero
hideturtle() # No mostrar comandos
tracer(False)
writer.goto(160, 160) # Tablero
writer.color('white')
writer.write(state['score'])
listen()
# Movimientos del pacman cuando se elije
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()