import cv2 as cv
import numpy as np
import astar
from matplotlib import pyplot as plt

def get_maze_image():
    """
    Reads the maze image from the file and tresholds it than returns it as a numpy array.
    """
    maze_image = cv.imread('./maze.jpg', cv.IMREAD_GRAYSCALE)
    _, maze_image = cv.threshold(maze_image, 127, 255, cv.THRESH_BINARY)
    plt.imshow(maze_image, cmap='gray')
    plt.show()
    return maze_image

def get_maze_path(maze_image, start, end):
    """
    This function returns the path from the start to the end point.
    """
    maze_image = maze_image.astype(np.uint8)
    maze_image = cv.cvtColor(maze_image, cv.COLOR_GRAY2BGR)
    path = astar.astar(maze_image, start, end)
    return path


maze_image = get_maze_image()
start, end = [0,0], [200,200]
path = get_maze_path(maze_image, start, end)
for i,j in path:
    maze_image[i,j] = 123

plt.imshow(maze_image, cmap='gray')
plt.show()
