import csv
import requests
from bs4 import BeautifulSoup
import json
from sp_script import spd
import sys
import os
import time


class Scraper:
 def __init__(self):
  self.name = "Scraper"
  self.finder = Finder()
 def get_hashes(self):
  scriptDirectory = os.path.dirname(os.path.realpath(__file__))
  hashes_to_return = []
  with open(scriptDirectory+"/rsl_list.csv") as csvfile:
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
#                       print(size + " not in inventory")
                       break
                   else :
                       hash_to_save = self.finder.findtheid(row[0])
                       if(hash_to_save != None):
                        hashes_to_return.append(hash_to_save)
                       break
       except:
           print(size+ " not in inventory")
  return hashes_to_return
class Finder:
    def findtheid(self, sku):
        for i in spd:
            if(i["sku"]==sku):
#                print("Id of " + sku + " = "+i["id"])
                return i["id"]
#        print(sku+ " not Found in .py file")
