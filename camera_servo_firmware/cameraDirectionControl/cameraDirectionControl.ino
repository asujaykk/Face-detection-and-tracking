/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

#define ELEMENTS_PER_DATA 5
#define MAX_CHAR_PER_DATA 20
#define SERVO_POSITION_COUNT=4


// create servo object to control a servo
Servo myservof1x;  
Servo myservof1y;
Servo myservof2x;
Servo myservof2y;




void setup() {
  // attaches the servo on pins to the servo object
  myservof2x.attach(3);  
  myservof2y.attach(5);
  myservof1x.attach(6);
  myservof1y.attach(9);
  Serial.begin(9600);

   int pos;
  
  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservof1x.write(pos);              // tell servo to go to position in variable 'pos'
    myservof2x.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 90; pos -= 1) { // goes from 180 degrees to 90 degrees
    myservof1x.write(pos);              // tell servo to go to position in variable 'pos'
    myservof2x.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }

  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    // in steps of 1 degree
    myservof1y.write(pos);              // tell servo to go to position in variable 'pos'
    myservof2y.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  for (pos = 180; pos >= 90; pos -= 1) { // goes from 180 degrees to 90 degrees
    myservof1y.write(pos);              // tell servo to go to position in variable 'pos'
    myservof2y.write(pos);
    delay(15);                       // waits 15ms for the servo to reach the position
  }
}

/*
 * SAMPLE data= #x1,y1,x2,y2,speed*
 * x1,y1,x2,y2 range = 0-180
 * speed 100 -- 10000
 * example: #90,90,90,90,1000*
 */

int eyePosEnd[ELEMENTS_PER_DATA]={90,90,90,90,100};
int eyePosStrt[ELEMENTS_PER_DATA]={90,90,90,90,100};
void loop() {
    String edata;
    String edataA[ELEMENTS_PER_DATA];
    //ser_send_data("read data");
    edata=read_data('#','*');

    //ser_send_data("split data"); 
    split_String(edata,edataA,',');
    
    //ser_send_data("update eye pos");    
    update_eyepos_array(edataA,eyePosEnd);
    //ser_send_data(edata);
    //servoWrite(eyePosEnd,200);
    //servoWrite(eyePos,200);
    //ser_send_data("move cam");
    moveCamera(eyePosStrt,eyePosEnd);

    //ser_send_data("array copy");
    arrayCopy(eyePosEnd,eyePosStrt);
}
