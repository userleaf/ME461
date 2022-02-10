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
        self.corners = np.zeros((7,7,4), dtype=int)
        for i in range(7):
            for j in range(7):
                for k in range(4):
                    if k == 0:
                        self.corners[i,j,k] = (50+i*100,50+j*100)
                    elif k == 1:
                        self.corners[i,j,k] = (100+i*100,50+j*100)
                    elif k == 2:
                        self.corners[i,j,k] = (50+i*100,100+j*100)
                    else:
                        self.corners[i,j,k] = (100+i*100,100+j*100)

        
        self.arena = np.zeros(7,dtype=int)

    def run(self, img, info):
        # get time 
        startTime = time.time()
        # get img and downsample
        for i in range(7):
            for j in range(7):
                self.arena[i][j] = self.colorVals[img[75+i*50,75+j*50]]
        # get info
        self.info = info
        for player in info['players']:
            if self.info[player] == self.name:
                self.myPos = self.info[player][0]
                self.myPoint = self.info[player][1]

