from tkinter import *
import serial
import time
import socket
import os
import platform 
import subprocess

angle=0
baud=9600

def select_board():
    global board
    print("If your receiver is arduino press 1, else if your receiver is esp8266 press 2 :")
    try:
        board=int(input())
    except:
        print("Please use an integer ")
        select_board()
    if (board!=1 and board!=2):
        print("Please input a valid choice:")
        select_board()
    else: 
        pass


def send_value(*args):
    if (board==1):
        angle=slider.get()
        angle=str(angle) + ":"
        arduino.write(bytes(angle,encoding='utf-8'))
        time.sleep(0.18)
    elif (board==2):
        angle = slider.get()
        angle=str(angle) + ":"
        sock.sendto(bytes(angle,encoding='utf-8'), (str(ip_port[0]).encode(),int(ip_port[1])))
        print(ip_port[0])
        print(ip_port[1])

def release_motor():
    if (board==1):
        arduino.write(bytes("500:",encoding='utf-8'))
    elif (board==2):
        sock.sendto(bytes("500:",encoding='utf-8'),(str(ip_port[0]).encode(),int(ip_port[1])))


def select_port():

    global port_user
    global arduino
    if (platform.system() == "Linux"):
        os.system("ls -la /dev/ | grep ttyUSB")
        ports=subprocess.run(['ls','/dev/','|','grep','tty'], stdout=subprocess.PIPE)
        print(ports)
    elif (platform.system() == "Windows"):
        os.system("chgport")
    else:
        pass

    print('Write serial port to continue (eg. COM1, /dev/ttyUSB0):')
    port_user=input()

    try:
        arduino = serial.Serial(port=port_user,baudrate=baud,timeout=.1)
    except:
        print("Please input a valid port:")
        select_port()


def select_ip_port():
    global ip_port
    global sock

    if (platform.system()=="Linux"):
        os.system("cat {}".format(port_user))
    print("Please write IP and port for ESP8266 (e.g. 192.168.1.1:80) :")
    ip_port=input().split(":") 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


select_board()

if (board==1):
    select_port()
elif (board==2):
    select_port()
    select_ip_port()


master=Tk()

slider=Scale(master, from_=0,to=180,variable=angle,orient=HORIZONTAL,command=send_value)
send=Button(master,text='Release',command=release_motor)
angle0=Radiobutton(master,text='0',variable=angle,value=0,command=send_value)
angle45=Radiobutton(master,text='45',variable=angle,value=45,command=send_value)
angle90=Radiobutton(master,text='90',variable=angle,value=90,command=send_value)
angle135=Radiobutton(master,text='135',variable=angle,value=135,command=send_value)
angle180=Radiobutton(master,text='180',variable=angle,value=180,command=send_value)

angle0.grid(row=0,column=0)
angle45.grid(row=0,column=1)
angle90.grid(row=0,column=2)
angle135.grid(row=0,column=3)
angle180.grid(row=0,column=4)
send.grid(row=0,column=5)
slider.grid(row=1,columnspan=6)

mainloop()
