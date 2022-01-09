import numpy as np
import cv2
frame = cv2.imread('sudoku.png')

width = int(frame.shape[1])
height = int(frame.shape[0])
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
corners = cv2.goodFeaturesToTrack(gray, 100, 0.99, 20)
corners = np.int0(corners)
for corner in corners:
    x,y = corner.ravel()
    cv2.circle(frame,(x,y),9,(255,0,0),2)
    print(corner)
frame=cv2.resize(frame,(0,0),fx=0.4,fy=0.4)
cv2.imshow("name",frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

