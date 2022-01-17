#define analogPin A0
String readString;
int potRead = 0;
unsigned int val = 0;
unsigned int freq;
unsigned int duty;
int rotation = 0;
int dutyPy;
const int MaxChars = 6; // Max number of characters to read from serial port
char strValue[MaxChars+1]; // String to hold the incoming data
int index = 0; // Index for the string
String serialOutput="";
String lastSerialOutput="";
long int frequency;
void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  TCCR1A = 0; //reset the register
  TCCR1B = 0; //reset the register
  TCCR1A |= (1<<WGM11)| (1<<COM1A1);
  TCCR1B |= (1<<CS11)|(1<< WGM12)|(1<< WGM13); 
 
  //Fast PWM mode activated, with 1 prescaler, the TOP determined by ICR1. 
  //Clear OCR1A/OCR1B on Compare Match when upcounting. Set OCR1A/OCR1B on Compare Match when downcounting.
  Serial.begin(115200);  // initialize serial communication at 115200 bps
//Try to increase communication speed
}
void loop() {
  
  if (bitRead(val, 15) == 0)
  { 
    rotation = 0;
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
  }
  else
  {
    rotation = 1;
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
  }
freq = val;
duty = val;
freq = freq % 32768;
freq = freq / 512;
duty %= 128;
ICR1 = map(freq, 0, 255, 1999, 65535);
OCR1A = map(duty, 0, 127, 0, ICR1);
potRead = analogRead(analogPin);  //read the input pin A0
dutyPy = map(duty,0,127,0,100);
frequency=(16000000/(ICR1+1));

delay(10);

serialOutput = String(rotation);
serialOutput += ":";
serialOutput += String(frequency);
serialOutput += ":";
serialOutput += String(dutyPy);
serialOutput += ":";
serialOutput += String(potRead);
if (serialOutput != lastSerialOutput){
  Serial.println(serialOutput);
  lastSerialOutput = serialOutput;
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
        if(index < MaxChars && isDigit(ch)) {  // If the character is a digit and the index is less than the max number of characters
            strValue[index++] = ch; // Add the character to the string
      } else { // If the character is not a digit or the index is greater than the max number of characters
            
            strValue[index] = 0;  // Null terminate the string 
            Serial.println(strValue);
            val = atoi(strValue); // Convert the string to an integer value
          
      }
      
     
    
  }
   index = 0; // Reset the index
}
