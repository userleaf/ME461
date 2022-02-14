import numpy as np
greedyLength = 301
boxSize = 50
halfBox = 25
nCorr = 8
colorz = {'black': ((1, 1, 1), 0, 13),
        'clr100':((225, 1, 1), 100, 1),
        'clr50':((1, 255, 1), 50, 2),
        'clr30':((1, 1, 255), 30, 2),
        'clr20':((200, 200, 1), 20, 2),
        'clr10':((255, 1, 255), 10, 2),
        'clr9':((1, 255, 255), 9, 3),
        'clr8':((1,1,150), 8, 3),
        'clr7':((120,120,40), 7, 3),
        'clr6':((150,1,150), 6, 3),
        'clr5':((1,150,150), 5, 3),
        'clr4':((222,55,222), 4, 3),
        'clr3':((1, 99, 55), 3, 3),
        'clr2':((200, 100, 10),2, 3),
        'clr1':((100, 10, 200),1, 3)
}

class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):

        self.name = userName  # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize  # maximum length of the returned path from run()
        self.maxTime = maxTime  # run() is supposed to return before maxTime
        self.colorz = clrDictionary
        self.grid = []
        for i in range(1, nCorr):
            self.grid.append([])
            for j in range(1, nCorr):
                node = Node(i, j)
                self.grid[i - 1].append(node)
        
    def run(self, img, info):
        # get info
        self.info = info
        self.myX,self.myY = self.info[self.name][0]
        
        # get the nodes closer than 401 steps
        myQueue = [float("inf")]
        target = []
        array = []
        for row in self.grid:
            for node in row:
                
                node.x_dist(self.myX)
                node.y_dist(self.myY)
                node.manDistance()
                 
                if node.man < greedyLength:
                    for dClr in colorz:
                        if tuple(img[node.x, node.y, :]) == colorz[dClr][0]:
                            node.update_points(colorz[dClr][1])
                        
                    if node.man-node.points*2 < myQueue[0] and not node.points == 0:
                        myQueue[0] = node.man-node.points
                        target = [node.x,node.y]
                        
        
        x,y = target
        #call create route here
        routeX,routeY = create_route(self.myX,x,self.myY,y)
        array.append(routeX)
        array.append(routeY)
        array = [ele for ele in array if ele != []]
        
        if get_distance(x,self.myX,y,self.myY) < 95:
            ##make it a function after here and call it
            self.myX,self.myY = array[-1]
            myQueue = [float("inf")]
            target = []
            for row in self.grid:
                for node in row:
                    if node.x == x and node.y == y:     
                        node.points = 0
                    else:  
                        pass  
                    
                    node.x_dist(self.myX)
                    node.y_dist(self.myY)
                    node.manDistance()
                    
                    if node.man < greedyLength:
                        
                        if node.man-node.points*2 < myQueue[0] and not node.points == 0:
                                
                            myQueue[0] = node.man-node.points
                            target = [node.x,node.y]
           
            x,y = target
            routeX,routeY = create_route(self.myX,x,self.myY,y)
            array.append(routeX)
            array.append(routeY)
            array = [ele for ele in array if ele != []]
            
            
        return array

def create_route(x1,x2,y1,y2):
    rx = [x1,y1]
    
    if x1 >=  x2 + 25:
        rx = [x2+24,y1]
        ry = [x2+24,y1]
    elif x1 <= x2 -25:
        rx = [x2-24,y1]
        ry = [x2-24,y1]
    else:
        rx =[]
        ry = [x1,y1]
           
    if y1 >=  y2 + 25:
        ry[1] = y2 + 24
    elif y1 <= y2 -25:
        ry[1] = y2 - 24
    else:
        ry = []
    

    return rx,ry

def get_distance(x1,x2,y1,y2):
    return abs(x1-x2)+abs(y1-y2)

class Node:
    def __init__(self,row,column):
        self.row = row
        self.col = column
        self.x = self.row * 2 * boxSize - halfBox
        self.y = self.col * 2 * boxSize - halfBox
        self.points = 0
        
    def update_points(self,points):
        self.points = points

    def x_dist(self,myX):
        self.dX = abs(myX - self.x)
        

    def y_dist(self,myY):
        self.dY = abs(myY - self.y)
        

    def manDistance(self):
        self.man = self.dX + self.dY
        
