import math
import cv2
import numpy as np
import Camera.jetsonCam as jetCam
cam1 = jetCam.jetsonCam()
cam2 = jetCam.jetsonCam()


cam1.open(sensor_id=1,
          sensor_mode=3,
          flip_method=4,
          display_height=540,
          display_width=960,
        )
cam2.open(sensor_id=0,
          sensor_mode=3,
          flip_method=4,
          display_height=540,
          display_width=960,
        )

cam1.start()
cam2.start()
first_run=True

def find_im_in_im(img1,img2):
   
   method = cv2.TM_SQDIFF

   # Read the images from the file
   #small_image = cv2.imread('small_image.png')
   #large_image = cv2.imread('large_image.jpeg')

   result = cv2.matchTemplate(img1,img2, method)
   #print('locations')
   #print(result)
   # We want the minimum squared difference
   mn,_,mnLoc,_ = cv2.minMaxLoc(result)

   # Draw the rectangle:
   # Extract the coordinates of our best match
   MPx,MPy = mnLoc

   # Step 2: Get the size of the template. This is the same size as the match.
   trows,tcols = img1.shape[:2]

   # Step 3: Draw the rectangle on large_image
   cv2.rectangle(img2,(MPx,MPy) ,(MPx+tcols,MPy+trows),(0,0,255),2)

   # Display the original image with the rectangle around the match.
   #cv2.imshow('output',large_image)

   # The image is only displayed if we call this
   #cv2.waitKey(0)
   return img2

x1=50
y1=50
w=50
h=50
x2=x1+h
y2=y1+h

ex=50

#detection
# Load the cascade
face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')

import serial
ser = serial.Serial('/dev/ttyACM0')  # open serial port
print(ser.name)         # check which port was really used
# write a string

eye1x=60
eye1y=90
eye2x=60
eye2y=100
spd=10

pt=7

def moveCam():
    data='#'+str(eye1x)+','+str(eye1y)+','+str(eye2x)+','+str(eye2y)+','+str(spd)+'*'
    ser.write(data.encode())

def reqIncr(val):
   if abs(val)<10:
      return 1
   elif abs(val) <20:
      return 1
   elif abs(val) <30:
      return 1
   elif abs(val) <40:
      return 2
   elif abs(val) <50:
      return 3
   elif abs(val) <60:
      return 4
   elif abs(val) <70:
      return 5
   elif abs(val) <80:
      return 6
   elif abs(val) <90:
      return 8
   else:
      return 10
   


moveCam()
for i in range(1000):
  ret1,frame1 = cam1.read()
  ret2,frame2 = cam2.read()

 
# resize image
  
  if ret1 and ret2:
     if first_run:
       scale_percent = 60 # percent of original size
       width = int(frame1.shape[1] * scale_percent / 100)
       height = int(frame1.shape[0] * scale_percent / 100)
       dim = (width, height)
       first_run=False
       res1 = cv2.resize(frame1, dim, interpolation = cv2.INTER_AREA)
       res2 = cv2.resize(frame2, dim, interpolation = cv2.INTER_AREA)
       prvf1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
       prvf2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)

     res1 = cv2.resize(frame1, dim, interpolation = cv2.INTER_AREA)
     res2 = cv2.resize(frame2, dim, interpolation = cv2.INTER_AREA)
     gray1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
     gray2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)  
     faces1 = face_cascade.detectMultiScale(gray1, 1.1, 4)
     faces2 = face_cascade.detectMultiScale(gray2, 1.1, 4)
     #print(type(faces1))
     for (x, y, w, h) in faces1:
            cv2.rectangle(res1, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #print('face2:x='+str(x)+" y="+str(y))
     for (x, y, w, h) in faces2:
            cv2.rectangle(res2, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #print('face2:x='+str(x)+" y="+str(y))

     #res1_s= res1[x1:x2,y1:y2]
     #cv2.rectangle(res1, (x1,y1),(x2,y2),(0,255,0),2)
     
     #res3 = find_im_in_im(res1_s,res2)
     
     if len(faces1)>0 and len(faces2)>0:
          e1x= faces1[0][0]        
          e2x= faces2[0][0]
          e1y= faces1[0][1]        
          e2y= faces2[0][1]
          
          f1cx= e1x+(faces1[0][2]/2) 
          f2cx= e2x+(faces2[0][2]/2)
          f1cy= e1y+(faces1[0][3]/2)
          f2cy= e2y+(faces2[0][3]/2)
          
          f1cx_d= f1cx-(width/2)
          f2cx_d= f2cx-(width/2)          

          f1cy_d= f1cy-(height/2)
          f2cy_d= f2cy-(height/2)
          
 
          eye1x_incr= reqIncr(f1cx_d)
          eye2x_incr= reqIncr(f2cx_d)
          eye1y_incr= reqIncr(f1cy_d)
          eye2y_incr= reqIncr(f2cy_d)
          
          #print(str(eye1x_incr)+" "+str(eye2x_incr)+" "+str(eye1y_incr)+" "+str(eye2y_incr))
          if f1cx<((width/2)-pt):
             eye1x -=eye1x_incr
          elif f1cx>((width/2)+pt):
             eye1x +=eye1x_incr


          if f1cy<((height/2)-pt):
             eye1y -=eye1y_incr
          elif f1cy>((height/2)+pt):
             eye1y +=eye1y_incr
      

          if f2cx<((width/2)-pt):
             eye2x -=eye2x_incr
          elif f2cx>((width/2)+pt):
             eye2x +=eye2x_incr

          if f2cy<((height/2)-pt):
             eye2y -=eye2y_incr
          elif f2cy>((height/2)+pt):
             eye2y +=eye2y_incr

          if f1cx>((width/2)-pt) and f1cx<((width/2)+pt) and f2cx>((width/2)-pt) and f2cx<((width/2)+pt):
               try:
                 Q1=(180-eye2x)
                 Q2=eye1x
                 d=6.5
                 d2=(2*d)/(math.sin(math.radians(180-(Q1+Q2))))
               
                 h=math.sqrt((d2*d2)+(d*d)-(d2*d*math.cos(math.radians(Q1))))
                 print("distance: "+str(h))
                 #print("distance: "+str(math.tan(180-eye1x)*0.04))
                 print("e1x:"+str(eye1x)+" e2x:"+str(eye2x)+" e1y:"+str(eye1y)+" e2y:"+str(eye2y))
               except:
                 print("error captured")
                 
          moveCam()

     
     cv2.imshow("f1diff",gray1-prvf1)
     cv2.imshow("f2diff",gray2-prvf2)
     cv2.imshow("f1", res1)
     cv2.imshow("f2", res2) 
     #cv2.imshow("f3",res3)   
     cv2.waitKey(30)
     prvf1=gray1;
     prvf2=gray2;


cam1.stop()
cam2.stop()
cam1.release()
cam2.release()
ser.close() 

def func():
      pass
#          if e1x>e2x:
#             eye2x -=2
#          elif e1x<e2x:
#             eye2x +=2
#
#          if e1y>e2y:
#             eye2y -=2
#          elif e1y<e2y:
#             eye2y +=2

