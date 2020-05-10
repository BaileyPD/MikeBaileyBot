import json
import pandas as pd

file = open('Covid_Georgia.json')
f = json.load(file)

print(type(f[4]['New_Tests']))

frameTest = pd.DataFrame(f)

frameTest = frameTest.replace(',','', regex=True)

#frameTest.to_csv('Covid_Georgia.csv')

allData = frameTest[:39]

allData[allData.columns[1:7]] = allData[allData.columns[1:7]].apply(pd.to_numeric)
allData['Date'] = allData['Date'].apply(pd.to_datetime)

allDataRev = allData.iloc[::-1]
print(allDataRev.head())
allDataRev.to_csv('Covid_Georgia.csv', index = False)