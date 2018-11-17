import requests
import json

def getCurrentEpoch():
    response = requests.get("http://egchallenge.tech/epoch")
    parsed = json.loads(response.content)
    return parsed["current_epoch"]

def getInstrumentById(instrumentID):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    instrument = [x for x in parsed if x["id"] == instrumentID]
    return instrument[0]


def getMarketData(instrumentID, historical):
    response = requests.get("http://egchallenge.tech/marketdata/instrument/" + str(instrumentID))
    parsed = json.loads(response.content)
    #Filter out the records we don't want
    if (historical != 0):
        relevant = parsed[len(parsed)-historical:]
    else:
        relevant = parsed
    #Create our own data structure
    marketData = {} #Holds the final data
    instrument = getInstrumentById(instrumentID) #Relevant information about the instrument
    marketData["name"] = instrument["company_name"]
    marketData["data"] = [x["price"] for x in relevant]
    return marketData
