#-- coding: utf-8 --

import RPi.GPIO as GPIO
from pirc522 import RFID

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


rc522 = RFID()
def rfid_search():
    while True :
        rc522.wait_for_tag()
        (error, tag_type) = rc522.request()
        if not error :
            (error, uid) = rc522.anticoll()
            if not error :
                print(uid)
                return uid
