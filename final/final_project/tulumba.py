import numpy as np
import time
import astar as a
class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
        self.name = userName # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize # maximum length of the returned path from run()
        self.maxTime = maxTime # run() is supposed to return before maxTime
        vals = list(clrDictionary.values())
        self.colorVals = {}
        for i,j,k in vals:
            self.colorVals[i] = j
        self.arena = np.zeros((7,7),dtype=int)
        print(self.colorVals)

    def run(self, img, info):
        # get time 
        startTime = time.time()
        self.oppPos = []
        # get img and downsample sort by val and store coordinates
        self.scores = []
        for i in range(7):
            for j in range(7):
                self.arena[i][j] = self.colorVals[tuple(img[i*100+50,j*100+50,:])]
                if self.arena[i][j] != 0:
                    self.scores.append([self.arena[i][j],(75+i*100,75+j*100),(i,j)])
        # sort by val descending
        self.scores.sort(key=lambda x: x[0], reverse=True)
        # get info
        self.info = info
        self.myPos=self.info[self.name][0]
        self.myPoints=self.info[self.name][1]
        for player in self.info:
            if player != self.name:
                self.oppPos.append(self.info[player][0])


        target = self.chooseTarget()
        # sort by val descending
        # make path
        self.path = []
        return self.chooseRoute(target)

    def chooseRoute(self, target):
        # sort the scores by first element decreasing
        self.scores.sort(key=lambda x: x[0], reverse=True)
        for score, coord,ij in self.scores:
            # check if coord is in between target and self.myPos
            if coord[0] > self.myPos[0] and coord[0] < target[0] and coord[1] > self.myPos[1] and coord[1] < target[1]:
                self.path.append([coord,ij])
            elif coord[0] < self.myPos[0] and coord[0] > target[0] and coord[1] < self.myPos[1] and coord[1] > target[1]:
                self.path.append([coord,ij])
            elif coord[0] > self.myPos[0] and coord[0] < target[0] and coord[1] < self.myPos[1] and coord[1] > target[1]:
                self.path.append([coord,ij])
            elif coord[0] < self.myPos[0] and coord[0] > target[0] and coord[1] > self.myPos[1] and coord[1] < target[1]:
                self.path.append([coord,ij])
            else:
                pass
        costMap = np.zeros((7,7))
        for coord,ij in self.path:
            costMap[ij[0]][ij[1]] = self.arena[ij[0]][ij[1]]
        selectedNodes = a.astar(costMap, [int(self.myPos[0]-50)/100,int(self.myPos[1]-50)/100], list(target))
        return [50,50]
        path = self.move(selectedNodes) 
        return path

    def move(self,selectedNodes):
        path = []
        for i in range(len(selectedNodes)):
            path.append(np.arange(self.myPos[0],selectedNodes[i][0]*100+50,1))
            path.append(np.arange(self.myPos[1],selectedNodes[i][1]*100+50,1))
        return path
        
    def chooseTarget(self):
        # find the closest corner
        for i in range(len(self.scores)):
            counter=0
            for j in range(len(self.oppPos)):
                if not self.manhattan(self.scores[i][1],self.oppPos[j]):
                    self.scores[i][0] = 0
                
                else:    
                    counter+=1
            
            if counter == len(self.oppPos):
                print(self.scores)
                return self.scores[i][2] 

    def manhattan(self, castle, opponent):
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):
            return False
        else:
            return True
    
def printer(string):
    print(string+"s")
