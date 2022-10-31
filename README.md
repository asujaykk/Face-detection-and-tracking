# Face-detection-and-tracking
This is a small project to detect faces from a camera image and also track the face based on the movement in the vision region. 

## Setting up the environment:

1. Hardware requirements.
2. Software  requirements.

### Hardware requirements:
1. A jetson nano developement kit
2. Two raspberry pi v2 8MP camera.
3. A stereo camera actuator system.

Here we are using jetson nano developement board as master computer and two raspberry pi v2 camera for recording images. We can connect two CSI camera to jetson nano, since Jetson nano b01 support two CSI camera port. 
  The next important part is the servo  assisted stereo camera holder to achive pan and tilt movement of the camera. For this we will be using the "Stereo_Camera_Actuator" system. Please refer this repository  https://github.com/asujaykk/Stereo_Camera_Actuator to build one.
  
  ### Software requirements:
  The code is completely writen in python. we need the following modules and libraries for our projects
  1. Camera module : To read images from two cameras
  2. Serial module : To send command to Stereo_Camera_Actuator for changing camera angle.
  3. OpenCv library : For detecting and tracking face in the image.
  
  
