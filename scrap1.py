import requests
from bs4 import BeautifulSoup
import json
#page= requests.get("http://seizoroi.com/api/dallas.html")
#page=requests.get('http://www.seizoroi.com/api/nova.html')
page=requests.get('http://seizoroi.com/api/short.html')
soup= BeautifulSoup(page.content,'html.parser')
cat=soup.find_all(class_="category-box")
dictionary=[]
inventory=1
for i in cat:
    dictionary.append(
        {
            "inventory" : inventory,
            'link':i.find('a')["href"],
            'category-title' : i.find(class_='category-title').get_text(),
            'colorCode' : i.find(class_="colorCode").get_text() , 
            'old-price' : i.find(class_='old-prise').get_text() if i.find(class_='old-prise') else '--', 
            'new-price' : i.find('strong').get_text() 
        }
    )
    inventory+=1
with open('short.json','w') as fp : 
    json.dump(dictionary,fp)
print(dictionary)