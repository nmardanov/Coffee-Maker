import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback
from gpiozero import Servo




def rotate(stage):
    pin = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(.615)
    GPIO.output(pin,GPIO.LOW)
    if(stage ==2):
        GPIO.output(pin,GPIO.HIGH)
        time.sleep(.275)
        GPIO.output(pin,GPIO.LOW)

def reset():
    time.sleep(60)
    pin = 16
    print("did it freak out yet?")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    print("finished drink")
    time.sleep(60)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(.675*2)
    GPIO.output(pin,GPIO.LOW)
