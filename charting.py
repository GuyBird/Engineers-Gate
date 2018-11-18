import matplotlib
import backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import *
from tkinter import ttk

matplotlib.use('TkAgg')
master = Tk()

style = ttk.Style()
style.configure("BW.TLabel", background="white")


master.title("Engineers Gate Hire Us")
tabs = ttk.Notebook(master, style="BW.TLabel")
master.configure(background='white')

tab1 = ttk.Frame(tabs)
tab2 = ttk.Frame(tabs)
tab3 = ttk.Frame(tabs)


f = Figure(figsize=(5, 4), dpi=100)
bigFrame = Frame(tab1, bg='white')
bigFrame.grid()
bigFrame2 = Frame(tab2, bg='white')
bigFrame2.grid()

tabs.add(tab1, text="Prices", compound=TOP)
tabs.add(tab2, text="Indicators")
tabs.add(tab3, text="To be implemented")
tabs.grid()

for r in range(6):
    master.rowconfigure(r, weight=1,)
for c in range(4):
    master.columnconfigure(c, weight=1)

FrameLeft = Frame(bigFrame)
FrameLeft.grid(row=0, column=0, rowspan=6, columnspan=4, sticky=W+N+S)

FrameLeft2 = Frame(bigFrame2)
FrameLeft2.grid(row=0, column=0, rowspan=6, columnspan=4, sticky=W+N+S)

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

s = Scale(bigFrame, from_=10, to=1000, resolution=10, activebackground="#40913F", highlightcolor='#40913F', orient=HORIZONTAL, bg='white', bd=0, highlightbackground='white')
s.set(500)
s.grid(row=5, column=0, sticky=N)


listbox = Listbox(bigFrame, width=50)
listbox.grid(row=4, column=0, sticky=W+S, columnspan = 2)


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


def select_button():
    count = 0
    for index in range(0, len(plot_graph) - 1):
        del plot_graph[index]
        count += 1
    listbox.delete(0, END)
    dataPlot.draw()
    add_button()


def moving_avg_button():
    if 'selected' in b211.state():
        index = backend.getInstrumentId(variable.get())
        market_data = backend.getMarketData(index, time_frame)
        simple_moving_avg = backend.movingAverage(market_data, time_frame)
        plot_graph.append(a.plot(list(range((market_data["currentEpoch"]) + 1 - len(simple_moving_avg), market_data["currentEpoch"] + 1)), simple_moving_avg))
    else:
        plot_graph[1].pop(0).remove()
    dataPlot.draw()


def expo_moving_avg_button():
    if 'selected' in b212.state():
        index = backend.getInstrumentId(variable.get())
        market_data = backend.getMarketData(index, time_frame)
        expo_moving_avg = backend.expMovingAverage(market_data, 1)
        plot_graph.append(a.plot(list(range((market_data["currentEpoch"]) + 1 - len(expo_moving_avg), market_data["currentEpoch"] + 1)), expo_moving_avg))
    else:
        plot_graph[2].pop(0).remove()
    dataPlot.draw()


def moving_standard_deviation_button():
    if 'selected' in b221.state():
        index = backend.getInstrumentId(variable.get())
        market_data = backend.getMarketData(index, time_frame)
        expo_moving_avg = backend.movingStdDev(market_data, 1)
        print(expo_moving_avg)
        plot_graph.append(a.plot(list(range((market_data["currentEpoch"]) + 1 - len(expo_moving_avg), market_data["currentEpoch"] + 1)), expo_moving_avg))
        a.set_ylim(0, 30)
    else:
        plot_graph[3].pop(0).remove()
    dataPlot.draw()


def expo_standard_deviation_button():
    if 'selected' in b222.state():
        index = backend.getInstrumentId(variable.get())
        market_data = backend.getMarketData(index, time_frame)
        expo_moving_avg = backend.expMovingStdDev(market_data, 1)
        plot_graph.append(a.plot(list(range((market_data["currentEpoch"]) + 1 - len(expo_moving_avg), market_data["currentEpoch"] + 1)), expo_moving_avg))
        a.set_ylim(0, 10)
    else:
        plot_graph[4].pop(0).remove()
    dataPlot.draw()



def autocorrelation_button():
    if 'selected' in b231.state():
        index = backend.getInstrumentId(variable.get())
        market_data = backend.getMarketData(index, time_frame)
        expo_moving_avg = backend.rangeAutocorrelation(market_data, 10)
        print(expo_moving_avg)
        a.set_ylim(-1, 1)
        a.set_xlim(4321, 4334)
        plot_graph.append(a.plot(list(range((market_data["currentEpoch"]) + 1 - len(expo_moving_avg), market_data["currentEpoch"] + 1)), expo_moving_avg))
    else:
        plot_graph[5].pop(0).remove()
    dataPlot.draw()


def chart_industry_indexes():
    return 1


b = Button(bigFrame, text='Add', bg='#00a86b', foreground="#ffffff", command=lambda: add_button())

b.grid(row=3, column=0, sticky=N)
b1 = Button(bigFrame, text='Remove', bg='#00a86b', foreground="#ffffff", command=lambda: remove_button())
b1.grid(row=3, column=1, sticky=N)
b2 = Button(bigFrame, text='Apply', bg='#00a86b', foreground="#ffffff", command=lambda: change_time_frame())
b2.grid(row=5, column=1, sticky=S)
w = OptionMenu(bigFrame, variable, *names)
w.config(width=40)
w.grid(row=2, column=0, sticky=N, columnspan=2)
dataPlot.get_tk_widget().grid(row=0, column=4, sticky=S+E+N)

w2 = OptionMenu(bigFrame2, variable, *names)
w2.config(width=30)
w2.grid(row=2, column=0, sticky=N)

b21 = Button(bigFrame2, text='Select', bg='#00a86b', foreground="#ffffff", command=lambda: select_button())
b21.grid(row=2, column=1, sticky=N)

b211 = ttk.Checkbutton(bigFrame2, text='Simlpe Moving Avg.', command=lambda: moving_avg_button())
b211.grid(row=3, column=0, sticky=E)

b212 = ttk.Checkbutton(bigFrame2, text='ExponentialMoving Avg.', command=lambda: expo_moving_avg_button())
b212.grid(row=3, column=1, sticky=E)

b221 = ttk.Checkbutton(bigFrame2, text='Moving standard deviation', command=lambda: moving_standard_deviation_button())
b221.grid(row=4, column=0, sticky=E)

b222 = ttk.Checkbutton(bigFrame2, text='Expo. weighted standard deviation', command=lambda: expo_standard_deviation_button())
b222.grid(row=4, column=1, sticky=E)

b231 = ttk.Checkbutton(bigFrame2, text='Autocorrelation', command=lambda: autocorrelation_button())
b231.grid(row=5, column=0, sticky=E)

b232 = ttk.Checkbutton(bigFrame2, text='chart industry indexes', command=lambda: chart_industry_indexes())
b232.grid(row=5, column=1, sticky=E)

master.mainloop()


