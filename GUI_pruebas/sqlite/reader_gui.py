import sys
import matplotlib
matplotlib.use('TkAgg')
import ttk
import sqlite3
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from time import sleep

if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

# Connect to database (file example.db)
conn = sqlite3.connect('example.db', isolation_level=None)
c = conn.cursor()
root = Tk.Tk()
root.wm_title("Embedding in TK")

# Initialize plot
time = []
stat1 = []
stat2 = []
f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
plt, = a.plot(time, stat1)


# a tk.DrawingArea
canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

toolbar = NavigationToolbar2TkAgg(canvas, root)
toolbar.update()
canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


def _update():
    time = []
    stat1 = []
    stat2 = []

    # MySQL query:
    c.execute("SELECT time, stat1, stat2 FROM statistics")
    for entry in c.fetchall():
        time.append(entry[0])
        stat1.append(entry[1])
        stat2.append(entry[2])

    plt.set_xdata(time)
    if combobox.get() == 'stat1':
        plt.set_ydata(stat1)
    elif combobox.get() == 'stat2':
        plt.set_ydata(stat2)

    # recompute the ax.dataLim
    a.relim()
    # update ax.viewLim using the new dataLim
    a.autoscale_view()
    # f.draw()
    canvas.draw()


def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

# Add button:
button = Tk.Button(master=root, text='Quit', command=_quit)
button.pack(side=Tk.BOTTOM)  # Send to the bottom of the window

# Add combobox:
combobox = ttk.Combobox(master=root, values=('stat1', 'stat2'))
combobox.set('stat1')
combobox.pack(side=Tk.BOTTOM)

# Add timer (every 50ms it calls _update)
timer = f.canvas.new_timer(interval=50)
timer.add_callback(_update)
timer.start()

# Start Tk loop!
Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager
