import requests, json
from bs4 import BeautifulSoup

URL = 'https://covidtracking.com/data/state/georgia'

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='main')

table = results.find('tbody', class_='state-history-table')
trs = []

trs = table.find_all('tr')

rows = []

for tr in trs:
    row = []
    for td in tr.find_all('td'):
        row.append(td.text)

    x = {
        "Date": row[0],
        "New_Tests": row[2],
        "Positive": row[3],
        "Negative": row[4],
        "Hospitalized": row[6],
        "Deaths": row[7],
        "Total": row[8],
    }

    rows.append(x)

with open('Covid_Georgia.json', 'w') as outfile:
    json.dump(rows, outfile)