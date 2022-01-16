#define analogPin A0
#define maxChars 4
int potRead = 0;
unsigned int val = 0;
unsigned int freq;
unsigned int duty;
char strValue[maxChars+1]; // String to hold the incoming data
int index = 0; // Index for the string
unsigned int lastval = 3131;
void setup() {
  pinMode(9, OUTPUT);
  pinMode(10, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  TCCR1A = 0; //reset the register
  TCCR1B = 0; //reset the register
  TCCR1A |= (1<<WGM11)| (1<<COM1A1)|(1<<COM1B1);
  TCCR1B |= (1<<CS10)|(1<<CS12)|(1<< WGM12)|(1<< WGM13); 
  //Fast PWM mode activated, with 1024 prescaler, the TOP determined by ICR1. 
  //Clear OCR1A/OCR1B on Compare Match when upcounting. Set OCR1A/OCR1B on Compare Match when downcounting.
  Serial.begin(9600);  // initialize serial communication at 9600 bps
}
void loop() {
  
  if (val!=lastval)
  {
    Serial.print("Arduino received: ");
    Serial.println(val); //see what was received
    lastval=val;
      }
  if (bitRead(val, 15) == 0)
  {
    digitalWrite(3, HIGH);
    digitalWrite(4, LOW);
  }
  else
  {
    digitalWrite(4, HIGH);
    digitalWrite(3, LOW);
  }
freq = val;
duty = val;
freq = freq % 32768;
freq = freq / 256;
duty %= 256;
ICR1 = map(freq, 0, 127, 5, 255);
OCR1A = map(duty, 0, 255, 0, ICR1);
potRead = analogRead(analogPin);  //read the input pin A0



}
void serialEvent(){

  /*
  This function is called whenever there is data available on the serial port.
  It reads the incoming data and changes variable onTime to control the servo with pwm.

  */
  
  while(Serial.available()) {
    char ch = Serial.read(); // Read the incoming character from the serial port
      if(index < maxChars && isDigit(ch)) {  // If the character is a digit and the index is less than the max number of characters
            strValue[index++] = ch; // Add the character to the string
            Serial.print("ch");
      } 
      else 
      { // If the character is not a digit or the index is greater than the max number of characters
            strValue[index] = 0;  // Null terminate the string 
            val = atoi(strValue); // Convert the string to an integer value
            Serial.println(strValue);
      }   
   index = 0; // Reset the index
  }
}
