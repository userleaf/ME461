import numpy as np
import time
class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
        
        self.name = userName # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize # maximum length of the returned path from run()
        self.maxTime = maxTime # run() is supposed to return before maxTime
        vals = list(clrDictionary.values())
        self.colorVals = {}
        for i,j,k in vals:
            self.colorVals[i] = j
        print(self.colorVals)

    def run(self, img, info):
        # get time 
        startTime = time.time()
        self.oppPos = np.zeros((len(info)-1,1),dtype=int)
        # get img and downsample sort by val and store coordinates
        self.scores = []
        for i in range(7):
            for j in range(7):
                self.arena[i][j] = self.colorVals[img[75+i*50,75+j*50]]
                if self.arena[i][j] != 0:
                    self.scores.append(self.arena[i][j],(i,j))

        # sort by val descending
        self.scores.sort(key=lambda x: x[0], reverse=True)

        # get info
        self.info = info
        for player in info.keys():
            if self.info[player] == self.name:
                self.myPos = self.info[player][0]
            else:
                self.oppPos.append(self.info[player][0])
        
        for i in range(len(self.scores)):
            for j in range(len(self.oppPos)):
                if not self.manhattan(self.scores[i][1],self.oppPos[j]):
                    self.scores[i][0] = 0
        # sort by val descending
        self.scores.sort(key=lambda x: x[0], reverse=True)
        # make path
        self.path = []
        target = self.scores[0][1]
        # return target to original scale
        target = (target[0]*100+50,target[1]*100+50)
        # find the closest corner
        
        

    def manhattan(self, a, b):
        if a[0]-b[0]+a[1]-b[1] < a[0]-self.myPos[0]+a[1]-self.myPos[1]:
            return False
        else:
            return True
