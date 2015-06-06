import requests
import pprint
import re
import csv
import numpy as np

ytunnukset = []
#Loading in company IDs aka y-tunnukset
data=np.loadtxt(r'ahjo-output-20-clean-test.csv',dtype=str,delimiter=';',skiprows=1,usecols=(1,))

#Reading company IDs to a new list that will be used for further API querying
ytunnukset = data.tolist()

#printing company id list 
print ytunnukset

#parameters for querying paten registry office api
tunnukset = ytunnukset
haku_parametrit = {'businessId': '',
                 }         
endpoint = "http://avoindata.prh.fi:80/bis/v1/"

#fetching data from api and storing data to a list

firmat = []
#could also be a dictioanry like firmat = {}

for tunnus in tunnukset:
    haku_parametrit['businessId'] = tunnus
    response = requests.get(endpoint, params=haku_parametrit)
    data = response.json()
    #print response status
    print response.status_code
    #storing data to list only if status ok 200
    if response.status_code == 200:
    	for item in data['results']:
    		firmat.append(tunnus)
    		firmat.append(item['name'].encode('utf-8'))
    		try:
    			print item['addresses'][0]['street']
    			firmat.append(item['addresses'][0]['street'].encode('utf-8'))
    		except: 
    			print 'sorry, no address'
    		try:
    			print item['addresses'][0]['postCode']	
    			firmat.append(item['addresses'][0]['postCode'].encode('utf-8'))
    		except: 
    			print 'sorry, no post code'
    		firmat.append('\n')
    #else inform that no data available
    else:
    	print 'no data available'
    			
#creating csv-file
#BUG - problem with this setup as puts the comma into a funny place - need to fix
out = csv.writer(open("yritykset.csv","w"), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow(firmat)

#alternatively just to create a text file without csv-writer module
#f = open('ytunnukset.txt', 'w')
#for y in firmat:
#	f.write(y + ",")
#f.close()

#finally printing the list with company id, company name and address to the screen
pprint.pprint(firmat)