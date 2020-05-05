import json
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from unidecode import unidecode

headers = ['name', 'total_views', 'creator_wards', 'past_members', 'genres', 'instruments', 'labels', 'associated_acts', 'years_active', 'occupation(s)', 'birth_name', 'origin', 'born', 'members', 'also_known_as', 'genre', 'years_active', 'subscribers', 'website', 'spouse(s)','occupation']
djlinks=['Nervo_(DJs)','Quintino_(DJ)','Alan_Walker_(music_producer)','The_Wolfpack','KURA','Martin_Jensen_(DJ)','Vintage_Culture','Mariana_BO','Mike_Williams_(DJ)','Fisher_(musician)','Illenium','Diplo','Da_Tweekaz','Marco_Carta','Carl Nunes','Radical_Redemption','Yellow_Claw_(DJs)','CamelPhat','Thomas_Gold_(DJ)','Black_Coffee_(DJ)']

out_file = open("dj_details.json", "a")

for person in djlinks:
    details = dict()
    for h in headers:
        details[h]=" "

    name = unidecode(person.replace("%26","&").replace("_"," "))
    print(name)
    tw = name + " wikipedia"
    temp = ""
    for i in search(tw, num=1,stop = 1):
        print(i)
        temp = requests.get(i).content

    soup = BeautifulSoup(temp,"lxml")
    table = soup.find("table",attrs={"class":"infobox vcard plainlist"})
    details['name'] = name
    
    if table:
        for tr in table.findAll("tr"):
            th = tr.find("th")
            td = tr.find("td")
            if td and th and th.text.replace(" ","_").lower() in headers:
                if td.find("li") is None:
                    details[th.text.replace(" ","_").lower()] = unidecode(td.text)
                else:
                    for k in td.findAll("li"):
                        details[th.text.replace(" ","_").lower()]+=k.text+", "
    print("Accessed wikipedia")
        
    json.dump(details, out_file)
    out_file.write(',\n')

out_file.close()