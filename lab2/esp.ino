#include <WiFi.h> // import WiFi library
#include <ESP8266WiFi.h> // import WiFi library for ESP8266
#include <WiFiUdp.h> // import WiFi UDP library for ESP8266 

#define pulse_pin 8 // define pulse pin as 8 (GPIO6)

char packetBuffer[255]; // create a packet buffer
char replyBuffer[] = "Received"; // create a reply buffer
char ssid[] = "AccessPoint"; // create a ssid buffer for the access point
char pass[] = "12345687"; // create a password buffer for the access point
char val[]; // create a value buffer

unsigned int localPort = 2390; // create a local port buffer for the UDP connection
int angle; // create an angle buffer for the servo
int pulse_min = 500; // create a pulse min variable for the servo
int pulse_max = 2500; // create a pulse max variable for the servo
int angle_min = 0; // create an angle min variable for the servo
int angle_max = 180; // create an angle max variable for the servo
int pulse_period =20000 ; // create a pulse period variable for the servo

void setup(){
    Serial.begin(9600); // start serial communication at 9600 baud
    WiFi.begin(ssid,pass); // connect to access point with the ssid and password
    while ( WiFi.status() != WL_CONNECTED ){ // check if the WiFi is connected
        Serial.println("."); // print a dot to the serial monitor
    }
    Serial.println("Connected"); // print a message to the serial monitor that the WiFi is connected
    Serial.println(WiFi.localIP()); // print the IP address of the ESP8266 to the serial monitor
    Udp.begin(localPort); // start the UDP connection on the local port
    }
}

void loop{
    if (packetSize) { // check if there is a packet in the buffer
        int len = Udp.read(packetBuffer, 255); // read the packet into the packet buffer
        if (len > 0) { // check if the packet is not empty
            packetBuffer[len] = 0; // add a null terminator to the end of the packet
            val=packetBuffer; // set the value buffer to the packet buffer
        }
    }
    
    angle = int(val); // set the angle variable to the value buffer
    
    move_pos(angle); // move the servo to the angle variable
}

int move_pos(int angle){ // create a function to move the servo to the angle variable
        if (angle >= 0){ // check if the angle is greater than or equal to 0
            int delay_high = map(angle, angle_min, angle_max, pulse_min, pulse_max); // map the angle variable to the pulse min and pulse max variables
            digitalWrite(pulse_pin,HIGH); // set the pulse pin to HIGH
            delayMicroseconds(delay_high); // delay the servo for the delay high variable
            digitalWrite(pulse_pin,LOW); // set the pulse pin to LOW
            delayMicroseconds(pulse_period-delay_high); // delay the servo for the pulse period minus the delay high variable
        }
        else if (angle==500){ // if the motor is released
        digitalWrite(pulse_pin,LOW); // set the pulse pin to LOW
        }
    }
}
