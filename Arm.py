import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback
from gpiozero import Servo




def rotate():
    pin = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(.65)
    GPIO.output(pin,GPIO.LOW)

def reset():
    pin = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1.3)
    GPIO.output(pin,GPIO.LOW)

rotate()
reset()