#!/usr/bin/env python

import json, requests, os, sys
from bs4 import BeautifulSoup
import lxml
from urllib import urlopen

url_home = 'https://people.nasa.gov/people/search'
t = 'https://people.nasa.gov/people/search?firstName=*&middleInitial=&lastName=&email=&phone='

ppl = {}

def hit_page():
    res = requests.get(url=t, timeout=10)
    if res.status_code != 200:
        raise Exception("unable to hit site: {err}".format(err=res.status_code))
    else:
        print '{}'.format(res.content)
        result = json.loads(res.content)
        print '{}'.format(json.dumps(result, indent=2))

def parse_row(row_soup):
    td = row_soup.find_all("td")
    name = td[0].text
    email = td[1].find("span").text
    phone = td[2].text

    if email == "":
        email = "NA"

    if phone == "":
        phone = "NA"

    #return "* ".join([name, email, phone])
    #return {email: {'name': name, 'phone': phone}}
    return (name, email, phone)

def search_for(search_list):
    prefix = "https://people.nasa.gov/people/search?email="
    fn_query_string = "&firstName="
    ln_query_string = "&lastName="

    result = set()

    for i in search_list:
        url = prefix + ln_query_string + i
        sys.stdout.write('Gathering data for [{}]: '.format(i))
        sys.stdout.flush()

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        if soup.find("div", {"class" : "warning"}):
            raise Exception("OH NO! we have too many results. Invalid! Bail")

        person = soup.find("tr", {"class" : "even"})
        count = 0
        while person:
            result.add(parse_row(person))
            person = person.find_next_sibling()
            count = count + 1
        print 'added {} [Total: {}]'.format(count, len(result))
    return result

search1 = []
search2 = []
search3 = []
search4 = []
search5 = []
letter_count = 6
for a in range(letter_count):
    search1.append(chr(97 + a))
    for b in range(letter_count):
        search2.append(chr(97 + a) + chr(97 + b))
        for c in range(letter_count):
            search3.append(chr(97 + a) + chr(97 + b) + chr(97 + c))
            for d in range(letter_count):
                search4.append(chr(97 + a) + chr(97 + b) + chr(97 + c) + chr(97 + d))
                for e in range(letter_count):
                    search5.append(chr(97 + a) + chr(97 + b) + chr(97 + c) + chr(97 + d) + chr(97 + e))
print "search1 count: {}".format(len(search1))
print "search2 count: {}".format(len(search2))
print "search3 count: {}".format(len(search3))
print "search4 count: {}".format(len(search4))
print "search5 count: {}".format(len(search5))

# loop over all the items in the search list (last name only)
# and ensure that we don't get any 'max results' returned.  if we do then our results
# are invalid.
# assuming we are getting full results, put all the results in a dictionary using
# the name as the key.  this will eliminate duplicates (i can warn if we hit a dup)
# count the results

query = search5

results = search_for(query)
print 'Total results for A-F search5 (from {} queries): {}'.format(len(query), len(results))
with open('results.csv', 'w') as f:
    f.write("name * email * phone\n")
    for (name, email, phone) in sorted(results):
        f.write("{n} * {e} * {p}\n".format(n=name, e=email, p=phone))
