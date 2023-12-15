import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback

grounds_list = [

    {

        "name": "Light",
        "grinder": "Grinder_1"

    },

    {

        "name": "Medium",

    },

    {

        "name": "Dark",
        "grinder": "Grinder_2"

    }

]

def Pump_Grounds():
    pin = 6
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(4)
    GPIO.output(pin,GPIO.HIGH)
    print("OFF")