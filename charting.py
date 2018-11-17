import backend
import matplotlib.pyplot as plt
import numpy as np

instrementData = backend.get()
print(instrementData["name"])


plt.plot(list(range((instrementData["current epoch"]) + 1 - len(instrementData["data"]), instrementData["current epoch"] + 1)), instrementData["data"])

plt.title(instrementData["name"])
plt.xlabel("epoch")
plt.ylabel("price")
plt.show()
