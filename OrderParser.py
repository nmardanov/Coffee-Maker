import re
from drinks import drink_list 
import json 


def CheckTextVaildity(order):
    

   drinks = []     

   for name in drink_list:
        drinks.append(name['name'])

   print(drinks)
   
   string = r'\b('
   for drink in drinks:
        string += drink + r'|'
   string = string[:-1]
   string += r')\b'
   coffeetype = re.findall(string, order, re.I)

   if len(coffeetype) > 1:
     print("Too many inputs")
 

   matches = False
   for value in drinks:
       if coffeetype:
           if value == coffeetype[0]:
              matches = True
              break
     
   if matches:
           return value
   else:
           return "Not on the menu"

