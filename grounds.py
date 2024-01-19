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
        "grinder": "Grinder_2"

    },

    {

        "name": "Dark",
        "grinder": "Grinder_2"

    }

]

def Pump_Grounds(ground):
    print('testing', ground)
    pin = 6
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(6)
    GPIO.output(pin,GPIO.HIGH)
    print("OFF")