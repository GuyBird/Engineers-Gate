import backend
import matplotlib.pyplot as plt

instrumentID = 2
timeframe = 500
instrementData = backend.getMarketData(instrumentID, timeframe)
print(instrementData["name"])

plt.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])

plt.title(instrementData["name"])
plt.xlabel("epoch")
plt.ylabel("price")
plt.show()
