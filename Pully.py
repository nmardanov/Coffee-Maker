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
    time.sleep(5)
    GPIO.output(pin,GPIO.LOW)
    print("is dorian's code the right one?")

def up():
    pin = 25
    
    print("did it go up yet?")
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    print("checking dorian's code")
    #time.sleep(60)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(1.6)
    GPIO.output(pin,GPIO.LOW)
    pin = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(5)
    GPIO.output(pin,GPIO.HIGH)   
    pin = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)

    #time.sleep(60)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pin,GPIO.LOW)

def reset():
    pin = 25
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)

    #time.sleep(60)
    GPIO.output(pin,GPIO.HIGH)
    time.sleep(10)
    GPIO.output(pin,GPIO.LOW)