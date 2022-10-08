# Task 2. Narysować fraktal

import turtle

turtle.speed('fastest')

x = 300
    
while x > 1:
    turtle.forward(x)
    turtle.left(90)

    turtle.forward(x)
    turtle.left(90)

    turtle.forward(x)
    turtle.left(90)

    turtle.forward(x)
    turtle.left(90)

    x*=0.9

turtle.done()