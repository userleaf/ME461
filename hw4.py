from math import *
from tkinter import *

class ball:

    def __init__(self, color, x=0, y=0, r=5):
        self.__x = -1
        self.__y = -1

        self.x = x
        self.y = y

    def __str__(self):
        return f'object at {self.__x},{self.__y}'

    def __add__(self, otherpoint):
        return ball(self.x + otherpoint.x, self.y + otherpoint.y)

    def dist(self):
        return sqrt(self.__x**2 + self.__y**2)

    @property
    def y(self):
        return __y

    @y.setter
    def y(self, value):
        if str(value).isnumeric():
            self.__y = value
        else:
            print('{} is not a value'.format(value))

    @property
    def x(self):
        return __x

    @x.setter
    def x(self, value):
        if str(value).isnumeric():
            self.__x = value
        else:
            print('{} is not a value'.format(value))

class vector(ball):

    def __init__(self,vx=5,vy=5,x=5,y=5):
        self.vx = vx
        self.vy = vy
        super().__init__(x,y)

    def __str__(self):
        return 'this is vector class'





    def __init__(self,color,x1,y1,x2,y2,x3,y3):
        '''
        color is the color of the triangle
        x1,y1,x2,y2,x3,y3 are the coordinates of the three red balls
        '''
        self.color = color
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.triangle = canvas.create_polygon(x1,y1,x2,y2,x3,y3,fill=colors[color])
    
    def __str__(self): # this is for printing the triangle
        return f'object at {self.__x},{self.__y}' # this is for printing the triangle
    
    def pos(self): # this is for returning the position of the triangle
        return canvas.coords(self.triangle) # this is for returning the position of the triangle
    
    def move(self): # this is for moving the triangle
        '''
        this is for moving the triangle
        '''
        self.x1 += self.vx
        self.y1 += self.vy
        self.x2 += self.vx
        self.y2 += self.vy
        self.x3 += self.vx
        self.y3 += self.vy
        canvas.coords(self.triangle,self.x1,self.y1,self.x2,self.y2,self.x3,self.y3) # this is for moving the triangle
    