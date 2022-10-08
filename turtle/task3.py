# Task 3. Narysować fraktal Sierpinskiego

import turtle

turtle.speed('fastest')

def draw_sierpinski(length, depth):
    if depth==0:
        for x in range(0,3):
            turtle.forward(length)
            turtle.left(120)
    else:
        draw_sierpinski(length/2, depth-1)
        turtle.forward(length/2)
        draw_sierpinski(length/2, depth-1)
        turtle.backward(length/2)
        turtle.left(60)
        turtle.forward(length/2)
        turtle.right(60)
        draw_sierpinski(length/2, depth-1)
        turtle.left(60)
        turtle.backward(length/2)
        turtle.right(60)


draw_sierpinski(300,5)
turtle.done()