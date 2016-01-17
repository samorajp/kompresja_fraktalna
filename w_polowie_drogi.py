# -*- coding: utf-8 -*-
"""Program rysujacy Trojkat Sierpinskiego na podstawie losowania
jednego z trzech punktow trojata rownobocznego."""
import turtle
import random

def w_polowie_drogi(od, do):
    x = 0.5 * (od[0] + do[0])
    y = 0.5 * (od[1] + do[1])
    return x, y

def przesun(punkt, wektor):
    x, y = punkt
    dx, dy = wektor
    return (x + dx, y + dy)
    

def pozdrowienia():
    turtle.setpos((-170, 90))
    turtle.write("Dziekuje i pozdrawiam! Pawel", font=("Arial", 20, "normal"))

KROK = 300  # dlugosc boku rysowanego trojkata
ILE_KROPEK = 100000  # ile kropek ma byc postawione w trakcie calej animacji
OKRES_ODSWIEZENIA = 10  # co ile kropek pokazywac rysunek 
WIERZCHOLKI = [(0, 0), (KROK, 0), (KROK / 2, KROK / 2 * 3 ** 0.5)]
WIERZCHOLKI = map(lambda punkt: przesun(punkt, (-KROK / 2, -KROK * 3 ** 0.5 / 3)), WIERZCHOLKI)

def rysuj():
    turtle.tracer(0, 0)  # wylaczenie animacji co KROK, w celu przyspieszenia
    turtle.hideturtle()  # ukrycie glowki zolwika
    turtle.penup() # podnosimy zolwia, zeby nie mazal nam linii podczas ruchu

    ostatnie_rysowanie = 0  # ile kropek temu zostal odrysowany rysunek

    for i in xrange(ILE_KROPEK):
        # losujemy wierzcholek do ktorego bedziemy zmierzac	
        do = random.choice(WIERZCHOLKI)
        # bierzemy nasza aktualna pozycje 
        teraz = turtle.position()
        # ustawiamy sie w polowie drogi do wierzcholka, ktorego wczesniej obralismy
        turtle.setpos(w_polowie_drogi(teraz, do))
        # stawiamy kropke w nowym miejscu
        turtle.dot(1)
        ostatnie_rysowanie += 1
        if ostatnie_rysowanie == OKRES_ODSWIEZENIA:
            # postawilismy na tyle duzo kropek, zeby odswiezyc rysunek
            turtle.update()
            ostatnie_rysowanie = 0

    pozdrowienia()

    turtle.update()

if __name__ == "__main__":
    rysuj()
