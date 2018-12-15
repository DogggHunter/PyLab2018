from turtle import *
import math


def draw_line(dist, left_deg):
    fd(dist)
    lt(left_deg)


def draw_triangle(dist):
    begin_fill()
    for i in range(3):
        draw_line(dist, 120)
    end_fill()


def recursion_draw(distance, depth, x1, y1):
    if depth > 1:
        pu()
        sety(y1)
        setx(x1)
        y = ycor()
        x = xcor()
        height = y + math.sqrt((distance * 4) ** 2 - (((distance * 4) / 2) ** 2)) / 2
        sety(height)
        pd()
        draw_triangle(distance)
        pu()
        sety(y)
        setx(x - distance)
        pd()
        draw_triangle(distance)
        pu()
        setx(x + distance)
        pd()
        draw_triangle(distance)
        recursion_draw(distance / 2, depth - 1, xcor(), ycor())
        recursion_draw(distance / 2, depth - 1, x - distance, y)
        recursion_draw(distance / 2, depth - 1, x, height)


def draw_sierpinski_triangle(dist, depth):
    pu()
    setpos(-150, -100)
    pd()
    color('red', 'red')
    draw_triangle(dist)
    if depth == 0:
        return
    elif depth >= 1:
        color('black', 'black')
        draw_line(dist/2, 60)
        draw_triangle(dist/2)
        distance = dist/4
        recursion_draw(distance, depth, xcor(), ycor())


draw_sierpinski_triangle(300, 5)
done()
