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
        startTime = time.time()
        self.oppPos = []
        self.scores = []
        self.info = info
        self.myPos=self.info[self.name][0]
        self.myPoints=self.info[self.name][1]
        runLoopTime = time.time()
        for player in self.info:
            if player != self.name:
                self.oppPos.append(self.info[player][0])

        for i in range(7):
            for j in range(7):
                self.arena[2*i+1][2*j+1] = self.colorVals[tuple(img[(2*i+1)*50+25][(2*j+1)*50+25])]
                if self.arena[2*i+1][2*j+1] != 0:
                    self.scores.append([self.arena[2*i+1][2*j+1],(25+(2*i+1)*50,25+(2*j+1)*50),(2*i+1,2*j+1)])
        print(f'Time for run loop: {time.time()-runLoopTime}')
        scoresTime= time.time()
        self.scores.sort(key=lambda x: x[0], reverse=True)
        print(f'Time for scores: {time.time()-scoresTime}')
        # get info

        print(f'Time for run: {time.time()-startTime}')
        targetTime = time.time()
        target = self.chooseTarget()
        print(f'Time for choose target: {time.time()-targetTime}')
        # sort by val descending
        # make path
        self.path = []
        returnPath = self.chooseRoute(target)
        print(f'Time for all: {time.time()-startTime}')
        return returnPath

    def chooseRoute(self, target):
        # sort the scores by first element decreasing
        startTime = time.time()
        self.scores.sort(key=lambda x: x[0], reverse=True)
        a = 150
        targetUpScale = [target[0]*50+25,target[1]*50+25]
        for score, coord,ij in self.scores:
            # check if coord is in between target and self.myPos
            if coord[0]+a > self.myPos[0] and coord[0]-a < targetUpScale[0] and coord[1]+a > self.myPos[1] and coord[1]-a < targetUpScale[1]:
                self.path.append([coord,ij])
            elif coord[0]-a < self.myPos[0] and coord[0]+a > targetUpScale[0] and coord[1]-a < self.myPos[1] and coord[1]+a > targetUpScale[1]:
                self.path.append([coord,ij])
            elif coord[0]+a > self.myPos[0] and coord[0]-a < targetUpScale[0] and coord[1]-a < self.myPos[1] and coord[1]+a > targetUpScale[1]:
                self.path.append([coord,ij])
            elif coord[0]-a < self.myPos[0] and coord[0]+a > targetUpScale[0] and coord[1]+a > self.myPos[1] and coord[1]-a < targetUpScale[1]:
                self.path.append([coord,ij])
            else:
                pass
        print(f'Time for if statements detemining square: {time.time()-startTime}')
        # crate np array
        costMap = np.ones((15,15),dtype=int)*100
        for coord,ij in self.path:
            if self.arena[ij[0]][ij[1]]<=self.myPoints:
                costMap[ij[0]][ij[1]] -= self.arena[ij[0]][ij[1]]
            else: 
                costMap[ij[0]][ij[1]] = -1

        my_ij = [int((self.myPos[0]-20)/50),int((self.myPos[1]-20)/50)]
        grid = Grid(matrix=costMap)
        start = grid.node(my_ij[0], my_ij[1])
        end = grid.node(target[0], target[1])
        mytime = time.time()
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        selectedPath, runs = finder.find_path(start, end, grid)
        print(f'Time for Choose Route: {time.time()-startTime}')

        path = self.move(selectedPath) 
        return path

    def move(self,selectedPath):
        startTime = time.time()
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
            if i == 0:
                continue
            elif j == path[i-1]:
                path.pop(i)
            else:
                continue
        if path[0] == self.myPos:
            path.pop(0)
        print(f'Time for move: {time.time()-startTime}')
        return path
        
    def chooseTarget(self):
        # find the closest corner
        startTime = time.time()
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
                print(f'Time for Choose Target: {time.time()-startTime}')

                return self.scores[i][2] 
        # if no castle is close get to middle

        return [5,3]

    def manhattan(self, castle, opponent):
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):
            return False
        else:
            return True
