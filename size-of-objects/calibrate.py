import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((5 * 5, 3), np.float32)
objp[:, :2] = np.mgrid[0:5, 0:5].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.

images = glob.glob('images\*.jpg')
print(images)

for fname in images:
    for i in range(6, len(fname)):
        fname[i - 1] = fname[i]
    print(fname)
    img = cv2.imread(fname)
    cv2.imshow('img', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray', gray)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (5, 5), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(
            gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (5, 5), corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(500)
    else:
        print("lol what")

cv2.destroyAllWindows()
