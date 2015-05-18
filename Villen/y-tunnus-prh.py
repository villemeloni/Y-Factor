import requests
import pprint
import re
import csv
import numpy as np

ytunnukset = []
#Luetaan sisaan y-tunnukset
data=np.loadtxt(r'ahjo-output-20-clean-test.csv',dtype=str,delimiter=';',skiprows=1,usecols=(1,))
#Luetaan y-tunnukset uuteen listaan jota kaytetaan api-kyselyyn
ytunnukset = data.tolist()
#tulostetaan ytunnukset
#print ytunnukset
print ytunnukset

#prh-apin alustus

tunnukset = ytunnukset
haku_parametrit = {'businessId': '',
                 }         
endpoint = "http://avoindata.prh.fi:80/bis/v1/"

#haetaan rajapinnasta y-tunnuksiin liittyva data ja tallennetaan nimet listaan

firmat = []
#firmat = {}

for tunnus in tunnukset:
    haku_parametrit['businessId'] = tunnus
    response = requests.get(endpoint, params=haku_parametrit)
    data = response.json()
    #print data
    print response.status_code
    if response.status_code == 200:
    	for item in data['results']:
    		firmat.append(tunnus)
    		firmat.append(item['name'].encode('utf-8'))
    		firmat.append('\n')
    		print item['addresses'][0]['street']
    		#if 'addresses' in item:
    			#firmat.append(item['addresses'][0]['street'].encode('utf-8'))
   	 		#pitaa viela poimia kaikki street esiintymat tuolta talteen - Petri tekee esimerki javascriptilla
	
    	
#tuotetaan csv-tiedosto
out = csv.writer(open("yritykset.csv","w"), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow(firmat)

#f = open('ytunnukset.txt', 'w')
#for y in firmat:
#	f.write(y + ",")
#f.close()

#tulostetaan lista
pprint.pprint(firmat)

"""
-luetaan sisaan ahjosta saadut y-tunnukset OK
-kysellaan y-tunnuksia vastaavat yritystiedot rajapinnasta OK
-tallennetaan yritystiedot
-viedaan yritystiedost csv-tiedostoon
"""