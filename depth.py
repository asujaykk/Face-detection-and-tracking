import cv2
import numpy as np
from matplotlib import pyplot as plt

import Camera.jetsonCam as jetCam
cam1 = jetCam.jetsonCam()
cam2 = jetCam.jetsonCam()


cam1.open(sensor_id=1,
          sensor_mode=3,
          flip_method=6,
          display_height=540,
          display_width=960,
        )
cam2.open(sensor_id=0,
          sensor_mode=3,
          flip_method=6,
          display_height=540,
          display_width=960,
        )

cam1.start()
cam2.start()
first_run=True
x1=50
y1=50
w=50
h=50
x2=x1+h
y2=y1+h
ex=50
stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
for i in range(100):
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
     gr1=cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
     gr2=cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)

     disparity = stereo.compute(gr1,gr2)
     plt.imshow(disparity,'gray')
     plt.show()   
     cv2.waitKey(30)

cam1.stop()
cam2.stop()
cam1.release()
cam2.release()


