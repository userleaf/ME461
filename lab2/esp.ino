#include <WiFi.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define pulse_pin 8

char packetBuffer[255];
char replyBuffer[] = "Received";
char ssid[] = "AccessPoint";
char pass[] = "12345687";
char val[];

unsigned int localPort = 2390;
int angle;
int pulse_min = 500;
int pulse_max = 2500;
int angle_min = 0;
int angle_max = 180;
int pulse_period =20000 ;

void setup(){
    Serial.begin(9600);
    WiFi.begin(ssid,pass);
    while ( WiFi.status() != WL_CONNECTED ){
        Serial.println(".");
    }
    Serial.println("Connected");
    Serial.println(WiFi.localIP());
    Udp.begin(localPort);
    }
}

void loop{
    if (packetSize) {
        int len = Udp.read(packetBuffer, 255);
        if (len > 0) {
            packetBuffer[len] = 0;
            val=packetBuffer;
        }
    }
    
    angle = int(val);
    
    move_pos(angle);
}

int move_pos(int angle){
        if (angle >= 0){
            int delay_high = map(angle, angle_min, angle_max, pulse_min, pulse_max);
            digitalWrite(pulse_pin,HIGH);
            delayMicroseconds(delay_high);
            digitalWrite(pulse_pin,LOW);
            delayMicroseconds(pulse_period-delay_high);
        }
        else if (angle==-1){
        digitalWrite(pulse_pin,LOW);
        }
    }
}
