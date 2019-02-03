import csv
import requests
from bs4 import BeautifulSoup
import json
from sp_script import spd
import sys
from os import name,system
import time
class Utils: 
    def clear(self): 
        if name == 'nt': 
            system('cls') 
        else: 
            system('clear') 
    def minuteconvert(self,a):
        return a*60;
class Finder :  
    def findtheid(self, sku):
        for i in spd: 
            if(i["sku"]==sku):
                print("Id of " + sku + " = "+i["id"])
                return 
        print(sku+ " not Found in .py file")



finder = Finder()
utility = Utils()
if __name__ == "__main__"  : 
    
    if len(sys.argv)==1: 
        timer=10
    else :
        timer= sys.argv[1]
    timer=utility.minuteconvert(timer)
    while True:
        utility.clear()
        with open("rsl_list.csv") as csvfile: 
            csvreader= csv.reader(csvfile,delimiter=",")
            for row in csvreader:
                page=requests.get(row[1])
                soup= BeautifulSoup(page.content,'html.parser')
                size=row[0].split("/")[1]
                try:
                    inv= soup.find(class_='tbl_productVariant')
                    inventory = inv.find_all(class_='row')
                    inventory.pop(0)
                    for i in inventory: 
                        if i.get_text() == size:
                            if(i.find(class_='inoutStock')):
                                print(size + " not in inventory")
                                break
                            else : 
                                finder.findtheid(row[0])
                                break
                except: 
                    print(size+ " not in inventory")
        time.sleep(timer)

        