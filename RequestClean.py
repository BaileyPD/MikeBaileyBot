import requests, json
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
class Request:
    CSVPath = ""
    URL = ""
    soup = ""
    table = ""
    rows = []
    data = pd.DataFrame()

    def __init__(self, URL):
        """
        Only used when the object is created. Requests the entire page contents in HTML.
        :param URL:
        """
        self.URL = URL
        page = requests.get(URL)
        self.soup = BeautifulSoup(page.content, 'html.parser')



    def requestData(self):
        """
        Requests page content. Finds table of data. Utilizes cleanData function.
        """
        page = requests.get(self.URL)
        self.soup = BeautifulSoup(page.content, 'html.parser')
        results = self.soup.find(id='main')
        self.table = results.find('tbody', class_='state-history-table')
        self.cleanData()

    def __organizeData(self):
        """
        Private method used in cleanData function to restructure data and organize it in a list of dictionaries
        """
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
        """
        Cleans data and outputs it into internal Pandas Dataframe
        """
        self.__organizeData()
        tempFrame = pd.DataFrame(self.rows)

        tempFrame = tempFrame.replace(',', '', regex=True)

        tempFrame = tempFrame[tempFrame.Hospitalized != "N/A"]

        tempFrame[tempFrame.columns[1:7]] = tempFrame[tempFrame.columns[1:7]].apply(pd.to_numeric)
        tempFrame['Date'] = tempFrame['Date'].apply(pd.to_datetime)

        tempFrame = tempFrame.iloc[::-1]

        self.data = tempFrame





    def displayToday(self):
        """
        For creating a basic plot through functions. Work in progress
        """
        dates = self.data['Date']

        fig, ax = plt.subplots()
        ax.plot(dates, self.data['Positive'])
        ax.plot(dates, self.data['Hospitalized'])
        ax.plot(dates, self.data['Deaths'])

        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m-%d"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%m-%d"))
        _ = plt.xticks(rotation=45)
        ax.legend(['Positive', 'Hospitalized', 'Deaths'])
        fig.show()

        # plt.plot(self.data['Date'], self.data['Positive'])
        # plt.plot(self.data['Date'], self.data['Hospitalized'])
        # plt.plot(self.data['Date'], self.data['Deaths'])
        # plt.format_xdata()
        # plt.xticks(rotation=45)
        # plt.legend(['Positive', 'Hospitalized', 'Deaths'])
        # plt.show()
        # print(self.data.info())


    def updateDatasetCSV(self, filePath):
        """
        Finds last listed day of data retrieval in CSV and will append new data to the end.
        :param filePath:
        """
        data = pd.read_csv(filePath)
        lastDate = data['Date'].iloc[-1]

        newData = self.data.loc[self.data['Date'] > lastDate]
        # print(self.data.loc[self.data['Date'] > lastDate])

        newData.to_csv(filePath, mode='a', header=False, index=False)

    def changeURL(self, newURL):
        """
        :param newURL: For changing Request objects internal URL variable
        """
        self.URL = newURL

    def changeCSVFilepath(self, newPath):
        self.CSVPath = newPath


    def dataToCSV(self,fileName):
        self.data.to_csv(fileName, index = False)



