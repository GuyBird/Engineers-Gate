import requests
import json

def getData(instrumentID, historical):
    response = requests.get("http://egchallenge.tech/marketdata/instrument/" + str(instrumentID))
    # print(response.url)
    parsed = json.loads(response.content)
    relevant = parsed[len(parsed)-historical:]
    return relevant
