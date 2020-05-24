import RequestClean as rc

#Creates Request object
req = rc.Request('https://covidtracking.com/data/state/georgia')


req.requestData() # Requests data from site

req.cleanData() # Cleans Data and stores in Dataframe in object

req.displayToday() # Displays graph


#req.updateDatasetCSV("Covid_Georgia.csv")
#print(req.data.tail())

