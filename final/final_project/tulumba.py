import numpy as np 
import itertools
class Node:
    
    def __init__(self,pos,parent=None):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self,other):
        return self.f < other.f

    def __eq__(self,other):
        return self.pos == other.pos

    def manhattan(self,end):
        global prescalar
        return prescalar*(abs(self.pos[0] - end.pos[0]) + abs(self.pos[1] - end.pos[1]))

    def __str__(self):
        return str(self.pos)

class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
        self.name = userName # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize # maximum length of the returned path from run()
        self.maxTime = maxTime # run() is supposed to return before maxTime
        self.maxPoint = 100 # maximum points you can have
        vals = list(clrDictionary.values())  # get the values of the color dictionary
        vals.append([(0,0,0),0,1])  # add black to the list of values
        vals.append([(255,255,255),0,1])  # add white to the list of values
        self.colorVals = {}  # create a dictionary of colors
        for i,j,k in vals:  # for each color in the list of values
            self.colorVals[i] = j  # add the color to the dictionary
        self.arena = np.zeros((15,15),dtype=int)  # create a 15x15 arena

    def run(self, img, info):  # img is a 2D numpy array, info is a dictionary
        self.oppPos = []  # list of opponent's positions
        self.scores = []  # list of scores
        self.info = info  # dictionary of info
        self.myPos=self.info[self.name][0]  # your position
        self.myPoints=self.info[self.name][1]  # your points
        self.my_ij = [int((self.myPos[0])/50),int((self.myPos[1])/50)]  # your position in the arena

        for player in self.info:  # for each player
            if player != self.name:  # if it's not you
                self.oppPos.append(self.info[player][0])  # add the position to the list of opponent's positions
        for i in range(7):  # for each castle
            for j in range(7):
                self.arena[2*i+1][2*j+1] = self.colorVals[tuple(img[(2*i+1)*50+25][(2*j+1)*50+25])] # add the color value to the arena
                if self.arena[2*i+1][2*j+1] != 0:  # if the color value is not 0
                    self.scores.append([self.arena[2*i+1][2*j+1],(25+(2*i+1)*50,25+(2*j+1)*50),(2*i+1,2*j+1)])  # add the score to the list
                    # self.scores
        self.scores.sort(key=lambda x: x[0], reverse=True) # sort the scores in descending order
        if not len(self.oppPos):
            return self.soloRunner()
        target = self.chooseTarget()  # choose the target
        return self.chooseRoute(target)  # choose the route to the target and return

    def chooseTarget(self):  # choose the target
        for i in range(len(self.scores)):  # for each score
            counter=0  # counter for the number of opponents
            if self.scores[i][0] > self.myPoints:  # if the color value is greater than your points
                self.scores[i][0] = -1  # set the color value to -1
            else:
                for j in range(len(self.oppPos)):  # for each opponent
                    if not self.amICloser(self.scores[i][1],self.oppPos[j]):  # if the opponent is closer to the castle
                        self.scores[i][0] = 0  # set the score to 0
                    else:    # if the opponent is not closer to the castle
                        counter+=1  # add 1 to the counter
                if counter == len(self.oppPos):  # if the counter is equal to the number of opponents and the score is less than or equal to yours
                    return self.scores[i][2]  # return the coordinates of the castle
        # if no target is found, return the biggest one
        for i in range(len(self.scores)): # for each score
            if self.scores[i][0] != -1: # if the color value is less than or equal to your points
                return self.scores[i][2]  # return the coordinates of the castle
    
    def chooseRoute(self, target):  # target is a coordinate
        costMap = np.ones((15,15),dtype=int)*100  # create a 15x15 cost map
        imin=max(min(self.my_ij[0],target[0])-1,0) 
        imax=min(max(self.my_ij[0],target[0])+1,14)  
        jmin=max(min(self.my_ij[1],target[1])-1,0)
        jmax=min(max(self.my_ij[1],target[1])+1,14)

        for i in range(imin,imax+1):  # for each row
            for j in range(jmin,jmax+1):  # for each column
                if self.arena[i][j] <= self.myPoints:  # if the color value is less than or equal to your points
                    costMap[i][j] -= self.arena[i][j]  # subtract the color value from the cost map
                else: # if the color value is greater than your points
                    costMap[i][j] = -1 # set the cost map to -1

        costMap = costMap[imin:imax+1,jmin:jmax+1]  # crop the cost map
        start = [self.my_ij[0]-imin,self.my_ij[1]-jmin]  # start position
        end = [target[0]-imin,target[1]-jmin]  # end position
        pathArena = astar(start,end,costMap,presclr=20)  # find the path using A*
        pathArena = [[index[0]+imin,index[1]+jmin] for index in pathArena]  # add the offset
        return self.move(pathArena)  # return the path

    def move(self,selectedPath):  # selectedPath is a list of coordinates in the arena
        selectedPath.reverse()  # reverse the path
        selectedPath.pop(0)
        for i in range(len(selectedPath)):
            selectedPath[i][0]*=50  # multiply the coordinates by 50
            selectedPath[i][1]*=50  # multiply the coordinates by 50
            selectedPath[i][0]+=25  # add 25 to the x coordinate
            selectedPath[i][1]+=25  # add 25 to the y coordinate
        path = [create_route(self.myPos[0], selectedPath[0][0], self.myPos[1], selectedPath[0][1])]
        for i in range(1,len(selectedPath)):
            path.append(create_route(path[i-1][0], selectedPath[i][0], selectedPath[i-1][1], selectedPath[i][1]))
        return path 

    def amICloser(self, castle, opponent):  # castle is a coordinate, opponent is a coordinate
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):  # opponent is closer
            return False  # return False
        return True  # return True
    
    def soloRunner(self):
        myTargets = self.scores[:7]
        # print(self.scores)
        for i in range(len(self.scores)):
            if self.scores[i][0] == 1:
                append=self.scores[i]
        myTargets.append(append)
        for i in range(7):
            for j in range(7):
                counter=0
                for k in myTargets:
                    if k[2]!=(2*i+1,2*j+1):
                        counter += 1
                    else:
                        self.arena[2*i+1][2*j+1] = k[0]
                    if counter == 8 and self.arena[2*i+1][2*j+1] != 0:
                        self.arena[2*i+1][2*j+1] = -1
        mymin=1000
        for i in range(len(myTargets)):
            if manhattan(self.myPos,myTargets[i][1]) < mymin:
                mymin = manhattan(self.myPos,myTargets[i][1])
                my_min = myTargets[i]
        myTargets.remove(my_min)
        mymin=1000
        for i in range(len(myTargets)):
            if manhattan(self.myPos,myTargets[i][1]) < mymin:
                mymin = manhattan(my_min[1],myTargets[i][1])
                my_min_2 = myTargets[i]
        myTargets.remove(my_min_2)

        myCoords=[]
        for i in range(len(myTargets)):
            myCoords.append(myTargets[i][1])
        permutations = list(itertools.permutations(myCoords))
        lastLen=float('inf')
        for i in range(len(permutations)):
            sumLen=0
            for j in range(len(permutations[i])):
                if j == 0:
                    sumLen = manhattan(my_min_2[1],permutations[i][j])
                else:
                    sumLen += manhattan(permutations[i][j-1],permutations[i][j])


            if lastLen > sumLen:
                lastLen = sumLen
                my_path = permutations[i]

        my_path = list(my_path)
        my_path.insert(0,my_min_2[1])
        my_path.insert(0,my_min[1])
        resultantPath=[]
        print(my_path)

        for i in range(1,len(my_path)):
            resultantPath.append(free_corridor(my_path[i-1][0],my_path[i-1][1],my_path[i][0],my_path[i][1]))
        # flatten resultantPath
        print(resultantPath)

        return my_path

def astar(start,end,costmap,presclr=1):
    '''
    This function implements a star algorithm over a cost map.
    '''
    global prescalar 
    prescalar = presclr
    open_list = []
    closed_list = []
    open_list.append(Node(start))
    endNode=Node(end)
    while len(open_list) > 0:
        open_list.sort()
        current = open_list.pop(0)
        closed_list.append(current)
        if current.pos == endNode.pos:
            return reconstruct_path(current)
        for neighbor in neighbors(current,costmap):
            if costmap[neighbor.pos[0]][neighbor.pos[1]] == -1:
                continue
            neighbor.g = current.g + costmap[neighbor.pos[0]][neighbor.pos[1]]
            neighbor.h = neighbor.manhattan(endNode)
            neighbor.f = neighbor.g + neighbor.h
            if neighbor not in open_list:
                open_list.append(neighbor)
    return None

def reconstruct_path(current):
    '''
    This function reconstructs the path from the current node to the start node.
    '''
    path = []
    while current.parent is not None:
        path.append(current.pos)
        current = current.parent
    path.append(current.pos)
    return path

def neighbors(current,costmap):
    '''
    This function returns the 4-way neighbors of the current node.
    '''
    neighbors = []
    for i in range(current.pos[0]-1,current.pos[0]+2):
        if i < 0 or i >= costmap.shape[0]:
            continue
        elif i == current.pos[0]:
            for j in range(current.pos[1]-1,current.pos[1]+2):
                if j < 0 or j >= costmap.shape[1]:
                    continue
                elif j == current.pos[1]:
                    continue
                else:
                    neighbors.append(Node([i,j],current))
        else:
            neighbors.append(Node([i,current.pos[1]],current))
    return neighbors

def create_route(x1,x2,y1,y2):
    array =[[],[]]
    if x1 >=x2 + 24:
        array[0] = [x2+23,y1]
        array[1] = [x2+23,y1]
    elif x1 <= x2 -25:
        array[0] = [x2-23,y1]
        array[1] = [x2-23,y1]
    else:
        array[0] =[]
        array[1] = [x1,y1]
           
    if y1 >= y2 + 24:
        array[1][1] = y2 + 23
    elif y1 <= y2 -24:
        array[1][1] = y2 - 23
    else:
        array[1] = []
    
    array = [ele for ele in array if ele != []]
    array=array[0]
    return array

def manhattan(start,end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])
def create_solo_route(x1,x2,y1,y2):
    array =[[],[]]
    
    
    if x1 >=  x2 + 24:
        array[0] = [x2+23,y1]
        array[1] = [x2+23,y1]
    elif x1 <= x2 -25:
        array[0] = [x2-23,y1]
        array[1] = [x2-23,y1]
    else:
        array[0] =[]
        array[1] = [x1,y1]
           
    if y1 >=  y2 + 24:
        array[1][1] = y2 + 23
    elif y1 <= y2 -24:
        array[1][1] = y2 - 23
    else:
        array[1] = []
    
    array = [ele for ele in array if ele != []]

    return array

def free_corridor(myX,myY,targetX,targetY):
    

    quotX,remX = divmod(myX,50)
    quotY,remY = divmod(myY,50)
    quotTX = targetX // 50
    quotTY = targetY // 50
    array = []
    if (abs(quotTX-quotX) + abs(quotTY-quotY))<3:
        array = create_solo_route(myX,targetX,myY,targetY)
        return array
         
    else:
        if (quotX % 2) == 0:
            if myY > targetY:
                array.append([myX,targetY+28])
                if myX >=  targetX + 24:
                    array.append([targetX+23 ,targetY+28])
                    array.append([targetX+23 ,targetY+23])
                elif myX <= targetX - 24:
                    array.append([targetX-23,targetY+28])
                    array.append([targetX-23,targetY+23])
            else:
                array.append([myX,targetY-28])
                if myX >=  targetX + 24:
                    array.append([targetX+23 ,targetY-28])
                    array.append([targetX+23 ,targetY-23])
                elif myX <= targetX - 24:
                    array.append([targetX-23,targetY-28])
                    array.append([targetX-23,targetY-23])
                    
        elif (quotY % 2) == 0:
                if myX > targetX:
                    array.append([targetX+28,myY])
                    if myY >=  targetY + 24:
                        array.append([targetX+28 ,targetY+23])
                        array.append([targetX+23 ,targetY+23])
                    elif myY <= targetY - 24:
                        array.append([targetX+28,targetY-23])
                        array.append([targetX+23,targetY-23])
                else:
                    array.append([targetX-28,myY])
                    if myY >=  targetY + 24:
                        array.append([targetX-28 ,targetY+23])
                        array.append([targetX-23 ,targetY+23])
                    elif myY <= targetY - 24:
                        array.append([targetX-28,targetY-23])
                        array.append([targetX-23,targetY-23])
        else:
            if myX >=  targetX:
                array.append([myX-(remX+2),myY])
                newX = myX-(remX+2)
                if myY > targetY:
                    array.append([newX,targetY+28])
                    if newX >=  targetX + 24:
                        array.append([targetX+23 ,targetY+28])
                        array.append([targetX+23 ,targetY+23])
                    elif newX <= targetX - 24:
                        array.append([targetX-23,targetY+28])
                        array.append([targetX-23,targetY+23])
                    else:
                        array.append([myX,targetY-28])
                        if newX >=  targetX + 24:
                            array.append([targetX+23 ,targetY-28])
                            array.append([targetX+23 ,targetY-23])
                        elif newX <= targetX - 24:
                            array.append([targetX-23,targetY-28])
                            array.append([targetX-23,targetY-23])
                
            else:
                array.append([myX+(52-remX),myY])
                newX = myX+(52-remX)
                if myY > targetY:
                    array.append([newX,targetY+28])
                    if newX >=  targetX + 24:
                        array.append([targetX+23 ,targetY+28])
                        array.append([targetX+23 ,targetY+23])
                    elif newX <= targetX - 24:
                        array.append([targetX-23,targetY+28])
                        array.append([targetX-23,targetY+23])
                    else:
                        array.append([myX,targetY-28])
                        if newX >=  targetX + 24:
                            array.append([targetX+23 ,targetY-28])
                            array.append([targetX+23 ,targetY-23])
                        elif newX <= targetX - 24:
                            array.append([targetX-23,targetY-28])
                            array.append([targetX-23,targetY-23])
    return array
