import requests
import json
import numpy as np
import statsmodels.stats.weightstats as ws
import pandas as pd

#Cache objects
industryIndices = None
prevEpoch = 0

#Data acquisition/Helper methods

def getCurrentEpoch():
    response = requests.get("http://egchallenge.tech/epoch")
    parsed = json.loads(response.content)
    return parsed["current_epoch"]

def getInstrumentById(instrumentID):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    instrument = [x for x in parsed if x["id"] == instrumentID]
    return instrument[0]

def getInstrumentId(instrumentName):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    instrument = [x for x in parsed if x["company_name"] == instrumentName]
    return instrument[0]["id"]

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

def instrumentsInIndustry(industry):
    response = requests.get("http://egchallenge.tech/instruments")
    parsed = json.loads(response.content)
    result = [x for x in parsed if x["industry"] == industry]
    return result

def epochMarketData(epoch):
    response = requests.get("http://egchallenge.tech/marketdata/epoch/" + str(epoch))
    return pd.DataFrame(response.json())

def getIndustries():
    response = requests.get("http://egchallenge.tech/instruments")
    return pd.DataFrame(response.json())["industry"]


#Charting indicators

def movingAverage(marketData, window):
    price = marketData["price"]
    result = []
    for i in range(0, len(price)):
        result.append(np.average(price[0 if i-window < 0 else i-window : i+1]))
    return result

def expMovingAverage(marketData, halflife):
    price = marketData["price"]
    print(price)
    df = pd.DataFrame({'price' : price})
    return list(df.ewm(halflife=halflife).mean()["price"])

def movingStdDev(marketData, window):
    price = marketData["price"]
    df = pd.DataFrame({'price' : price})
    return list(df.rolling(window).std()["price"])

def expMovingStdDev(marketData, halfLife):
    price = marketData["price"]
    df = pd.DataFrame({'price' : price})
    return list(df.ewm(halfLife).std()['price'])

def autocorrelation(marketData, lag=1):
    returns = marketData["return"]
    s = pd.Series(returns)
    return s.autocorr(lag)

def rangeAutocorrelation(marketData, maxLag=1):
    result = []
    for lag in range(1, maxLag+1):
        result.append(autocorrelation(marketData, lag))
    return result

def industryIndex():
    currentEpoch = getCurrentEpoch()
    if (globals()["prevEpoch"] != currentEpoch):
        r = {}
        currentEpoch = getCurrentEpoch()
        for i in range(currentEpoch):
            r[i] = epochMarketData(i)["epoch_return"]
        r = pd.DataFrame(r)
        r["industry"] = getIndustries()
        epochMean = r.groupby(by="industry").mean()
        industryIndex = pd.DataFrame(epochMean.index).set_index("industry")
        industryIndex[0] = 100
        for c in epochMean.columns:
            industryIndex[c] = (epochMean[c] + 1) * industryIndex[c-1]
        globals()["industryIndices"] = industryIndex # put the thing into the cache
        globals()["prevEpoch"] = currentEpoch
        return industryIndex
    else:
        return industryIndices


def rollingCorrelation(instruments, historical=0, window=10):
    #TODO Make this calculate the correlation between N instruments, not just 2
    marketDatas = []
    #Acquire market data for every instrument
    for instrument in instruments:
        marketDatas.append(getMarketData(getInstrumentId(instrument), historical))
    #Special (and easy) case
    series1 = pd.Series(marketDatas[0]["return"])
    series2 = pd.Series(marketDatas[1]["return"])
    return list(series1.rolling(window).corr(series2))

def expRollingCorrelation(instruments, historical=0, halflife=1):
    #TODO Make this calculate the correlation between N instruments, not just 2
    marketDatas = []
    #Acquire market data for every instrument supplied
    for instrument in instruments:
        marketDatas.append(getMarketData(getInstrumentId(instrument), historical))
    series1 = pd.Series(marketDatas[0]["return"])
    series2 = pd.Series(marketDatas[1]["return"])
    return list(series1.ewm(halflife).corr(series2))

