import numpy as np
import time
class tulumba:

    def __init__(self, userName, clrDictionary, maxStepSize, maxTime):
        
        self.name = userName # your object will be given a user name, i.e. your group name
        self.maxStep = maxStepSize # maximum length of the returned path from run()
        self.maxTime = maxTime # run() is supposed to return before maxTime
        self.clrDict = clrDictionary
        self.colorz = clrDictionary.keys().copy()
        # make dictionary from first two columns of colorz
        self.colorzDict = {}
        for i in range(len(self.colorz)):
            self.colorzDict[self.colorz[i][0]] = self.colorz[i][1]
        self.arena = np.zeros(7,7)

    def run(self, img, info):
        # get time 
        startTime = time.time()
        # get img and downsample
        for i in range(7):
            for j in range(7):
                self.arena[i,j] = self.colorzDict[img[25+i*50,25+j*50]]
        # get info
        self.info = info
        print(self.info)
