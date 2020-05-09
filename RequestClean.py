import requests, json
import pandas as pd
from bs4 import BeautifulSoup
class Request:
    URL = ""
    soup = ""
    table = ""
    rows = []
    data = pd.DataFrame()

    def __init__(self, URL):
        self.URL = URL
        page = requests.get(URL)
        self.soup = BeautifulSoup(page.content, 'html.parser')



    def requestData(self):
        page = requests.get(self.URL)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        results = self.soup.find(id='main')
        self.table = results.find('tbody', class_='state-history-table')
        self.cleanData()

    def __organizeData(self):
        trs = self.table.find_all('tr')
        holder = []
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

            holder.append(x)
        self.rows = holder

    def cleanData(self):
        self.__organizeData()
        tempFrame = pd.DataFrame(self.rows)

        tempFrame = tempFrame.replace(',', '', regex=True)

        tempFrame = tempFrame[tempFrame.Hospitalized != "N/A"]

        tempFrame[tempFrame.columns[1:7]] = tempFrame[tempFrame.columns[1:7]].apply(pd.to_numeric)
        tempFrame['Date'] = tempFrame['Date'].apply(pd.to_datetime)

        tempFrame = tempFrame.iloc[::-1]

        self.data = tempFrame


    def changeURL(self, newURL):
        self.URL = newURL


    def displayToday(self):
        return


    def updateDatasetCSV(self, filePath):
        newDataHolder = []
        data = pd.read_csv(filePath)
        lastDate = data[-1]





