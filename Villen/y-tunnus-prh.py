#This program uses a list of company ids from open ahjo to fetch company information from prh api
#Created by Ville Meloni
#github.com/villemeloni/Y-Factor

#NOTE - using global variables - could pass local ones instead via main function I guess

import requests
import pprint
import re
import csv
import numpy as np

def load_companyids_list():
    #loading list of companyids from a given csv-files
    print "LOADING COMPANY IDs"
    global ytunnukset
    ytunnukset = []
    #Loading in company IDs aka y-tunnukset
    data=np.loadtxt(r'ahjo-output-20-clean-test.csv',dtype=str,delimiter=';',skiprows=1,usecols=(1,))

    #Reading company IDs to a new list that will be used for further API querying
    ytunnukset = data.tolist()
    print ytunnukset
    return ytunnukset

#printing companyidlist 
#print ytunnukset

def query_prhapi(): 
    #fetching data from the prh api
    print "QUERY PRHAPI"
    #setting parameters for querying paten registry office api
    global tunnukset
    tunnukset = ytunnukset
    haku_parametrit = {'businessId': '',
                 }         
    endpoint = "http://avoindata.prh.fi:80/bis/v1/"

    #creating a onte time list to store result of each companyid query
    global firmat
    firmat = []

    #creating a list of lists to aggregate each companyid query to
    #could also be a dictionary like firmat = {}
    csvheader = ['CompanyID','Name','Address','Postcode','City']
    global kaikkifirmat
    kaikkifirmat = []
    kaikkifirmat.append(csvheader)

    #using companyid list to query prh-api

    for tunnus in tunnukset:
        haku_parametrit['businessId'] = tunnus
        response = requests.get(endpoint, params=haku_parametrit)
        data = response.json()
        #print response status
        print response.status_code
        #storing data to list only if status ok 200
        if response.status_code == 200:

            print 'OK, data available'
            for item in data['results']:
                firma = [tunnus]  # Create a new list form firma data
                firma.append(item['name'])
                if 'addresses' in item and len(item['addresses']) > 0:
                    address = item['addresses'][0]
                    firma.append(address.get('street', ''))
                    firma.append(address.get('postCode', ''))
                    firma.append(address.get('city', ''))
                firma = [x.encode('utf-8') for x in firma]
                print firma
                kaikkifirmat.append(firma)

        else:
            print 'Sorry, no data available'
        
    #print 'kaikkifirmat tallessa'
    #print kaikkifirmat
    #return kaikkifirmat

def print_companies():
    #printing the list with company id, company name and address and postcode to the screen
    print 'PRINTING COMPANIES'                
    pprint.pprint(kaikkifirmat)

def companydata_csv():
    #creating csv-file with company info
    print "WRITING CSV"
    out = csv.writer(open("yritykset.csv","w"), delimiter=',',quoting=csv.QUOTE_ALL)
    out.writerows(kaikkifirmat)

def main():
    #main function that calls the other functions
    load_companyids_list()
    query_prhapi()
    print_companies()
    companydata_csv()

main()


#BUGLIST
#UTF8 encoding problem with reading data from api or outputting to csv-file
#FIXED - commas in wrong places in csv-output
##how to get rid of quoting escape character?
###used lists within list to solve it
"""
For fetching more data for example
                try:
                    print item['businessLines'][0]['code']
                    firmat.append(item['businessLines'][0]['code'].encode('utf-8'))
                    print item['businessLines'][0]['name']
                    firmat.append(item['businessLines'][0]['name'].encode('utf-8'))
                except: 
                    print 'sorry, no businessline info'
"""
