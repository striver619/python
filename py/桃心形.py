#桃心形曲线参数方程:
#x=a·15·(sin θ)³
#y=a(15cosθ-5cos2θ-2cos3θ-cos4θ)
from turtle import *
from math import pi, sin, cos

color("red")
up()

a, t = 10, 0

begin_fill()

while t <= 2 * pi:
    x = a * 15 * sin(t) ** 3
    y = a * (15 * cos(t) - 5 * cos(2 * t) - 2 * cos(3*t) - cos(4*t))
    goto(x,y)

    down()

    t = t + 0.01
end_fill()

ht()
