#!/usr/bin/env python

import json, requests, os, sys
from bs4 import BeautifulSoup
import lxml
from urllib import urlopen

def save_data(fname, results):
    with open(fname, 'w') as f:
        f.write("name * email * phone\n")
        for (name, email, phone) in sorted(results):
            f.write("{n} * {e} * {p}\n".format(n=name, e=email, p=phone))

def parse_row(row_soup):
    td = row_soup.find_all("td")
    name = td[0].text
    email = td[1].find("span").text
    phone = td[2].text

    if email == "":
        email = "NA"

    if phone == "":
        phone = "NA"

    return (name, email, phone)


def search_for_f_l(first, last):
    prefix = "https://people.nasa.gov/people/search?email="
    fn_query_string = "&firstName="
    ln_query_string = "&lastName="

    result = set()
    for f in first:
        for l in last:
            url = prefix + ln_query_string + l + fn_query_string + f
            sys.stdout.write('Gathering data for [{}][{}]: '.format(f,l))
            sys.stdout.flush()

            fname = 'data/'+l+'/last-'+l+'_first-'+f+'_query.html'
            if os.path.isfile(fname):
                sys.stdout.write(' [pre-downloaded]: ')
                sys.stdout.flush()
                with open(fname, 'r') as filename:
                    html = filename.read()
            else:
                sys.stdout.write(' [downloading]: ')
                sys.stdout.flush()
                html = urlopen(url).read()
                if not os.path.exists('data/'+l):
                    os.makedirs('data/'+l)
                with open(fname, 'w') as filename:
                    filename.write(html)

            soup = BeautifulSoup(html, "lxml")

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
letter_count = 26
for a in range(letter_count):
    search1.append(chr(97 + a))
    for b in range(letter_count):
        search2.append(chr(97 + a) + chr(97 + b))

print "search1 count: {}".format(len(search1))
print "search2 count: {}".format(len(search2))

search = []
search.extend(search1)
search.extend(search2)


# TODO, make the search1 a list of ['a', 'b', ... 'aa', 'ab', ... 'aaa', ]
#  up to 4 letters and make that my total list (this search will take ~5 days
# >>> 26**4/60.0/60/24 = 5.289074074074073 days (assuming 1 second per query)
#  -- 456976 combinations
# >>> 26**5/60.0/60/24 = 137.51592592592593 days (assuming 1 second per query)
# -- 11881376 combinations
print 'Searching for names using {} combinations'.format(len(search))
results = search_for_f_l(search, search)
print 'Total results for first, last (from queries): {}'.format(len(results))
save_data('results_all.csv', results)
