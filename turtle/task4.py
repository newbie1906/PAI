# Task 4. Narysować 2 dowolne fraktale.

import turtle

turtle.speed('fastest')

def draw_snowflake(length, depth):
    if depth==0:
        turtle.forward(length)
        return
    else:
        draw_snowflake(length/3, depth-1)
        turtle.left(60)
        draw_snowflake(length/3, depth-1)
        turtle.right(120)
        draw_snowflake(length/3, depth-1)
        turtle.left(60)
        draw_snowflake(length/3, depth-1)

def create_snowflake(length, depth):
    for x in range(depth):
        draw_snowflake(length, depth)
        turtle.right(360 / depth)


def draw_tree(length):
    if length < 10:
        return
    else:
        turtle.forward(length)
        turtle.left(30)
        draw_tree(3*length/4)
        turtle.right(60)
        draw_tree(3*length/4)
        turtle.left(30)
        turtle.backward(length)

def create_trees(length, sides):
    for x in range(sides):
        draw_tree(50)
        turtle.right(360 / sides)

create_trees(50, 6) # fraktal drzewo dobry length 50
# create_snowflake(300,4) # fraktal płatek śniegu

turtle.done()