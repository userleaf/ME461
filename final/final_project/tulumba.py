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
        
        
        self.arena = np.zeros(7,dtype=int)

    def run(self, img, info):
        # get time 
        startTime = time.time()
        # get img and downsample
        for i in range(7):
            for j in range(7):
                self.arena[i][j] = self.colorVals[img[75+i*50,75+j*50]]
        print(self.arena)

