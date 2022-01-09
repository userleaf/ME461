import numpy as np
import cv2
cap =cv2.VideoCapture(0)
ret, frame = cap.read()
frame= cv2.imread("test.png")
display=np.zeros(frame.shape)
h=frame.shape[0]
w=frame.shape[1]
mini_frame=cv2.resize(frame,(0,0),fx=0.5,fy=0.5)
r=np.zeros(mini_frame.shape)
g=np.zeros(mini_frame.shape)
b=np.zeros(mini_frame.shape)
for i in range(w//2):
    for j in range(h//2):
        r[j][i][2]=mini_frame[j][i][2]
        g[j][i][1]=mini_frame[j][i][1]
        b[j][i][0]=mini_frame[j][i][0]
r = cv2.convertScaleAbs(r)
g = cv2.convertScaleAbs(g)
b = cv2.convertScaleAbs(b)
display[:h//2+1, :w//2]=r
display[h//2:, :w//2]=g
display[:h//2+1, w//2:]=b
display[h//2:, w//2:]=mini_frame
display=cv2.resize(display,(0,0),fx=0.3,fy=0.3)
cv2.imshow('chaneled.png',display)
k = cv2.waitKey(0)
if k == ord("s"):
    cv2.destroyAllWindows()
