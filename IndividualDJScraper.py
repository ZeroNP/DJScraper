import json
import requests
from bs4 import BeautifulSoup
from googlesearch import search
from unidecode import unidecode

headers = ['name', 'total_views', 'creator_wards', 'past_members', 'genres', 'instruments', 'labels', 'associated_acts', 'years_active', 'occupation(s)', 'birth_name', 'origin', 'born', 'members', 'also_known_as', 'genre', 'years_active', 'subscribers', 'website', 'spouse(s)']
djlinks=['Dimitri_Vegas_%26_Like_Mike', 'Martin_Garrix', 'David_Guetta', 'Armin_Van_Buuren', 'Marshmello', 'Don_Diablo', 'Oliver_Heldens', 'Tiësto', 'Afrojack', 'Steve_Aoki', 'Alok', 'Hardwell', 'Timmy_Trumpet', 'R3hab', 'KSHMR', 'DJ_Snake', 'Eric_Prydz', 'W_%26_W', 'Calvin_Harris', 'Lost_Frequencies', 'Skrillex', 'Above_%26_Beyond', 'DVBBS', 'Nervo', 'Quintino', 'The_Chainsmokers', 'Alan_Walker', 'VINAI', 'Headhunterz', 'Fedde_Le_Grand', 'Vini_Vici', 'Ummet_Ozcan', 'Angerfist', 'Bassjackers', 'Carl_Cox', 'Blasterjaxx', 'Nicky_Romero', 'Wolfpack', 'ATB', 'Kura', 'Danny_Avila', 'Swedish_House_Mafia', 'Tujamo', 'Alison_Wonderland', 'Martin_Jensen', 'Cat_Dealers', 'Vintage_Culture', 'Adam_Beyer', 'Mariana_Bo', 'Zedd', 'MATTN', 'Kygo', 'Claptone', 'Mike_Williams', 'Diego_Miranda', 'Yves_V', 'Will_Sparks', 'Steve_Angello', 'Ferry_Corsten', 'Nina_Kraviz', 'Alesso', 'Breathe_Carolina', 'FISHER', 'Illenium', 'Deorro', 'Richie_Hawtin', 'Diplo', 'Da_Tweekaz', 'Miss_K8', '3_Are_Legend', 'Deadmau5', 'Carta', 'Carl_Nunes', 'Charlotte_de_Witte', 'Warface', 'Cedric_Gervais', 'Yellow_Claw', 'Lucas_%26_Steve', 'Andy_C', 'Peggy_Gou', 'Deniz_Koyu', 'Robin_Schulz', 'Vicetone', 'Tom_%26_Collins', 'Boris_Brejcha', 'Marco_Carola', 'Paul_van_Dyk', 'Solardo', 'Thomas_Gold', 'Black_Coffee', 'Paul_Kalkbrenner', "Daddy's_Groove", 'Julian_Jordan', 'Rave_Republic', 'Sub_Zero_Project', 'D.O.D', 'Henri_PFR', 'Florian_Picasso', 'Swanky_Tunes', 'Solomun']
out_file = open("dj_details.json", "a")

for person in djlinks:
    details = dict()
    for h in headers:
        details[h]=" "
    url = "https://en.wikipedia.org/wiki/"+person
    print(person)
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"lxml")
    table = soup.find("table",attrs={"class":"infobox vcard plainlist"})
    name = unidecode(person.replace("%26","&").replace("_"," "))
    details['name'] = name
    
    if table:
        for tr in table.findAll("tr"):
            th = tr.find("th")
            td = tr.find("td")
            if td and th:
                if td.find("li") is None:
                    details[th.text.replace(" ","_").lower()] = unidecode(td.text)
                else:
                    for k in td.findAll("li"):
                        details[th.text.replace(" ","_").lower()]+=k.text+", "
    print("Accessed wikipedia")
        
    tw = "twitter "+name
    temp = ""
    for i in search(tw, num=1,stop = 1):
        temp = requests.get(i).content

    print("Accessed Google")
    soup = BeautifulSoup(temp,"lxml")
    links = soup.findAll("a",attrs={"data-nav":"followers"})
    details['twitter_followers'] = ''
    if links:
        spans = links[0].findAll("span")
        if spans and len(spans)==3:
            details['twitter_followers'] = spans[2].text
    print("Accessed Twitter")
    json.dump(details, out_file)
    out_file.write(',\n')

out_file.close()