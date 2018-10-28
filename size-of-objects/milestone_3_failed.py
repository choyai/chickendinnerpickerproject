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


try:
    cap = cv2.VideoCapture(1)
except:
    cap = cv2.VideoCapture(0)
period = 0.1
nexttime = time.time() + period
# bgsub = cv2.bgsegm.createBackgroundSubtractorMOG()
# ret, bg = cap.read()
# bgsub.apply(bg, learningRate=0.5)
# cv2.imshow("background", bg)
edged = []
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
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # gray = cv2.bilateralFilter(gray, 9, 75, 75)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        cv2.imshow('filtered', gray)

        # perform edge detection, then perform a dilation + erosion to
        # close gaps in between object edges
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=1)
        edged = cv2.erode(edged, None, iterations=1)
        cv2.imshow('edged', edged)
        # find contours in the edge map
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]

        # sort the contours from left-to-right and initialize the
        # 'pixels per metric' calibration variable
        (cnts, _) = contours.sort_contours(cnts)
        pixelsPerMetric = None

        orig = image.copy()
        # loop over the contours individually
        for c in cnts:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(c) < 1000 or cv2.contourArea(c) > 45000:
                continue

            # compute the rotated bounding box of the contour
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(
                box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")

            # order the points in the contour such that they appear
            # in top-left, top-right, bottom-right, and bottom-left
            # order, then draw the outline of the rotated bounding
            # box
            box = perspective.order_points(box)
            cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

            # loop over the original points and draw them
            for (x, y) in box:
                cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

            # unpack the ordered bounding box, then compute the midpoint
            # between the top-left and top-right coordinates, followed by
            # the midpoint between bottom-left and bottom-right coordinates
            (tl, tr, br, bl) = box
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)

            # compute the midpoint between the top-left and top-right points,
            # followed by the midpoint between the top-righ and bottom-right
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
            (midX, midY) = midpoint((tlblX, tlblY), (trbrX, trbrY))

            print(str(midX) + ' ' + str(midY))
            # draw the midpoints on the image
            cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
            cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

            # draw lines between the midpoints
            cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                     (255, 0, 255), 2)
            cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                     (255, 0, 255), 2)

            # compute the Euclidean distance between the midpoints
            dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
            dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

            print(str(dA) + 'mm' + str(dB))
            # if the pixels per metric has not been initialized, then
            # compute it as the ratio of pixels to supplied metric
            # (in this case, centimeters)
            if pixelsPerMetric is None:
                pixelsPerMetric = dB / width

            # compute the size of the object
            dimA = dA / pixelsPerMetric
            dimB = dB / pixelsPerMetric

            # draw the object sizes on the image
            cv2.putText(orig, "{:.1f}in".format(dimA),
                        (int(tltrX - 15), int(tltrY - 10)
                         ), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 2)
            cv2.putText(orig, "{:.1f}cm".format(dimB),
                        (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 255, 255), 2)

            # show the output image
            cv2.imshow("Image", orig)
    else:
        orig = frame.copy()
        # gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        # gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        # # clahe = cv2.createCLAHE(cliplimit=clm, tilegridsize=tgs)
        # # Contrast Limited Adaptive Histogram Equalization
        # clahe = cv2.createCLAHE()
        # cl1 = clahe.apply(gray)
        # # gaussian blur
        # gauss = cv2.GaussianBlur(gray, (gauss_args[0], gauss_args[1]), 0)
        # # global Histogram Equalization
        # global_histeq = cv2.equalizeHist(gray)
        # # bilateralFilter
        # bilat = cv2.bilateralFilter(
        #     gray, bilat_args[0], bilat_args[1], bilat_args[2])
        # #gauss + bilat
        # gauss_bilat = cv2.bilateralFilter(
        #     gauss, bilat_args[0], bilat_args[1], bilat_args[2])
        # #bilat + clahe
        # bilat_clahe = cv2.bilateralFilter(
        #     cl1, bilat_args[0], bilat_args[1], bilat_args[2])
        #
        # # total list of individual filters
        # # filtered = [gray, global_histeq, gauss,
        # #             bilat, gauss_bilat, cl1, bilat_clahe]
        # filtered = [gray, bilat]
        cv2.imshow("image", orig)
        # # perform Canny edge detection on all filters
        # for i in range(len(filtered)):
        #     edged.append(cv2.Canny(filtered[i], 50, 100))
        #     edged[i] = cv2.dilate(edged[i], None, iterations=1)
        #     cv2.imshow("dilated" + str(i), edged[i])
        #     edged[i] = cv2.erode(edged[i], None, iterations=1)
        #     cv2.imshow("eroded" + str(i), edged[i])
        #
        # for i in range(len(filtered)):
        #     edged[i] = (cv2.Canny(filtered[i], 50, 100))
        #     edged[i] = cv2.dilate(edged[i], None, iterations=1)
        #     edged[i] = cv2.erode(edged[i], None, iterations=1)
        #     cv2.imshow("dilated" + str(i), edged[i])

    # for i in range(len(filtered)):
    #     cv2.imshow('filtered' + str(i), filtered[i])
    # for i in range(len(edged)):
    #     cv2.imshow('edged' + str(i), edged[i])
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
