from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time
from bags import *

try:
    capt = cv2.VideoCapture(0)
except:
    capt = cv2.VideoCapture(1)

# return single frame
iter = 100
bag_types = {
    '1': 'colored',
    '2': 'large_pebbles',
    '3': 'small_pebbles',
}
while(True):
    try:
        bag_type = bag_types[input(
            'what type?\n1: colored\n2: large_pebbles\n3: small_pebbles\n>>')]
        break
    except:
        pass
while(True):
    # display the captured image
    ret, frame = capt.read()
    img = frame
    cv2.imshow('original', frame)
    # Resize using Areal interpolation(assuming camera has higher resolution)
    scaled = crop_pic(frame, 180, 260, 100, 100)
    cv2.imshow('scaled', scaled)
    gray = cv2.cvtColor(scaled, cv2.COLOR_BGR2GRAY)
    cv2.imshow('grayscale', gray)
    # save on pressing 's'
    if cv2.waitKey(1) & 0xFF == ord('s'):
        iterstring = str(iter)

        cv2.imwrite(bag_type + iterstring + '.jpg', scaled)
        # cv2.imwrite('scaled' + iterstring + '.jpg', scaled)
        # cv2.imwrite('grayscale' + iterstring + '.jpg', gray)
        iter += 1
        # cv2.imshow('img', scaled)
    elif cv2.waitKey(1) & 0xFF == ord('r'):
        cv2.imwrite(bag_type + str(iter - 1) + '.jpg', scaled)

    # quit on pressing 'q'
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
capt.release()
