#!/usr/bin/python

import csv
import re
import sys
import wikipedia

cw = csv.writer(sys.stdout)

years = [2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016]
months = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11,
    'December':12}

dayentry = re.compile(r'(?m)^=== \d+ ===\n(.*\n)+?(?=^(=== |== ))')
person_entry = re.compile(r'^(?m)(\w+.*)$')
name_age = re.compile(r'^(\w+), (\d+), (.*)')

cw.writerow(['date', 'name', 'age', 'comments'])
#
#a = re.compile(r'(?m)^=== \d+ ===\n(.*\n)*?')
for i in years:
    for j in months.keys():
        p = wikipedia.page("Deaths_in_"+j+"_"+str(i))
        # print type(p.content.encode('utf-8'))
        for match in dayentry.finditer(p.content):
            day_match = match.group(0)
            day_of_month = re.search(r'=== (\d+) ===', day_match).groups()[0]
            for pmatch in person_entry.finditer(day_match):
                na = re.match(r'^(\w+ .*) (\d+), (.*)', pmatch.group(0))
                if na:
                    line = [ str(i)+"-"+str(months[j])+"-"+day_of_month] + list(na.groups())
                    cw.writerow([x.encode('utf-8') for x in line])
