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
  self.list_path = "rsl_list.csv"

 def set_logger(self,logger):
  self.logger = logger
 def get_page_content(self,url):
  page=requests.get(url)
  return page.content
 def get_hashes(self):
  self.active_hashes = []
  self.inactive_hashes = []
  with open(self.list_path) as csvfile:
   csvreader= csv.reader(csvfile,delimiter=",")
   for row in csvreader:
#       print(row[1])
       self.logger.wtil(row[1])
       content = self.get_page_content(row[1])
       time.sleep(5.0)


       soup= BeautifulSoup(content,'html.parser')
       if(len(row[0].split("/"))==1):
            size="NULL"
       else:
            size=row[0].split("/")[1]
       try:
           inv= soup.find(class_='tbl_productVariant')
           inventory = inv.find_all(class_='row')
           inventory.pop(0)
           for i in inventory:
               if i.get_text().strip()=='Udsolgt':
#                    self.logger.wtil('No Size in inventory')

                    hash_to_save = self.finder.findtheid(row[0])
                    if(hash_to_save != None):
                     self.inactive_hashes.append(hash_to_save)

                    break
               elif i.get_text()=="":
                    hash_to_save = self.finder.findtheid(row[0])
                    if(hash_to_save != None):
                        self.active_hashes.append(hash_to_save)
                    break
               elif i.get_text() == size:
                   if(i.find(class_='inoutStock')):
#                       print(size + " not in inventory")
                       break
                   else :
                       hash_to_save = self.finder.findtheid(row[0])
                       if(hash_to_save != None):
                        self.active_hashes.append(hash_to_save)
                       break
       except:
           self.logger.wtil(size+ " not in inventory")
class Finder:
    def findtheid(self, sku):
        for i in spd:
            if(i["sku"]==sku):
#                print("Id of " + sku + " = "+i["id"])
                return i["id"]
#        print(sku+ " not Found in .py file")
