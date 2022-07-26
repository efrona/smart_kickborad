import smbus
from time import sleep

address = 0x48
AIN1 = 0x41
AIN2 = 0x42

bus = smbus.SMBus(1)
def analogread():
    while True:
        bus.write_byte(address, AIN1)
        bus.read_byte(address) #dummy
        slider = bus.read_byte(address)
        bus.write_byte(address, AIN2)
        bus.read_byte(address) #dummy
        pressure = bus.read_byte(address)
        arr = [slider, pressure]
        return arr