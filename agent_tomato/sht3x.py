import time

import smbus
import sys


#Write the read sensor command
bus.write_byte_data(0x45, 0x24, 0x00)
time.sleep(0.01) #This is so the sensor has tme to preform the mesurement and write its registers before you read it

# Read data back, 8 bytes, temperature MSB first then lsb, Then skip the checksum bit then humidity MSB the lsb.
data0 = bus.read_i2c_block_data(0x45, 0x00, 8)
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
H = ((100 * h_val) / 65536.0 )ü


print ("{:.2f}".format(T))
print ("{:.2f}".format(H))