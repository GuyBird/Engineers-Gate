import matplotlib
import backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

matplotlib.use('TkAgg')
master = Tk()
master.title("Engineers Gate Hire Us")

instrumentID = 2
timeframe = 500
instrementData = backend.getMarketData(instrumentID, timeframe)

f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
a.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])
#a.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])

a.set_title(instrementData["name"])
a.set_xlabel("epoch")
a.set_ylabel("price")

dataPlot = FigureCanvasTkAgg(f, master=master)
dataPlot.draw()

e = Entry(master)
e.pack()
variable = StringVar(master)

names = []
for i in range(1, 10):
    names.append(backend.getInstrumentById(i)["company_name"])

names.sort()
variable.set(names[0]) # default value

w = OptionMenu(master, variable, *names)
w.pack()

listbox = Listbox(master)
listbox.pack()

b = Button(master, text='Add', command=lambda: listbox.insert(END, variable.get()))
b.pack(side='bottom')

dataPlot.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

master.mainloop()
