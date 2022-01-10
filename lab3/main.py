from tkinter import *
import serial
import time
import os
import platform

pwm = 0 
freq = 100 
freqMin = 0
freqMax = 127
pwmMin = 0
pwmMax = 255

baud=9600

read = "pwm=0,freq=o,dire=ccw"

is_cw = False
start_stop = True

port_user=None
arduino=None

def byte_converter():
    global pwm 
    global freq
    global is_cw
    if is_cw:  # if the direction is clockwise
        return 32768 + 16384 * freq + pwm  # convert to bytes
    else:  # if the direction is counter clockwise
        return 16384 * freq + pwm  # convert to bytes

def change_text():
    global read 
    line=arduino.readline()  # read the line of text from the serial port
    line=line.split(":")  # split the line into a list
    if line[0]:
        read = "Rotation:CW " + "Frequency:" + line[1] + " Duty Cycle:" + line[2]  # set the text to the line
    else:
        read = "Rotation:CCW " + "Frequency:" + line[1] + " Duty Cycle:" + line[2]  # set the text to the line
    text.configure(text=read)

def select_port():
    global port_user 
    global arduino
    if (platform.system() == "Linux"):  # if the system is linux
        os.system("ls -la /dev/ | grep ttyUSB")  # list all usb ports
    elif (platform.system() == "Windows"):  # if the system is windows
        os.system("chgport")  # open a window to select a port
    else:
        pass  # if the system is not linux or windows then do nothing

    print('Write serial port to continue (eg. COM1, /dev/ttyUSB0):')  # ask user to write port
    port_user=input()  # get user input

    try:  # try to open the port
        arduino = serial.Serial(port=port_user,baudrate=baud,timeout=.1)  # open the port
    except:  # if the port is not open
        print("Please input a valid port:")  # tell user to input a valid port
        select_port()  # call select_port function again

def send_value(*foo):
    global pwm
    global freq
    global is_cw
    global arduino
    global start_stop

    pwm = slider_pwm.get()  # gets duty cycle value from slider
    is_cw = direction.get()  # gets direction value from radio button
    data = byte_converter()  # converts data to bytes

    if (start_stop):
        arduino.write(bytes(data))  # writes data to the port 
    else:
        arduino.write(bytes(0))  # sends stop data to arduino

    time.sleep(0.01)  # delays program for 1/10th of a second
    # change_text()  # calls change_text function
    print(data)

def stop_motor():
    global start_stop
    start_stop = False
    send_value()

def start_motor():
    global start_stop
    start_stop = True
    send_value()


select_port()

master=Tk()

direction=BooleanVar()  # create a boolean variable for the radio button to determine direction

slider_pwm=Scale(master, from_=pwmMin,to=pwmMax,variable=pwm,orient=HORIZONTAL,command=send_value)  # create a slider 
slider_freq=Scale(master, from_=freqMin,to=freqMax,variable=freq,orient=HORIZONTAL,command=send_value)  # create a slider 

cw=Radiobutton(master,text='cw',variable=direction,value=True,command=send_value)  # create a radio button
ccw=Radiobutton(master,text='ccw',variable=direction,value=False,command=send_value)  # create a radio button

pwm0=Radiobutton(master,text='0',variable=pwm,value=0,command=send_value)  # create a radio button for pwm
pwm25=Radiobutton(master,text='25',variable=pwm,value=25,command=send_value)  # create a radio button for pwm
pwm50=Radiobutton(master,text='50',variable=pwm,value=50,command=send_value)  # create a radio button for pwm
pwm75=Radiobutton(master,text='75',variable=pwm,value=75,command=send_value)  # create a radio button for pwm
pwm100=Radiobutton(master,text='100',variable=pwm,value=100,command=send_value)  # create a radio button for pwm

start=Button(master,text='Start',command=start_motor)  # create a button to start the motor
stop=Button(master,text='Stop',command=stop_motor)  # create a button to stop the motor

text=Label(master,text=read)  # create a label to display the data acquired from the arduino


cw.grid(row=0,column=0)  # place the radio button in the grid
ccw.grid(row=0,column=1)  # place the radio button in the grid

pwm0.grid(row=0,column=2)  # place the radio button in the grid
pwm25.grid(row=0,column=3)  # place the radio button in the grid
pwm50.grid(row=0,column=4)  # place the radio button in the grid
pwm75.grid(row=0,column=5)  # place the radio button in the grid
pwm100.grid(row=0,column=6)  # place the radio button in the grid

start.grid(row=0,column=7)  # place the button in the grid

slider_pwm.grid(row=1,columnspan=8)  # place the slider in the grid
slider_freq.grid(row=2,columnspan=8)  # place the slider in the grid
stop.grid(row=3,columnspan=8)  # place the button in the grid

text.grid(row=4,columnspan=8)  # place the label in the grid

mainloop()  # start the main loop

