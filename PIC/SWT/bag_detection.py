from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import time

width = 200


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def crop_minAreaRect(img, rect):

    # rotate img
    angle = rect[2]
    rows, cols = img.shape[0], img.shape[1]
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    img_rot = cv2.warpAffine(img, M, (cols, rows))

    # rotate bounding box
    rect0 = (rect[0], rect[1], 0.0)
    box = cv2.boxPoints(rect)
    pts = np.int0(cv2.transform(np.array([box]), M))[0]
    pts[pts < 0] = 0

    # crop
    img_crop = img_rot[pts[1][1]:pts[0][1],
                       pts[1][0]:pts[2][0]]

    return img_crop


def find_box(contours, max_area, image):
    box_contour = contours[0]
    for c in contours:
        if cv2.contourArea(c) > cv2.contourArea(box_contour) and cv2.contourArea(c) < max_area:
            box_contour = c
            # print(cv2.contourArea(box_contour))
    box = cv2.minAreaRect(box_contour)
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


def colourCheck(im, lowH, lowS, lowV, upH, upS, upV, threshblue):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    lower_blue = np.array([lowH, lowS, lowV])
    upper_blue = np.array([upH, upS, upV])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(im, im, mask=mask)

    # check for blue from grayscale
    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('frame', im)
    # cv2.imshow('mask', mask)
    # cv2.imshow('bluecheck' + str(cX), res)
    # cv2.imshow('gray', gray)
    # bluecount = 0
    # for i in gray:
    #     for j in i:
    #         if j > 10:
    #             bluecount += 1
    bluecount = np.asscalar(np.sum(res))

    # print("blue: " + str(bluecount) + '<' + str(threshblue))
    # print(str(type(bluecount)) + "," + str(type(threshblue)))
    if bluecount >= threshblue:
        return True
    else:
        return False


def sizeCheck(im, lowH, lowS, lowV, upH, upS, upV, thresh, cX):
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    # define range of blue color in HSV
    # lower_color = np.array([110, 50, 50])
    # upper_color = np.array([130, 255, 255])
    lower_color = np.array([lowH, lowS, lowV])
    upper_color = np.array([upH, upS, upV])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_color, upper_color)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(im, im, mask=mask)
    cv2.imshow('sizecheck' + str(cX), res)
    iteration = 0
    # for i in range(len(mask)):
    #     for j in range(len(mask[i])):
    #         if mask[i][j] > 0:
    #             iteration += 1
    iteration = np.asscalar(np.sum(res))
    print("size" + str(cX) + ":  " + str(iteration))
    if iteration > thresh:
        return True
    else:
        return False


def detect_type(big_box, orig, c, lowH, lowS, lowV, upH, upS, upV, thresh, lowblueH, lowblueS, lowblueV, upperblueH, upperblueS, upperblueV, bluethresh):
    # c = big_box[2]
    colors = ((0, 0, 255), (240, 0, 159), (0, 165, 255),
              (255, 255, 0), (255, 0, 255))
    pixelsPerMetric = big_box[2]
    cv2.drawContours(orig, c, 0, (0, 255, 0), 2)
    label = 'unknown'
    box = cv2.boundingRect(c)
    # contour_im = image[box[1]:box[1] +
    #                    box[3], box[0]:box[0] + box[2]]
    box = cv2.minAreaRect(c)
    contour_im = crop_minAreaRect(orig, box)
    # contour_im = image[int(box[0][1] - box[1][1] / 2):int(box[0][1] + box[1][1] / 2),
    #                    int(box[0][0] - box[1][0] / 2): int(box[0][0] + box[1][0] / 2)]
    min_rect = box
    box = cv2.cv.BoxPoints(
        box) if imutils.is_cv2() else cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    cX = np.average(box[:, 0])
    cY = np.average(box[:, 1])
    try:
        colour = colourCheck(
            contour_im, lowblueH, lowblueS, lowblueV, upperblueH, upperblueS, upperblueV, bluethresh)
        size = sizeCheck(contour_im, lowH, lowS,
                         lowV, upH, upS, upV, thresh, cX)
        if cX == big_box[1][0]:
            label = 'box'
        elif colour == True:
            label = 'colored'
        elif size == True:
            label = 'small_pebbles'
        else:
            label = 'large_pebbles'
    except Exception:
        raise Exception
        label = 'unknown'
    cv2.imshow(label + str(int(cX)), contour_im)

    cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
    if big_box is not None:
        cv2.drawContours(
            orig, [big_box[0].astype("int")], -1, (0, 255, 0), 2)
        refCoords = np.vstack([big_box[0], big_box[1]])
        objCoords = np.vstack([box, (cX, cY)])
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
            (tl, tr, br, bl) = box
            cv2.putText(
                orig, label, (bl[0], bl[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
            (tltrX, tltrY) = midpoint(tl, tr)
            (blbrX, blbrY) = midpoint(bl, br)
            (tlblX, tlblY) = midpoint(tl, bl)
            (trbrX, trbrY) = midpoint(tr, br)
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
            # cv2.putText(orig, "{:.1f}mm".format(dimA),
            #             (int(tltrX - 15), int(tltrY - 10)
            #              ), cv2.FONT_HERSHEY_SIMPLEX,
            #             0.65, (255, 255, 255), 2)
            # cv2.putText(orig, "{:.1f}mm".format(dimB),
            #             (int(trbrX + 10), int(trbrY)),
            #             cv2.FONT_HERSHEY_SIMPLEX,
            #             0.65, (255, 255, 255), 2)
    return label, min_rect

# returns an array of bags which are an array of type and minAreaRect and also the big_box and image
# too many levels of abstraction is killing me ugh


def get_bags(cap):
    g_kernel = 3
    bi_kernel = 5
    bi_area = 140
    min_area = 1700
    max_area = 45000
    LOW_edge = 50
    HIGH_edge = 139
    current_filter = 2
    center_x = 288
    center_y = 300
    roi_width = 360
    roi_height = 275
    lowH = 25
    lowS = 6
    lowV = 25
    upH = 25
    upS = 255
    upV = 255
    thresh = 42000
    lowblueH = 110
    lowblueS = 50
    lowblueV = 50
    upperblueH = 130
    upperblueS = 255
    upperblueV = 255
    bluethresh = 10000

    gauss_args = [g_kernel, g_kernel]
    bilat_args = [bi_kernel, bi_area, bi_area]

    ret, frame = cap.read()
    cv2.imshow("uncropped image", frame)
    orig = frame.copy()
    roi = frame[int(center_y - roi_height / 2): int(center_y + roi_height / 2),
                int(center_x - roi_width / 2): int(center_x + roi_width / 2)]
    now = time.time()

    image = roi

    edged = []
    # Apply filters

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

    # total list of individual filters
    filtered = [gray, global_histeq, gauss,
                bilat]

    # perform Canny edge detection on all filters
    for i in range(len(filtered)):
        edged.append(cv2.Canny(filtered[i], LOW_edge, HIGH_edge))
        edged[i] = cv2.dilate(edged[i], None, iterations=2)
        edged[i] = cv2.erode(edged[i], None, iterations=2)
        # cv2.imshow("dilated" + str(i) + str(num), edged[i])
    cv2.imshow("dilated" + str(3), edged[3])

    # findContours
    index = current_filter
    cnts = cv2.findContours(edged[index].copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    if len(cnts) is not 0:

        # (cnts, _) = contours.sort_contours(cnts)
        orig = image.copy()
        big_box = find_box(cnts, max_area, image)
        bags = []
        for c in cnts:
            if cv2.contourArea(c) < min_area or cv2.contourArea(c) > max_area:
                continue

            type, min_rect = detect_type(big_box, orig, c, lowH, lowS, lowV, upH, upS, upV, thresh, lowblueH,
                                         lowblueS, lowblueV, upperblueH, upperblueS, upperblueV, bluethresh)
            # important!!!!
            # print(type)
            bags.append([type, min_rect])
        cv2.imshow("orig", orig)
        return bags, big_box, orig


# try:
#     cap = cv2.VideoCapture(0)
# except:
#     cap = cv2.VideoCapture(1)
#
# period = 0.1
# nexttime = time.time() + period
# # bgsub = cv2.bgsegm.createBackgroundSubtractorMOG()
# # ret, bg = cap.read()
# # bgsub.apply(bg, learningRate=0.5)
# # cv2.imshow("background", bg)
# while(True):
#     print(get_bags(cap))
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
