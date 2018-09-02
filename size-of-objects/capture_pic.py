import numpy as np
import cv2

capt = cv2.VideoCapture(0)
# return single frame
iter = 0
while(True):
    # display the captured image
    ret, frame = capt.read()
    img = frame
    cv2.imshow('img1', frame)
    # save on pressing 's'
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        iterstring = str(iter)
        cv2.imshow('grayscale', gray)
        cv2.imwrite('im' + iterstring + '.jpg', frame)
        iter += 1
        cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
capt.release()
