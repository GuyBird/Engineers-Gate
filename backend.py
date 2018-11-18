import requests
import json
import numpy as np
import statsmodels.stats.weightstats as ws
import pandas as pd

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
    parsed = json.loads(response.content)
    return parsed

#Charting indicators

def movingAverage(marketData, window):
    data = marketData["data"]
    result = []
    for i in range(0, len(data)):
        result.append(np.average(data[0 if i-window < 0 else i-window : i+1]))
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

def industryIndex(industry, endEpoch):
    pass

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
