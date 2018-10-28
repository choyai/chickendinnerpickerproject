# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 20:47:48 2018

@author: G_Peav
"""

import serial
import time
import struct

BAUDRATE = int(input("input baud rate: "))
portName = "COM" + str(input("Port: COM"))
serialDevice = serial.Serial(portName, BAUDRATE, 8, 'N', 1, 0, 0, 0, 0, 0)
serialDevice.setRTS(0)
serialDevice.setDTR(0)

time.sleep(0.5)
# print("ready")
# floatData = 12.354
# ba = bytearray(struct.pack("f", floatData))
# # print(["0x%02x" % b for b in ba])
Packet = [0xFF, 0xFF, 0x02, 0x17]
str_packet = ''
str_packet = str_packet.join([chr(c) for c in Packet])
print(str_packet)

# serialDevice.write(str_packet.encode('utf-8'))
# serialDevice.write(ba)

arrayData = [255, 169, 69, 65]
# chararr = ""
print(struct.pack('4B', *arrayData))
serialDevice.write(struct.pack('4B', *arrayData))
v = struct.unpack('f', struct.pack('4B', *arrayData))[0]
# # print("get data = " + str(v))
# countData = 0
# arrayData = []

startTime = time.time()
# while ((time.time() - startTime) < 10.0):
while(1):
    if serialDevice.inWaiting() > 0:
        data = serialDevice.read(1)
        print("data =", ord(data))
serialDevice.close()
print("end")
