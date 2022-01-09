#include <WiFi.h>
#include <ESP8266WiFi.h>
#include <SPI.h>
#include <WiFiUdp.h>

#define pulse_pin=8;

char packetBuffer[255];
char replyBuffer[] = "Received";
char ssid[] = "Kablonet Netmaster-1757-G";
char pass[] = "e9601252"
char val[];

unsigned int localPort = 2390;
int angle;
int pulse_min = 500;
int pulse_max = 2500;
int angle_min = 0;
int angle_max = 180;
int pulse_period =100000 ;

void setup(){
    Serial.begin(9601);
    WiFi.begin(ssid,pass)
    while ( WiFi.status() != WL_CONNECTED ){
        Serial.println(".");
    }
    Serial.println("Connected");
    Serial.println(WiFi.localIP());
    Udp.begin(localPort);
    }
}

void loop{

  for (int i = 0; i < frequency; i++){
  digitalWrite(pwmPin,HIGH);
  delayMicroseconds(x);
  digitalWrite(pwmPin,LOW);
  delayMicroseconds(20000-x);
  }
    
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

