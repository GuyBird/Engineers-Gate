import matplotlib

import backend
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

master = Tk()
master.title("Engineers Gate Hire Us")
#-------------------------------------------------------------------------------
instrumentID = 2
timeframe = 500
instrementData = backend.getMarketData(instrumentID, timeframe)
print(instrementData["name"])

f = Figure(figsize=(5,4), dpi=100)
a = f.add_subplot(111)
a.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])

a.set_title(instrementData["name"])
a.set_xlabel("epoch")
a.set_ylabel("price")

dataPlot = FigureCanvasTkAgg(f, master=master)
dataPlot.draw()
dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
#-------------------------------------------------------------------------------
master.mainloop()

