from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import serial
import time
import struct
from bags import *
from serial_coms_list import *


def startUpRoutine(ser, cap):
    setHome(ser)
    gripClose(ser)
    gripRotate(180, ser)
    ret, frame = cap.read()
    while(1):
        try:
            roi = crop_pic(frame)
            contours = get_contours(roi)
            for c in contours:
                cv2.drawContours(frame, c, 0, (0, 255, 0), 2)
            box, x_pixels_per_mil, y_pixels_per_mil = find_box(
                contours, 45000, roi)
            print('ready to start')
            cv2.imshow("bg", frame)
            # cv2.waitKey(0)
            return box, x_pixels_per_mil, y_pixels_per_mil, frame
        except:
            pass


def handleBag(ser, desired_type, bag_list, config, countsPerMillimeter, countsPerMillimeter_z, x_pixels_per_mil, y_pixels_per_mil, roi_width, roi_height):
    print('remaining bags: ')
    for bag in bag_list:
        print(str(bag))
    # setHome(ser)
    gripClose(ser)
    gripRotate(180, ser)
    for bag in bag_list:
        bag_x, bag_y = bag.center
        bag_x_grip = bag_x / x_pixels_per_mil + 10  # 10 mm from the gripper 0
        bag_y_grip = bag_y / y_pixels_per_mil - 50  # pic 0 is -50 mm
        if bag_y_grip < 0:  # Saturate for output
            bag_y_grip = 0
        bag_x_count = int(bag_x_grip * countsPerMillimeter)
        bag_y_count = int(bag_y_grip * countsPerMillimeter)
        # angle in minAreaRect is clockwise, and servo turns clockwise. the conditional is to checkthe width and height
        if bag.angle < 90:
            if bag.width >= bag.height:
                bag_angle = 90 + bag.angle
            else:
                bag_angle = bag.angle
        elif bag.angle >= 90:
            if bag.width >= bag.height:
                bag_angle = 180 + bag.angle
            else:
                bag_angle = 90 + bag.angle
        else:
            print('wtf')
            bag_angle = bag.angle
        if bag_angle < 0:
            bag_angle += 180
        if bag.type == desired_type and bag_x_grip < 160:
            goal = config[0]
            setPosXY(bag_x_count, bag_y_count, ser)
            gripRotate(int(bag_angle), ser)
            gripOpen(ser)
            setPosZ(int(135 * countsPerMillimeter_z), ser)
            gripClose(ser)
            setPosZ(int(50 * countsPerMillimeter_z), ser)
            gripRotate(goal[3], ser)
            setPosXY(int(goal[0] * countsPerMillimeter),
                     int(goal[1] * countsPerMillimeter), ser)
            setPosZ(int(goal[2] * countsPerMillimeter_z), ser)
            gripOpen(ser)
            setHome(ser)
            gripClose(ser)
            gripRotate(180, ser)
            del config[0]
        if bag.type != desired_type and bag_x_grip < 160:
            setPosXY(bag_x_count, bag_y_count, ser)
            gripRotate(int(bag_angle), ser)
            gripOpen(ser)
            setPosZ(int(135 * countsPerMillimeter_z), ser)
            gripClose(ser)
            setPosZ(int(50 * countsPerMillimeter_z), ser)
            gripRotate(0, ser)
            setPosXY(int(360 * countsPerMillimeter),
                     0, ser)
            setPosZ(int(100 * countsPerMillimeter_z), ser)
            gripOpen(ser)
            setHome(ser)
        if bag.type != desired_type and bag_x_grip > 160:
            print('nothing can be done')
        bag_list.remove(bag)

    start = 0
    for bag in baglist:
        print(str(bag))
    config = []


# connect to video
try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)
# Connect to PIC
try:
    BAUDRATE = 9600
    portName = "COM" + str(6)
    serialDevice = serial.Serial()
    serialDevice.baudrate = BAUDRATE
    serialDevice.port = portName
    serialDevice.timeout = 1
    serialDevice.rts = 0
    serialDevice.dtr = 0
    serialDevice.open()
    print('connected to pic')
except:
    try:
        BAUDRATE = 9600
        portName = "COM" + str(13)
        serialDevice = serial.Serial()
        serialDevice.baudrate = BAUDRATE
        serialDevice.port = portName
        serialDevice.timeout = 1
        serialDevice.rts = 0
        serialDevice.dtr = 0
        serialDevice.open()
        print('connected to pic')
    except:
        BAUDRATE = int(input("input baud rate: "))
        portName = "COM" + str(input("Port: COM"))
        serialDevice = serial.Serial()
        serialDevice.baudrate = BAUDRATE
        serialDevice.port = portName
        serialDevice.timeout = 1
        serialDevice.rts = 0
        serialDevice.dtr = 0
        serialDevice.open()
        print('connected to pic')


box, x_pixels_per_mil, y_pixels_per_mil, image = startUpRoutine(
    serialDevice, cap)
# set up stuff here then
countsPerMillimeter = (331 / 300 * 400) / (np.pi * 10)
countsPerMillimeter_z = (12 * 66) / (np.pi * 12)
Xbox, Ybox = box.center
center_x = Xbox - x_pixels_per_mil * 50 + 270 - 185
center_y = Ybox - y_pixels_per_mil * 50 + 250 - 157.5
roi_width = x_pixels_per_mil * 400
roi_height = y_pixels_per_mil * 400
rectangle = [(center_x, center_y), (roi_width, roi_height), box.angle]

bag_configs = {
    '1': [[322, 172, 208, 0], [196, 172, 208, 180], [322, 172, 186, 0], [196, 172, 186, 180], [322, 172, 164, 0], [196, 172, 164, 180]],
    '2': [[322, 238, 208, 180], [228, 252, 208, 270], [212, 163, 190, 0], [292, 133, 192, 90]],
    '3': [[188, 175, 208, 180], [188, 200, 186, 180], [188, 225, 164, 180], [322, 175, 208, 0], [322, 200, 186, 0], [322, 225, 164, 0]],
}
print(str(countsPerMillimeter))
print(str(countsPerMillimeter_z))
# print("pixpermil" + str(x_pixels_per_mil))
# print(type(roi_height))
# print(int(np.asscalar(center_x)))
# print(type(int(np.asscalar(center_x))))
# print("cX: " + str(center_x))
# print("cY: " + str(center_y))
# print("roi_width: " + str(roi_width))
# print("roi_height: " + str(roi_height))

time.sleep(0.5)

startTime = time.time()
desired_types = {
    '1': 'colored',
    '2': 'large_pebbles',
    '3': 'small_pebbles',
}
while(1):
    try:
        keydt = input(
            "input desired bag type:\n1: colored\n2: large_pebbles\nsmall_pebbles\n")
        desired_type = desired_types[keydt]
        break
    except:
        print('try again')

while(1):
    try:
        config = bag_configs[input("input desired bag placement:\n1\n2\n3\n")]
        break
    except:
        print('try again')
bag_list = []
start = 0

while(1):
    print("remaining spots: ")
    print(config)
    ret, frame = cap.read()
    # frame = frame[int(250 - 315 / 2): int(250 + 315 / 2),
    #               int(270 - 370 / 2): int(370 + 370 / 2)]
    # cv2.drawContours(frame, [box[0].astype("int")], -1, (0, 0, 0), 3)
    if abs(box.min_rect[2]) < 45:
        roteangle = 0 - box.min_rect[2]
    else:
        roteangle = box.min_rect[2] - 270
    roted = imutils.rotate(frame, angle=roteangle)
    for i in config:
        cv2.circle(roted, ((int(x_pixels_per_mil *
                                i[0] + 270 - 185)), int(y_pixels_per_mil * i[1] + 250 - 157.5)), 5, (0, 0, 255), -1)
    # cv2.imshow("uncropped", frame)
    cv2.imshow("roted", roted)
    if serialDevice.inWaiting() > 0:
        # data = serialDevice.read(1)
        # print("data =", ord(data))
        try:
            print(serialDevice.readline().decode('utf-8'))
        except:
            pass
    if start == 1 and config is not []:
        cv2.waitKey(0)
        if bag_list == []:
            baglist, bowox, labeled_image = get_bags(
                roted, center_x, center_y, roi_width, roi_height)
            bag_list.extend(baglist)
            cv2.imshow('current', labeled_image)

        handleBag(serialDevice, desired_type, bag_list,
                  config, countsPerMillimeter, countsPerMillimeter_z, x_pixels_per_mil, y_pixels_per_mil, roi_width, roi_height)
    elif start == 1 and config == []:
        start = 0
        break
    else:
        print("1: set Home\n2: set x, y \n3: set z \n4: close gripper\n5: open gripper\n6: rotate gripper\nka: set gains for A-axis\nkb: set gains for the B-axis\nkz: set gains for the Z-axis")
        keyinput = input("input command: ")
        if keyinput != '':
            if keyinput == '0':
                break
            elif keyinput == '1':
                setHome(serialDevice)
            elif keyinput == '2':
                x = int(input("input x: "))
                y = int(input("input y: "))
                setPosXY(x, y, serialDevice)
            elif keyinput == '3':
                z = int(input("input z: "))
                setPosZ(z, serialDevice)
            elif keyinput == '4':
                gripClose(serialDevice)
            elif keyinput == '5':
                gripOpen(serialDevice)
            elif keyinput == '6':
                angle = int(input("input angle: "))
                gripRotate(angle, serialDevice)
            elif keyinput == 'ka':
                K_Pa = float(input("input K_Pa:"))
                K_Ia = float(input("input K_Ia:"))
                K_Da = float(input("input K_Da:"))
                setAGains(K_Pa, K_Ia, K_Da, serialDevice)
            elif keyinput == 'kb':
                K_Pb = float(input("input K_Pb:"))
                K_Ib = float(input("input K_Ib:"))
                K_Db = float(input("input K_Db:"))
                setBGains(K_Pb, K_Ib, K_Db, serialDevice)
            elif keyinput == 'kz':
                K_Pz = float(input("input K_Pz:"))
                K_Iz = float(input("input K_Iz:"))
                K_Dz = float(input("input K_Dz:"))
                setZGains(K_Pz, K_Iz, K_Dz, serialDevice)
            elif keyinput == 'tol':
                setTolerances(serialDevice)
            elif keyinput == 'bags':
                baglist, newbox, labeled_image = get_bags(
                    roted, center_x, center_y, roi_width, roi_height)
                bag_list.extend(baglist)
                start = 1
                cv2.imshow('current', labeled_image)
            elif keyinput == 'posxy':
                x = int(input("input x: "))
                y = int(input("input y: "))
                setPosXY_mm(x, y, serialDevice, x_pixels_per_mil,
                            y_pixels_per_mil, countsPerMillimeter)
            elif keyinput == 'posz':
                z = int(input("input z: "))
                setPosZ_mm(z, serialDevice, countsPerMillimeter_z)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
serialDevice.close()
print("end")
