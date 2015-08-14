import Tkinter as tk
import numpy as np
import ttk
import pickle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
# from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import flufl.lock

lock = flufl.lock.Lock('./map.lock')  # JUST FOR DEBUG


class GenericObserver(object):

    def __init__(self, subject, title, x, y, width, height):
        self.widgets = []
        self.subject = subject
        self.root = subject.get_root()
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.title = title
        self.minimized_x = -1  # To be assigned by root
        self.minimized_y = -1
        self.minimized_width = -1
        self.minimized_height = -1
        self.flag_moving = False
        self.direction_resizing = ''
        self.has_focus = True
        self.is_minimized = False
        # Creates the observer (self.frame)
        self.frame = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.frame.place(x=x, y=y, width=self.width, height=self.height)

        # Create the window bar
        self.label = tk.Label(
            self.frame, bd=1, bg="#08246b", fg="white", text=title)
        self.button_close = tk.Button(self.frame, text="X", justify=tk.CENTER)
        self.button_minmaximize = tk.Button(self.frame, text="-")

        self.widgets.append(self.frame)
        self.widgets.append(self.label)
        self.widgets.append(self.button_close)
        self.widgets.append(self.button_minmaximize)

    def update_widgets_positions(self):
        # Label position
        self.label.place(x=0, y=0, width=self.width, height=20)
        # Buttons position
        self.button_close.place(x=1, y=1,
                                width=30, height=18)
        self.button_minmaximize.place(x=32, y=1,
                                      width=30, height=18)

    def minimize_window(self):
        """
            Minimize window
        """
        self.frame.place_configure(x=self.minimized_x,
                                   y=self.minimized_y,
                                   width=self.minimized_width,
                                   height=self.minimized_height)
        self.is_minimized = True
        self.label.place_configure(width=self.minimized_width)
        self.button_minmaximize.config(text="+")

    def restore_window_size(self):
        """
            Restore window
        """
        self.frame.place_configure(x=self.x, y=self.y,
                                   width=self.width, height=self.height)
        self.label.place_configure(width=self.width)
        self.is_minimized = False
        self.button_minmaximize.config(text="-")

    def cursor_is_in_border(self, x_root, y_root):
        """
            Return direction of resizing if cursor is in border of
            the observer. Otherwise, returns ''
        """
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
        """
            Start resizing mode (i.e. self.direction_resizing != "")
        """
        self.direction_resizing = self.cursor_is_in_border(x_root, y_root)
        self.move_lastx = x_root
        self.move_lasty = y_root

    def stop_resizing(self):
        """
            Stop resizing mode (i.e. self.direction_resizing = "")
        """
        self.direction_resizing = ""

    def is_resizing(self):
        """
            True is in resizing mode
        """
        return self.direction_resizing != ""

    def resize_window(self, x_root, y_root):
        """
            Resize observer (called while moving mouse)
        """
        self.root.update_idletasks()
        dx = x_root - self.move_lastx
        dy = y_root - self.move_lasty
        self.move_lastx = x_root
        self.move_lasty = y_root
        if self.direction_resizing == 'bottom_right_corner':
            limits_width = [50, self.root.winfo_width() - self.x]
            limits_height = [50, self.root.winfo_height() - self.y]
            self.width = min(max(self.width + dx, limits_width[0]),
                             limits_width[1])
            self.height = min(max(self.height + dy, limits_height[0]),
                              limits_height[1])
            self.frame.place_configure(width=self.width, height=self.height)
        self.update_widgets_positions()

    def start_moving(self, x_root, y_root):
        """
            Start moving observer mode
        """
        self.flag_moving = True
        self.move_lastx = x_root
        self.move_lasty = y_root

    def stop_moving(self):
        """
            Stops moving observer mode
        """
        self.flag_moving = False

    def is_moving(self):
        """
            True if in moving observer mode
        """
        return self.flag_moving

    def move_window(self, x_root, y_root):
        """
            Move observer (called while moving mouse)
        """
        self.root.update_idletasks()
        dx = x_root - self.move_lastx
        dy = y_root - self.move_lasty
        self.move_lastx = x_root
        self.move_lasty = y_root
        limits_x = [0, self.root.winfo_width() - self.width]
        limits_y = [0, self.root.winfo_height() - self.height]
        self.x = min(max(self.x + dx, limits_x[0]), limits_x[1])
        self.y = min(max(self.y + dy, limits_y[0]), limits_y[1])
        self.frame.place_configure(x=self.x, y=self.y)


class NavigationObserver(GenericObserver):

    def __init__(self, subject, title, x, y,
                 width, height, commands_file_path):
        """
            Initialize a histogram observer
        """
        super(NavigationObserver, self).__init__(
            subject, title, x, y, width, height)

        # Creates 'Play' button
        self.play_button = tk.Button(self.frame, text="Play",
                                     command=self.callback_play)

        # Creates 'Pause' button
        self.pause_button = tk.Button(self.frame, text="Pause",
                                      command=self.callback_pause)

        self.widgets.append(self.play_button)
        self.widgets.append(self.pause_button)

        # Update widgets_positions
        self.update_widgets_positions()

        # Focus current observer
        self.subject.focus(observer_to_be_focused=self)

        # Commands file lock
        self.commands_file_path = commands_file_path
        self.commands_lock = flufl.lock.Lock(self.commands_file_path +
                                             '.lock')

    def update_widgets_positions(self):
        """
            Update all widgets positions according to new width and height
        """
        super(NavigationObserver, self).update_widgets_positions()

        # Buttons
        self.play_button.place(x=0, y=50, width=100, height=25)
        self.pause_button.place(x=self.width - 120, y=50, width=100, height=25)

    def callback_play(self):
        # TODO: Implement Play
        self.commands_lock.lock()
        with open(self.commands_file_path, 'w') as f:
            f.write('PLAY')  # JUST FOR DEBUG
        self.commands_lock.unlock()

    def callback_pause(self):
        # TODO: Implement Pause
        self.commands_lock.lock()
        with open(self.commands_file_path, 'w') as f:
            f.write('PAUSE')  # JUST FOR DEBUG
        self.commands_lock.unlock()


class MapObserver(GenericObserver):

    def __init__(self, subject, title, x, y, width, height):
        """
            Initialize a histogram observer
        """
        super(MapObserver, self).__init__(
            subject, title, x, y, width, height)

        # Creates a matplotlib
        self.matplotlib_fig = Figure()
        self.matplotlib_axes = self.matplotlib_fig.add_subplot(
            111, aspect='auto')
        self.matplotlib_fig.set_tight_layout(True)
        self.image = self.matplotlib_axes.imshow(np.zeros((1, 1)),
                                                 interpolation='None',
                                                 aspect='auto',
                                                 extent=[0, 1, 0, 1],
                                                 origin='lower')
        # plt, = self.matplotlib_axes.plot([], [])
        self.canvas = FigureCanvasTkAgg(self.matplotlib_fig,
                                        master=self.frame)
        self.canvas._tkcanvas.config(highlightthickness=0)
        self.canvas.mpl_connect('button_press_event',
                                self.callback_start_selection)
        self.canvas.mpl_connect('motion_notify_event',
                                self.callback_resize_selection)
        self.canvas.mpl_connect('button_release_event',
                                self.callback_end_selection)
        self.is_selecting = False
        self.selection_rect = None
        self.zoom_observer = None
        self.canvas.show()

        # Creates a button
        self.button1 = tk.Button(self.frame, text="Hola",
                                 command=self.update_map)

        # Add widgets to the list of widgets
        self.widgets.append(self.canvas.get_tk_widget())
        self.widgets.append(self.button1)

        # Update widgets_positions
        self.update_widgets_positions()

        # Focus current observer
        self.subject.focus(observer_to_be_focused=self)

    def update_widgets_positions(self):
        """
            Update all widgets positions according to new width and height
        """
        super(MapObserver, self).update_widgets_positions()

        # Matplotlib position
        self.canvas.get_tk_widget().place(
            x=3, y=25,
            width=self.width * 0.66, height=self.height * 0.66)
        self.matplotlib_axes.tick_params(labelsize=10)
        # Buttons
        self.button1.place(x=self.width - 120, y=50, width=100, height=25)

    def update_map(self):
        lock.lock()
        RGB_matrix = pickle.load(open("map.p", "rb"))  # JUST FOR DEBUG
        lock.unlock()
        self.image.set_data(RGB_matrix)
        self.image.set_extent([0, RGB_matrix.shape[0],
                               0, RGB_matrix.shape[1]])
        self.image.autoscale()
        self.canvas.draw()
        if self.zoom_observer is not None:
            self.zoom_observer.update_map(RGB_matrix)

    def erase_selection(self):
        if type(self.selection_rect) == Rectangle:
            self.selection_rect.remove()
            self.selection_rect = None

    def callback_start_selection(self, e):
        if e.xdata is None or e.ydata is None:
            # Discard if mouse is outside axes
            return
        if e.button == 1:
            self.is_selecting = True
            self.erase_selection()
            self.selection_rect = Rectangle((e.xdata, e.ydata), 0, 0,
                                            linewidth=2, fill=None,
                                            ec='white')
            self.matplotlib_axes.add_patch(self.selection_rect)
            self.selection_x0 = e.xdata
            self.selection_y0 = e.ydata
            self.selection_width = 0
            self.selection_height = 0

    def callback_resize_selection(self, e):
        if e.xdata is None or e.ydata is None:
            # Discard if mouse is outside axes
            return
        if self.is_selecting:
            self.selection_width = e.xdata - self.selection_x0
            self.selection_height = e.ydata - self.selection_y0
            self.selection_rect.set_width(self.selection_width)
            self.selection_rect.set_height(self.selection_height)

    def callback_end_selection(self, e):
        if self.is_selecting:
            self.is_selecting = False
            if self.zoom_observer is None:
                self.zoom_observer = self.subject.add_zoom_observer(
                    title='Zoom' + self.title,
                    x=self.x + 200,  # TODO: Think about a better position
                    width=self.width,
                    y=self.y + 200,
                    height=self.height,
                    parent_mapobserver=self)


class ZoomMapObserver(GenericObserver):

    def __init__(self, subject, title, x, y, width, height,
                 parent_mapobserver):
        """
            Initialize a histogram observer
        """
        self.parent_mapobserver = parent_mapobserver
        super(ZoomMapObserver, self).__init__(
            subject, title, x, y, width, height)

        # Creates a matplotlib
        self.matplotlib_fig = Figure()
        self.matplotlib_axes = self.matplotlib_fig.add_subplot(
            111, aspect='auto')
        # self.matplotlib_axes.axis('off')
        self.matplotlib_fig.subplots_adjust(left=0.1,
                                            bottom=0.1,
                                            right=0.9,
                                            top=0.9)
        self.image = self.matplotlib_axes.imshow(np.zeros((1, 1)),
                                                 interpolation='None',
                                                 aspect='auto',
                                                 extent=[0, .5, 0, .5],
                                                 origin='lower')
        # plt, = self.matplotlib_axes.plot([], [])
        self.canvas = FigureCanvasTkAgg(self.matplotlib_fig,
                                        master=self.frame)
        self.canvas._tkcanvas.config(highlightthickness=0)
        self.canvas.show()

        # Add widgets to the list of widgets
        self.widgets.append(self.canvas.get_tk_widget())

        # Update widgets_positions
        self.update_widgets_positions()

        # Focus current observer
        self.subject.focus(observer_to_be_focused=self)

    def update_widgets_positions(self):
        """
            Update all widgets positions according to new width and height
        """
        super(ZoomMapObserver, self).update_widgets_positions()
        label_height = 20  # TODO: Get from actual label
        # Matplotlib position
        self.canvas.get_tk_widget().place(
            x=3, y=3 + label_height,
            width=self.width - 6, height=self.height - label_height - 6)
        # self.matplotlib_axes.tick_params(labelsize=10)

    def update_map(self, RGB_matrix):
        zoom_x0 = self.parent_mapobserver.selection_x0
        zoom_y0 = self.parent_mapobserver.selection_y0
        zoom_width = self.parent_mapobserver.selection_width
        zoom_height = self.parent_mapobserver.selection_height
        start_x = round(min(zoom_x0, zoom_x0 + zoom_width))
        end_x = round(max(zoom_x0, zoom_x0 + zoom_width))
        start_y = round(min(zoom_y0, zoom_y0 + zoom_height))
        end_y = round(max(zoom_y0, zoom_y0 + zoom_height))
        if (end_x > start_x + 1) and (end_y > start_y + 1):
            zoom_RGB_matrix = RGB_matrix[start_y:end_y,
                                         start_x:end_x,
                                         :]
            # zoom_RGB_matrix is organized in row-columns, which
            # correspond to y-x axis.
            self.image.set_data(zoom_RGB_matrix)
            self.image.set_extent([start_x, end_x,
                                   start_y, end_y])
        else:
            zoom_RGB_matrix = np.zeros((1, 1))
            self.image.set_data(zoom_RGB_matrix)
            self.image.set_extent([0, 1,
                                   0, 1])

        self.image.autoscale()
        self.canvas.draw()


class HistogramObserver(GenericObserver):

    def __init__(self, subject, title, x, y, width, height):
        """
            Initialize a histogram observer
        """
        super(HistogramObserver, self).__init__(
            subject, title, x, y, width, height)

        # Creates a matplotlib
        self.matplotlib_fig = Figure()
        self.matplotlib_axes = self.matplotlib_fig.add_subplot(
            111, aspect='auto')
        self.matplotlib_fig.set_tight_layout(True)
        # plt, = self.matplotlib_axes.plot([], [])
        self.canvas = FigureCanvasTkAgg(self.matplotlib_fig,
                                        master=self.frame)
        self.canvas._tkcanvas.config(highlightthickness=0)
        self.canvas.show()

        # SET OF WIDGETS:
        # Creates a button
        self.button1 = tk.Button(self.frame, text="Hola")
        # Creates two combobox
        self.combo1 = ttk.Combobox(self.frame, values=('value1', 'value2'))
        self.scale1 = tk.Scale(
            self.frame, from_=0, to=10000,
            orient=tk.HORIZONTAL, command=self.callback_scale1)

        # Add widgets to the list of widgets
        self.widgets.append(self.canvas.get_tk_widget())
        self.widgets.append(self.button1)
        self.widgets.append(self.scale1)
        self.widgets.append(self.combo1)

        # Update widgets_positions
        self.update_widgets_positions()

        # Focus current observer
        self.subject.focus(observer_to_be_focused=self)

    def update_widgets_positions(self):
        """
            Update all widgets positions according to new width and height
        """
        super(HistogramObserver, self).update_widgets_positions()

        # Matplotlib position
        self.canvas.get_tk_widget().place(
            x=3, y=25,
            width=self.width * 0.66, height=self.height * 0.66)
        self.matplotlib_axes.tick_params(labelsize=10)
        # Buttons
        self.button1.place(x=self.width - 120, y=50, width=100, height=25)
        # Combobox
        self.combo1.place(x=self.width - 120, y=80, width=100, height=25)
        # Scale
        self.scale1.place(x=10, y=self.height - 50, width=300, height=40)

    # LOCAL CALLBACKS:

    def callback_scale1(self, value):
        self.subject.callback_scale1(self, value)


class Subject:

    def __init__(self):
        """
            Creates the Tk main window of our application
        """
        # Initialize Tk
        self.root = tk.Tk()
        self.root.resizable(0, 0)
        self.root.geometry("{0}x{1}+0+0".format(
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight() - 50))
        self.root.title("Ecosystems")
        self.observers = []
        # Bind motion, mouse_pressed and mouse_released generic events
        self.root.bind('<Motion>',
                       self.callback_motion)
        self.root.bind('<Button>',
                       self.callback_mouse_pressed_button)
        self.root.bind('<ButtonRelease>',
                       self.callback_mouse_released_button)
        # Initialize menu
        self.create_menu()

        # Start timer
        time_interval = 100  # TODO: Set as input parameter
        self.timer_update_data(time_interval)

    def create_menu(self):
        """
            Creates the menu of the application
        """
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)
        self.fileMenu = tk.Menu(self.menubar)
        self.submenu = tk.Menu(self.fileMenu)
        self.submenu.add_command(
            label="Opcion 1",
            command=lambda: self.callback_menu_command(option='Option1'))
        self.submenu.add_command(
            label="Opcion 2",
            command=lambda: self.callback_menu_command(option='Option2'))
        self.submenu.add_command(
            label="Opcion 3",
            command=lambda: self.callback_menu_command(option='Option3'))
        self.fileMenu.add_cascade(
            label='Import', menu=self.submenu,
            underline=0)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(
            label="Exit", underline=0,
            command=lambda: self.callback_menu_command(option='Exit'))
        self.menubar.add_cascade(label="File", underline=0,
                                 menu=self.fileMenu)

    def update_minimized_positions(self):
        """
            Update the positions for each minimized window, depending
            on the amount of windows
        """
        minimized_width = 200
        minimized_height = 25
        starting_x = 25
        x_gap = 250
        starting_y = self.root.winfo_height() - minimized_height
        for i, observer in enumerate(self.observers):
            observer.minimized_y = starting_y
            observer.minimized_x = starting_x + i * x_gap
            observer.minimized_width = minimized_width
            observer.minimized_height = minimized_height

    def focus(self, observer_to_be_focused):
        """
            Focus observer_to_be_focused
        """
        for observer in self.observers:
            if observer_to_be_focused is observer:
                observer.frame.tkraise()
                observer.label.configure(bg="#08246b", fg="white")
                observer.has_focus = True
            else:
                observer.label.configure(bg="#d9d9d9", fg="black")
                observer.has_focus = False

    def add_zoom_observer(self, title, x, y, width, height,
                          parent_mapobserver):
        zoom_observer = ZoomMapObserver(self, title, x, y,
                                        width, height, parent_mapobserver)
        self.observers.append(zoom_observer)
        self.update_minimized_positions()
        return zoom_observer

    def add_observer(self, title, x, y, width, height):
        """
            Add a observer to the main window
        """
        #aux_observer = MapObserver(self, title, x, y, width, height)
        aux_observer = NavigationObserver(self, title, x, y, width, height, '../ecosystem.commands')
        self.observers.append(aux_observer)
        self.update_minimized_positions()

    def get_root(self):
        """
            Get root reference
        """
        return self.root

    # TIMER FUNCTIONS
    def timer_update_data(self, time_interval):
        for observer in self.observers:
            if type(observer) == MapObserver:
                observer.update_map()
        self.root.after(time_interval, self.timer_update_data, time_interval)

    # CALLBACKS

    def callback_menu_command(self, option):
        """
            Callback to manage menu options
        """
        for observer in self.observers:
            observer.button1.config(text=option)

    def callback_scale1(self, parent_observer, value):
        """
            Callback to manage scale1 movement
        """
        for observer in self.observers:
            observer.scale1.set(value)

    def callback_mouse_pressed_button(self, event):
        """
            Generic callback for mouse pressed event
        """

        for observer in self.observers:
            # If click in any widget of a observer get focus
            if event.widget in observer.widgets:
                self.focus(observer)
            # If click in the label of a observer, start moving
            if event.widget is observer.label:
                observer.start_moving(event.x_root, event.y_root)
            if observer.has_focus:
                cursor_is_in_border = observer.cursor_is_in_border(
                    event.x_root, event.y_root)
                if cursor_is_in_border != "":
                    observer.start_resizing(event.x_root,
                                            event.y_root)
            if event.widget is observer.button_close:
                if type(observer) == ZoomMapObserver:
                    # If a ZoomMapObserver is closed,
                    # deselect zoom region from parent.
                    observer.parent_mapobserver.erase_selection()
                    observer.parent_mapobserver.zoom_observer = None
                if type(observer) == MapObserver:
                    # If a MapObserver is closed and it has a ZoomMapObserver,
                    # close it as well.
                    if observer.zoom_observer is not None:
                        observer.zoom_observer.frame.destroy()
                        self.observers.remove(observer.zoom_observer)
                observer.frame.destroy()
                self.observers.remove(observer)
            if event.widget is observer.button_minmaximize:
                if observer.is_minimized:
                    self.focus(observer)
                    observer.restore_window_size()
                else:
                    self.focus(observer)
                    observer.minimize_window()

    def callback_mouse_released_button(self, event):
        """
            Generic callback for mouse relased event
        """

        for observer in self.observers:
            observer.stop_moving()
            observer.stop_resizing()

    def callback_motion(self, event):
        """
            Generic callback for mouse motion event
        """

        for observer in self.observers:
            # If a observer is moving, move it
            if not observer.is_minimized:
                if observer.is_moving():
                    observer.move_window(event.x_root, event.y_root)
                elif observer.is_resizing():
                    observer.resize_window(event.x_root, event.y_root)
                elif observer.has_focus:
                    cursor_is_in_border = observer.cursor_is_in_border(
                        event.x_root, event.y_root)
                    self.root.config(cursor=cursor_is_in_border)
                    self.root.update()


if __name__ == "__main__":
    subject = Subject()
    subject.add_observer("Observer1", 10, 10, 400, 300)
    subject.add_observer("Observer2", 100, 100, 400, 300)
    subject.get_root().mainloop()
