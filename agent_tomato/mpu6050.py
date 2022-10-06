import smbus
import math
import time
import openpyxl

# Guc yonetim register'lari
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

excelPATH = ""

def parseExcel(gx,gy,gz,acx,acy,acz,sgx,sgy,sgz,sacx,sacy,sacz):
    #puts values to Excel
    file = openpyxl.load_workbook(excelPATH)
    sheet = file['sheet']

    roww = ((gx,gy,gz,acx,acy,acz,sgx,sgy,sgz,sacx,sacy,sacz))

    #for row in roww:
    sheet.append(roww)

    file.save(excelPATH)


def read_byte(adr):
 return bus.read_byte_data(address, adr)

def read_word(adr):
 high = bus.read_byte_data(address, adr)
 low = bus.read_byte_data(address, adr+1)
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

def get_z_rotation(x,y,z):
    radians = math.atan2( , dist(y,x))
    return -math.degrees(radians)

def get_y_rotation(x,y,z):
 radians = math.atan2(x, dist(y,z))
 return -math.degrees(radians)

def get_x_rotation(x,y,z):
 radians = math.atan2(y, dist(x,z))
 return math.degrees(radians)


bus = smbus.SMBus(1)
address = 0x68 #MPU6050 I2C adresi

#MPU6050 ilk calistiginda uyku modunda oldugundan, calistirmak icin asagidaki komutu veriyoruz:
bus.write_byte_data(address, power_mgmt_1, 0)

while True:
 time.sleep(0.05)
 #Jiroskop register'larini oku
 gyro_xout = read_word_2c(0x43)
 gyro_yout = read_word_2c(0x45)
 gyro_zout = read_word_2c(0x47)

 gyro_xout_scaled = gyro_xout/131
 gyro_yout_scaled = gyro_yout/131
 gyro_zout_scaled = gyro_zout/131
 

 accel_xout = read_word_2c(0x3b)
 accel_yout = read_word_2c(0x3d)
 accel_zout = read_word_2c(0x3f)

 accel_xout_scaled = accel_xout / 16384.0
 accel_yout_scaled = accel_yout / 16384.0
 accel_zout_scaled = accel_zout / 16384.0


 time.sleep(0.1)
 
 