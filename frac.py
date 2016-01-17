import random
from random import random as rn
import turtle

turtle.setworldcoordinates(-10, -1, 10, 19)

def move(start, transformation):
    x, y = start
    a, b, c, d, e, f = transformation
    return a * x + b * y + e, c * x + d * y + f
    
def scale_point(point, scale=2):
    x, y = point
    return scale * x, scale * y
    
def choose(weights):
    colors = ["red", "green", "blue", "yellow",
			  "purple", "pink"]
    sum_weights = sum(weights)
    normalized = [w / sum_weights for w in weights] 
    rand = rn()
    total_weight = 0
    for i, weight in enumerate(normalized):
        total_weight += weight
        if rand < total_weight:
            turtle.color(colors[i])
            return i


iterations = 100000
refresh_freq = 10


transformations = [
    (.0, .0, .0, .16, .0, .0),
    (.85, .04, -.04, .85, 0, 1.6),
    (.2, -.26, .23, .22, 0, 1.6),
    (-.15, .28, .26, .24, 0, .44),
]

weights = [.1, 6.9, .6, .3]

_transformations = [
    (.382, .0, .0, .382, .3, .619),
    (.382, .0, .0, .382, .6, .4),
    (.382, .0, .0, .382, .01, .4),
    (.382, .0, .0, .382, .12, .059),
    (.382, .0, .0, .382, .49, .059),
]

_weights = [1., 1., 1., 1., 1.]

turtle.tracer(0, 0)
turtle.hideturtle()
turtle.penup()

point = (100, 100)

to_refresh = refresh_freq

for _ in xrange(iterations):
    point = move(point, transformations[choose(weights)])
    turtle.setpos(scale_point(point))
    turtle.dot(1)
    
    to_refresh -= 1
    
    if to_refresh == 1:
        turtle.update()
        to_refresh = refresh_freq
    
turtle.exitonclick()
