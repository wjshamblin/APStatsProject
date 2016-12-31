# APStatsProject

Ben Shamblin's AP Stats project comparing notable deaths from 2006 through
2016 in order to determine if 2016 notable deaths were indeed higher than
normal as some reports have claimed. 

In this comparison, I compared three sources:

Death Server (http://dpsinfo.com/dps/)

Wikipedia Deaths (https://en.wikipedia.org/wiki/YEAR#Deaths)

NY Times Obituaries

The Death Server data was scraped and parsed using a custom script
(parse_death_stats.py). The Wikipedia data was collected using the
wikipedia python module (https://pypi.python.org/pypi/wikipedia/) and
a custom script (wikipedia_search.py) that generates a CSV file from
the collected data. The NYTimes data
was collected through their article API (http://developer.nytimes.com/)
and a custom script to retrieve the results (nytimes.py) and parse
the returned results into a CSV file (parse_nytimes.py). Using the NYTimes
API turned out to difficult since you can only return 10 results per page,
and a maximum of 120 pages from the API. This meant that I had to chop the
searches into parts and stitch them together. In addition, each API key
can only be used for 1000 queries per day. After trying to get a higher
limit from the NYTimes (and failing) I obtained multiple keys and spread
the queries out over those keys in order to complete the 11 year data
collection.

