import requests
import json
import numpy as np
import statsmodels.stats.weightstats as ws
import pandas as pd

industryReturnsCache = {}

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
    data = marketData["data"]
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

previousEpoch = getCurrentEpoch()

def calculateIndustryIndicesUpToEpoch(industry, epoch):
    result = [100]
    #Get all instruments id's for a given industry
    relevantInstrumentIds = [x["id"] for x in getAllInstrumentsInIndustry(industry)]
    currentEpoch = getCurrentEpoch()
    #If there is not a chaced version of the thing, build it
    if (not industry in industryReturnsCache.keys()):
        for epoch in range(1, epoch):
            epochMarketData = getMarketDataForEpoch(epoch)
            returns = [x["epoch_return"] for x in epochMarketData if x["instrument_id"] in relevantInstrumentIds]
            industryReturn = np.average(returns)
            result.append(result[-1] * (1. + industryReturn))
        industryReturnsCache[industry] = result #Add the results to the cache
    #Otherwise just append to the cached version
    else:
        result = industryReturnsCache[industry]
        if (currentEpoch != previousEpoch):
            #Loop through all epochs missed and cache their indices
            for epoch in range(previousEpoch, currentEpoch):
                epochMarketData = getMarketDataForEpoch(getCurrentEpoch())
                returns = [x["epoch_return"] for x in epochMarketData if x["instrument_id"] in relevantInstrumentIds]
                industryReturn = np.average(returns)
                result.append(result[-1] * (1. + industryReturn))
    globals()["previousEpoch"] = currentEpoch
    return result

def calculateIndustryIndices(industry):
    return calculateIndustryIndicesUpToEpoch(industry, getCurrentEpoch())

def getInstrumentId(instrumentName):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    instrument = [x for x in parsed if x["company_name"] == instrumentName]
    return instrument[0]["id"]

def simpleRollingCorrelation(instruments, historical=0, window=10):
    marketDatas = []
    #Acquire market data for every instrument
    for instrument in instruments:
        marketDatas.append(getMarketData(getInstrumentId(instrument), historical))
    #Special (and easy) case
    if (len(marketDatas) == 2):
        series1 = pd.Series(marketDatas[0]["return"])
        series2 = pd.Series(marketDatas[1]["return"])
        return list(series1.rolling(window).corr(series2))
    return [1] * historical #Dummy, until there is clarification of what the correlation of N lists is
