import RPi.GPIO as GPIO
import serial
import time,sys
import smbus

modulePin = 0

GPIO.setmode(GPIO.BOARD)
GPIO.setup(modulePin, GPIO.OUT)

SERIAL_PORT = ""

shockDetectorPin= 0

potr = serial.Serial(SERIAL_PORT, baudrate = 115200 , timeout = 5)


bus = smbus.SMBus(1)
imuaddr = 0x68 #MPU6050 I2C adresi
shtaddr = 0x44

#MPU6050 ilk calistiginda uyku modunda oldugundan, calistirmak icin asagidaki komutu veriyoruz:
bus.write_byte_data(imuaddr, power_mgmt_1, 0)

#Write the read sensor command ST3X
bus.write_byte_data(shtaddr, 0x24, 0x00)
time.sleep(0.01) #This is so the sensor has tme to preform the mesurement and write its registers before you read it

def setGPIOAnalogRead(shockDetectorPin)
    GPIO.setmode(GPIO.BCM)
    # Set up input pins.
    GPIO.setup(shockDetectorPin, GPIO.IN)

def readShock(shockDetectorPin):

    shockval = GPIO.input(shockDetectorPin)
    print("Shock val is")
    print(shockval)

def readSHT():
    data0 = bus.read_i2c_block_data(shtaddr, 0x00, 8)
    
    s = data0[0]
    i = data0[1]
    t = data0[2]
    y = data0[3]
    u= data0[4]
    o= data0[5]
    p = data0[6]
    q = data0[7]

    t_val = (data0[0]<<8) + i #convert the data
    h_val = (data0[3] <<8) + u     # Convert the data

    T = ((175.72 * t_val) / 65536.0 ) - 45 #do the maths from datasheet
    H = ((100 * h_val) / 65536.0 )

    print("Temperature is")
    print ("{:.2f}".format(T))

    print("Humidity is")
    print ("{:.2f}".format(H))
    
    return [T, H]



def read_byte(adr):
    return bus.read_byte_data(imuaddr, adr)

def read_word(adr):
    high = bus.read_byte_data(imuaddr, adr)
    low = bus.read_byte_data(imuaddr, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
    return -((65535 - val) + 1)
    else:
    return val

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)


def getIMU():
    time.sleep(0.05)
    #Jiroskop register'larini oku
    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    print "Jiroskop X : ", gyro_xout, " olcekli: ", (gyro_xout / 131)
    print "Jiroskop Y : ", gyro_yout, " olcekli: ", (gyro_yout / 131)
    print "Jiroskop Z: ", gyro_zout, " olcekli: ", (gyro_zout / 131)
    
    #Ivmeolcer register'larini oku
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    print "Ivmeolcer X: ", accel_xout, " olcekli: ", accel_xout_scaled
    print "Ivmeolcer Y: ", accel_yout, " olcekli: ", accel_yout_scaled
    print "Ivmeolcer Z: ", accel_zout, " olcekli: ", accel_zout_scaled

    print "X dondurme: " , get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    print "Y dondurme: " , get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)


    arr = [gyro_xout , gyro_yout, gyro_zout, accel_xout_scaled, accel_yout_scaled, accel_zout_scaled, get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled), get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)]

    return arr

    time.sleep(0.1)

def powerGSM():
    answer = sendCommand("AT", "OK")
    if answer = 0:
        GPIO.output(modulePin, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(modulePin, GPIO.LOW)

        while answer = 0
            answer = sendCommand("AT", "OK")



def sendCommand(command,response):
    ans = 0
    port.write(command + '\r\n')
    answer = port.read(15)

    if answer == response:
        ans = 1
    else:
        ans = 0
    return ans

def sendCommand(command,response, response2):
    ans = 0
    port.write(command + '\r\n')
    answer = port.read(15)

    if answer == response:
        answer = port.read(15)
        if answer == response2:
            ans = 1
    else:
        ans = 0
    return ans

def pushData(data):

    setGPRS()

    resp = sendCommand("AT+HTTPINIT", "OK")
    if resp == 1:
        resp = sendCommand("AT+HTTPPARA=\"CID\",1", "OK")
        if resp == 1:
            resp = sendCommand("AT+HTTPPARA=\"URL\",\"" + url + "\"", "OK")
            if resp == 1:
                resp = sendCommand("AT+HTTPACTION=0" , "+HTTPACTION:0,200")
                if resp == 1:
                    port.write("AT+HTTPREAD=1,10000" + '\r\n')
                else:
                    print("Error getting the url\n")
            else:
                print("Error setting the url\n")
        else:
            print("Error setting the CID")
    else:
        print("Error on initialization")

    sendCommand("AT+HTTPTERM", "OK")

    time.sleep(0.2)

    closeGate()

def setGPRS():
    
    sendCommand("AT+SAPBR=3,1,\"Contype\",\"GPRS\"", "OK")
    
    r = sendCommand("AT+SAPBR=1,1", "OK")
    while r==0:
        r = sendCommand("AT+SAPBR=1,1", "OK")

def closeGate():
    sendCommand("AT+SAPBR=0,1")

