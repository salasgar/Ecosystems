import Tkinter as tk
import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure


class SubWindow:

    def minimize_window_size(self):
        minimized_width = 100
        minimized_height = 25
        self.frame.place_configure(x=self.minimized_x,
                                   y=self.minimized_y,
                                   width=self.minimized_width,
                                   height=self.minimized_height)
        self.is_minimized = True

    def restore_window_size(self):
        self.frame.place_configure(x=self.x, y=self.y,
                                   width=self.width, height=self.height)
        self.is_minimized = False

    def cursor_is_in_border(self, x_root, y_root):
        border_tol = 3  # Border tolerance
        frame_xleft = self.frame.winfo_rootx()
        frame_xright = self.frame.winfo_rootx() + self.frame.winfo_width()
        frame_ytop = self.frame.winfo_rooty()
        frame_ybottom = self.frame.winfo_rooty() + self.frame.winfo_height()
        in_xleft = abs(x_root - frame_xleft) <= border_tol
        in_xmiddle = (frame_xleft + border_tol <
                      x_root <
                      frame_xright - border_tol)
        in_xright = abs(x_root - frame_xright) <= border_tol
        in_ytop = abs(y_root - frame_ytop) <= border_tol
        in_ymiddle = (frame_ytop + border_tol <
                      y_root <
                      frame_ybottom - border_tol)
        in_ybottom = abs(y_root - frame_ybottom) <= border_tol
        direction = ''
        if in_xleft and in_ytop:
            direction = ''  # top_left_corner'
        if in_xleft and in_ymiddle:
            direction = ''  # left_side'
        if in_xleft and in_ybottom:
            direction = ''  # 'bottom_left_corner'
        if in_xmiddle and in_ytop:
            direction = ''  # 'top_side'
        if in_xmiddle and in_ybottom:
            direction = ''  # 'bottom_side'
        if in_xright and in_ytop:
            direction = ''  # 'top_right_corner'
        if in_xright and in_ymiddle:
            direction = ''  # 'right_side'
        if in_xright and in_ybottom:
            direction = 'bottom_right_corner'
        return direction

    def start_resizing(self, x_root, y_root):
        self.flag_resizing = self.cursor_is_in_border(x_root, y_root)
        self.move_lastx = x_root
        self.move_lasty = y_root

    def stop_resizing(self):
        self.flag_resizing = ""

    def is_resizing(self):
        return self.flag_resizing != ""

    def resize_window(self, x_root, y_root):
        self.root.update_idletasks()
        dx = x_root - self.move_lastx
        dy = y_root - self.move_lasty
        self.move_lastx = x_root
        self.move_lasty = y_root
        if self.flag_resizing == 'bottom_right_corner':
            limits_width = [50, self.root.winfo_width() - self.x]
            limits_height = [50, self.root.winfo_height() - self.y]
            self.width = min(max(self.width + dx, limits_width[0]),
                             limits_width[1])
            self.height = min(max(self.height + dy, limits_height[0]),
                              limits_height[1])
            self.frame.place_configure(width=self.width, height=self.height)

    def start_moving(self, x_root, y_root):
        self.flag_moving = True
        self.move_lastx = x_root
        self.move_lasty = y_root

    def stop_moving(self):
        self.flag_moving = False

    def is_moving(self):
        return self.flag_moving

    def move_window(self, x_root, y_root):
        self.root.update_idletasks()
        dx = x_root - self.move_lastx
        dy = y_root - self.move_lasty
        self.move_lastx = x_root
        self.move_lasty = y_root
        limits_x = [0, self.root.winfo_width()-self.width]
        limits_y = [0, self.root.winfo_height()-self.height]
        self.x = min(max(self.x + dx, limits_x[0]), limits_x[1])
        self.y = min(max(self.y + dy, limits_y[0]), limits_y[1])
        self.frame.place_configure(x=self.x, y=self.y)

    def __init__(self, main_window, title, x, y, width, height):
        self.all = []
        self.widgets = []
        self.main_window = main_window
        self.root = main_window.get_root()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.title = title

        # Creates the subwindow (self.frame)
        self.frame = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.frame.place(x=x, y=y, width=self.width, height=self.height)
        self.label = tk.Label(
            self.frame, bd=1, bg="#08246b", fg="white", text=title)
        self.label.pack(fill=tk.BOTH)  # TODO: Everything with place?
        # Creates a matplotlib within the frame
        self.matplotlib_fig = Figure()
        self.matplotlib_axes = self.matplotlib_fig.add_subplot(
            111, aspect='auto')
        #plt, = a.plot(time, stat1)
        self.canvas = FigureCanvasTkAgg(self.matplotlib_fig,
                                        master=self.frame)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.widgets.append(self.frame)
        self.widgets.append(self.label)
        self.widgets.append(self.canvas.get_tk_widget())

        self.minimized_x = -1  # To be assigned by root
        self.minimized_y = -1
        self.minimized_width = -1
        self.minimized_height = -1

        self.flag_moving = False
        self.flag_resizing = ''
        self.has_focus = True
        self.is_minimized = False
        self.main_window.focus(self)


class MainWindow:

    def update_minimized_positions(self):
        minimized_width = 100
        minimized_height = 25
        starting_x = 25
        x_gap = 150
        starting_y = self.root.winfo_height() - minimized_height
        for i, subwindow in enumerate(self.subwindows):
            subwindow.minimized_y = starting_y
            subwindow.minimized_x = starting_x + i * x_gap
            subwindow.minimized_width = minimized_width
            subwindow.minimized_height = minimized_height

    def focus(self, subwindow_to_be_focused):
        for subwindow in self.subwindows:
            if subwindow_to_be_focused is subwindow:
                subwindow.frame.tkraise()
                subwindow.label.configure(bg="#08246b", fg="white")
                subwindow.has_focus = True
            else:
                subwindow.label.configure(bg="#d9d9d9", fg="black")
                subwindow.has_focus = False

    def callback_mouse_double_button(self, event):
        for subwindow in self.subwindows:
            if event.widget is subwindow.label:
                if subwindow.is_minimized:
                    self.focus(subwindow)
                    subwindow.restore_window_size()
                else:
                    self.focus(subwindow)
                    subwindow.minimize_window_size()

    def callback_mouse_pressed_button(self, event):
        for subwindow in self.subwindows:
            if not subwindow.is_minimized:
                # If click in any widget of a subwindow get focus
                if event.widget in subwindow.widgets:
                    self.focus(subwindow)
                # If click in the label of a subwindow, start moving
                if event.widget is subwindow.label:
                    subwindow.start_moving(event.x_root, event.y_root)
                if subwindow.has_focus:
                    cursor_is_in_border = subwindow.cursor_is_in_border(
                        event.x_root, event.y_root)
                    if cursor_is_in_border != "":
                        subwindow.start_resizing(event.x_root,
                                                 event.y_root)

    def callback_mouse_released_button(self, event):
        for subwindow in self.subwindows:
            subwindow.stop_moving()
            subwindow.stop_resizing()

    def callback_motion(self, event):
        for subwindow in self.subwindows:
            # If a subwindow is moving, move it
            if subwindow.is_moving():
                subwindow.move_window(event.x_root, event.y_root)
            elif subwindow.is_resizing():
                subwindow.resize_window(event.x_root, event.y_root)
            elif subwindow.has_focus:
                cursor_is_in_border = subwindow.cursor_is_in_border(
                    event.x_root, event.y_root)
                self.root.config(cursor=cursor_is_in_border)
                self.root.update()

    def add_subwindow(self, title, x, y, width, height):
        aux_subwindow = SubWindow(self, title, x, y, width, height)
        self.subwindows.append(aux_subwindow)

    def get_root(self):
        return self.root

    def __init__(self):
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.geometry("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight() - 50))
        self.root.title("...")
        self.root.bind('<Motion>',
                       self.callback_motion)
        self.root.bind('<Button>',
                       self.callback_mouse_pressed_button)
        self.root.bind('<Double-Button>',
                       self.callback_mouse_double_button)
        self.root.bind('<ButtonRelease>',
                       self.callback_mouse_released_button)
        self.subwindows = []

if __name__ == "__main__":
    main_window = MainWindow()
    main_window.add_subwindow("Window1", 10, 10, 200, 200)
    main_window.add_subwindow("Window2", 100, 100, 200, 200)
    main_window.update_minimized_positions()
    main_window.get_root().mainloop()
