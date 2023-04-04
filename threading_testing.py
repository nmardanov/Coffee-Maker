import threading
import logging
import time
from GmailAPI import Gmail_API as g
import OrderParser as o

orders = []

def CheckForOrder():
    ordered = True
    order = g.checkMail().lower()
    if order:
        order = o.CheckTextVaildity(order)
        print(order)
        return order
    return 'ESC'

def threaded_function():
    print('hi')
    o = CheckForOrder()
    orders.append(o)

    

gettingOrders = threading.Thread(target=threaded_function)
gettingOrders.start()

while True:
    time.sleep(1)
    print(orders)



