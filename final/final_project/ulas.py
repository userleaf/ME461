import numpy as np
import time
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
        vals.append([(0,0,0),0,1])
        vals.append([(255,255,255),0,1])
        self.colorVals = {}
        for i,j,k in vals:
            self.colorVals[i] = j
        self.arena = np.zeros((15,15),dtype=int)

    def run(self, img, info):
        self.oppPos = []
        self.scores = []
        self.info = info
        self.myPos=self.info[self.name][0]
        self.myPoints=self.info[self.name][1]
        self.my_ij = [int((self.myPos[0]-20)/50),int((self.myPos[1]-20)/50)]

        for player in self.info:
            if player != self.name:
                self.oppPos.append(self.info[player][0])
        for i in range(7):
            for j in range(7):
                self.arena[2*i+1][2*j+1] = self.colorVals[tuple(img[(2*i+1)*50+25][(2*j+1)*50+25])]
                if self.arena[2*i+1][2*j+1] != 0:
                    self.scores.append([self.arena[2*i+1][2*j+1],(25+(2*i+1)*50,25+(2*j+1)*50),(2*i+1,2*j+1)])
        scoresTime= time.time()
        self.scores.sort(key=lambda x: x[0], reverse=True)
        target = self.chooseTarget()
        self.path = []
        returnPath = self.chooseRoute(target)
        return returnPath

    def chooseRoute(self, target):
        self.scores.sort(key=lambda x: x[0], reverse=True)
        targetUpScale = [target[0]*50+25,target[1]*50+25]
        costMap = np.ones((15,15),dtype=int)*100
        for coord,ij in self.path:
            if self.arena[ij[0]][ij[1]]<=self.myPoints:
                costMap[ij[0]][ij[1]] -= self.arena[ij[0]][ij[1]]
            else: 
                costMap[ij[0]][ij[1]] = -1
        imin=max(min(self.my_ij[0],target[0])-1,0)
        imax=min(max(self.my_ij[0],target[0])+1,14)
        jmin=max(min(self.my_ij[1],target[1])-1,0)
        jmax=min(max(self.my_ij[1],target[1])+1,14)

        for i in range(imin,imax+1):
            for j in range(jmin,jmax+1):
                costMap[i][j] -= self.arena[i][j]

        costMap = costMap[imin:imax+1,jmin:jmax+1]
        print(target,self.my_ij,imin,imax,jmin,jmax)
        print(costMap)

        grid = Grid(matrix=costMap)
        start = grid.node(self.my_ij[0]-imin, self.my_ij[1]-jmin)
        end = grid.node(target[0]-imin, target[1]-jmin)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        selectedPath, runs = finder.find_path(start, end, grid)
        for i,j in selectedPath:
            self.path.append([(i+imin),(j+imin)])
        path = self.move(selectedPath) 
        return path

    def pathFinder(self,start,end,grid):
        # find the best path from start to end
        path = []
            
    def move(self,selectedPath):
        path = []
        # reverse selectedNodes
        for i in range(len(selectedPath)):
            if i ==0:
                path.append([selectedPath[i][0]*50+25,self.myPos[1]])
                path.append([self.myPos[0],selectedPath[i][1]*50+25])
            else:
                path.append([selectedPath[i][0]*50+25,selectedPath[i-1][1]*50+25])
                path.append([selectedPath[i][0]*50+25,selectedPath[i][1]*50+25])
        for i,j in enumerate(path):
            if i==0 and j==self.myPos:
                path.pop(0)
            elif j == path[i-1]:
                path.pop(i)
        return path
        
    def chooseTarget(self):
        if self.myPoints <= self.maxPoint:
            for i in range(len(self.scores)):
                if self.scores[i][0] > self.maxPoint:
                    self.scores[i][2] = -1
            self.scores.sort(key=lambda x: x[0], reverse=True)
            return self.scores[0][2]
        for i in range(len(self.scores)):
            counter=0
            for j in range(len(self.oppPos)):
                if not self.manhattan(self.scores[i][1],self.oppPos[j]):
                    self.scores[i][0] = 0
                else:    
                    counter+=1
            if counter == len(self.oppPos) and self.scores[i][0] <= self.myPoints:
                return self.scores[i][2] 
        return [10,8]

    def manhattan(self, castle, opponent):
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):
            return False
        else:
            return True
