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


def setPos(x, y):

    pass


def split_large_ints(num):
    numstring = str(hex(num))
    lsB = '0x'
    msB = '0x'
    if len(numstring) < 5:
        msB = '0x00'
    else:
        if len(numstring) == 5:
            msB += numstring[2]
        else:
            msB = msB + numstring[len(numstring) - 4] + \
                numstring[len(numstring) - 3]
    if len(numstring) < 4:
        lsB += numstring[len(numstring) - 1]
    else:
        lsB = lsB + numstring[len(numstring) - 2] + \
            numstring[len(numstring) - 1]
    return [int(msB, 16), int(lsB, 16)]


BAUDRATE = int(input("input baud rate: "))
portName = "COM" + str(input("Port: COM"))
serialDevice = serial.Serial()
serialDevice.baudrate = BAUDRATE
serialDevice.port = portName
serialDevice.timeout = 1
serialDevice.rts = 0
serialDevice.dtr = 0
serialDevice.open()


time.sleep(0.5)

arrayData = [255, 255, 69, 65]

ox = '0x'
n = 3000

# print(str(hex(n)))

print(str(split_large_ints(n)))
startTime = time.time()
while(1):
    if serialDevice.inWaiting() > 0:
        data = serialDevice.read(1)
        print("data =", ord(data))
    a = input("hey")
    if a != '':
        serialDevice.write(bytes(arrayData))
serialDevice.close()
print("end")
