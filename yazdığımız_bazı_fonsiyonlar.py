
frames+=1


if frames-last_frame>=40:
    last_frame=frames

if frames-last_frame==10:
    for i in cp: # move all the balls
        for j in cp: # check for collisions
            if i != j:
                if dist(i,j)*0.9 < j.r+i.r and i.x>1+i.r and i.x<w-i.r+1 and i.y>1+i.r and i.y<h-i.r+1 and j.x>1+j.r and j.x<w-j.r+1 and j.y>1+j.r and j.y<h-j.r+1: # if the balls are touching
                    sticky_balls.append(i)
                    sticky_balls.append(j)
    
if frames-last_frame>=30:
    for i in sticky_balls:
        for j in sticky_balls:
            if i != j:
                if dist(i,j) < j.r+i.r and i.x>1+i.r and i.x<w-i.r+1 and i.y>1+i.r and i.y<h-i.r+1 and j.x>1+j.r and j.x<w-j.r+1 and j.y>1+j.r and j.y<h-j.r+1: # if the balls are touching
                    #i.vx,i.vy,j.vx,j.vy = 4,4,-4,-4
                    i.x,i.y,j.x,j.y=j.x+2*j.r,j.y+2*j.r,i.x+2*i.r,i.y+2*i.r





    for i in cp:
        if i.corner:
            if i.color!=0:
                corner_placeholder=triangle.select_corner_ball()
                if len(corner_placeholder)==3:
                    corners=corner_placeholder
                    ucgen.update_triangle()
                    is_there_a_triangle=True
                else:
                    is_there_a_triangle=False
                    pass




from tkinter import *
import time
from random import randint
from math import *
import numpy as np

colors=['red','green','blue'] # colors for the balls
w,h=800,600 # width and height of the window
high_treshold=15
low_treshold=11
r=20
counter=0
is_there_a_triangle=False

corners=[] # this is for creating the corners of the triangle
cp=[] # list of balls
sticky_balls=[]

gui = Tk() # create a window
gui.geometry("{}x{}".format(w,h)) # set the size of the window
gui.title("ballz") # set the title of the window
canvas = Canvas(gui, width=w, height=h, bg='#111111') # create a canvas
canvas.pack() # put the canvas on the window

class ball:
    '''
    this is the class for the ball
    '''
    def __init__(self, color, x=0, y=0, r=5, vx=2,vy=2,corner=False,isittouching=False):
        '''
        color is the color of the ball
        x,y are the coordinates of the ball
        r is the radius of the ball
        vx,vy are the velocities of the ball
        '''
        self.corner=corner
        self.x = x # x position
        self.y = y # y position
        self.vx = vx # x velocity
        self.vy = vy # y velocity
        self.color = color # color of the ball
        self.r = r # radius of the ball
        self.isittouching=isittouching
        self.circle=canvas.create_oval(x-r,y-r,x+r,y+r,fill=colors[color]) # the ball itself

    def __str__(self): # this is for printing the ball
        return f'object at {self.__x},{self.__y}' # this is for printing the ball
    
    def dist(self,otherball): # this is for calculating the distance between two balls
        return sqrt((self.x - otherball.x)**2 + (self.y - otherball.y)**2) # this is for calculating the distance between two balls
    
    def pos(self): # this is for returning the position of the ball
        return canvas.coords(self.circle) # this is for returning the position of the ball

    def change_color(self,color):
        '''
        this is for changing the color of the ball
        '''
        self.color = color
        canvas.itemconfig(self.circle,fill=colors[color]) # this is for changing the color of the ball
    
    def move(self): # this is for moving the ball
        '''
        this is for moving the ball
        '''
        self.x += self.vx # this is for moving the ball
        self.y += self.vy # this is for moving the ball
        canvas.coords(self.circle,self.x-self.r,self.y-self.r,self.x+self.r,self.y+self.r) # this is for moving the ball
    
    def teleport(self,x,y):
        '''
        this is for teleporting the ball
        '''
        self.x = x
        self.y = y
        self.move()

    def split(ball1,ball2):
        '''
        this function removes the ball from cp and creates another two balls arround destroyed ball
        '''
        global cp

        new_ball1 = ball(ball1.color,ball1.x-ball1.r,ball1.y-ball1.r,ball1.r/2,-ball1.vx,-ball1.vy,False)
        new_ball2 = ball(ball1.color,ball1.x+ball1.r,ball1.y-ball1.r,ball1.r/2,-ball1.vx,ball1.vy,False)
        new_ball3 = ball(ball2.color,ball2.x-ball2.r,ball2.y+ball2.r,ball2.r/2,-ball2.vx,ball2.vy,False)
        new_ball4 = ball(ball2.color,ball2.x+ball2.r,ball2.y+ball2.r,ball2.r/2,-ball2.vx,-ball2.vy,False)
        cp.append(new_ball1)
        cp.append(new_ball2)
        cp.append(new_ball3)
        cp.append(new_ball4)
        canvas.itemconfig(new_ball1.circle,fill=colors[new_ball1.color])
        canvas.itemconfig(new_ball2.circle,fill=colors[new_ball2.color])
        canvas.itemconfig(new_ball3.circle,fill=colors[new_ball3.color])
        canvas.itemconfig(new_ball4.circle,fill=colors[new_ball4.color])
        canvas.update()

    def join(ball1,ball2):
        '''
        this function removes balls and creates one ball
        '''
        global cp
        new_ball = ball(ball1.color,ball1.x,ball1.y,ball1.r+ball2.r,(ball1.vx+ball2.vx)/2,(ball1.vy+ball2.vy)/2,False)
        cp.append(new_ball)
        canvas.itemconfig(new_ball.circle,fill=colors[new_ball.color])
        canvas.update()
      
class triangle:
    '''
    this class creates a triangle from the center randomly selected three red balls
    '''
    def __init__(self):
        corner1,corner2,corner3=corners
        x1,y1,x2,y2,x3,y3=corner1.x,corner1.y,corner2.x,corner2.y,corner3.x,corner3.y
        self.corner1=corner1
        self.corner2=corner2
        self.corner3=corner3
        self.x1=x1
        self.x2=x2
        self.x3=x3
        self.y1=y1
        self.y2=y2
        self.y3=y3
        self.triangle=self.update_triangle()

    def select_corner_ball():
        '''
        select three random red balls
        '''
        coords=[]
        counter=0
        for i in cp:
            i.corner=False
    
        
        for i in cp:
            if i.color==0 and counter<3:
                i.corner=True
                counter+=1
        
        for i in cp:
            if i.corner==True:
                coords.append(i)
        return coords
    
    def update_triangle(self):
        corner1,corner2,corner3=corners
        self.x1,self.y1,self.x2,self.y2,self.x3,self.y3=corner1.x,corner1.y,corner2.x,corner2.y,corner3.x,corner3.y
        try:
            canvas.delete('tri')
        except:
            pass

        return canvas.create_polygon(self.x1,self.y1,self.x2,self.y2,self.x3,self.y3,outline=colors[0],fill='',tags='tri')
    
    def is_the_ball_in_the_triangle(self,ball):
        '''
        this is for checking if the ball is in the triangle
        '''

        c1,c2,c3=[self.x1,self.y1] , [self.x2,self.y2] , [self.x3,self.y3]
        ball_coord=[ball.x,ball.y]
        a1=getAngle(c1,ball_coord,c2)
        a2=getAngle(c2,ball_coord,c3)
        a3=getAngle(c3,ball_coord,c1)
        if abs(a1+a2+a3-360)<=0.0001:
            print(a1+a2+a3)
            return True
        else:
            return False

def area(x1, y1, x2, y2, x3, y3):
 
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1)
                + x3 * (y1 - y2)) / 2.0)

def dist(i,j): # this is for calculating the distance between two balls
    return sqrt((i.x-j.x)**2+(i.y-j.y)**2) # this is for calculating the distance between two balls

def is_the_triangle_small():
    '''
    this function checks if the triangle is small
    '''
    global corners
    corner1,corner2,corner3=corners
    x1,y1,x2,y2,x3,y3=corner1.x,corner1.y,corner2.x,corner2.y,corner3.x,corner3.y
    A = area (x1, y1, x2, y2, x3, y3)
    h1,h2,h3=A/(sqrt((x1-x2)**2+(y1-y2)**2))+0.01,A/(sqrt((x2-x3)**2+(y2-y3)**2))+0.01,A/(sqrt((x3-x1)**2+(y3-y1)**2))+0.01
    if h1<=2*r or h2<=2*r or h3<=2*r:
        return True
    else:
        return False

def create_new_random_triangle():
    '''
    create a new random triangle from red balls
    ''' 
    cornerlarim=corners
    cornerlarim=triangle.select_corner_ball()
    for i in cp:
        if i.corner==False and i.color==0:
            cornerlarim[0]=i
    return cornerlarim

def is_it_touching_the_triangle(ball):
    '''
    check if the ball touches the triangle's lines
    '''
    global corners
    corner1,corner2,corner3=corners
    c1,c2,c3=[corner1.x,corner1.y],[corner2.x,corner2.y],[corner3.x,corner3.y]
    ball_coord=[ball.x,ball.y]
    a1=getAngle(c1,ball_coord,c2)
    a2=getAngle(c2,ball_coord,c3)
    a3=getAngle(c3,ball_coord,c1)
    print(a1,a2,a3)
    if a1>=170 or a2>=170 or a3>=170:
        return True
    else:
        return False

def unstuck_the_ball(i,j):
    '''
    this function checks if the ball is stuck and fixes it recursively until they are no
    longer touching
    '''

    if dist(i,j) < j.r+i.r and i.x>1+i.r and i.x<w-i.r+1 and i.y>1+i.r and i.y<h-i.r+1 and j.x>1+j.r and j.x<w-j.r+1 and j.y>1+j.r and j.y<h-j.r+1: # if the balls are touching    
        i.move() # move the ball
        j.move() # move the ball
        unstuck_the_ball(i,j)
    else:
        pass

def getAngle(a, c, b):
    '''
    get the angle of abc from coordinates
    '''
    da=dista(b,c)
    db=dista(a,c)
    dc=dista(a,b)
    try:
        return degrees(acos((da**2+db**2-dc**2)/(2*da*db)))
    except:
        return inf

def dista(a,b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def triangle_bounce(ball):
    '''
    this function determines the bounce direction when the ball hits the triangle
    '''
    global corners
    corner1,corner2,corner3=corners
    c1,c2,c3=[corner1.x,corner1.y],[corner2.x,corner2.y],[corner3.x,corner3.y]
    ball_coord=[ball.x,ball.y]
    mx=c1[0]+c2[0]+c3[0]/3
    my=c1[1]+c2[1]+c3[1]/3
    v=sqrt(ball.vx**2+ball.vy**2)
    if ball.color==2:
        dx=(ball.x-mx)/mx
        dy=(ball.y-my)/my
    elif ball.color==1:
        dx=(mx-ball.x)/mx
        dy=(my-ball.y)/my
    ball.vx=v*dx
    ball.vy=v*dy

for i in range(3): # create 3 red balls
    cp.append(ball(color=0, x=randint(50,750),y=randint(50,550),r=20,vx=randint(1,4),vy=randint(1,4))) # create a red ball

for i in range(randint(4,5)): # create some balls
    cp.append(ball(color=randint(0,2), x=randint(50,750),y=randint(50,550),r=20,vx=randint(1,4),vy=randint(1,4))) # create a ball

corners=triangle.select_corner_ball() # this is for selecting three random red balls
ucgen=triangle() # create a triangle

while True:

    if is_the_triangle_small and is_there_a_triangle: # if the triangle is small and there is a triangle
        try:
            corners=create_new_random_triangle() # create a new random triangle
            ucgen=triangle() # create a new triangle with the new corners
            ucgen.update_triangle() # update the triangle
        except:
            pass

    for ii,i in enumerate(cp): # split and merge the balls
        for jj,j in enumerate(cp):
            if ii > jj and dist(i,j) < i.r+j.r : # if the balls are touching
                if i.r>high_treshold and j.r>high_treshold and i.r==j.r and i.corner==False and j.corner==False: # if the balls are big enough  
                    ball.split(i,j) # split the balls
                    canvas.delete(i.circle) # delete the balls
                    canvas.delete(j.circle) # delete the balls
                    cp.remove(i)      # remove the balls from the list
                    cp.remove(j)    # remove the balls from the list
                    break
                if i.r<low_treshold and j.r<low_treshold and i.r==j.r and i.corner==False and j.corner==False: # if the balls are small enough
                    ball.join(i,j) # join the balls
                    canvas.delete(i.circle) # delete the balls
                    canvas.delete(j.circle) # delete the balls
                    cp.remove(i)     # remove the balls from the list
                    cp.remove(j)  # remove the balls from the list
                    break
                else:
                    pass

    for i in cp: # move all the balls
        position=i.pos() # get the position of the ball
        if i.color != 2: # if the ball is not blue        
            if position[3] >= h or position[1] <= 0: # if the ball hits the bottom or top
                i.vy = -i.vy # reverse the y velocity
            if position[2] >= w or position[0] <= 0: # if the ball hits the right or left
                 i.vx = -i.vx # reverse the x velocity
        else: # if the ball is blue
            if i.y >= h+i.r :
                i.teleport(i.x,4-i.r)
            elif i.y <= 0-i.r: 
                i.teleport(i.x,h+i.r-4)
            elif i.x >= w+i.r :
                i.teleport(4-i.r,i.y)
            elif i.x <= 0-i.r: 
                i.teleport(w+i.r-4,i.y)
        
        if i.corner==False:
            if ucgen.is_the_ball_in_the_triangle(i) and is_there_a_triangle: # if the ball is in the triangle
                if i.color==1 and is_it_touching_the_triangle(i) :  # if the ball is green and touches the triangle
                    i.vx,i.vy=-i.vx,-i.vy # reverse the x and y velocity
                    i.move() # move the ball
                    
            if ucgen.is_the_ball_in_the_triangle(i)==False and is_there_a_triangle:
                if i.color==2 and is_it_touching_the_triangle(i):
                    i.vx,i.vy=-i.vx,-i.vy
        else:
            pass
        
        for j in cp: # check for collisions
            if i != j:
                if dist(i,j) < j.r+i.r and i.x>1+i.r and i.x<w-i.r+1 and i.y>1+i.r and i.y<h-i.r+1 and j.x>1+j.r and j.x<w-j.r+1 and j.y>1+j.r and j.y<h-j.r+1: # if the balls are touching    
                    i.isittouching=True
                    j.isittouching=True

                    i.vx,i.vy,j.vx,j.vy = j.vx,j.vy,i.vx,i.vy # swap the velocities
                    if i.color == j.color: # if the balls are the same color
                        i.change_color((i.color+1)%3) # change the color of the ball
                        j.change_color((j.color+2)%3) # change the color of the ball
                    else :# if the balls are different colors
                        for renk in range(3):
                            if renk != i.color and renk != j.color:
                                j.change_color(renk)
                                i.change_color(renk)
                                break
            if i.x<i.r or i.x>w-i.r or i.y<i.r or i.y>h-i.r:
                i.isittouching=True

        i.move() # move the ball

    for i in cp:
        for j in cp:
            if i != j and i.isittouching==True and j.isittouching==True:
                unstuck_the_ball(i,j)
                i.isittouching=False
                j.isittouching=False
    canvas.delete('tri')

    try:
        ucgen.update_triangle() # update the triangle
    except:
        pass

    for i in cp: # change triangle if one of the red balls changed color
        if i.corner: # if the ball is a corner of triangle
            if i.color!=0: # if its color is not red
                corner_placeholder=triangle.select_corner_ball() #call class function to cast corner list
                if len(corner_placeholder)==3: # if 3 corners availible
                    corners=corner_placeholder # placeholder can be casted to global corners list
                    ucgen.update_triangle() # update the triangle
                    is_there_a_triangle=True # change is_there_a_triangle boolean to True
                else:
                    is_there_a_triangle=False # change is_there_a_triangle boolean to False
                    canvas.delete('tri') # delete the triangle
    
    if not is_there_a_triangle:    # if there is not a triangle
        corner_placeholder=triangle.select_corner_ball() #call class function to cast corner list
        if len(corner_placeholder)==3: # if 3 corners availible
            corners=corner_placeholder# placeholder can be casted to global corners list
            ucgen.update_triangle() # update the triangle
            is_there_a_triangle=True # change is_there_a_triangle boolean to True
        else:
            is_there_a_triangle=False # change is_there_a_triangle boolean to False
            canvas.delete('tri') # delete the triangle
    else:
        pass
    gui.update() # update the window
    time.sleep(.08) # wait a bit

gui.mainloop # keep the window open
