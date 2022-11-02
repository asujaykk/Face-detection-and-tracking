import serial 
import time

ser=serial.Serial("/dev/ttyACM0",baudrate=9600)
print("SCA initializing....")
data="empty"

while  data.find("SCA ready")==-1:
    if ser.inWaiting():
        time.sleep(1)
        data=str(ser.read(ser.inWaiting()))
        print("SCA initialized")



x1=60
y1=60
x2=60
y2=60
spd=1
time.sleep(2)

data_frame='#'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(spd)+'*'
time.sleep(2)
print("SCA rotated")

def SCA_move(sca_object,x1,y1,x2,y2,spd=10):
    data_frame='#'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(spd)+'*'
    sca_object.write(data_frame.encode())

SCA_move(ser,x1,y1,x2,y2)

ser.close()