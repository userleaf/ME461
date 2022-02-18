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
        self.soloCount = 0
        self.startCount =0
        initLocs = [(25, 175),(25, 375),(25, 575),(175, 25),(375, 25),(575, 25),(175, 725),(375, 725),(575, 725)]
        self.starting = {}
        for i in range(len(initLocs)):
            self.starting[initLocs[i]]=i+1
        for i,j,k in vals:  # for each color in the list of values
            self.colorVals[i] = j  # add the color to the dictionary
        self.arena = np.zeros((15,15),dtype=int)  # create a 15x15 arena

    def run(self, img, info):  # img is a 2D numpy array, info is a dictionary
        self.oppPos = []  # list of opponent's positions
        self.oppPoints = []  # list of opponent's positions
        self.scores = []  # list of scores
        self.info = info  # dictionary of info
        self.myPos=self.info[self.name][0]  # your position
        self.myPoints=self.info[self.name][1]  # your points
        self.my_ij = [int((self.myPos[0])/50),int((self.myPos[1])/50)]  # your position in the arena
       
        for player in self.info:  # for each player
            if player != self.name:  # if it's not you
                self.oppPos.append(self.info[player][0])  # add the position to the list of opponent's positions
                self.oppPoints.append(self.info[player][1])
        for i in range(7):  # for each castle
            for j in range(7):
                self.arena[2*i+1][2*j+1] = self.colorVals[tuple(img[(2*i+1)*50+25][(2*j+1)*50+25])] # add the color value to the arena
                if self.arena[2*i+1][2*j+1] != 0:  # if the color value is not 0
                    self.scores.append([self.arena[2*i+1][2*j+1],(25+(2*i+1)*50,25+(2*j+1)*50),(2*i+1,2*j+1)])  # add the score to the list
                   
        self.scores.sort(key=lambda x: x[0], reverse=True) # sort the scores in descending order
        
        if not len(self.oppPos):
            return self.soloRunner()
        if self.startCount == 0:
            self.img = img
            return self.first_move()
        if self.startCount == 1:
            self.startCount = 2
            return self.nextRoute
            
        target = self.chooseTarget()  # choose the target
        return self.chooseRoute(target)  # choose the route to the target and return

    def chooseTarget(self):  # choose the target
        for i in range(len(self.scores)):  # for each score
            counter=0  # counter for the number of opponents
            if self.scores[i][0] > self.myPoints:  # if the color value is greater than your points
                self.scores[i][0] = -1  # set the color value to -1
            else:
                for j in range(len(self.oppPos)):  # for each opponent
                    if (not self.amICloser(self.scores[i][1],self.oppPos[j])) and (self.scores[i][0]< self.oppPoints[j]):  # if the opponent is closer to the castle
                        self.scores[i][0] = 0  # set the score to 0
                    else:    # if the opponent is not closer to the castle
                        counter+=1  # add 1 to the counter
                if counter == len(self.oppPos):  # if the counter is equal to the number of opponents and the score is less than or equal to yours
                    return self.scores[i][2]  # return the coordinates of the castle
        # if no target is found, return the biggest one
        for i in range(len(self.scores)): # for each score
            if self.scores[i][0] != -1: # if the color value is less than or equal to your points
                return self.scores[i][2]  # return the coordinates of the castle
        return [6,6]
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
        posAppend = []
        counter=0
        for i in range(len(pathArena)):
            if pathArena[i][0]%2 and pathArena[i][1]%2:
                posAppend.append[i]
        for i in range(len(posAppend)):
            pathArena.insert(posAppend[i+counter],pathArena[posAppend[i+counter-1]])
            counter +=1

        return self.move(pathArena)  # return the path

    def move(self,selectedPath):  # selectedPath is a list of coordinates in the arena
        selectedPath.reverse()  # reverse the path
        selectedPath.pop(0)
        
        if len(selectedPath) > 3 and self.myPoints <= 100:
            for i,j in selectedPath:
                    if(self.arena[i][j]) == self.myPoints:
                        return free_corridor(self.myPos[0],self.myPos[1],i*50+25,j*50+25)

            if (self.arena[selectedPath[0][0],selectedPath[0][1]]+self.arena[selectedPath[1][0],selectedPath[1][1]]+self.arena[selectedPath[2][0],selectedPath[2][1]])>self.myPoints:
                if self.arena[selectedPath[2]] > self.arena[selectedPath[0]]:
                    return free_corridor(self.myPos[0],self.myPos[1],selectedPath[2][0]*50+25,selectedPath[2][1]*50+25)
                elif self.arena[selectedPath[2]] < self.arena[selectedPath[0]]:
                    return free_corridor(self.myPos[0],self.myPos[1],selectedPath[0][0]*50+25,selectedPath[0][1]*50+25)
                else:
                    return free_corridor(self.myPos[0],self.myPos[1],selectedPath[1][0]*50+25,selectedPath[1][1]*50+25)


                
            
                
                
                
                        

                

        for i in range(len(selectedPath)):
            selectedPath[i][0]*=50  # multiply the coordinates by 50
            selectedPath[i][1]*=50  # multiply the coordinates by 50
            selectedPath[i][0]+=25  # add 25 to the x coordinate
            selectedPath[i][1]+=25  # add 25 to the y coordinate
       
        if selectedPath == []:

            path = [[self.myPos[0],(self.my_ij[1]+1)*50+25]]
            path.append([(self.my_ij[0]+1)*50+25,(self.my_ij[1]+1)*50+25])
        else:
            path = [create_myroute(self.myPos[0], selectedPath[0][0], self.myPos[1], selectedPath[0][1])]
        
            for i in range(1,len(selectedPath)):
                path.append(create_myroute(path[i-1][0], selectedPath[i][0], path[i-1][1], selectedPath[i][1]))
       
        return path 

    def amICloser(self, castle, opponent):  # castle is a coordinate, opponent is a coordinate
        if abs(castle[0]-opponent[0])+abs(castle[1]-opponent[1]) < abs(castle[0]-self.myPos[0])+abs(castle[1]-self.myPos[1]):  # opponent is closer
            return False  # return False
        return True  # return True
    
    def soloRunner(self):
        if self.soloCount == 0:
            myTargets = self.scores[:7]
            
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
            
            dummyStep = free_corridor(self.myPos[0],self.myPos[1],my_path[0][0],my_path[0][1])
            resultantPath.append(dummyStep)
            my_path[0] = (dummyStep[-1][0],dummyStep[-1][1])
                
            
            for i in range(1,len(my_path)):
                dummyStep = free_corridor(my_path[i-1][0],my_path[i-1][1],my_path[i][0],my_path[i][1])
                resultantPath.append(dummyStep)
                my_path[i] = (dummyStep[-1][0],dummyStep[-1][1])
                
            # flatten resultantPath
            flat_list = [item for sublist in resultantPath for item in sublist]
            flat_list.insert(0,list(self.myPos))
            self.soloCount = 1
            self.soloPath, myMove = self.nextStop(flat_list)
            return myMove
        else:
            self.soloPath, myMove = self.nextStop(self.soloPath)
            return myMove
    def TrimPath(self,path, L):
        '''
        path is the candidate path, i.e a list of points [[y1,x1], ... [yn,xn]]
        the function assumes that [y1,x1] is where the agent currently is, 
        and hence [y2,x2] is the first point to move
        L is the total distance that the agent can cover
        function returns the path trimmed so that it has a length of L
        '''
        # first veryfy path
        res = [path[0]] # initially coordinate is approved by default, others will be added if they are valid and within the span of L
        distRemaining = L # originially this is the distance to be covered by the send path
        for i in range(len(path)-1): # using pairs move on the path
            # move on only any distance to move is left
            
            if distRemaining <= 0:
                return res
            # get the points and their coordinates explicitly
            p1, p2 = path[i], path[i+1] # get two consequitive point coordinates
            try:
                y1, x1 = path[i][0], path[i][1]
                y2, x2 = path[i+1][0], path[i+1][1]
                dy = y2 - y1 # p2[0] - p1[0]
                dx = x2 - x1 # p2[1] - p1[1]
                # one of these has to be zero on a N4 path
                if abs(dx) >0 and abs(dy)>0: # we have a problem, one of them has to be zero on a N4 path
                    # just return the valid path found so far
                    return res
                # we also have a problem if consequtive points are the same, if so just ignore the latest one
                if not(dx == 0 and dy == 0): # 
                    pathL = max(abs(dy), abs(dx)) # length between p1-p2
                    if pathL <= distRemaining: # this part of the path (p1 to p2) completely belongs to the resulting path
                        res.append(p2)
                        distRemaining -= pathL
                        
                    else: # this is the tricky part, some part of the path will belong
                        # partial path should expand either in X or Y direction
                        # note that either dx or dy has to be zero at all times
                        if abs(dx) > 0: # going in X direction
                            res.append([y1, x1+np.sign(dx)*distRemaining])
                            
                        else: # going in Y direction
                            res.append([y1+np.sign(dy)*distRemaining, x1])
                            
                        return res
            except:
                pass
        return res

    def nextStop(self,path):
        nextMove = self.TrimPath(path,100)
        for i in range(len(nextMove)-1):
            path.pop(0)
        path.insert(0,nextMove[-1])
        return path, nextMove           

    def first_move(self):
        myLoc=self.starting[tuple(self.myPos)]
        return eval(f'self.start{myLoc}()')

    def start1(self):
       
        node11 = self.colorVals[tuple(self.img[75][75])]
        node13 = self.colorVals[tuple(self.img[75][275])]
        node22 = self.colorVals[tuple(self.img[175][175])]
        node23 = self.colorVals[tuple(self.img[175][275])]
        node32 = self.colorVals[tuple(self.img[275][175])]
        node33 = self.colorVals[tuple(self.img[275][275])]
        if node11 == 100:
            route = [[52,175],[52,102]]
            self.nextRoute =[[52,98],[52,194]]
            
        elif node11 == 50 and (node22+node32+node33)<50 and (node22+node23+node33)<50:
            route = [[52,175],[52,102]]
            self.nextRoute =[[52,98],[52,194]]
            
        elif (node22+node23)>=(node13+node23) and (node22+node23)>=(node32+node22):
            route = [[125,175]]
            self.nextRoute = [[152,175],[152,248]]
            
        elif (node22+node32)>=(node13+node23) and (node22+node32)>=(node22+node23):
            route = [[125,175]]
            self.nextRoute =[[225,175]]
                    
        else:
            route = [[52,175],[52,248]]
            self.nextRoute =[[52,252],[148,252]]
        self.startCount = 1
        return route   
    def start2(self):
        
        node11 = self.colorVals[tuple(self.img[75][275])]
        node21 = self.colorVals[tuple(self.img[175][275])]
        node31 = self.colorVals[tuple(self.img[275][275])]
        node22 = self.colorVals[tuple(self.img[175][375])]
        node32 = self.colorVals[tuple(self.img[275][375])]
        node13 = self.colorVals[tuple(self.img[75][475])]
        node23 = self.colorVals[tuple(self.img[175][475])]
        node33 = self.colorVals[tuple(self.img[275][475])]
        if (node11+node21+node31) >= (node22+node32) and (node11+node21+node31) >= (node13+node23+node33):
            route = [[52,375],[52,302]]
            self.nextRoute =[[52,298],[148,298]]
            
        elif (node13+node23+node33) >= (node11+node21+node31) and (node13+node23+node33) >= (node22+node32):
            route = [[52,375],[52,448]]
            self.nextRoute = [[52,452],[148,452]]
            
        else:
            route =[[125,375]]        
            if node32 >= node21 and node32 >= node23:
                self.nextRoute = [[225,375]]
            elif node23 >= node32 and node23 >= node21:
                self.nextRoute = [[152,375],[152,448]]
            else:
                self.nextRoute = [[152,375],[152,302]]
        self.startCount = 1
        return route
    def start3(self):
      
        node11 = self.colorVals[tuple(self.img[75][675])]
        node13 = self.colorVals[tuple(self.img[75][475])]
        node22 = self.colorVals[tuple(self.img[175][575])]
        node23 = self.colorVals[tuple(self.img[175][475])]
        node32 = self.colorVals[tuple(self.img[275][575])]
        node33 = self.colorVals[tuple(self.img[275][475])]
        if node11 == 100:
            route = [[52,575],[52,648]]
            self.nextRoute =[[52,652],[52,556]]
            
        elif node11 == 50 and (node22+node32+node33)<50 and (node22+node23+node33)<50:
            route = [[52,575],[52,648]]
            self.nextRoute =[[52,652],[52,556]]
            
        elif (node22+node23)>=(node13+node23) and (node22+node23)>=(node32+node22):
            route = [[125,575]]
            self.nextRoute = [[152,575],[152,502]]
            
        elif (node22+node32)>=(node13+node23) and (node22+node32)>=(node22+node23):
            route = [[125,575]]
            self.nextRoute =[[225,575]]
            
        else:
            route = [[52,575],[52,502]]
            self.nextRoute =[[52,498],[148,498]]
        self.startCount = 1
        return route
    def start4(self):
        
        node11 = self.colorVals[tuple(self.img[75][75])]
        node13 = self.colorVals[tuple(self.img[275][75])]
        node22 = self.colorVals[tuple(self.img[175][175])]
        node23 = self.colorVals[tuple(self.img[275][175])]
        node32 = self.colorVals[tuple(self.img[175][275])]
        node33 = self.colorVals[tuple(self.img[275][275])]
        if node11 == 100:
            route = [[175,52],[102,52]]
            self.nextRoute =[[98,52],[194,52]]
            
        elif node11 == 50 and (node22+node32+node33)<50 and (node22+node23+node33)<50:
            route = [[175,52],[102,52]]
            self.nextRoute =[[98,52],[194,52]]
            
        elif (node22+node23)>=(node13+node23) and (node22+node23)>=(node32+node22):
            route = [[175,125]]
            self.nextRoute = [[175,152],[248,152]]
            
        elif (node22+node32)>=(node13+node23) and (node22+node32)>=(node22+node23):
            route = [[175,125]]
            self.nextRoute =[[175,225]]
        
        else:
            route = [[175,52],[248,52]]
            self.nextRoute =[[252,52],[252,148]]
        self.startCount = 1
        return route   
    def start5(self):
        node11 = self.colorVals[tuple(self.img[275][75])]
        node12 = self.colorVals[tuple(self.img[275][175])]
        node13 = self.colorVals[tuple(self.img[275][275])]
        node22 = self.colorVals[tuple(self.img[375][175])]
        node23 = self.colorVals[tuple(self.img[375][275])]
        node31 = self.colorVals[tuple(self.img[475][75])]
        node32 = self.colorVals[tuple(self.img[475][175])]
        node33 = self.colorVals[tuple(self.img[475][275])]
        
        
        if (node31+node32+node33) >= (node22+node23) and (node31+node32+node33) >= (node11+node12+node13):
            route = [[375,52],[448,52]]
            self.nextRoute =[[452,52],[452,148]]
        
        elif (node11+node12+node13) >= (node31+node32+node33) and (node11+node12+node13) >= (node22+node23):
            route = [[375,52],[302,52]]
            self.nextRoute = [[298,52],[298,148]]
    
        else:
            route =[[375,125]]
            
            if node23 >= node12 and node23 >= node32:
                self.nextRoute = [[375,225]]
            elif node32 >= node23 and node32 >= node12:
                self.nextRoute = [[375,152],[448,152]]
            else:
                self.nextRoute = [[375,152],[302,152]]
        self.startCount = 1
        return route
    def start6(self):
        node11 = self.colorVals[tuple(self.img[475][75])]
        node12 = self.colorVals[tuple(self.img[475][175])]
        node22 = self.colorVals[tuple(self.img[575][175])]
        node31 = self.colorVals[tuple(self.img[675][75])]
        if node31 == 100:
            route = [[575,52],[648,52]]
            self.nextRoute =[[652,52],[652,148]]
        
        elif node31 == 50 and (node11+node12+node22)<50:
            route = [[575,52],[648,52]]
            self.nextRoute =[[652,52],[652,148]]
            
        else:
            route = [[575,52],[502,52]]
            self.nextRoute =[[498,52],[498,148]]
        self.startCount = 1
        return route
    def start7(self):
        node11 = self.colorVals[tuple(self.img[75][675])]
        node13 = self.colorVals[tuple(self.img[275][675])]
        node22 = self.colorVals[tuple(self.img[175][575])]
        node23 = self.colorVals[tuple(self.img[275][575])]
        node32 = self.colorVals[tuple(self.img[175][475])]
        node33 = self.colorVals[tuple(self.img[275][475])]
        if node11 == 100:
            route = [[175,698],[102,698]]
            self.nextRoute =[[98,698],[194,556]]
            
        elif node11 == 50 and (node22+node32+node33)<50 and (node22+node23+node33)<50:
            route = [[175,698],[102,698]]
            self.nextRoute =[[98,698],[194,556]]
            
        elif (node22+node23)>=(node13+node23) and (node22+node23)>=(node32+node22):
            route = [[175,625]]
            self.nextRoute = [[175,598],[248,598]]
            
        elif (node22+node32)>=(node13+node23) and (node22+node32)>=(node22+node23):
            route = [[175,625]]
            self.nextRoute =[[175,525]]
            
        else:
            route = [[175,698],[248,698]]
            self.nextRoute =[[252,698],[252,602]]
        self.startCount = 1
        return route
    def start8(self):
        node11 = self.colorVals[tuple(self.img[275][675])]
        node12 = self.colorVals[tuple(self.img[275][575])]
        node13 = self.colorVals[tuple(self.img[275][475])]
        node22 = self.colorVals[tuple(self.img[375][575])]
        node23 = self.colorVals[tuple(self.img[375][475])]
        node31 = self.colorVals[tuple(self.img[475][675])]
        node32 = self.colorVals[tuple(self.img[475][575])]
        node33 = self.colorVals[tuple(self.img[475][475])]
        
        if (node31+node32+node33) >= (node22+node23) and (node31+node32+node33) >= (node11+node12+node13):
            route = [[375,698],[448,698]]
            self.nextRoute =[[452,698],[452,602]]
        
        elif (node11+node12+node13) >= (node31+node32+node33) and (node11+node12+node13) >= (node22+node23):
            route = [[375,698],[302,698]]
            self.nextRoute = [[298,698],[298,602]]
        
        else:
            route =[[375,625]]
            if node23 >= node12 and node23 >= node32:
                self.nextRoute = [[375,525]]
            elif node32 >= node23 and node32 >= node12:
                self.nextRoute = [[375,598],[448,598]]
            else:
                self.nextRoute = [[375,598],[302,598]]
        self.startCount = 1
        return route
    def start9(self):
        node11 = self.colorVals[tuple(self.img[475][675])]
        node12 = self.colorVals[tuple(self.img[475][575])]
        node22 = self.colorVals[tuple(self.img[575][575])]
        node31 = self.colorVals[tuple(self.img[675][675])]
        if node31 == 100:
            route = [[575,698],[648,698]]
            self.nextRoute =[[652,698],[652,602]]
        
        elif node31 == 50 and (node11+node12+node22)<50:
            route = [[575,698],[648,698]]
            self.nextRoute =[[652,698],[652,602]]
        
        else:
            route = [[575,698],[502,698]]
            self.nextRoute =[[498,698],[498,602]]
        self.startCount = 1
        return route
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

def create_myroute(x1,x2,y1,y2):
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
def create_route(x1,x2,y1,y2):
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
        array = create_route(myX,targetX,myY,targetY)
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
                    array.append([newX,targetY-28])
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
                    array.append([newX,targetY-28])
                    if newX >=  targetX + 24:
                        array.append([targetX+23 ,targetY-28])
                        array.append([targetX+23 ,targetY-23])
                    elif newX <= targetX - 24:
                        array.append([targetX-23,targetY-28])
                        array.append([targetX-23,targetY-23])
    return array

