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
from bag_detection import get_bags
from serial_coms_list import *


def startUpRoutine(ser, cap):
    setHome(ser)
    gripClose(ser)
    gripRotate(0)
    while(1)
       try:
            bags, box, image = get_bags(cap)
            print('ready to start')
            return box, image
        except:
            pass


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

# connect to video

try:
    cap = cv2.VideoCapture(0)
except:
    cap = cv2.VideoCapture(1)

startUpRoutine(serialDevice, cap)

time.sleep(0.5)

startTime = time.time()
while(1):
    if serialDevice.inWaiting() > 0:
        # data = serialDevice.read(1)
        # print("data =", ord(data))
        try:
            print(serialDevice.readline().decode('utf-8'))
        except:
            pass
    print("1: set Home\n2: set x, y \n3: set z \n4: close gripper\n5: open gripper\n6: rotate gripper\nka: set gains for A-axis\nkb: set gains for the B-axis\nkz: set gains for the Z-axis")
    keyinput = input("input command: ")
    if keyinput != '':
        if keyinput == 'd':
            serialDevice.write(bytes(arrayData))
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
serialDevice.close()
print("end")
