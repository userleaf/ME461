#define analogPin A0
String readString;
int potRead = 0;
unsigned int val = 0;
unsigned int freq;
unsigned int duty;
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
  while (!Serial.available()) {}
  // serial read section
  while (Serial.available())
  {
    delay(30);  //delay to allow buffer to fill
    if (Serial.available() > 0)
    {
      char c = Serial.read();  //gets one byte from serial buffer
      readString += c; //makes the string readString
      val = readString.toInt(); 
    }
  }

  if (readString.length() > 0)
  {
    Serial.print("Arduino received: ");
    Serial.println(val); //see what was received
    readString = "";
    Serial.println(freq);
    Serial.println(duty);
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
