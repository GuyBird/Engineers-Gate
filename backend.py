import requests
import json
import numpy as np
import statsmodels.stats.weightstats as ws

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
    marketData["price"] = [x["price"] for x in relevant]
    marketData["return"] = [x["epoch_return"] for x in relevant]
    marketData["currentEpoch"] = getCurrentEpoch()
    return marketData

def simpleMovingAverage(marketData, window):
    data = marketData["price"]
    result = []
    for i in range(0, len(data)):
        result.append(np.average(data[0 if i-window < 0 else i-window : i+1]))
    return result

def exponentialMovingAverage(marketData, window):
    data = marketData["data"]
    weights = np.exp(np.linspace(-1., 0., window-1))
    weights /= weights.sum()
    result = np.convolve(data, weights)[:len(data)]
    result[:window-1] = result[window-1]
    return list(result)

def movingStdDev(marketData, window):
    data = marketData["data"]
    result = []
    for i in range(0, len(data)):
        result.append(np.std(data[0 if i - window < 0 else i - window: i + 1]))
    return result

def expMovingStdDev(marketData, window):
    data = marketData["data"]
    results = []
    for j in range(len(data)):
        weights = np.ones((j+1 if j-window < 0 else window+1))
        for i in range(len(weights)):
            weights[i] = np.exp(len(weights)-i)
        d = ws.DescrStatsW(data[0 if j-window < 0 else j-window : j+1], weights=weights)
        if (len(d.var.shape) != 0):
            results.append(d.var[0])
        else:
            results.append(d.var)
    return results

def returnAutocorrelation(marketData, lag):
    returns = marketData["return"]
    return np.correlate(returns[:-lag], returns[lag:], 'valid')[0]

def rangeReturnAutocorrelation(marketData, maxLag=1):
    result = []
    for lag in range(1, maxLag+1):
        result.append(returnAutocorrelation(marketData, lag))
    return result

def getAllInstrumentsInIndustry(industry):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    result = [x for x in parsed if x["industry"] == industry]
    return result

def getMarketDataForEpoch(epoch):
    response = requests.get("http://egchallenge.tech/marketdata/epoch/" + str(epoch))
    parsed = json.loads(response.content)
    return parsed

def calculateIndustryIndices(industry):
    result = [100]
    for epoch in range(1, getCurrentEpoch()):
        epochMarketData = getMarketDataForEpoch(epoch)
        returns = [x["epoch_return"] for x in epochMarketData]
        industryReturn = np.average(returns)
        result.append(result[-1] * industryReturn)
    return result

def getInstrumentId(instrumentName):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    instrument = [x for x in parsed if x["company_name"] == instrumentName]
    return instrument[0]["id"]
