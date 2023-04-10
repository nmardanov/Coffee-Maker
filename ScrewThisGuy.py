import time
import sys
import RPi.GPIO as GPIO
import json 
import threading
import traceback
from GmailAPI import Gmail_API as g
import OrderParser as o


from menu import MenuItem, Menu, Back, MenuContext, MenuDelegate
from drinks import drink_list, drink_options



GPIO.setmode(GPIO.BCM)


FLOW_RATE = 60.0/100.0

class Bartender(MenuDelegate): 
	
    def __init__(self):
        print("Initializing...")

        self.possibleDrinks = drink_list
        self.running = False
        # load the pump configuration from file
        self.pump_configuration = Bartender.readPumpConfiguration()
        for pump in self.pump_configuration.keys():
            #Finding the pin numbers per pump and seting up the GPIO
            if not self.pump_configuration[pump]['pin'] == 21:
                GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.HIGH)
            else:    
                GPIO.setup(self.pump_configuration[pump]["pin"], GPIO.OUT, initial=GPIO.LOW)
            

        print("Done initializing")

    @staticmethod
    def readPumpConfiguration():
        return json.load(open('/home/lamarcsnhscoffee/Desktop/Coffee-MakerV.2/Coffee-Maker/pump_config.json'))
        

    def clean(self):
        waitTime = 60
        pumpThreads = []

        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        self.running = True

        for pump in self.pump_configuration.keys():
            pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))

            if self.pump_configuration[pump]["pin"]==21:
                continue
            pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        #self.progressBar(waitTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        #self.menuContext.showMenu()

        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2)

        # reenable interrupts
        # self.startInterrupts()
        self.running = False

    def displayMenuItem(self, menuItem):
        print(menuItem.name)

    def pour(self, pin, waitTime):
        if pin == 21:
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(waitTime)
            GPIO.output(pin, GPIO.LOW)
        else:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(waitTime)
            GPIO.output(pin, GPIO.HIGH)


    def makeDrink(self, ingredients):
        # cancel any button presses while the drink is being made
        # self.stopInterrupts()
        #The drink parameter is a string that represents the name of the drink being made 
        #ingredients is a dictionary where the keys are strings representing the names of the ingredients and the values are floats representing the amount of each ingredient required to make the drink.
        #For example a drink like half and half 50% coffee and 50% milk
        #Would have ingredients 'Coffee' : 50, 'Milk' :50

        if ingredients == "ESC":
            return "dumbass. enter a real drink"

        self.running = True

        maxTime = 0
        pumpThreads = []
        #This loop goes though each ingredient 
        for ing in ingredients.keys():
            #This loop looks though each pump in the pump config to see if there is one that matches the label of the ingredent we are attempting to add
            for pump in self.pump_configuration.keys():
                if ing == self.pump_configuration[pump]["value"]:
                    #This finds how long we should pour the drink for
                    waitTime = ingredients[ing] * FLOW_RATE
                    if (waitTime > maxTime):
                        maxTime = waitTime
                    #Bro really worte it weird for no reason but args is just the paramenters for the pour method
                    #So this opens a thread which goes to the pour method for each ingredient
                    #THE THREADS HAVENT STARTED YET
                    #Then it adds them to a list of not started threads 
                    pump_t = threading.Thread(target=self.pour, args=(self.pump_configuration[pump]["pin"], waitTime))
                    pumpThreads.append(pump_t)

        # start the pump threads
        for thread in pumpThreads:
            thread.start()

        # start the progress bar
        #I dont think we need this
        #self.progressBar(maxTime)

        # wait for threads to finish
        for thread in pumpThreads:
            thread.join()

        # show the main menu
        #Don't think we need this either 
        #self.menuContext.showMenu()


        # sleep for a couple seconds to make sure the interrupts don't get triggered
        time.sleep(2);

        # reenable interrupts
        # self.startInterrupts()
        self.running = False


    #WTF does this code do
    def run(self):
        self.startInterrupts()
        # main loop
        try:  
            while True:
                time.sleep(0.1)
            
        except KeyboardInterrupt:  
            GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
        GPIO.cleanup()           # clean up GPIO on normal exit 

        traceback.print_exc()

    def ChooseDrink(self, drinkName):
        for drink in self.possibleDrinks:
            if drink['name'] == drinkName:
                print(drink['ingredients'])
                return drink['ingredients']

orders = []


def CheckForOrder():
    ordered = True
    thing = g.checkMail()
    order = thing[0].lower()
    print(order)
    order = o.CheckTextVaildity(order)
    if not order == None:
        print('This is the order')
        print(order)
        return order
    else:
        d = 'Please choose from one of these drinks: '
        for drink in drink_list:
            d += (drink['name'])  
            d += ', '
        print(d)
        g.SendEmail(thing[1], None, d)
        print(thing[1])
        return CheckForOrder()

bartender = Bartender()


def orderThread():
    while True:
        o = CheckForOrder()
        print(o)
        orders.append(o)
        print(orders)




    


#SomethingNasty = {'Milk' : 1, 'Water' : 1}
#bartender.makeDrink(SomethingNasty)
#time.sleep(2)

#print('How many drinks do we want to make')
#drinkLimit = input()

d = []
for drink in drink_list:
      d.append(drink['name'])  
print(d)
print('Which drink are you making')

gettingOrders = threading.Thread(target=orderThread)
gettingOrders.start()

drinkcount = 0

while True:
    print(orders)
    if len(orders) > 0:
        order = orders[0]
        orders.pop(0)
        order = bartender.ChooseDrink(order)
        bartender.makeDrink(order)
        drinkcount += 1
    #if drinkcount == drinkLimit:
    #   break
    time.sleep(1)

gettingOrders.join()


#test2 = input()
#If that works test this
#test2 = bartender.ChooseDrink(test2)
#print(test2)
#bartender.makeDrink(test2)

#If that works we just need to connect up the text API

#If we want to clean the pumps attach water to them and run this code
#bartender.clean()

#WTF Does this code do?
#bartender.buildMenu(drink_list, drink_options)
#bartender.run()




