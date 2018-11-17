import matplotlib

import backend
import matplotlib.pyplot as plt
import tkinter;
matplotlib.use('TkAgg')
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import *

master = Tk()
master.title("Engineers Gate Hire Us")
#-------------------------------------------------------------------------------
instrumentID = 2
timeframe = 500
instrementData = backend.getMarketData(instrumentID, timeframe)
print(instrementData["name"])
#
# plt.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])
#
# plt.show()
f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
t = arange(0.0,3.0,0.01)
s = sin(2*pi*t)
a.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])

# a.title(instrementData["name"])
# a.xlabel("epoch")
# a.ylabel("price")

dataPlot = FigureCanvasTkAgg(f, master=master)
dataPlot.draw()
dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
#-------------------------------------------------------------------------------
master.mainloop()

