#define pwmPin 8 // PWM pin for the servo
#define potPin A0 // Analog pin for potentiometer
const int minPulseWidth = 400; // Min pulse width for servo
const int maxPulseWidth = 2350; // Max pulse width for servo
const int frequency = 10; // to allow signal to be sent unterrupted
const int MaxChars = 4; // Max number of characters to read from serial port
char strValue[MaxChars+1]; // String to hold the incoming data
int index = 0; // Index for the string
int onTime; // Variable to hold the value to be sent to the servo
int val; // Variable to hold the value read from the potentiometer or from the serial port 
int lastRead = 0; // Variable to hold the last value read from the potentiometer 

void setup() 
{
Serial.begin(9600); // Start serial communication at 9600 bps
pinMode(pwmPin,OUTPUT); // Set the pin as output for the servo


}

void loop()
{
  for (int i = 0; i < frequency; i++){ // This loop will mock a pwm signal
  digitalWrite(pwmPin,HIGH); // Send a HIGH pulse to the servo 
  delayMicroseconds(onTime); // Wait for the pulse to finish 
  digitalWrite(pwmPin,LOW); // Send a LOW pulse to the servo
  delayMicroseconds(20000-onTime); // Wait for the pulse to finish 
  } 
  val=analogRead(potPin); // Read the value from the potentiometer 
  val=map(val,0,1023,minPulseWidth,maxPulseWidth); // Map the value read from the potentiometer to the range of the servo 
  
  if(abs(lastRead - val) > 4){ // If the value read from the potentiometer is different from the last value read, send the value to the servo 
    lastRead=val; // Update the last value read from the potentiometer
    onTime=val; // Update the value to be sent to the servo
    int feedback = map(onTime,minPulseWidth,maxPulseWidth,0,180); // Map the value of the range of the servo to the angle of the servo
    Serial.println(feedback); // Print the value to the serial port
  }
}

void release(){ // Function to release the servo
    while(Serial.available()==0){ // Wait for the serial port to be available
      digitalWrite(pwmPin,LOW); // Send a LOW pulse to the servo
    }
    
}

 void serialEvent() 
{
  /*
  This function is called whenever there is data available on the serial port.
  It reads the incoming data and changes variable onTime to control the servo with pwm.

  */
  
  while(Serial.available()) {
    char ch = Serial.read(); // Read the incoming character from the serial port
      Serial.write(ch); // Write the character to the serial port
      if(index < MaxChars && isDigit(ch)) {  // If the character is a digit and the index is less than the max number of characters
            strValue[index++] = ch; // Add the character to the string
      } else { // If the character is not a digit or the index is greater than the max number of characters
            strValue[index] = 0;  // Null terminate the string 
            val = atoi(strValue); // Convert the string to an integer value
  }   
  if (val != 500){ 
  onTime = map(val,0,180,minPulseWidth,maxPulseWidth); // Map the value read from the potentiometer to the range of the servo 
  }
  else if (val==500){ // If the value read from the potentiometer is equal to 500, release the servo
          
    release(); // Call the release function
  }  
  }
   index = 0; // Reset the index
}
