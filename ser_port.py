"""
This code is simply to test the serial port
Usage:
  Connect the usb serial device to PC (baud rate :9600)
  Then run this python code from console
  This script will try to connect to ttyACM0 port
  The same port name will be printed on the console if it get connected
  And after 10 seconds the script will send an encoded string over the channel

"""

import serial
import time
ser = serial.Serial('/dev/ttyACM0')  # open serial port
print(ser.name)         # check which port was really used

eye1x=0
eye1y=90
eye2x=60
eye2y=100
spd=10

pt=3

time.sleep(10)

data='#'+str(eye1x)+','+str(eye1y)+','+str(eye2x)+','+str(eye2y)+','+str(spd)+'*'
ser.write(data.encode())
ser.close()
