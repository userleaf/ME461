import numpy as np 

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
        self.my_ij = [int((self.myPos[0]-20)/50),int((self.myPos[1]-20)/50)]  # your position in the arena

        for player in self.info:  # for each player
            if player != self.name:  # if it's not you
                self.oppPos.append(self.info[player][0])  # add the position to the list of opponent's positions
        for i in range(7):  # for each castle
            for j in range(7):
                self.arena[2*i+1][2*j+1] = self.colorVals[tuple(img[(2*i+1)*50+25][(2*j+1)*50+25])] # add the color value to the arena
                if self.arena[2*i+1][2*j+1] != 0:  # if the color value is not 0
                    self.scores.append([self.arena[2*i+1][2*j+1],(25+(2*i+1)*50,25+(2*j+1)*50),(2*i+1,2*j+1)])  # add the score to the list
        self.scores.sort(key=lambda x: x[0], reverse=True) # sort the scores in descending order
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
        path = [[self.myPos[0],selectedPath[1][1]*50+25],[selectedPath[1][0]*50+25,selectedPath[1][1]*50+25]]  # list of coordinates for path
        for i in range(2,len(selectedPath)):  # for each coordinate in the path
            path.append([selectedPath[i][0]*50+25,selectedPath[i-1][1]*50+25])  # add the coordinates to the path
            path.append([selectedPath[i][0]*50+25,selectedPath[i][1]*50+25])  # add the coordinates to the path
        return path  # return the path

    def amICloser(self, castle, opponent):  # castle is a coordinate, opponent is a coordinate
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):  # opponent is closer
            return False  # return False
        return True  # return True

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
