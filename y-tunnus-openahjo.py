import requests
import pprint
import re
import csv

#gittesti
#hakee openahjo-rajapinnasta y-tunnus maskilla ulos listan y-tunnuksia halutun maaran
#openahjo apin alustus
haku_parametrit = {'page': 1,
                 'format': 'json',
                 'limit': 5,
                 'text': 'y-tunnus'
                 }

endpoint = "http://dev.hel.fi/paatokset/v1/issue/search/"

#ladataan data rajapinnasta muistiin
response = requests.get(endpoint, params=haku_parametrit)
data = response.json()

#parsitaan datasta haluttuja arvoja listaan
lista = []

for item in data['objects']:
    lista.append(item['slug']) #slug kusee - lainausmerkki tulee mukaan jostain syysta
    lista.append(re.findall(r'\d\d\d\d\d\d\d-\d', item['search_highlighted']))
    lista.append(item['resource_uri'])
    lista.append(item['category'].encode('utf-8'))
    lista.append(item['category_name'].encode('utf-8'))
    lista.append(item['subject'].encode('utf-8'))    
    #lista.append(item['districts'][1]['name'].encode('utf-8')) #ei toimi ilman tsekkausluuppia koska ei ole vakiomaara
    lista.append(item['districts'])
    lista.append('\n')

#tuotetaan csv-tiedosto
out = csv.writer(open("ahjo.csv","wb"), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow(lista)

#tulostetaan lista
#pprint.pprint(lista)




"""
OHJELMAN KUVAUS
-ohjelma hakee open ahjo rajapinnasta http://dev.hel.fi/paatokset/v1/issue/search/?text=y-tunnus&format=json&limit=500 tietoja jotka tallennetaan CSV-tiedostoon
-CSV-tiedoston sarakerakenne: subject, diaarinumero slug,y-tunnus,ahjon top_category_name, asian kohteena oleva kaupunginosa disctricts - type, resource uri
-CSV tuottaa meille listan y-tunnus havaintoja

OHJELMAN VAIHEET

-funktio joka tekee kyselyn halutulla merkkijonolla open ahjo rajapintaan ja palauttaa json-objektin
-funktio joka ottaa json-objektista talteen diaarinumerot listaksi jossa on y-tunnus ja diaarinumero
-funktio joka tallentaa listan pilkuilla erotetuksi tekstitiedostoksi

HUOM
-jokaista diaariloytoa kohden voi olla enemman kuin yksi y-tunnus jolloin kirjataan loydos omalle rivilleen, talloin uniikki tunniste on diaarin ja y-tunnuksen yhdistelma
-rivityksen haun voi tehda urlin kovakoodauksella
"""

