from tkinter import * # Tkinter GUI
import serial # for serial interface
import time # for timeouts and sleep
import socket # for udp package sending
import os # for os commands to check ports etc
import platform # for os commands to check ports etc

angle=0 # angle of servo in degrees (0-180)
baud=9600 # baud rate for serial communication

def update_slider():
    if (board==1): # if arduino
        val=arduino.readline() # read serial port and set slider value
        try:
            slider.set(val) # set slider value
        except:
            pass
        print(val)
        master.after(1,update_slider)

def select_board():
    '''
    this function is used to select the board to be used for the program to run on
    it will ask the user to select the board and then set the global variable board
    if the board is valid it will set the global variable board to the selected board
    else it will call the function again
    '''
    global board 
    print("If your receiver is arduino press 1, else if your receiver is esp8266 press 2 :") 
    try:
        board=int(input()) # input is string, so we need to convert to int
    except:
        print("Please use an integer ") # if input is not an integer
        select_board() # call function again
    if (board!=1 and board!=2): # if input is not 1 or 2
        print("Please input a valid choice:") 
        select_board() # call function again
    else: 
        pass

def send_value(*args):
    '''
    This function is used to send the value of the angle to the board 
    the value is sent as a string in the form of "angle:", where angle is the angle in degrees

    '''
    angle = slider.get() # get value from slider
    angle=str(angle) + ":" # add colon to end of value

    if (board==1): # if arduino
        arduino.write(bytes(angle,encoding='utf-8')) # send value to arduino
        time.sleep(0.20) # wait for arduino to process value
    elif (board==2): # if esp8266
        sock.sendto(bytes(angle,encoding='utf-8'), (str(ip_port[0]).encode(),int(ip_port[1]))) # send value to esp8266

def release_motor():
    '''
    This function is used to release the motor by an invalid angle value 
    '''

    if (board==1): # if arduino
        arduino.write(bytes("500:",encoding='utf-8')) # send a value to stop the motor to arduino
    elif (board==2): # if esp8266
        sock.sendto(bytes("500:",encoding='utf-8'),(str(ip_port[0]).encode(),int(ip_port[1]))) # send a value to stop the motor to esp8266

def select_port():
    '''
    This function is used to select the port to be used for the program to run on
    it will ask the user to select the port and then set the global variable port
    function will check the operating system and use the correct command to list ports
    and it will also check if the port is valid or not 
    if the port is valid it will set the global variable port to the selected port
    else it will call the function again 
    '''
    global port_user
    global arduino
    if (platform.system() == "Linux"): # if linux
        os.system("ls -la /dev/ | grep ttyUSB") # list all ttyUSB ports
    elif (platform.system() == "Windows"): # if windows
        os.system("chgport") # list all USB ports
    else: # if other
        pass # do nothing

    print('Write serial port to continue (eg. COM1, /dev/ttyUSB0):') # ask for port
    port_user=input() # get port

    try: # try to open port
        arduino = serial.Serial(port=port_user,baudrate=baud,timeout=.1) # open serial port
    except: # if port is not available
        print("Please input a valid port:") 
        select_port() # call function again

def select_ip_port():
    '''
    This function is used to select the ip and port to be used for the program to run on
    it will ask the user to select the ip and port and then set the global variable ip_port
    function will check the operating system and use the correct command to list ports
    and it will also check if the port is valid or not 
    if the port is valid it will set the global variable ip_port to the selected ip and port
    else it will call the function again and mock the user
    '''
    global ip_port
    global sock

    if (platform.system()=="Linux"): # if linux
        os.system("arp -a") # list all ip addresses
    else: # if windows or other
        print("Use an Operating System for true engineers!!") # mock user
    
    print("Please write IP and port for ESP8266 (e.g. 192.168.1.1:80) :") # ask for ip and port
    ip_port=input().split(":") # split ip and port into two variables 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # create udp socket
    ping=os.system("ping -c1 {}".format(ip_port[0])) # ping ip address to test connection
    if (ping==0): # if ping is successful
        pass # do nothing
    else:
        print(
            '''
______________
            ''') 
        os.system("arp -e|awk '{if(NR==2) print $1}'") # list all ip addresses
        print(
        '''
--------------
        \   ^__^
         \  (oo)\_______
            (__)\       )\\/\\
                ||----w |
                ||     ||
        ''') # mock user
        select_ip_port() # call function again


select_board() # call function to select board

if (board==1):
    select_port() # call function to select port
elif (board==2):
    select_ip_port() # call function to select ip and port

master=Tk() # create window 

slider=Scale(master, from_=0,to=180,variable=angle,orient=HORIZONTAL,command=send_value) # create slider with range 0-180 and command to send value
send=Button(master,text='Release',command=release_motor) # create button to release motor 
angle0=Radiobutton(master,text='0',variable=angle,value=0,command=send_value) # create radiobutton to set angle to 0
angle45=Radiobutton(master,text='45',variable=angle,value=45,command=send_value) # create radiobutton to set angle to 45
angle90=Radiobutton(master,text='90',variable=angle,value=90,command=send_value) # create radiobutton to set angle to 90
angle135=Radiobutton(master,text='135',variable=angle,value=135,command=send_value) # create radiobutton to set angle to 135 
angle180=Radiobutton(master,text='180',variable=angle,value=180,command=send_value) # create radiobutton to set angle to 180


angle0.grid(row=0,column=0) # place radiobutton for 0 degrees
angle45.grid(row=0,column=1) # place radiobutton for 45 degrees 
angle90.grid(row=0,column=2) # place radiobutton for 90 degrees
angle135.grid(row=0,column=3) # place radiobutton for 135 degrees
angle180.grid(row=0,column=4) # place radiobutton for 180 degrees
send.grid(row=0,column=5) # place button to release motor
slider.grid(row=1,columnspan=6) # place slider

update_slider()
mainloop() # start GUI
