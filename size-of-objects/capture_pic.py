import numpy as np
import cv2

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((5*5, 3), np.float32)
objp[:, :2] = np.mgrid[0:5, 0:5].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
# capture video
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

        ret1, corners = cv2.findChessboardCorners(gray, (5, 5), None)

        # If found, add object points, image points (after refining them)
        if ret1 == True:
            print('hello')
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (5, 5), corners2, ret)
            cv2.imshow('img', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
capt.release()
