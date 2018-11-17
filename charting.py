import backend
import matplotlib.pyplot as plt
# import tkinter as tk
# import matplotlib as mpl
# import matplotlib.backends.tkagg as tkagg
# from matplotlib.backends.backend_agg import FigureCanvasAgg
#
# from tkinter import *

instrementData = backend.getMarketData(2, 500)
print(instrementData["name"])


plt.plot(list(range((instrementData["currentEpoch"]) + 1 - len(instrementData["data"]), instrementData["currentEpoch"] + 1)), instrementData["data"])

plt.title(instrementData["name"])
plt.xlabel("epoch")
plt.ylabel("price")
plt.show()

# def draw_figure(canvas, figure, loc=(0, 0)):
#     """ Draw a matplotlib figure onto a Tk canvas
#
#     loc: location of top-left corner of figure on canvas in pixels.
#     Inspired by matplotlib source: lib/matplotlib/backends/backend_tkagg.py
#     """
#     figure_canvas_agg = FigureCanvasAgg(figure)
#     figure_canvas_agg.draw()
#     figure_x, figure_y, figure_w, figure_h = figure.bbox.bounds
#     figure_w, figure_h = int(figure_w), int(figure_h)
#     photo = tk.PhotoImage(master=canvas, width=figure_w, height=figure_h)
#
#     # Position: convert from top-left anchor to center anchor
#     canvas.create_image(loc[0] + figure_w/2, loc[1] + figure_h/2, image=photo)
#
#     # Unfortunately, there's no accessor for the pointer to the native renderer
#     tkagg.blit(photo, figure_canvas_agg.get_renderer()._renderer, colormode=2)
#
#     # Return a handle which contains a reference to the photo object
#     # which must be kept live or else the picture disappears
#     return photo
#
# # Create a canvas
# w, h = 600, 400
# window = tk.Tk()
# window.title("Engineers Gate Hackathon")
# canvas = tk.Canvas(window, width=w, height=h)
# canvas.pack()
#
# # Create the figure we desire to add to an existing canvas
# fig = mpl.figure.Figure(figsize=(2, 1))
# ax = fig.add_axes([0, 0, 1, 1])
# ax.plot(list(range((instrementData["current epoch"]) + 1 - len(instrementData["data"]), instrementData["current epoch"] + 1)), instrementData["data"])
# # Keep this handle alive, or else figure will disappear
# fig_x, fig_y = 100, 100
# fig_photo = draw_figure(canvas, fig, loc=(fig_x, fig_y))
# fig_w, fig_h = fig_photo.width(), fig_photo.height()
#
# # Let Tk take over
# tk.mainloop()
