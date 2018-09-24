from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time

cap = cv2.VideoCapture(0)
period = 0.1
nexttime = time.time() + period

while(True):
    gauss_args = [3, 3]
    bilat_args = [9, 75, 75]
    k1size = 3
    kernel1 = np.ones((k1size, k1size), np.float32) / (k1size ^ 2)

    # argument input
    gauss_args[0] = int(input("gauss x"))
    gauss_args[1] = int(input("gauss y"))
    bilat_args[0] = int(input("bilat kernel size"))
    bilat_args[1] = int(input("bilat1"))
    bilat_args[2] = int(input("bilat2"))

    # Capture frame-by-frame
    ret, frame = cap.read()
    orig = frame.copy()
    now = time.time()
    refObj = None

    if(nexttime <= now):
        image = frame
        nexttime = now + period
        width = 26
        edged = []
        # Apply filters
        # grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Averaging
        conv2d = cv2.filter2D(gray, -1, kernel1)
        # Contrast Limited Adaptive Histogram Equalization
        clahe = cv2.createCLAHE()
        cl1 = clahe.apply(gray)
        # gaussian blur
        gauss = cv2.GaussianBlur(gray, (gauss_args[0], gauss_args[1]), 0)
        # global Histogram Equalization
        global_histeq = cv2.equalizeHist(gray)
        # bilateralFilter
        bilat = cv2.bilateralFilter(
            gray, bilat_args[0], bilat_args[1], bilat_args[2])
        #gauss + bilat
        gauss_bilat = cv2.bilateralFilter(
            gauss, bilat_args[0], bilat_args[1], bilat_args[2])
        #bilat + clahe
        bilat_clahe = cv2.bilateralFilter(
            cl1, bilat_args[0], bilat_args[1], bilat_args[2])

        # total list of individual filters
        filtered = [gray, conv2d, global_histeq, gauss,
                    bilat, gauss_bilat, cl1, bilat_clahe]
    for i in range(len(filtered)):
        cv2.imshow('filtered' + str(i), filtered[i])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
