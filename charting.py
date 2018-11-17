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
bigFrame = Frame()
bigFrame.grid()

for r in range(6):
    master.rowconfigure(r, weight=1)
for c in range(3):
    master.columnconfigure(c, weight=1)

FrameLeft = Frame(bigFrame, bg="red")
FrameLeft.grid(row = 0, column = 0, rowspan = 6, columnspan = 3, sticky = W+N+S)

a = f.add_subplot(111)
a.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])

a.set_title(instrementData["name"])
a.set_xlabel("epoch")
a.set_ylabel("price")

dataPlot = FigureCanvasTkAgg(f, master=master)
dataPlot.draw()

e = Entry(master)

e.grid(row=0,column=0,sticky=N)
variable = StringVar(master)


names = []
for i in range(1, 10):
    names.append(backend.getInstrumentById(i)["company_name"])

names.sort()
variable.set(names[0]) # default value

w = OptionMenu(master, variable, *names)
w.grid(row=1,column=0,sticky=N)


s = Scale(master, tickinterval=25, orient=HORIZONTAL)
s.grid(row=5,column=0,sticky=N+W)


listbox = Listbox(master)
listbox.grid(row=2,colomn=1,sticky=W)

b = Button(master, text='Add', command=lambda: listbox.insert(END, variable.get()))
b.grid(row=0,column=1,sticky=N)
dataPlot.get_tk_widget().grid(row=1,column=3,sticky=S+E+N)

master.mainloop()
