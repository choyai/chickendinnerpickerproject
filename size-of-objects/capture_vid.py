from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


cap = cv2.VideoCapture(0)
period = 0.1
nexttime = time.time() + period
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    orig = frame.copy()
    now = time.time()
    refObj = None
    if(nexttime <= now):
        nexttime = now + period
        image = frame
        width = 26
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        (cnts, _) = contours.sort_contours(cnts)
        colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255), (255, 255, 0), (255, 0, 255))
        pixelsPerMetric = None
        for c in cnts:
            if cv2.contourArea(c) < 100:
                continue
                orig = image.copy()
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            cX = np.average(box[:, 0])
            cY = np.average(box[:, 1])
            if refObj is None:
                (tl, tr, br, bl) = box
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                refObj = (box, (cX, cY), D / width)
                continue
            orig = image.copy()
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            cv2.drawContours(orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
            refCoords = np.vstack([refObj[0], refObj[1]])
            objCoords = np.vstack([box, (cX, cY)])
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
                (tl, tr, br, bl) = box
                (tltrX, tltrY) = midpoint(tl, tr)
                (blbrX, blbrY) = midpoint(bl, br)
                (tlblX, tlblY) = midpoint(tl, bl)
                (trbrX, trbrY) = midpoint(tr, br)
                cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
                cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
                cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                         (255, 0, 255), 2)
                cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                         (255, 0, 255), 2)
                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                if pixelsPerMetric is None:
                    pixelsPerMetric = dB/width
                dimA = dA / pixelsPerMetric
                dimB = dB / pixelsPerMetric
                for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
                    cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
                    cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
                    cv2.line(orig, (int(xA), int(yA)), (int(xB), int(yB)), color, 2)
                    D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
                    (mX, mY) = midpoint((xA, yA), (xB, yB))
                    cv2.putText(orig, "{:.1f}mm".format(D), (int(mX), int(mY - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                    cv2.putText(orig, "{:.1f}mm".format(dimA),
                                (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (255, 255, 255), 2)
                    cv2.putText(orig, "{:.1f}mm".format(dimB),
                                (int(trbrX + 10), int(trbrY)),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.65, (255, 255, 255), 2)
        cv2.imshow("measured", orig)
        # cv2.waitKey(0)
    else:
        orig = frame.copy()
        cv2.imshow('unedited', orig)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
