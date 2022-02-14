import numpy as np
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement

class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
        self.name = userName # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize # maximum length of the returned path from run()
        self.maxTime = maxTime # run() is supposed to return before maxTime
        self.maxPoint = 100 # maximum points you can have
        vals = list(clrDictionary.values())
        vals.append([(0,0,0),1,1])
        vals.append([(255,255,255),1,1])
        self.colorVals = {}
        for i,j,k in vals:
            self.colorVals[i] = j
        self.arena = np.zeros((15,15),dtype=int)
        self.depth=0

    def run(self, img, info):
        self.img=img
        self.oppPos = []
        self.scores = []
        self.info = info
        self.myPos=self.info[self.name][0]
        self.myPoints=self.info[self.name][1]
        self.my_ij = [int(self.myPos[0]/50),int(self.myPos[1]/50)]

        for player in self.info:
            if player != self.name:
                self.oppPos.append(self.info[player][0])
        for i in range(7):
            for j in range(7):
                self.arena[2*i+1][2*j+1] = self.colorVals[tuple(img[(2*i+1)*50+25][(2*j+1)*50+25])]
                if self.arena[2*i+1][2*j+1] != 0:
                    self.scores.append([self.arena[2*i+1][2*j+1],(25+(2*i+1)*50,25+(2*j+1)*50),(2*i+1,2*j+1)])
        self.scores.sort(key=lambda x: x[0], reverse=True)
        target = self.chooseTarget()
        returnPath = self.chooseRoute(target)
        return returnPath

    def chooseRoute(self, target):
        costMap = np.ones((15,15),dtype=int)*101
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

        myMap = np.ones((15,15),dtype=int)*-1
        myMap[imin:imax+1,jmin:jmax+1] = costMap[imin:imax+1,jmin:jmax+1]
        grid = Grid(matrix=costMap)
        Grid.cleanup(grid)

        start = grid.node(self.my_ij[0],self.my_ij[1])
        end = grid.node(target[0],target[1])
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        selectedPath, runs = finder.find_path(start, end, grid)
        path = self.move(selectedPath) 
        return path

    def pathFinder(self,start,end,grid):
        # find the best path from start to end
        path = []
            
    def move(self,selectedPath):
        path = []
        # reverse selectedNodes
        path = [[self.myPos[0],selectedPath[1][1]*50+25],[selectedPath[1][0]*50+25,selectedPath[1][1]*50+25]]  # list of coordinates for path
        for i in range(2,len(selectedPath)):  # for each coordinate in the path
            path.append([selectedPath[i][0]*50+25,selectedPath[i-1][1]*50+25])  # add the coordinates to the path
            path.append([selectedPath[i][0]*50+25,selectedPath[i][1]*50+25])  # add the coordinates to the path
        if manhattan(path[-1],self.myPos) < self.maxStep and self.depth < 2:
            self.depth += 1
            #  path.append(self.run(self.img,self.info))
        self.depth = 0
        return path  # return the path

        
    def chooseTarget(self):
        for i in range(len(self.scores)):  # for each score
            counter=0  # counter for the number of opponents
            if self.scores[i][0] > self.myPoints:  # if the color value is greater than your points
                self.scores[i][0] = -1  # set the color value to -1
            else:
                for j in range(len(self.oppPos)):  # for each opponent
                    if not self.amICloser(self.scores[i][1],self.oppPos[j]):  # if the opponent is closer to the castle
                        self.scores[i][0] = 1  # set the score to 0
                    else:    # if the opponent is not closer to the castle
                        counter+=1  # add 1 to the counter
                if counter == len(self.oppPos):  # if the counter is equal to the number of opponents and the score is less than or equal to yours
                    return self.scores[i][2]  # return the coordinates of the castle
        # if no target is found, return the biggest one
        for i in range(len(self.scores)): # for each score
            if self.scores[i][0] != -1: # if the color value is less than or equal to your points
                return self.scores[i][2]  # return the coordinates of the castle
    

    def amICloser(self, castle, opponent):
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):
            return False
        else:
            return True
def manhattan(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])
