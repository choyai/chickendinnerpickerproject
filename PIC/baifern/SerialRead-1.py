import serial
import numpy as np

BAUDRATE = 115200
PORT = 'COM5'
max_data = 2000


def count2angle(count):
    """
    :param count:  pulsecount from encoder
    :return: motor armature angle
    """
    angle = count * np.pi * 2 / 768
    return angle


ser = serial.Serial()
ser.baudrate = BAUDRATE
ser.port = PORT
ser.timeout = 1
ser.dtr = 0
ser.rts = 0
while True:
    try:
        ser.open()
        print("connected to: " + ser.portstr)
        break
    except:
        print("No permission to access " + PORT)


counter = 1
data = ""
while True:
    line = ser.readline().decode('utf-8')
    print(line)
# parse data and do conversions
    if len(line) > 0:
        time_in_millisecs = int(line.split(",")[0])
        # get time in seconds
        time_in_seconds = time_in_millisecs / 1000.0
        # get angle in radians
        count = int(line.split(",")[1])
        angle = count2angle(count)
        # get voltage
        millivoltage = int(line.split(",")[2])
        voltage = millivoltage / 1000.0

        # create new string entry with all the values separated by commas
        new = "{0:.5f}".format(time_in_seconds) + \
            ",{0:.5f},".format(voltage) + "{0:.5f}".format(angle)
        # Save to CSV file and exit after 20s or 2000 entries
        if counter >= max_data or time_in_seconds > 20:
            f = open("log_file2.csv", "w")
            f.write(data)
            f.close()
            data = ''
            print("File saved")
            break
        data += (str(new) + "\n")
        counter += 1
    else:
        pass

ser.close()
