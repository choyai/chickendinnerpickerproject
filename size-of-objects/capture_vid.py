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


cap = cv2.VideoCapture(1)
period = 0.1
nexttime = time.time() + period
bgsub = cv2.bgsegm.createBackgroundSubtractorMOG()
ret, bg = cap.read()
bgsub.apply(bg, learningRate=0.5)
while(True):
    gauss_args = [3, 3]
    bilat_args = [9, 75, 75]

    # argument input
    # gauss_args[0] = int(input("gauss_args0"))
    # gauss_args[1] = int(input("gauss_args1"))
    # bilat_args[0] = int(input("bilat0"))
    # bilat_args[1] = int(input("bilat1"))
    # bilat_args[2] = int(input("bilat2"))
    # clm = int(input("clm"))
    # tgs = int(input("tgs"))

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
        bgsubbed = bgsub.apply(image, learningRate=0)
        gray = bgsubbed
        # gray = cv2.cvtColor(bgsubbed, cv2.COLOR_BGR2GRAY)
        # clahe = cv2.createCLAHE(cliplimit=clm, tilegridsize=tgs)
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
        filtered = [gray, global_histeq, gauss,
                    bilat, gauss_bilat, cl1, bilat_clahe]

        # perform Canny edge detection on all filters
        for i in range(len(filtered)):
            edged.append(cv2.Canny(filtered[i], 50, 100))
            edged[i] = cv2.dilate(edged[i], None, iterations=1)
            edged[i] = cv2.erode(edged[i], None, iterations=1)
            cv2.imshow("dilated" + str(i), edged[i])

        # findContours
        index = 2
        cnts = cv2.findContours(edged[index].copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        # (cnts, _) = contours.sort_contours(cnts)

        colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255),
                  (255, 255, 0), (255, 0, 255))
        pixelsPerMetric = None

        orig = image.copy()
        for c in cnts:
            if cv2.contourArea(c) < 1000 or cv2.contourArea(c) > 40000:
                continue
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(
                box) if imutils.is_cv2() else cv2.boxPoints(box)
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
                if pixelsPerMetric is None:
                    pixelsPerMetric = D / width
                continue
            orig = image.copy()
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
            cv2.drawContours(
                orig, [refObj[0].astype("int")], -1, (0, 255, 0), 2)
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
                # cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                #          (255, 0, 255), 2)
                # cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                #          (255, 0, 255), 2)
                dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
                dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
                dimA = dA / pixelsPerMetric
                dimB = dB / pixelsPerMetric
                for ((xA, yA), (xB, yB), color) in zip(refCoords, objCoords, colors):
                    cv2.circle(orig, (int(xA), int(yA)), 5, color, -1)
                    cv2.circle(orig, (int(xB), int(yB)), 5, color, -1)
                (xA, yA) = refObj[1]
                (xB, yB) = (cX, cY)
                color = (0, 255, 255)
                cv2.line(orig, (int(xA), int(yA)),
                         (int(xB), int(yB)), color, 2)
                D = dist.euclidean((xA, yA), (xB, yB)) / refObj[2]
                (mX, mY) = midpoint((xA, yA), (xB, yB))
                cv2.putText(orig, "{:.1f}mm".format(D), (int(mX), int(mY - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                cv2.putText(orig, "{:.1f}mm".format(dimA),
                            (int(tltrX - 15), int(tltrY - 10)
                             ), cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (255, 255, 255), 2)
                cv2.putText(orig, "{:.1f}mm".format(dimB),
                            (int(trbrX + 10), int(trbrY)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.65, (255, 255, 255), 2)
        cv2.imshow("orig", orig)
        # cv2.waitKey(0)
    else:
        orig = frame.copy()
        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        # clahe = cv2.createCLAHE(cliplimit=clm, tilegridsize=tgs)
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

        # perform Canny edge detection on all filters
        for i in range(len(filtered)):
            edged[i] = (cv2.Canny(filtered[i], 50, 100))
            edged[i] = cv2.dilate(edged[i], None, iterations=1)
            edged[i] = cv2.erode(edged[i], None, iterations=1)
            cv2.imshow("dilated" + str(i), edged[i])

    for i in range(len(filtered)):
        cv2.imshow('filtered' + str(i), filtered[i])
    for i in range(len(edged)):
        cv2.imshow('edged' + str(i), edged[i])
    # WAITKEY sucks
    # if cv2.waitKey(1) & 0xFF == ord('x'):
    #     for i in gauss_args:
    #         i += 1
    #         print(str(i))
    # if cv2.waitKey(1) & 0xFF == ord('c'):
    #     for i in gauss_args:
    #         i -= 1
    #         print(str(i))
    #
    # if cv2.waitKey(1) & 0xFF == ord('y'):
    #     bilat_args[0] += 1
    #     print(str(bilat_args[0]))
    # if cv2.waitKey(1) & 0xFF == ord('u'):
    #     bilat_args[0] -= 1
    #     print(str(bilat_args[0]))
    # if cv2.waitKey(1) & 0xFF == ord('i'):
    #     bilat_args[1] += 5
    #     bilat_args[2] += 5
    #     print(str(bilat_args[1]))
    #     print(str(bilat_args[2]))
    # if cv2.waitKey(1) & 0xFF == ord('o'):
    #     bilat_args[1] -= 5
    #     bilat_args[2] -= 5
    #     print(str(bilat_args[1]))
    #     print(str(bilat_args[2]))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
