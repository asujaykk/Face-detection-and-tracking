import serial 
import time
import Camera.jetsonCam as jetcam
import cv2


#Inistialize serial port to communicate with SCA module
ser=serial.Serial("/dev/ttyACM0",baudrate=9600)


# Waiting for the "SCA ready" message from SCA module.
print("SCA initializing....")
data=""
while  data.find("SCA ready")==-1:
    if ser.inWaiting():
        time.sleep(1)
        data=str(ser.read(ser.inWaiting()))
        print("SCA initialized")



# function to move the camera 
def cam_move(sca_object,x1,y1,x2,y2,spd=10):
    """
    This method will send command to SCA module to change the camera angle
    parameters
    x1, y1 : x and y angle for left camera 
    x2,y2 : x and y angle for right camera
    spd: Speed in which sca need to perform (not active, hence this value is dummy)
    """
    data_frame='#'+str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(spd)+'*'
    sca_object.write(data_frame.encode())


#creating global variable to store camera angle
# initialized with current angle ( SCA module will initialize all servos to 90 degree )
x1=90
y1=90
x2=90
y2=90
spd=1
# Driving SCA module to the angle initialized above
cam_move(ser,x1,y1,x2,y2)

# input frame size
img_shape=(960,540,3)

# the image size need to be reduced  to 60% before processing
scale_percent = 60 # percent of original size
width = int(img_shape[0] * scale_percent / 100)   #reduced  width
height = int(img_shape[1] * scale_percent / 100)  #reduced height
reduced_dim = (width, height)                     #reduced dimension

img_centre=((width//2),(height//2))    #centre of the reduced image. 




#Intialize camera objects and start camera streams 
leftcam=jetcam.jetsonCam()
rightcam=jetcam.jetsonCam()

leftcam.open(sensor_id=0,
                sensor_mode=3,
                flip_method=4,
                display_height=img_shape[1],
                display_width=img_shape[0],
            )

rightcam.open(sensor_id=1,
                sensor_mode=3,
                flip_method=4,
                display_height=img_shape[1],
                display_width=img_shape[0],
            )

# start the camera streams
leftcam.start()
rightcam.start()


#method to find the angle incriment required for the deviation in the pixel width.
def reqIncr(val):
    """
     This method recieve the pixel difference (can be +ve or -ve) centre pont of image 
     and centre point of detected face.

     And this method return an integer camera angle value  to be incrimented  to achive a smooth rotation.
    """
    a=0.000328152
    b=0.0298791
    c=0.23834
    #d=int((a*abs(val))+b)  #d=a*val+b
    d=int((a*abs(val)*abs(val))+(b*abs(val))+c)
    if val<0: 
       return d*(-1)
    else:
        return d
     
  

# Load opencv cascade classifier data file
face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_default.xml')


#Execute the face tracking for 500 counts
for i in range(500):
  #read cam1 and cam2 images
  ret1,left_frame = leftcam.read()    
  ret2,right_frame = rightcam.read()

  if ret1 and ret2:  
     #reduce the input image size to recuced_dim
     left_frame = cv2.resize(left_frame, reduced_dim, interpolation = cv2.INTER_AREA)   
     right_frame = cv2.resize(right_frame, reduced_dim, interpolation = cv2.INTER_AREA) 

     #convert RGB image to grayscale before passsing to face detector
     left_gray = cv2.cvtColor(left_frame, cv2.COLOR_BGR2GRAY)
     right_gray = cv2.cvtColor(right_frame, cv2.COLOR_BGR2GRAY)  

     #detect faces in the input images
     left_faces = face_cascade.detectMultiScale(left_gray, 1.1, 4)
     right_faces = face_cascade.detectMultiScale(right_gray, 1.1, 4)
     
     #draw detected faces on the input image
     for (x, y, w, h) in left_faces:
            cv2.rectangle(left_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #print('face2:x='+str(x)+" y="+str(y))
     for (x, y, w, h) in right_faces:
            cv2.rectangle(right_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            #print('face2:x='+str(x)+" y="+str(y))
     
     #This system can only track if the image contain one face only.
     if len(left_faces)==1 and len(right_faces)==1:
          
          #calculate centre of detected face in left and right images
          leftface_cx= left_faces[0][0]+(left_faces[0][2]//2) 
          rightface_cx= right_faces[0][0]+(right_faces[0][2]//2)

          leftface_cy= left_faces[0][1]+(left_faces[0][3]//2)
          rightface_cy= right_faces[0][1]+(right_faces[0][3]//2)
          
          #calculate pixel deviation of face centre from image centre.
          left_xd= leftface_cx-(width//2)
          right_xd= rightface_cx-(width//2)          

          left_yd= leftface_cy-(height//2)
          right_yd= rightface_cy-(height//2)
          
          #print(str(left_xd)+" " +str(left_yd)+" " + str(right_xd)+" "+str(right_yd))
          
          #Find required incriment in each angle based on the pixel deviation
          x1 += reqIncr(left_xd)
          x2 += reqIncr(right_xd) 

          y1 += reqIncr(left_yd)
          y2 += reqIncr(right_yd)

     #show left and right frame with faces 
     cv2.imshow("left_frmae",left_frame)
     cv2.imshow("right_frmae",right_frame)
     cv2.waitKey(1) 
    
     #send command to SCA module to updte camera angles
     cam_move(ser,x1,y1,x2,y2)    
      


#close camera nd serial port after execution
leftcam.stop()
rightcam.stop()
leftcam.release()
rightcam.release()

ser.close()