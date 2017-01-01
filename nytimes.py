#!/usr/bin/python

import json
import re
import requests
import time

nyurl = 'https://api.nytimes.com/svc/search/v2/articlesearch.json'
# for a full run
#years = ['2006', '2007', '2008', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016']
#se_dates = {'01'01':'0331', '0401':'0731', '0801':'12'31'}

# catch up for last couple of days in 2016
se_dates = {'1130':'1231'}
years = ['2016']

# read in entire file into string
api_file = open('.nytimes_api_keys', 'r').read()
# multiline match for the key
api_re = re.compile(r'^(?m)api_key = (.*)$')
key_matches =  api_re.findall(api_file)
if key_matches:
    # Find useable key (anyone that is uncommented)
    api_key = key_matches[0]
else:
    raise Exception("No useable key")

payload = {'api_key': api_key, 'q':'obituary'}

for year in years:
    # Set initial status
    status = 'OK'
    # Break up the year into smaller chunks to get around the 120 page search limit
    for j in se_dates:
        # Declare a container for the results
        all_results = []
        f = open("NYTimesData/" + 'nytimes-'+year+"-"+j+'.json', 'w')
        # Reset the status to OK for each run, will be overridden if the query fails
        status = 'OK'
        # Grad the fields that we are interested in
        payload['begin_date'] = year + j
        payload['end_date'] = year + se_dates[j]
        payload['page'] = 0
        # iterate over all of the possible pages, nytimes seems to have a limited API
        for i in range(120):
            # make the query
            r = requests.get(nyurl, params=payload)
            # check return code make sure it is OK (200)
            if r.status_code == 200 and r.text:
                # get the returned documents from the json text we were returned
                docs = json.loads(r.text)['response']['docs']
                # if we have results, append the to the results container
                if docs:
                    all_results.append(docs)
            # increment the page to get the next page of results
            payload['page'] = i + 1
            # this seems to be needed to work around too many queries in a short time
            time.sleep(3)
        # write all of the results out to a file
        f.write(json.dumps(all_results, default=str, indent=2))
        f.close()

