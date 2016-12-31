#!/usr/bin/python3

import csv
from dateutil import parser
import os
import re
import sys

# J. D. Salinger (reclusive writer) -- Dead. Died January 27, 2010. Born January 1, 1919. Catcher in the Rye  IMDb  Obituary
death_entry = re.compile(r'^(?m)^(.*) -- Dead\. (.*)Died (.*) Born (.*?)\. (.*)$')

outfile = open('celebrity_deaths.csv', 'w')
csvwrite= csv.writer(outfile)
csvwrite.writerow(['name','cause of death', 'born', 'died', 'comments'])
files = os.listdir(".")
for f in files:
        if re.match(r'^20.*\.txt', f):
            file_text = open(f, 'r').read()
            for match in death_entry.finditer(file_text):
                name = match.group(1)
                cause = match.group(2)
                died = match.group(3).replace('.', '')
                born = match.group(4).replace('.', '')
                comments = match.group(5)
                csvwrite.writerow([name, cause, born, died, comments])

