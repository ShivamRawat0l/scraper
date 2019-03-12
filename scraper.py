import csv
import requests
from bs4 import BeautifulSoup
import json
from sp_script import spd
from sp_script_active import spda
import sys
import os
import time


class RSLContent:
 def __init__(self):
  self.name = "RSLContent"
  self.sites = []
 def add_site(self,site):
  self.sites.append(site)

 def get_content_for_url(self,url):
  for site2 in self.sites:
   if(site2.url == url):
    return site2.content
  return False
 def is_stored(self,url):
  for site2 in self.sites:
   if(site2.url == url):
    return True
  return False
  
class SiteContent:
 def __init__(self):
  self.name = "SiteContent"
 def set_url(self,url):
  self.url = url
 def set_content(self,content):
  self.content = content
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

  self.active_skus = []
  self.inactive_skus = []

  self.rsl_content = RSLContent()
  with open(self.list_path) as csvfile:
   csvreader= csv.reader(csvfile,delimiter=",")
   for row in csvreader:
#       print(row[1])
       url = row[1]
       if(self.rsl_content.is_stored(url)):
        html_content = self.rsl_content.get_content_for_url(url)
       else:
#        self.logger.wtil(url)
        html_content = self.get_page_content(url)
        time.sleep(5.0)

        content = SiteContent()

        content.set_url(url)
        content.set_content(html_content)

        self.rsl_content.add_site(content)

       soup= BeautifulSoup(html_content,'html.parser')
       if(len(row[0].split("/"))==1):
            size="NULL"
       else:
            size=row[0].split("/")[1]
       try:
           inv= soup.find(class_='tbl_productVariant')
           inventory = inv.find_all(class_='row')
           inventory.pop(0)
           available = False
           not_available = False
           self.logger.wtil(str(url))
           for i in inventory:

#               variant = inv.find_all(class_='variant')
#               for v in inventory:
#                self.logger.wtil(str(v.get_text()))

               variant = inv.find_all(class_='col-md-4 col-sm-6')
               for v in inventory:
                size_from_site = str(v.get_text())
                if("Udsolgt" in size_from_site):
                 size_from_site = size_from_site[0:-8]
                 available = False
                 not_available = True
                else:
                 available = True
                 not_available = False
                if(size_from_site == size):
                 hash_to_save = self.finder.findtheid_active(row[0])
                 if(hash_to_save != None):
                  if(not_available):
                   self.inactive_hashes.append(hash_to_save)
                   self.inactive_skus.append(row[0])
                  if(available):
                   self.active_hashes.append(hash_to_save)
                   self.active_skus.append(row[0])
                 break
#                self.logger.wtil(size_from_site)


               if "input class=" in str(i):
                    hash_to_save = self.finder.findtheid(row[0])
                    if(hash_to_save != None):
                        self.active_hashes.append(hash_to_save)
                        self.active_skus.append(row[0])
                        available = True
                        not_available = False

               elif 'Udsolgt' in str(i.get_text().strip()):
#                    self.logger.wtil('No Size in inventory')

                    hash_to_save = self.finder.findtheid_active(row[0])
                    if(hash_to_save != None):
                     self.inactive_hashes.append(hash_to_save)
                     self.inactive_skus.append(row[0])
                     available = False
                     not_available = True
                    break

               elif i.get_text()=="":
                    hash_to_save = self.finder.findtheid(row[0])
                    if(hash_to_save != None):
                        self.active_hashes.append(hash_to_save)
                        self.active_skus.append(row[0])
                        available = True
                        not_available = False
                    break
               elif i.get_text() == size:
                   if(i.find(class_='inoutStock')):
#                       print(size + " not in inventory")
                       break
                   else :
                       hash_to_save = self.finder.findtheid(row[0])
                       if(hash_to_save != None):
                        self.active_hashes.append(hash_to_save)
                        self.active_skus.append(row[0])
                        available = True
                        not_available = False
                       break
           if(available and not not_available):
            self.logger.wtil(str(row[0])+" AVAILABLE")
           elif(not available and not_available):
            self.logger.wtil(str(row[0])+" NOT_AVAILABLE")
           elif(not available and not not_available):
            self.logger.wtil("PROBLEM: "+str(row[0]))
       except:
           self.logger.wtil(size+ " not in inventory")
class Finder:
    def findtheid(self, sku):
        for i in spd:
            if(i["sku"]==sku):
#                print("Id of " + sku + " = "+i["id"])
                return i["id"]
    def findtheid_active(self, sku):
        for i in spda:
            if(i["sku"]==sku):
#                print("Id of " + sku + " = "+i["id"])
                return i["id"]
#        print(sku+ " not Found in .py file")
