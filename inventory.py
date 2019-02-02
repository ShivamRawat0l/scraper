import requests
from bs4 import BeautifulSoup
import json
#page= requests.get("http://seizoroi.com/api/dallas.html")
page=requests.get('http://www.seizoroi.com/api/nova.html')
#page=requests.get('http://seizoroi.com/api/short.html')
soup= BeautifulSoup(page.content,'html.parser')
dictionary=[]
try:
    inv= soup.find(class_='tbl_productVariant')
    inventory = inv.find_all(class_='row')
    inventory.pop(0)
    for i in inventory: 
        if(i.find(class_='inoutStock')):
            dictionary.append({i.find(class_='variantudsolgt').get_text(): 'Unavailable'})
        else:
            dictionary.append({i.get_text(): 'Available'})
except:
    dictionary={"None":"None"}
with open('nova.json','w') as fp : 
        json.dump(dictionary,fp)
print(dictionary)