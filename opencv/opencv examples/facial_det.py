import cv2

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
hat=cv2.imread("fedora.png", cv2.IMREAD_UNCHANGED)
while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2BGRA)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        w=int(w*1.4)
        h=int(hat.shape[0]*(w/hat.shape[1]))
        rhat=cv2.resize(hat,(w,h))
        for i in range(w):
            for ii in range(h):
                if rhat[ii][i][3]>5:
                    frame[y-int(2*h/3.3)+ii][x-int(w/8)+i]=rhat[ii][i]

        # frame[y:y+h][x:x+w]=rhat
        # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # roi_gray = gray[y:y+h, x:x+w]
        # roi_color = frame[y:y+h, x:x+w]
        # eyes = eye_cascade.detectMultiScale(roi_gray, 1.3, 5)
        # for (ex, ey, ew, eh) in eyes:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

