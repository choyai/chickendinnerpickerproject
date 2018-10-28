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


width = 200


def find_box(contours):
    box_contour = contours[0]
    for c in contours:
        if cv2.contourArea(c) > cv2.contourArea(box_contour) and cv2.contourArea(c) < max_area:
            box_contour = c
            # print(cv2.contourArea(box_contour))
    box = cv2.minAreaRect(box_contour)
    label = 'box'
    straight_rect = cv2.boundingRect(box_contour)
    box_im = image[straight_rect[1]:straight_rect[1] + straight_rect[3],
                   straight_rect[0]: straight_rect[0] + straight_rect[2]]
    # print(box_im)
    try:
        cv2.imshow('box', box_im)
    except Exception:
        raise Exception
    box = cv2.cv.BoxPoints(
        box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])
    (tl, tr, br, bl) = box
    (tlblX, tlblY) = midpoint(tl, bl)
    (trbrX, trbrY) = midpoint(tr, br)
    D = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
    refObj = (box, (cX, cY), D / width, box_contour)
    pixelsPerMetric = D / width
    return refObj


def nothing(n):
    pass


try:
    cap = cv2.VideoCapture(1)
except:
    cap = cv2.VideoCapture(0)
# Create Trackbars to adjust settings
cv2.namedWindow('menu', cv2.WINDOW_NORMAL)
cv2.createTrackbar('Gauss Kernel', 'menu', 3, 9, nothing)
cv2.createTrackbar('Bilat Kernel', 'menu', 3, 9, nothing)
cv2.createTrackbar('Bilat Area', 'menu', 75, 200, nothing)
cv2.createTrackbar('Canny Low', 'menu', 50, 255, nothing)
cv2.createTrackbar('Canny High', 'menu', 100, 255, nothing)
cv2.createTrackbar('MinArea', 'menu', 1000, 100000, nothing)
cv2.createTrackbar('MaxArea', 'menu', 45000, 100000, nothing)
cv2.createTrackbar('Filter Type', 'menu', 3, 6, nothing)
cv2.createTrackbar('center_x', 'menu', 320, 640, nothing)
cv2.createTrackbar('center_y', 'menu', 240, 480, nothing)
cv2.createTrackbar('width', 'menu', 320, 640, nothing)
cv2.createTrackbar('height', 'menu', 240, 480, nothing)

period = 0.1
nexttime = time.time() + period
# bgsub = cv2.bgsegm.createBackgroundSubtractorMOG()
# ret, bg = cap.read()
# bgsub.apply(bg, learningRate=0.5)
# cv2.imshow("background", bg)
while(True):
    # get values from Trackbars
    g_kernel = cv2.getTrackbarPos('Gauss Kernel', 'menu')
    bi_kernel = cv2.getTrackbarPos('Bilat Kernel', 'menu')
    bi_area = cv2.getTrackbarPos('Bilat Area', 'menu')
    min_area = cv2.getTrackbarPos('MinArea', 'menu')
    max_area = cv2.getTrackbarPos('MaxArea', 'menu')
    LOW_edge = cv2.getTrackbarPos('Canny Low', 'menu')
    HIGH_edge = cv2.getTrackbarPos('Canny High', 'menu')
    current_filter = cv2.getTrackbarPos('Filter Type', 'menu')
    center_x = cv2.getTrackbarPos('center_x', 'menu')
    center_y = cv2.getTrackbarPos('center_y', 'menu')
    roi_width = cv2.getTrackbarPos('width', 'menu')
    roi_height = cv2.getTrackbarPos('height', 'menu')
    if HIGH_edge < LOW_edge:
        HIGH_edge = LOW_edge + 1
    if center_x == 0:
        center_x = 1
    if center_y == 0:
        center_y = 1
    if center_x + roi_width / 2 > 640:
        roi_width = 2 * (640 - center_x)
    if center_x - roi_width / 2 < 0:
        roi_width = 2 * center_x
    if center_y + roi_height / 2 > 480:
        roi_height = 2 * (480 - center_y)
    if center_y - roi_height / 2 < 0:
        roi_height = 2 * center_y
    if min_area == 0:
        min_area = 1
    if g_kernel % 2 == 0:
        g_kernel += 1
    if bi_kernel == 0:
        bi_kernel = 1
    if bi_area == 0:
        bi_area = 1

    gauss_args = [g_kernel, g_kernel]
    bilat_args = [bi_kernel, bi_area, bi_area]

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
    cv2.imshow("uncropped image", frame)
    orig = frame.copy()
    roi = frame[int(center_y - roi_height / 2): int(center_y + roi_height / 2),
                int(center_x - roi_width / 2): int(center_x + roi_width / 2)]
    now = time.time()
    # refObj = None

    if(nexttime <= now):
        image = roi
        nexttime = now + period

        edged = []
        # Apply filters
        # grayscale
        # bgsubbed = bgsub.apply(image, learningRate=0)
        # gray = bgsubbed
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # clahe = cv2.createCLAHE(cliplimit=clm, tilegridsize=tgs)
        # Contrast Limited Adaptive Histogram Equalization
        clahe = cv2.createCLAHE()
        cl1 = clahe.apply(gray)

        # gaussian blur
        # gauss = cv2.GaussianBlur(gray, (3, 3), 0)
        gauss = cv2.GaussianBlur(gray, (gauss_args[0], gauss_args[1]), 0)

        # global Histogram Equalization
        global_histeq = cv2.equalizeHist(gray)

        # bilateralFilter
        bilat = cv2.bilateralFilter(
            gray, bilat_args[0], bilat_args[1], bilat_args[2])

        # # gauss + bilat
        # gauss_bilat = cv2.bilateralFilter(
        #     gauss, bilat_args[0], bilat_args[1], bilat_args[2])
        #
        # # bilat + clahe
        # bilat_clahe = cv2.bilateralFilter(
        #     cl1, bilat_args[0], bilat_args[1], bilat_args[2])

        # total list of individual filters
        filtered = [gray, global_histeq, gauss,
                    bilat]

        # perform Canny edge detection on all filters
        for i in range(len(filtered)):
            edged.append(cv2.Canny(filtered[i], LOW_edge, HIGH_edge))
            edged[i] = cv2.dilate(edged[i], None, iterations=1)
            edged[i] = cv2.erode(edged[i], None, iterations=1)
            cv2.imshow("dilated" + str(i), edged[i])

        # findContours
        index = current_filter
        cnts = cv2.findContours(edged[index].copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if imutils.is_cv2() else cnts[1]
        if len(cnts) is not 0:

            # (cnts, _) = contours.sort_contours(cnts)

            colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255),
                      (255, 255, 0), (255, 0, 255))
            orig = image.copy()
            big_box = find_box(cnts)
            pixelsPerMetric = big_box[2]
            for c in cnts:
                if cv2.contourArea(c) < min_area or cv2.contourArea(c) > max_area:
                    continue
                label = 'unknown'
                box = cv2.boundingRect(c)
                contour_im = image[box[1]:box[1] +
                                   box[3], box[0]:box[0] + box[2]]
                box = cv2.minAreaRect(c)
                # rot_box_im = image[int(box[0][0]):int(
                #     box[2][1]), int(box[0][1]):int(box[2][1])]
                box = cv2.cv.BoxPoints(
                    box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                box = perspective.order_points(box)
                try:
                    if c.all() == big_box[3].all():
                        label = 'box'
                    cv2.imshow(label + str(cnts.index(c)), contour_im)
                except:
                    label = 'unknown'
                cX = np.average(box[:, 0])
                cY = np.average(box[:, 1])
                cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
                if big_box is not None:
                    print('hi')
                    cv2.drawContours(
                        orig, [big_box[0].astype("int")], -1, (0, 255, 0), 2)
                    refCoords = np.vstack([big_box[0], big_box[1]])
                    objCoords = np.vstack([box, (cX, cY)])
                    for (x, y) in box:
                        cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
                        (tl, tr, br, bl) = box
                        cv2.putText(orig, label,
                                    (int(midpoint(tl, bl)[1]),
                                     int(midpoint(tl, tr)[0])),
                                    cv2.FONT_HERSHEY_SIMPLEX,
                                    0.65, (255, 0, 255), 2)
                        (tltrX, tltrY) = midpoint(tl, tr)
                        (blbrX, blbrY) = midpoint(bl, br)
                        (tlblX, tlblY) = midpoint(tl, bl)
                        (trbrX, trbrY) = midpoint(tr, br)
                        cv2.circle(orig, (int(tltrX), int(tltrY)),
                                   5, (255, 0, 0), -1)
                        cv2.circle(orig, (int(blbrX), int(blbrY)),
                                   5, (255, 0, 0), -1)
                        cv2.circle(orig, (int(tlblX), int(tlblY)),
                                   5, (255, 0, 0), -1)
                        cv2.circle(orig, (int(trbrX), int(trbrY)),
                                   5, (255, 0, 0), -1)
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
                        (xA, yA) = big_box[1]
                        (xB, yB) = (cX, cY)
                        color = (0, 255, 255)
                        # cv2.line(orig, (int(xA), int(yA)),
                        #          (int(xB), int(yB)), color, 2)
                        # D = dist.euclidean((xA, yA), (xB, yB)) / big_box[2]
                        # (mX, mY) = midpoint((xA, yA), (xB, yB))
                        # cv2.putText(orig, "{:.1f}mm".format(D), (int(mX), int(mY - 10)),
                        #             cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
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
        orig = roi.copy()
        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
        # gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
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
        # gauss + bilat
        gauss_bilat = cv2.bilateralFilter(
            gauss, bilat_args[0], bilat_args[1], bilat_args[2])
        # bilat + clahe
        bilat_clahe = cv2.bilateralFilter(
            cl1, bilat_args[0], bilat_args[1], bilat_args[2])

        # perform Canny edge detection on all filters
        for i in range(len(filtered)):
            edged[i] = (cv2.Canny(filtered[i], 50, 100))
            edged[i] = cv2.dilate(edged[i], None, iterations=1)
            edged[i] = cv2.erode(edged[i], None, iterations=1)
            # cv2.imshow("dilated" + str(i), edged[i])

    # for i in range(len(filtered)):
    #     cv2.imshow('filtered' + str(i), filtered[i])
    for i in range(len(edged)):
        cv2.imshow('edged' + str(i), edged[i])
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
