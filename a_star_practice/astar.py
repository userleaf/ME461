import numpy as np
import time
import optparse as op
# import matplotlib.pyplot as plt

'''
This library implements a star algorithm over a cost map.
'''
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
        return prescalar*abs(self.pos[0] - end.pos[0]) + abs(self.pos[1] - end.pos[1])

    def __str__(self):
        return str(self.pos)

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
            if neighbor in closed_list:
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
        if i == current.pos[0]:
            for j in range(current.pos[1]-1,current.pos[1]+2):
                if j < 0 or j >= costmap.shape[1]:
                    continue
                if j == current.pos[1]:
                    continue
                neighbors.append(Node([i,j],current))
        else:
            neighbors.append(Node([i,current.pos[1]],current))
    return neighbors

def main():
    start_time = time.time()
    parser = op.OptionParser()
    parser.add_option('-s','--start',dest='start',help='Start node',default='0,0')
    parser.add_option('-e','--end',dest='end',help='End node',default='30,40')
    parser.add_option('-c','--costmap',dest='costmapsize',help='Costmap size',default='50,50')
    parser.add_option('-p','--prescalar',dest='prescalar',help='Prescalar',default=1)
    (options,args) = parser.parse_args()
    start = options.start.split(',')
    end = options.end.split(',')
    costmapsize = options.costmapsize.split(',')
    prescalar = int(options.prescalar)
    start[1] = int(start[1])
    start[0] = int(start[0])
    end[1] = int(end[1])
    end[0] = int(end[0])
    costmapsize[1] = int(costmapsize[1])
    costmapsize[0] = int(costmapsize[0])
    costmap = np.random.randint(5,10,(int(costmapsize[0]),int(costmapsize[1])))
    path = astar(start,end,costmap)
    # for i,j in path:
    #    costmap[i][j] = 0
    # plt.imshow(costmap,cmap='gray')
    print(time.time()-start_time)
    # plt.show()


if __name__ == '__main__':
    main()
