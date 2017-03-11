from bs4 import BeautifulSoup
import lxml
from urllib.request import urlopen

prefix = "https://people.nasa.gov/people/search?email="
fn_query_string = "&firstName="
ln_query_string = "&lastName="

def parse_row(row_soup):
    td = row_soup.find_all("td")
    name = td[0].text
    email = td[1].find("span").text
    phone = td[2].text

    if email == "":
        email = "NA"

    if phone == "":
        phone = "NA"

    return "* ".join([name, email, phone])

def parse_soup(soup):
    header = "name * email * phone"

    even = soup.find("tr", {"class" : "even"})
    row = even

    rows = ""

    while row:
        rows += parse_row(row) + "\n"
        row = row.find_next_sibling()

    return rows

# takes first letter of first name
def subdivideA(ln_fl):
    for i in range(26):
        ln_query = ln_fl + chr(97+i)
        url = prefix + ln_query_string + ln_query
        file_name = ln_query[0] + ".csv"

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        # check for result overflow
        if soup.find("div", {"class" : "warning"}):
            subdivideB(ln_query)
            continue

        # check for empty results page
        evens = soup.find("tr", {"class" : "even"})
        if evens:
            file = open(file_name, "a")
            file.write(parse_soup(soup))
            file.close()

# takes two-letter first name query
def subdivideB(ln_query):
    for i in range(26):
        fn_query = chr(97  + i)
        url = prefix + ln_query_string + ln_query + fn_query_string + fn_query
        file_name = ln_query[0] + ".csv"

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        # check for result overflow
        if soup.find("div", {"class" : "warning"}):
            subdivideC(fn_query, ln_query)
            continue

        # check for empty results page
        evens = soup.find("tr", {"class" : "even"})
        if evens:
            file = open(file_name, "a")
            file.write(parse_soup(soup))
            file.close()


def subdivideC(fn_query, ln_query):
    for i in range(26):
        fn_query = fn_query + chr(97  + i)
        url = prefix + ln_query_string + ln_query + fn_query_string + fn_query
        file_name = ln_query[0] + ".csv"

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        # check for result overflow
        if soup.find("div", {"class" : "warning"}):
            subdivideD(fn_query, ln_query)
            continue

        # check for empty results page
        evens = soup.find("tr", {"class" : "even"})
        if evens:
            file = open(file_name, "a")
            file.write(parse_soup(soup))
            file.close()


def subdivideD(fn_query, ln_query):
    for i in range(26):
        ln_query = ln_query + chr(97  + i)
        url = prefix + ln_query_string + ln_query + fn_query_string + fn_query
        file_name = ln_query[0] + ".csv"

        html = urlopen(url).read()
        soup = BeautifulSoup(html, "lxml")

        # check for result overflow
        if soup.find("div", {"class" : "warning"}):
            subdivideB(ln_query)
            continue

        # check for empty results page
        evens = soup.find("tr", {"class" : "even"})
        if evens:
            file = open(file_name, "a")
            file.write(parse_soup(soup))
            file.close()

from sys import argv, exit

start = 0
end = 0

if len(argv) == 3:
    if int(argv[1]) > int(argv[2]) or int(argv[1]) < 0 or int(argv[2]) > 26:
        exit()
    start = int(argv[1])
    end = 26 - int(argv[2])


for i in range(0+start,26-end):
    ln_query = chr(97+i)
    url = prefix + ln_query_string + ln_query
    file_name = ln_query + ".csv"

    html = urlopen(url).read()
    soup = BeautifulSoup(html, "lxml")

    # check for result overflow
    if soup.find("div", {"class" : "warning"}):
        subdivideA(ln_query)
        continue

    # check for empty results page
    evens = soup.find("tr", {"class" : "even"})
    if evens:
        file = open(file_name, "w")
        file.write(parse_soup(soup))
        file.close()
