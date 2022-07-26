#-- coding: utf-8 --

import threading
from time import sleep
from rfid_scan import rfid_search
from lcd import print_lcd, lclear
import gps as gps_func
from analogread import analogread as a_read
import motor
import helmet

#나이를 변수로 설정
age = 21

SLEEPTIME = 0.01

stop = False
breaks = False
speed = 30
address= ""
in_park = False
weight = 0
maxspeed = 25
speed = 0
gps_minus = 0
kmspeed = 0
age_minus = 0
motorspeed = 0


def rfid_r():
    #define
    get_in_code = [[23, 124, 125, 90, 76],
                    [179, 92, 7, 64, 168],
                    [59, 246, 80, 78, 211],
                    [75, 77, 53, 78, 125],
                    [75, 73, 250, 78, 182],
                    [36, 72, 74, 86, 112],
                    [36, 68, 255, 86, 201]]
    get_out_code = [[59, 3, 245, 78, 131],
                    [59, 76, 159, 78, 166],
                    [43, 194, 84, 78, 243],
                    [59, 26, 86, 78, 57],
                    [124, 218, 125, 175, 116],
                    [36, 41, 27, 86, 64],
                    [59, 244, 175, 78, 46]]

    while True:
        sleep(SLEEPTIME)
        global stop, breaks, weight
        try:
            id = rfid_search()
            #read stop tag
            if id in get_in_code:
                #all stop
                print("stop")
                stop = True
                breaks = True

            #read get out tag
            elif id in get_out_code:
                stop = False
                breaks = False
                print("non stop")
            else:
                print('nope')
        except:
            pass
            print("except")
def gps():
    global address, in_park, gps_minus
    while True:
        in_park = gps_func.read_GPS()
        if in_park == 1:
            print("in the park")
            #cut 16 char (to print_lcd)
            gps_minus = 0
            address = gps_func.gps_address
            address = list(address)
            temp = []
            for i in range(16):
                temp.append(address[i])
            address = temp

        elif in_park == 0:
            print("out of park")
            gps_minus = 5
            #cut 16 char (to print_lcd)
            address = gps_func.gps_address
            address = list(address)
            temp = []
            for i in range(16):
                temp.append(address[i])
            address = temp
        elif in_park == -1:
            #print("can not find address")
            address = "cant location"
            gps_minus = 5
def read():
    global weight, stop, breaks, speed, kmspeed, motorspeed
    while True:
        sleep(SLEEPTIME)
        try:
            value = a_read()
            speed = int(value[0])
            weight= int(value[1])
            #weight    
            if weight >= 50:
                breaks = True
            elif weight < 50:
                breaks = False
            #speed
            motorspeed = int((speed /240)*100)
            kmspeed = int((speed /230)*25)
            print(value)
        except:
            print("except")

def stop_check():
    global stop, breaks
    if stop == True:
        lclear()
        print_lcd("STOP STOP STOP", 1)
        print_lcd("GET OFF",2)
        while True:
            sleep(SLEEPTIME)
            if breaks == False:
                lclear()
                print("break false")
                print_lcd("Draw your", 1)
                print_lcd("kick board",2)
                while True:
                    if stop == False:
                        break
                    sleep(SLEEPTIME)
            if stop == False:
                break
                
def check():
    for i in range(3):
        stop_check()
        sleep(1)
    lclear()

def lcd():
    #global
    global address, in_park, kmspeed, maxspeed, gps_minus, age_minus
    while True:
        if kmspeed > maxspeed-gps_minus-age_minus:
            print_lcd(f"Speed:{maxspeed-gps_minus-age_minus}km/s",1)
            print_lcd(f"Max Speed:{maxspeed-gps_minus-age_minus}km/s", 2)
        else:
            print_lcd(f"Speed:{kmspeed}km/s",1)
            print_lcd(f"Max Speed:{maxspeed-gps_minus-age_minus}km/s", 2)

        check()
    
        print_lcd(f"Age : {age}",1)
        
        check()

        print_lcd(address, 1)
        if in_park == True:
            print_lcd("in the park",2)
        elif in_park == False:
            print_lcd("out of park",2)
            
        check()

#main
#check helmet
lclear()
print_lcd("checking your",1 )
print_lcd("helmet...", 2)
helmet.callback()

lclear()
print_lcd("helmet checked.",1 )
sleep(3)
lclear()
#starting thread
thread_list = [lcd, gps,read, rfid_r]
for i in thread_list:
    thread = threading.Thread(target=i)
    thread.start()

#motor
while True:
    if age < 16:
        stop == True
    elif age >= 16 and age < 19:
        age_minus = 5
    elif age >= 19 :
        age_minus = 0
    if stop == True:
        if breaks == True:
            motor.backward(20)
        else :
            motor.forward(0)
    else:
        if kmspeed > maxspeed-gps_minus-age_minus:
            motor.forward((maxspeed-gps_minus-age_minus)*4)
            print(f"speed : {maxspeed-gps_minus-age_minus}")
        else : 
            motor.forward(motorspeed)
            print(f"speed :{kmspeed}")
    sleep(SLEEPTIME)
