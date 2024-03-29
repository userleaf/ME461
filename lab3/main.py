from tkinter import *
import serial
import time
import os
import platform
from numpy import interp  # import interp function from numpy
import subprocess
from tkinter import ttk
pwm = 0  # initial duty cycle value
freq = 250  # initial frequency value
freqMin = 32  # minimum frequency value
freqMax = 1000  # maximum frequency value
pwmMin = 0  # minimum duty cycle value
pwmMax = 100  # maximum duty cycle value
prescalar = 8  # prescalar value
baud = 115200  # set baud rate to 9600 bps 

read = "No data available!"  # initial text to display

is_cw = False  # initial direction value is set to counter clockwise
start_stop = True  # start_stop is set to true by default

port_user=None  # initial port value is set to none 
arduino=None  # initial arduino variable is set to none

class App(Tk):
    '''
    Class to create the GUI
    '''
    def __init__(self):
        '''
        Initialize the GUI
        '''
        super().__init__()
        # set the windowclass atribute to pop-up window 
        self.wm_attributes("-type", True)
        myColor = '#405062'                 # Its a light blue color

        s = ttk.Style()                     # Creating style element
        s.configure('Wild.TRadiobutton', background=myColor, foreground='black')

        self.direction=BooleanVar()  # create a boolean variable for the radio button to determine direction

        self.title("Servo Control")  # set the title of the GUI

        self.slider_pwm=Scale(self, from_=pwmMin,to=pwmMax,variable=pwm,orient=HORIZONTAL,command=send_value)  # create a slider 
        self.slider_freq=Scale(self, from_=freqMin,to=freqMax,variable=freq,orient=HORIZONTAL,command=send_value)  # create a slider 

        self.cw=ttk.Radiobutton(self,text='cw',variable=self.direction,value=True,command=send_value,style='Wild.TRadiobutton')  # create a radio button
        self.ccw=ttk.Radiobutton(self,text='ccw',variable=self.direction,value=False,command=send_value,style='Wild.TRadiobutton')  # create a radio button

        self.pwm0=Radiobutton(self,text='0',variable=pwm,value=0,command=send_value)  # create a radio button for pwm
        self.pwm25=Radiobutton(self,text='25',variable=pwm,value=25,command=send_value)  # create a radio button for pwm
        self.pwm50=Radiobutton(self,text='50',variable=pwm,value=50,command=send_value)  # create a radio button for pwm
        self.pwm75=Radiobutton(self,text='75',variable=pwm,value=75,command=send_value)  # create a radio button for pwm
        self.pwm100=Radiobutton(self,text='100',variable=pwm,value=100,command=send_value)  # create a radio button for pwm

        self.start=Button(self,text='Start',command=start_motor)  # create a button to start the motor
        self.stop=Button(self,text='Stop',command=stop_motor)  # create a button to stop the motor

        self.datafield=Label(self,text=read)  # create a label to display the data acquired from the arduino

        self.cw.grid(row=0,column=0)  # place the radio button in the grid
        self.ccw.grid(row=0,column=1)  # place the radio button in the grid

        self.pwm0.grid(row=0,column=2)  # place the radio button in the grid
        self.pwm25.grid(row=0,column=3)  # place the radio button in the grid
        self.pwm50.grid(row=0,column=4)  # place the radio button in the grid
        self.pwm75.grid(row=0,column=5)  # place the radio button in the grid
        self.pwm100.grid(row=0,column=6)  # place the radio button in the grid

        self.start.grid(row=0,column=7)  # place the button in the grid

        self.slider_pwm.grid(row=1,columnspan=8)  # place the slider in the grid
        self.slider_freq.grid(row=2,columnspan=8)  # place the slider in the grid
        self.stop.grid(row=3,columnspan=8)  # place the button in the grid

        self.datafield.grid(row=4,columnspan=8)  # place the label in the grid

        self.datafield.after(10,self.change_text)  # call the update_text function after 100ms

    def change_text(self):
        '''
        Changes the text on the screen to display the current values of the frequency, duty cycle, pot position, and direction
        '''
        global read  # the text to display on the screen
        line=arduino.readline()  # read the line of text from the serial port
        try:
            line=line.decode("utf-8")  # decode the line of text
            line=line.split(":")  # split the line into a list

            if int(line[0]):  # if the first element of the list is not zero
                read = "Rotation:CW " + "Frequency:" + line[1] + " Duty Cycle:" + line[2] + " Pot Value:" + line[3]  # set the text to the line
            else:  # if the first element of the list is zero
                read = "Rotation:CCW " + "Frequency:" + line[1] + " Duty Cycle:" + line[2] + " Pot Value:" + line[3]  # set the text to the line
        except:
            pass
        self.datafield.configure(text=read)  # change the text on the screen
        self.datafield.after(10,self.change_text)  # call the update_text function after 100ms

def byte_converter():
    '''
    Converts the data to bytes to be sent to the arduino     
    '''
    global pwm  # gets duty cycle value from slider
    global freq  # gets frequency value from slider
    global is_cw  # gets direction value from radio button
    icr1 = 16000000 / (prescalar * freq) - 1  # calculates the value of icr1
    icr1 = interp(icr1,[1999,65535],[0,511])  # divides by 2 to get the value of icr1
    duty = pwm / (100 / 63)
    icr1 = int(icr1)  # converts icr1 to an integer
    duty = int(duty)  # converts duty to an integer
    if is_cw:  # if the direction is clockwise 
        return 32768 + 64 * icr1 + duty  # convert to bytes
    else:  # if the direction is counter clockwise
        return 64 * icr1 + duty  # convert to bytes 


def select_port():  # function to select the port
    '''
    Selects the port to be used to communicate with the arduino 
    '''

    global port_user  # gets the port value from the user
    global arduino  # gets the arduino variable
    if (platform.system() == "Linux"):  # if the system is linux
        p1 = subprocess.Popen(["ls", "-la","/dev/"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", "ttyUSB"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
        output,err = p2.communicate()
        output=output.decode("utf-8")  # decode the output
        output=output.split(" ")  # split the output into a list
        output[-1]=output[-1].split("\n")[0]  # remove the new line character from the last element of the list
        port_user='/dev/' + output[-1]
        print(output[-1])
    elif (platform.system() == "Windows"):  # if the system is windows
        os.system("chgport")  # open a window to select a port
        print('Write serial port to continue (eg. COM1, /dev/ttyUSB0):')  # ask user to write port
        port_user=input()  # get user input
    else:  # if the system is mac
        pass  # if the system is not linux or windows then do nothing

    try:  # try to open the port
        arduino = serial.Serial(port=port_user,baudrate=baud,timeout=.1)  # open the port
    except:  # if the port is not open
        print("Please input a valid port:")  # tell user to input a valid port
        select_port()  # call select_port function again

def send_value(*foo):  # function to send the value to the arduino
    '''
    Sends the value to the arduino in the form of bytes arranged as rotation, frequency, and duty cycle 
    rotations are either 1 or 0 for clockwise and counter clockwise respectively
    frequency is a value between 0 and 127 (inclusive) and duty cycle is a value between 0 and 255 (inclusive) 
    which sums up to a max value of 65535 (inclusive) it correspons to the size of an unsigned integer in arduino 
    '''
    global pwm  # gets duty cycle value from slider
    global freq  # gets frequency value from slider
    global is_cw  # gets direction value from radio button
    global arduino  # gets the arduino variable
    global start_stop  # gets the start_stop variable

    pwm = master.slider_pwm.get()  # gets duty cycle value from slider
    freq = master.slider_freq.get()  # gets frequency value from slider
    is_cw = master.direction.get()  # gets direction value from radio button
    data = byte_converter()  # converts data to bytes

    if (start_stop):  # if the motor is started
        arduino.write(bytes(str(data) + ":",encoding='utf-8'))  # writes data to the port 
        time.sleep(.19)  # sleep for a tenth of a second
    else:  # if the motor is stopped
        arduino.write(bytes(str(0) + ":", encoding='utf-8'))  # sends stop data to arduino

    # change_text()  # calls change_text function
    print(data)  # prints data to the console

def stop_motor():  # function to stop the motor
    '''
    Stops the motor by setting start_stop to false and sending the stop data to the arduino
    '''
    global start_stop
    start_stop = False
    send_value()

def start_motor():
    '''
    Starts the motor by setting start_stop to true and sending the start data to the arduino
    '''
    global start_stop
    start_stop = True
    send_value()


select_port()  # call select_port function

master=App()  # create a window
master.mainloop()  # start the main loop

