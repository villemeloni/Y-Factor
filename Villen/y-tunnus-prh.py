#This program uses a list of company ids from open ahjo to fetch company information from prh api
#Created by Ville Meloni
#github.com/villemeloni

import requests
import pprint
import re
import csv
import numpy as np

def load_companyids_list():
	ytunnukset = []
	#Loading in company IDs aka y-tunnukset
	data=np.loadtxt(r'ahjo-output-20-clean-test.csv',dtype=str,delimiter=';',skiprows=1,usecols=(1,))

	#Reading company IDs to a new list that will be used for further API querying
	ytunnukset = data.tolist()
	print ytunnukset
	return ytunnukset

#printing company id list 
#print ytunnukset

def query_prhapi(ytunnukset): #calling function with ytunnukset value from load_companyids_list func
	print "QUERY PRHAPI"
	#setting parameters for querying paten registry office api
	tunnukset = load_companyids_list()
	haku_parametrit = {'businessId': '',
                 }         
	endpoint = "http://avoindata.prh.fi:80/bis/v1/"

	#creating a onte time list to store result of each companyid query
	firmat = []

	#creating a list of lists to aggregate each companyid query to
	#could also be a dictionary like firmat = {}
	kaikkifirmat = []

	#using companyid list to query prh-api
	for tunnus in tunnukset:
  	  haku_parametrit['businessId'] = tunnus
  	  response = requests.get(endpoint, params=haku_parametrit)
  	  data = response.json()
 	  #print response status
 	  print response.status_code
  	  #storing data to list only if status ok 200
  	  if response.status_code == 200:
  	  	print 'ok, data available'
    		for item in data['results']:
    			firmat.append(tunnus)
    			firmat.append(item['name'].encode('utf-8'))
    			print (item['name'].encode('utf-8'))
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
    			try:
    				print item['addresses'][0]['city']	
    				firmat.append(item['addresses'][0]['city'].encode('utf-8'))
    			except:
    				print 'sorry, no city'	
    			"""
    			try:
    				print item['businessLines'][0]['code']
    				firmat.append(item['businessLines'][0]['code'].encode('utf-8'))
    				print item['businessLines'][0]['name']
    				firmat.append(item['businessLines'][0]['name'].encode('utf-8'))
    			except: 
    				print 'sorry, no businessline info'
    			"""
   		 
		kaikkifirmat.append(firmat)
    	firmat = []
    	return kaikkifirmat

def print_companies():
	print 'PRINTING COMPANIES'    			
	# printing the list with company id, company name and address and postcode to the screen
	firmalista = query_prhapi()
	pprint.pprint(firmalista)

def companydata_csv():
	print "WRITING CSV"
	#creating csv-file
	firmatoutput = query_prhapi()
	print 'Creating CSV-file'
	out = csv.writer(open("yritykset.csv","w"), delimiter=',',quoting=csv.QUOTE_ALL)
	out.writerows(firmatoutput)

def main():
	load_companyids_list()
	query_prhapi(load_companyids_list())
	#print_companies(query_prhapi())
	#companydata_csv()

main()


#BUGLIST
#UTF8 encoding problem with reading data from api or outputting to csv-file
#FIXED - commas in wrong places in csv-output
##how to get rid of quoting escape character?
###used lists within list to solve it
