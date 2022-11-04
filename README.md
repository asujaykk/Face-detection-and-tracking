# Face-detection-and-tracking

This is a basic project to demonstrate a face detection and tracking system using python and opencv on a jetson nano developement board.

## Setting up the environment:

1. Hardware requirements.
2. Software  requirements.

### Hardware requirements:
1. A jetson nano developement kit
2. Two raspberry pi v2 8MP camera.
3. A stereo camera actuator system.

Here we are using jetson nano developement board as master computer and two raspberry pi v2 camera for capturing images. We can connect two CSI camera to jetson nano b01, since it support two CSI camera port. 
  
  The next important part is the servo  assisted stereo camera holder to achive pan and tilt movement of the camera. For this we will be using the "Stereo_Camera_Actuator" system. Please refer this repository  https://github.com/asujaykk/Stereo_Camera_Actuator to build one.
  
  ### Software requirements: 
  First boot your jetson nano developement board with latest JDK. Then we need to install the following modules and libraries.
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
       
          python3 face_tracker.py
      
      If you are getting permission error with serial port, then please run below command .
      
          sudo chmod 666 /dev/ttyACM0
       
      Also restart the 'nvargus-daemon' with below command. to release the two camera instances which was not closed properly in the first run. 
      
          sudo systemctl restart nvargus-daemon
      
      Then again run 'python3 face_tracker.py'
   
   4. If the system is working fine, then you will receive the folloing messages on the terminal.  
       *SCA initializing...*  
       *SCA initialized.*
       
       After this message, two camera stream window will appear (one for left camera and another for right camera).
       If there is any face detected in the frame, then the  overall system will continously track that face until the face leave the visible range of the camera. 
   
   6. The following GIF shows the output of the detection and tracking system. 
   ![20221105_010505](https://user-images.githubusercontent.com/78997596/200060611-66d617e3-8d94-4264-a370-3359ee19adcd.gif)

    
  
  
