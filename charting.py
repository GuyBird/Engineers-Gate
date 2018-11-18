import matplotlib
import backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *

matplotlib.use('TkAgg')
master = Tk()
master.title("Engineers Gate Hire Us")

f = Figure(figsize=(5, 4), dpi=100)
bigFrame = Frame()
bigFrame.grid()

for r in range(6):
    master.rowconfigure(r, weight=1)
for c in range(4):
    master.columnconfigure(c, weight=1)

FrameLeft = Frame(bigFrame)
FrameLeft.grid(row=0, column=0, rowspan=6, columnspan=4, sticky=W+N+S)

a = f.add_subplot(111)

plot_graph = []
time_frame = 500

a.set_xlabel("epoch")
a.set_ylabel("price")

dataPlot = FigureCanvasTkAgg(f, master=master)
dataPlot.draw()

e = Entry(master)

variable = StringVar(master)


names = []
for i in range(1, 10):
    names.append(backend.getInstrumentById(i)["company_name"])

names.sort()
variable.set(names[0])

s = Scale(bigFrame, from_=10, to=1000, resolution=10, orient=HORIZONTAL)
s.set(500)
s.grid(row=5, column=0, sticky=N)


listbox = Listbox(bigFrame)
listbox.grid(row=4, column=0, sticky=W+S)


def add_button():
    is_unique = True
    elements = listbox.get(0, listbox.size())
    for i in elements:
        if i == variable.get():
            is_unique = False
    if is_unique:
        listbox.insert(END, variable.get())
        instrumentID = backend.getInstrumentId(variable.get())
        global time_frame
        time_frame = s.get()
        instrument_data = backend.getMarketData(instrumentID, time_frame)
        global plot_graph
        plot_graph.append(a.plot(list(range((instrument_data["currentEpoch"]) + 1 - len(instrument_data["price"]), instrument_data["currentEpoch"] + 1)), instrument_data["price"]))
        dataPlot.draw()
        color = plot_graph[listbox.size() - 1][0].get_color()
        listbox.itemconfig(listbox.size() - 1, {'bg': color})
    change_time_frame()


def remove_button():
    if listbox.curselection():
        index = listbox.curselection()[0]
        listbox.delete(listbox.curselection())
        plot_graph[index].pop(0).remove()
        move_array(index)
        maxvalue = 0
        minvalue = 10000
        for i in plot_graph:
            if max(i[0].get_ydata()) > maxvalue:
                maxvalue = max(i[0].get_ydata())
            if min(i[0].get_ydata()) < minvalue:
                minvalue = min(i[0].get_ydata())
            if len(plot_graph) > 1:
                a.set_ylim(minvalue - (minvalue * 0.05), maxvalue + (maxvalue * 0.05))
            else:
                a.set_ylim(minvalue, maxvalue)
        dataPlot.draw()


def move_array(index):
    for i in range(index, len(plot_graph)):
        if i + 1 < len(plot_graph):
            plot_graph[i] = plot_graph[i + 1]

    del plot_graph[len(plot_graph) - 1]


def change_time_frame():
    global time_frame
    global plot_graph
    elements = listbox.get(0, listbox.size())
    count = 0
    for i in elements:
        plot_graph[count][0].remove()
        instrumentID = backend.getInstrumentId(i)
        time_frame = s.get()
        instrument_data = backend.getMarketData(instrumentID, time_frame)
        color = plot_graph[count][0].get_color()
        plot_graph[count] = (a.plot(list(range((instrument_data["currentEpoch"]) + 1 - len(instrument_data["price"]), instrument_data["currentEpoch"] + 1)), instrument_data["price"], color=color))
        count += 1
    a.set_xlim(instrument_data['currentEpoch'] - time_frame, instrument_data['currentEpoch'])
    maxvalue = 0
    minvalue = 10000
    for i in plot_graph:
        if max(i[0].get_ydata()) > maxvalue:
            maxvalue = max(i[0].get_ydata())
        if min(i[0].get_ydata()) < minvalue:
            minvalue = min(i[0].get_ydata())
        if len(plot_graph) > 1:
            a.set_ylim(minvalue - (minvalue * 0.05), maxvalue + (maxvalue * 0.05))
        else:
            a.set_ylim(minvalue, maxvalue)
    dataPlot.draw()


b = Button(bigFrame, text='Add', bg='#488cf9', foreground="#ffffff", command=lambda: add_button())
b.grid(row=3, column=0, sticky=N)
b1 = Button(bigFrame, text='Remove', bg='#488cf9', foreground="#ffffff", command=lambda: remove_button())
b1.grid(row=3, column=1, sticky=N)
b2 = Button(bigFrame, text='Apply', bg='#488cf9', foreground="#ffffff", command=lambda: change_time_frame())
b2.grid(row=5, column=1, sticky=S)
w = OptionMenu(bigFrame, variable, *names)

w.grid(row=2, column=0, sticky=N)
dataPlot.get_tk_widget().grid(row=0, column=4, sticky=S+E+N)

master.mainloop()


