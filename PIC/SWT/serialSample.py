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


def sendCommand(command, ser):
    ser.write(bytes(command))
    while(1):
        if serialDevice.inWaiting() > 0:
            # data = serialDevice.read(1)
            # print("data =", ord(data))
            response = serialDevice.readline().decode('utf-8')
            print(response)
            if response == 'resend':
                ser.write(bytes(command))
            elif response == 'done':
                break


def setHome(ser):
    buffer = [255, 255, 0, 0, 0, 0, 0, 0, 0]
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def setPosXY(x, y, ser):
    buffer = [255, 255, 1]
    a = int(np.sqrt(2) / 2 * (y - x))
    b = int(np.sqrt(2) / 2 * (y + x))
    print("a = " + str(a))
    print("b = " + str(b))
    buffer.extend(split_large_ints(a))
    buffer.extend(split_large_ints(b))
    buffer.extend([0, 0])
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def setPosZ(z, ser):
    buffer = [255, 255, 2]
    buffer.extend(split_large_ints(z))
    buffer.extend([0, 0, 0, 0])
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def gripClose(ser):
    buffer = [255, 255, 3, 0, 0, 0, 0, 0, 0]
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def gripOpen(ser):
    buffer = [255, 255, 4, 0, 0, 0, 0, 0, 0]
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def gripRotate(angle, ser):
    buffer = [255, 255, 5]
    buffer.extend(split_large_ints(angle))
    buffer.extend([0, 0, 0, 0])
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def setAGains(K_P, K_I, K_D, ser):
    buffer = [255, 255, 6]
    buffer.extend(split_floats(K_P))
    buffer.extend(split_floats(K_I))
    buffer.extend(split_floats(K_D))
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def setBGains(K_P, K_I, K_D, ser):
    buffer = [255, 255, 7]
    buffer.extend(split_floats(K_P))
    buffer.extend(split_floats(K_I))
    buffer.extend(split_floats(K_D))
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def setZGains(K_P, K_I, K_D, ser):
    buffer = [255, 255, 8]
    buffer.extend(split_floats(K_P))
    buffer.extend(split_floats(K_I))
    buffer.extend(split_floats(K_D))
    checksum = 0
    for i in buffer:
        checksum += i
    checksum = checksum % 256
    buffer.append(checksum)
    print('sending ')
    print(buffer)
    sendCommand(buffer, ser)


def startUpRoutine(ser):
    setHome(ser)
    print('ready to start')


def split_large_ints(num):
    # numstring = str(hex(num))
    # lsB = '0x'
    # msB = '0x'
    # if len(numstring) < 5:
    #     msB = '0x00'
    # else:
    #     if len(numstring) == 5:
    #         msB += numstring[2]
    #     else:
    #         msB = msB + numstring[len(numstring) - 4] + \
    #             numstring[len(numstring) - 3]
    # if len(numstring) < 4:
    #     lsB += numstring[len(numstring) - 1]
    # else:
    #     lsB = lsB + numstring[len(numstring) - 2] + \
    #         numstring[len(numstring) - 1]
    msB = (num // 256) % 256
    lsB = num % 256

    return [msB, lsB]


# splits floats from their decimals and turns them into ints
def split_floats(num):
    a, b = divmod(num, 1.0)
    a = int(a) % 256
    b = int(b * 256)
    return [a, b]


try:
    BAUDRATE = 9600
    portName = "COM" + str(input("Port: COM"))
    serialDevice = serial.Serial()
    serialDevice.baudrate = BAUDRATE
    serialDevice.port = portName
    serialDevice.timeout = 1
    serialDevice.rts = 0
    serialDevice.dtr = 0
    serialDevice.open()
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


time.sleep(0.5)

arrayData = [255, 255, 69, 65, 0, 0, 0, 0, 0, 45]

ox = '0x'
n = 3000

# print(str(hex(n)))

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
