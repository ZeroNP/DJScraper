import requests
response = requests.get("https://djmag.com/top100djs")
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.content,"lxml")
for dj in soup.findAll("div",attrs={"class":"top100dj-name"}):
    print(dj.find("a").text)
l = []
for dj in soup.findAll("div",attrs={"class":"top100dj-name"}):
    l.append(dj.find("a").text)
djlinks = []
for i in l:
    djlinks.append(i.replace(" ","_").replace("&","%26"))

for person in djlinks:
    details = dict()
    url = "https://en.wikipedia.org/wiki/"+person

    response = requests.get(url)
    soup = BeautifulSoup(response.content,"lxml")
    table = soup.find("table",attrs={"class":"infobox vcard plainlist"})
    for tr in table.findAll("tr"):
        th = tr.find("th")
        td = tr.find("td")
        if td and th:
            details[th.text] = td.text
    
