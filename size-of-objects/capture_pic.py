import numpy as np
import cv2

# try:
capt = cv2.VideoCapture(0)
# except:
# capt = cv2.VideoCapture(0)

# return single frame
iter = 0
while(True):
    # display the captured image
    ret, frame = capt.read()
    img = frame
    cv2.imshow('original', frame)
    # Resize using Areal interpolation(assuming camera has higher resolution)
    scaled = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_AREA)
    cv2.imshow('scaled', scaled)
    gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    cv2.imshow('grayscale', gray)

    # save on pressing 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        iterstring = str(iter)
        cv2.imwrite('single' + iterstring + '.jpg', frame)
        cv2.imwrite('scaled' + iterstring + '.jpg', scaled)
        cv2.imwrite('grayscale' + iterstring + '.jpg', gray)
        iter += 1
        cv2.imshow('img', gray)
    # quit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
capt.release()
