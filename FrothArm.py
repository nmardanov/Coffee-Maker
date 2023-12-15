import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback
from gpiozero import Servo




def down():
    pin = 24
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pin,GPIO.LOW)
    print("up??")

def up():
    
    pin = 25
    
    print("did it go down yet?")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    print("finished drink")
    #time.sleep(60)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pin,GPIO.LOW)

