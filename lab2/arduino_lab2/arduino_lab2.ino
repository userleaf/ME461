#define pwmPin 8
#define potPin A0
const int minPulseWidth = 500;
const int maxPulseWidth = 2500;
const int frequency = 10;
const int MaxChars = 4;
char strValue[MaxChars+1];
int index = 0;
int x;
int val;
int lastRead = 0;

void setup()
{
Serial.begin(9600);
pinMode(pwmPin,OUTPUT);


}

void loop()
{
  for (int i = 0; i < frequency; i++){
  digitalWrite(pwmPin,HIGH);
  delayMicroseconds(x);
  digitalWrite(pwmPin,LOW);
  delayMicroseconds(20000-x);
  }
  val=analogRead(potPin);
  val=map(val,0,1023,minPulseWidth,maxPulseWidth);
  
  if(abs(lastRead - val) > 2){
    lastRead=val;
    x=val;
  }
}

void release(){
    while(Serial.available()==0){
      digitalWrite(pwmPin,LOW);
    }
    
}



 void serialEvent()
{
  while(Serial.available())
  {char ch = Serial.read();
      Serial.write(ch);
      if(index < MaxChars && isDigit(ch)) { 
            strValue[index++] = ch; 
      } else { 
            strValue[index] = 0; 
            val = atoi(strValue);
  }   
  if (val != 500){
  x = map(val,0,180,minPulseWidth,maxPulseWidth);
  Serial.println(x);
  }
  else if (val==500){
          
    release();
  }  
  }
   index = 0;
}
