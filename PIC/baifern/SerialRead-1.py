import serial

BAUDRATE = 115200
PORT = 'COM5'
m_in_voltage = 12
max_data = 840


def msec2sec(msec):
    """
    :param msec: time in milli seconds unit
    :return: time in seconds unit
    """
    return msec / 1000


def impulse2voltage(duty_cycle):
    """
    :param duty_cycle: duty cycle
    :return: motor output voltage
    """
    voltage = (duty_cycle / 100) * m_in_voltage
    return voltage


def count2distance(count):
    """
    :param count:  pulsecount from encoder
    :return: motor armature angle
    """
    distance = 0.000052359 * (1 / 125) * 30 * count
    return distance


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

    if len(line) > 0:
        time = int(line.split(",")[0])
        time = msec2sec(time)
        # voltage = count2voltage(voltage)
        pulse = int(line.split(",")[1])
        voltage = int(line.split(",")[2])
        distance = count2distance(pulse)
        new = str(time) + ",{0:.5f},".format(voltage) + str(distance)
        if counter >= max_data:
            f = open("log_file.csv", "w")
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
