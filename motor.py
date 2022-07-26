import RPi.GPIO as GPIO
from time import sleep

#motor = Motor(forward = 20, backward = 21)
num1 = 40
num2 = 38
num3 = 37
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(num1, GPIO.OUT)
GPIO.setup(num2, GPIO.OUT)
GPIO.setup(num3, GPIO.OUT)

pwm = GPIO.PWM(num3, 50)
pwm.start(0)
def forward(value):
    pwm.ChangeDutyCycle(value)

    GPIO.output(num1,1)
    GPIO.output(num2,0)

def backward(value):
    pwm.ChangeDutyCycle(value)

    GPIO.output(num1,0)
    GPIO.output(num2,1)

def breaks():
    pwm.ChangeDutyCycle(1)

    GPIO.output(num1,0)
    GPIO.output(num2,1)