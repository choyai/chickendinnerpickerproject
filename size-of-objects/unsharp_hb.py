# from scipy.spatial import distance as dist
# from imutils import perspective
# from imutils import contours
import numpy as np
# import argparse
# import imutils
import cv2


image = cv2.imread("gofestoneyear.jpg")
gaussian_3 = cv2.GaussianBlur(image, (5, 5), 10.0)
unsharp_image = cv2.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)
highboost1 = cv2.addWeighted(unsharp_image, 1.5, gaussian_3, -0.5, 0, image)
highboost2 = cv2.addWeighted(highboost1, 1.5, gaussian_3, -1, -0.5, image)
cv2.imwrite("gofestunsharp.jpg", unsharp_image)
cv2.imwrite("gofesthb1.jpg", highboost1)
cv2.imwrite("gofesthb2.jpg", highboost2)
