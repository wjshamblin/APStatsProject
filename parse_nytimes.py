#!/usr/bin/python
"""
Parse all of the files that were downloaded from the NYTimes article API
"""

import csv
from dateutil import parser
import json
import os
import re

f = open('nytimes-obituaries-2006-2016.csv', 'w')
csvwriter = csv.writer(f)
years = [2006, 2007, 2008, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
fields = {'totals': {}, 'entries':{}}

all_documents = {}
for k, v in fields.items():
    all_documents[k] = v
for year in years:
    all_documents['totals'][year] = 0

csvwriter.writerow(['date of death', 'article id', 'type of article', 'headline'])
files = os.listdir('NYTimesData')
for f in files:
    if re.match(r'nytimes-.*\.json$', f):
        try:
            json_content = json.loads(open("NYTimesData/" + f, 'r').read())
        except Exception as e:
            print e
        for i in json_content:
            for j in i:
                correction = re.match(r'Correction', j['type_of_material'])
                keyword_match = False
                for keyword in j['keywords']:
                    if re.search(r'(?i)Deaths \(Obituaries\)', keyword['value']):
                        keyword_match = True
                        # print "keyword matched"

                if (re.search(r'(?i)Obituary', j['type_of_material']) or keyword_match) and not correction:
                    pub_date = parser.parse(j['pub_date'])
                    if j['_id'] not in  all_documents['entries']:
                        all_documents['totals'][pub_date.year] += 1
                        all_documents['entries'][j['_id']] = {}
                        all_documents['entries'][j['_id']]['pub_date'] = pub_date
                        all_documents['entries'][j['_id']]['article'] = j
                    # else:
                    #     print "DUPLICATE KEYS", j['headline']['main']

                   # csvwriter.wrtiterow([pub_date.strftime("%Y-%m-%d"), j['type_of_material'], j['headline']['main'], j['snippet']])

for j in sorted(all_documents['entries'], key=lambda x:all_documents['entries'][x]['pub_date']):
    pub_date = all_documents['entries'][j]['pub_date']
    type_of = all_documents['entries'][j]['article']['type_of_material']
    headline = all_documents['entries'][j]['article']['headline']['main']
    snippet = all_documents['entries'][j]['article']['snippet']
    article_id = all_documents['entries'][j]['article']['_id']
    csvwriter.writerow([pub_date.strftime("%Y-%m-%d"),article_id, type_of, headline.encode('utf-8')])
    # for j in all_documents[i]:
for y in sorted(all_documents['totals']):
    print y, all_documents['totals'][y]
