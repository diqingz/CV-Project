/*
    
*/
#include <Servo.h>
Servo myservo;
 int x;
void setup() {
    
    Serial.begin(115200);
    
   myservo.attach(9);
    myservo.write(0);
    delay(1000);
    myservo.detach(); 
   pinMode(13, OUTPUT);
   pinMode(12, OUTPUT);
 
}

void loop() {
    // send data only when you receive data:
    
while (!Serial.available());{
 x = Serial.readString().toInt();

 if (x == 1234){
    Serial.print("match");
    myservo.attach(9);
    delay(1000);
     myservo.write(90);
    delay(3000);
    myservo.write(0);
    delay(1000);
    myservo.detach(); 

    x = 0;
 }
 }
 

 }


   
 
  
