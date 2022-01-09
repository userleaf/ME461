//create an array from 3 to 10
int ledPin[]={
  4,5,6,7,8,9,10,11};
int minNum = 0;
int maxNum = 255;
int inByte =0;
int buttonState = 1;
int previousButtonState = 1;
int buttonCount = 0;
int autoCounter = 0;
int autoDelta = 1; 

int readings[3];
int headIndex = 0;

bool pause = false;
volatile bool trigger = false;

String command ="";
String val = "";
String inputString = "";         // a String to hold incoming data

bool stringComplete = false;  // whether the string is complete

#define button 2

void setup() {
    inputString.reserve(200);
    for (int i = 0; i < 9; i++) { 
        pinMode(ledPin[i], OUTPUT); // set pin to output

    } // for loop ends
    
    pinMode(A0,INPUT); // set pin A0 as input
    pinMode(button,INPUT_PULLUP); // set button pin as input with internal pullup resistor
    Serial.begin(9600); // start serial communication
    Serial.print("Enter: \n 1 for Automatic up/down counter \n 2 for Serial display mode \n 3 for POT value display \n 4 for Programmable mode ");
    attachInterrupt(0,command_func,FALLING);

} // setup ends


void loop() {
    //choice is the serial interrupted input
    int choice = Serial.parseInt(); // read the input
    //switch-case statement to determine the choice from 1 to 4
    switch(choice){
        case(1): 
        		func1();
      		
        case(2):
                func2();
            
        case(3):
                func3();

        case(4):
                func5();
                
        

    }// swich-case statement ends
} // loop ends

void func1(){
    while(1){
        buttonState = digitalRead(button); // read the state of the button
        Serial.println(buttonState); // print the button state
        if (buttonState != previousButtonState){ // if the button state has changed
            buttonCount++; // increment the button count
            delay(10); // wait for 10 milliseconds
        }
        previousButtonState = buttonState; // update the previous button state
        byteReader(buttonCount); // call the byteReader function
    }
} // func1 ends

void func2(){
    while(1){
        if (Serial.available()) { // get incoming decimal number:            
            inByte = Serial.parseInt(); // read the input with the setting of no line ending
            Serial.println(inByte); // print the input
            if (inByte > maxNum) { // if the input is greater than the maximum number
                inByte = maxNum; // set the input to the maximum number
            }
            
        }
        byteReader(inByte); // call the byteReader function      
    }
} // func2 ends

void func3(){
    while(1){

        int min=0,max=0;
        int readings[8];
        for(int index=0; index<8; index++)
        {
        readings[index] = analogRead(A0);
        if(readings[index]<min)
            min = readings[index];
        else if(readings[index]>max)
            max = readings[index];
        }
        byteReader(max);  // call the byteReader function
    }
} // func3 ends

void func4(){
    while(1){
        autoCounter += autoDelta; // increment the autoCounter
        byteReader(autoCounter);  // call the byteReader function
        delay(150); // wait for 500 milliseconds
        if(autoCounter == minNum || autoCounter == maxNum) autoDelta = -autoDelta;  // if the autoCounter is equal to the minimum number or the maximum number, change the autoDelta
        
        while (trigger || pause){
            if ( digitalRead(2)) trigger=false;
            Serial.println(pause);
            while (!(digitalRead(2))){  
                if (Serial.available()) {          
                    command = Serial.read(); // read the input with the setting of no line ending
                    Serial.println("command"); // print the input
                    if (command[0]=='!'){
                        char cmd;
                        cmd = command[1];
                        
                        if (cmd == 'p') pause = true;
                        if (cmd == 'c') pause = false;
                        if (cmd == 'm') Serial.println('Fuck ME');

                    }
                    
                }
                
                
            }

        }
    }
     
} // func4 ends

void func5(){
    while(1){
        
        if ( digitalRead(2)) trigger=false;
            if (Serial.available() && trigger) {          
                command = Serial.readString(); // read the input with the setting of no line ending
                Serial.println("command"); // print the input
                if (command[0]=='!'){
                    char cmd;
                    cmd = command[1];
                    
                    if (cmd == 'p') pause = true;
                    if (cmd == 'c') pause = false;
                    if (cmd == 'm') {
                        if (isDigit(command[4])){
                            val +=command[2];
                            val +=command[3];
                            val +=command[4];
                        }
                        else{
                            val +=command[2];
                            val +=command[3];
                        }
                        maxNum=val.toInt();
                    }

                }
                        
            }    
        

        if ( digitalRead(2)) trigger=false;

        if(!(trigger) || !(pause)){

                autoCounter += autoDelta; // increment the autoCounter
                byteReader(autoCounter);  // call the byteReader function
                delay(150); // wait for 500 milliseconds
                if(autoCounter == minNum || autoCounter == maxNum) autoDelta = -autoDelta;  // if the autoCounter is equal to the minimum number or the maximum number, change the autoDelta
                
            
        }
    }

}



void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();
    // add it to the inputString:
    inputString += inChar;
    // if the incoming character is a newline, set a flag so the main loop can
    // do something about it:
    if (inChar == '\n') {
      stringComplete = true;
    }
  }
}
void  byteReader(byte decimalNum){
    for(int i = 0; i < 8; i++) { // for loop to iterate through the array
        if (bitRead(decimalNum,i)==1){ // if the bit is 1
            digitalWrite(ledPin[i],HIGH); // turn on the led
        }
        else{ // if the bit is 0
            digitalWrite(ledPin[i],LOW); // turn off the led
        }
  } // for loop ends
} // byteReader ends

void command_func(){
       trigger=true;  
    
}

void pote_fixer(){


}

int removeHeadAddTail(int tail) {
    int head = array[headIndex];
    array[headIndex] = tail;
    headIndex = (headIndex + 1) % size; 
    return head;
}