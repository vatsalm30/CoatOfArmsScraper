import requests
from bs4 import BeautifulSoup
import re
import csv

def getdata(url):  
    r = requests.get(url)  
    return r.text  

htmldata = getdata("https://en.wikipedia.org/wiki/Armorial_of_sovereign_states")  
soup = BeautifulSoup(htmldata, 'html.parser')  
for item in soup.find_all('img', attrs={'class':'mw-file-element'}): 

    imgurl = item['src'].rsplit('/', 1)[0]

    thumbPos = imgurl.find('/thumb')
    if thumbPos != -1:
        imgurl = imgurl[:thumbPos] + imgurl[thumbPos+6:]
    if not imgurl.endswith(".svg"):
        continue
    imgurl = imgurl[2:]
    countryName = item.get('alt')

    patterns_to_remove = ['Coat of arms of', 'Emblem of', 'Seal of', 'Great Seal of']

    countryName = re.sub(r'\(.*?\)', '', countryName)

    for pattern in patterns_to_remove:
        countryName = countryName.replace(pattern, '').strip()
    countryName = re.sub(' +', ' ', countryName).strip()
    
    coatOfArms = {"Country Name":countryName, "Image URL":imgurl}

    with open('coatOfArms.csv', 'a', newline='', encoding="utf-8") as csvfile:
        fieldnames = ['Country Name', 'Image URL']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(coatOfArms)