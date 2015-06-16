from Tkinter import *
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure

def clamp(lo, hi, x):
    return min(max(x, lo), hi)

class blah:
    all = []

    def Motion(self, event):
        border_tol = 20
        if 0 <= event.y <= self.l.winfo_height():
            self.labelselected = True
        else:
            self.labelselected = False
        if ((self.width - border_tol <= event.x < self.width + border_tol) and
           (self.height - border_tol <= event.y < self.height + border_tol)):
            self.root.config(cursor='bottom_right_corner')
            self.root.update()
            self.borderselected = True
        else:
            self.borderselected = False
            self.root.config(cursor="")
            self.root.update()

    def LeaveWindow(self, event):
        self.root.config(cursor="")
        self.root.update()
        pass

    def MoveWindowStart(self, event):
        self.move_lastx = event.x_root
        self.move_lasty = event.y_root
        self.focus()

    def MoveWindow(self, event):
        self.root.update_idletasks()
        dx = event.x_root - self.move_lastx
        dy = event.y_root - self.move_lasty
        self.move_lastx = event.x_root
        self.move_lasty = event.y_root
        if not self.borderselected and self.labelselected:
            self.x = clamp(0, self.root.winfo_width()-self.width, self.x + dx) # should depend on
            self.y = clamp(0, self.root.winfo_height()-self.height, self.y + dy) # actual size here
            self.f.place_configure(x=self.x, y=self.y, width=self.width, height=self.height)
        elif self.borderselected:
            self.width = self.width + dx
            self.height = self.height + dy
            self.f.place_configure(x=self.x, y=self.y, width=self.width, height=self.height)


    def __init__(self, root, title, x, y):
        self.root = root
        self.width = 300
        self.height = 300
        self.x = x; self.y = y
        self.f = Frame(self.root, bd=1, relief=RAISED)
        self.f.place(x=x, y=y, width=self.width, height=self.height)

        self.l = Label(self.f, bd=1, bg="#08246b", fg="white",text=title)
        self.l.pack(fill=BOTH)
        print self.l.winfo_height()

        # Initialize plot
        time = []
        stat1 = []
        stat2 = []
        fig = Figure()
        a = fig.add_subplot(111, aspect='auto')
        #plt, = a.plot(time, stat1)

        # a tk.DrawingArea
        subframe = Frame(self.f)
        subframe.pack(side=BOTTOM, fill=X)

        #subFrame = Frame(self.f, bg="#000000")
        canvas = FigureCanvasTkAgg(fig, master=self.f)
        canvas.show()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand = 1)
        b1 = Button(subframe, text='Hola')
        b1.pack(side=RIGHT, fill=BOTH)
        c = ttk.Combobox(subframe, values=('ge','gr'))
        c.pack(side=BOTTOM)
        c = ttk.Combobox(subframe, values=('ge','gr'))
        c.pack(side=BOTTOM)
        #subFrame.pack(side=TOP, fill=BOTH, expand=1)


        #toolbar = NavigationToolbar2TkAgg(canvas, self.f)
        #toolbar.update()
        #canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=0)

        self.f.bind('<1>', self.MoveWindowStart)
        self.l.bind('<1>', self.MoveWindowStart)
        subframe.bind('<1>', self.MoveWindowStart)
        self.f.bind('<B1-Motion>', self.MoveWindow)
        self.l.bind('<B1-Motion>', self.MoveWindow)
        subframe.bind('<B1-Motion>', self.MoveWindow)
        self.f.bind('<Motion>', self.Motion)
        self.l.bind('<Motion>', self.Motion)
        subframe.bind('<Motion>', self.Motion)
        self.f.bind('<Leave>', self.LeaveWindow)
        #fig.canvas.mpl_connect('motion_notify_event', self.Motion)
        self.borderselected = False
        self.labelselected = False
        # self.f.bind('<B1-Motion>', self.MoveWindow)
        self.all.append(self)


        self.focus()

    def focus(self, event=None):
        self.f.tkraise()
        for w in self.all:
            if w is self:
                w.l.configure(bg="#08246b", fg="white")
            else:
                w.l.configure(bg="#d9d9d9", fg="black")

root = Tk()
root.title("...")
#root.resizable(0,0)
root.geometry("%dx%d%+d%+d"%(1100, 700, 0, 0))
x = blah(root, "Window 1", 10, 10)
y = blah(root, "Window 2", 220, 10)
y = blah(root, "Window 3", 10, 220)
root.mainloop()