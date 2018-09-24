# from scipy.spatial import distance as dist
# from imutils import perspective
# from imutils import contours
import numpy as np
# import argparse
# import imutils
import cv2

orig = cv2.imread('gofestoneyear.jpg')

# Grayscale conversion
gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)

# Blur with Gaussian filter
gauss = cv2.GaussianBlur(gray, (5, 5), 3)

# generate mask
mask = gray - gauss

# Add mask to original for k = 1 to k = 3(highboost)
sharp = []

while True:
    cv2.imshow("grayscale", gray)
    cv2.imshow("mask", mask)
    for k in range(3):
        sharp.append(gray + (k + 1) * mask)
        cv2.imshow("k = " + str(k + 1), sharp[k])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
