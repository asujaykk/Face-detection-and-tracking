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
  The code is completely writen in python. Once you boot your jetson nano developement board. we need to install the following modules and libraries.
  1. First clone this repository to your working directory.
          
          git clone https://github.com/asujaykk/Face-detection-and-tracking.git
  2. Camera module : To read images from two cameras.
        Add Camera module to "Face-detection-and-tracking" folder.
          
          cd Face-detection-and-tracking
          git clone https://github.com/asujaykk/Camera.git
  3. Serial module : To send command to Stereo_Camera_Actuator for changing camera angle.
     Serial module need to be installed in your PC using below command
          
          pip3 install pyserial
  4. OpenCv library : For detecting and tracking face in the image.
        Opencv is pre installed in jetson SDK. So no need to install it explicitly.
  
  ## Running the face tracker.
  
  First connect 'Stereo_Camera_System' (arduino board) to jetson nano via usb cable.     
  Connect LEFT camera to CAM0 CSI port.   
  Connect RIGHT camera to CAM1 CSI port.   
  
  1. Open terminal and navigate to your working directory
  2. Open Face-detection-and-tracking directory:
       
          cd Face-detection-and-tracking
  3. Run the following command to start face tracking process.
       
          python3 visual_fast_with_depth.py
      
      If you are getting permission ierror with serial port, then please run below command .
      
          sudo chmod 666 /dev/ttyACM0
       
      Also restart the 'nvargus-daemon' with below command. to release the two camera instances which was not closed properly in the efirst run. 
      
          sudo systemctl restart nvargus-daemon
      
      Then again run 'visual_fast_with_depth.py'
   
   4. The two camera view will be shown in two windows.
   5. 
  
  
