import numpy as np
import time
greedyLength = 301
boxSize = 50
nCorr = 8
colorz = {
        'black':((1,1,1), 0, 13),
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

    def _init_(self, userName, clrDictionary, maxStepSize, maxTime):

        self.name = userName  # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize  # maximum length of the returned path from run()
        self.maxTime = maxTime  # run() is supposed to return before maxTime

    def run(self, img, info):
        # get time
        startTime = time.time()

        grid = []
        for i in range(1, nCorr):
            grid.append([])
            for j in range(1, nCorr):
                for dClr in colorz:
                    if tuple(img[i * 2 * boxSize - boxSize, j * 2 * boxSize - boxSize, :]) == colorz[dClr][0]:
                        node = Node(i, j, colorz[dClr][1])
                        grid[i - 1].append(node)
        
        # get info
        self.info = info
        self.myX,self.myY = self.info[self.name][0]
        
        # get the nodes closer than 201 steps
        myQueue = [float("inf")]
        target = []
        array = []
        for row in grid:
            for node in row:
                xDistance = node.x_dist(self.myX)
                yDistance = node.y_dist(self.myY)
                manDistance = node.manDistance()
                 
                if manDistance < greedyLength:
                    
                    if node.man-node.points*2 < myQueue[0] and not node.points == 0:
                        myQueue[0] = node.man-node.points
                        target = [node.x,node.y]
                        
        
        x,y = target
        array.append([x,self.myY])
        if not y == self.myY: 
            array.append([x,y])
        try:
            array.remove([self.myX,self.myY])
        except:
            pass
        #if get_distance(x,self.myX,y,self.myY) < 50:
        #    self.run(img,)
        return array
#def get_distance(x1,x2,y1,y2):
#    return abs(x1-x2)+abs(y1-y2)
class Node:
    def _init_(self,row,column,points):
        self.row = row
        self.col = column
        self.points = points
        self.x1 = self.row * 2 * boxSize - boxSize
        self.y1 = self.col * 2 * boxSize - boxSize
        self.x2 = self.x1 + boxSize
        self.y2 = self.y1 + boxSize

        
    def x_dist(self,myX):
        dX1 = abs(myX - self.x1)
        dX2 = abs(myX - self.x2)
        if dX1 < dX2:
            self.xd = dX1
            self.x = self.x1+2
        else: 
            self.xd = dX2
            self.x = self.x2-2
        return self.xd

    def y_dist(self,myY):
        dY1 = abs(myY - self.y1)
        dY2 = abs(myY - self.y2)
        if dY1 < dY2:
            self.yd = dY1
            self.y = self.y1+2
        else: 
            self.yd = dY2
            self.y = self.y2-2

        return self.yd

    def manDistance(self):
        self.man = self.xd + self.yd
        return self.man
