import RPi_I2C_driver as rpi_lcd
from time import *
import smbus
lcd = rpi_lcd.lcd()

def print_lcd(args, num):
    lcd.lcd_display_string(args,num)

def lclear():
    lcd.lcd_clear()