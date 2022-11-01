import cv2
import serial
import Camera.jetsonCam as jetcam




cam1=jetcam.jetsonCam()
cam2=jetcam.jetsonCam()

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

for _ in range(500):
   ret1, frame1=cam1.read()
   ret2, frame2=cam2.read()
   if ret1 and ret2:
    cv2.imshow("fr1",frame1)
    cv2.imshow("fr2",frame2)
    cv2.waitKey(30)

cam1.stop()
cam1.release()
cam2.stop()
cam2.release()