from datetime import datetime
from sys import version_info, exit

import threading
from time import sleep

if version_info[0] < 3:
    import Tkinter as tk
else:
    import tkinter as tk

from tkinter import ttk

from os import sys, path
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "common"))
from common_functionality import *

cfg = read_config()


class GuiPart(tk.Tk, object):
    """
    Defines the GUI.
    """
    def __init__(self):
        super(GuiPart, self).__init__()
        self.attributes("-fullscreen", True)
        self.configure(background=cfg.get('colors', 'background'))
        self.thread = ThreadedClient(self)
        self.thread.start()

        s = ttk.Style()
        s.configure('TButton', background=cfg.get('colors', 'background'))
        s.configure('TButton', activebackground=cfg.get('colors', 'background'))
        s.configure('TButton', foreground=cfg.get('colors', 'text'))
        s.configure('TButton', highlightbackground=cfg.get('colors', 'background'))
        s.configure('TButton', font=(cfg.get('font', 'face'), int(cfg.get('font', 'size'))))
        s.configure('TLabel', background=cfg.get('colors', 'background'))
        s.configure('TLabel', foreground=cfg.get('colors', 'text'))
        s.configure('TLabel', highlightbackground=cfg.get('colors', 'background'))
        s.configure('TLabel', font=(cfg.get('font', 'face'), int(cfg.get('font', 'size'))))
        s.configure('Vertical.TProgressbar',  background=cfg.get('colors', 'sub_text'))
        s.configure('Vertical.TProgressbar',  troughcolor=cfg.get('colors', 'text'))
        s.configure('Vertical.TProgressbar',  highlightbackground=cfg.get('colors', 'border'))
        s.configure('Vertical.TProgressbar',  highlightthickness=int(cfg.get('layout', 'border_width')))

        self.day_bar = ttk.Progressbar(self)
        self.day_bar.grid(row=0, column=1, rowspan=2)
        self.day_label = tk.Label(self)

        self.day_label.grid(row=1, column=0)
        program_label = ttk.Label(self, text=cfg.get("variables", "main_label"))
        program_label.grid(row=0, column=0)
        self.pause_button = ttk.Button(self)
        self.pause_button.grid(row=2, column=0)
        self.quit_button = ttk.Button(self, text="Quit")
        self.quit_button.grid(row=2, column=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.day_bar.configure(orient="vertical", mode="determinate")

        self.day_bar_value = tk.IntVar()
        self.day_label_value = tk.StringVar()
        self.pause_button_label = tk.StringVar()
        self.day_bar.configure(variable=self.day_bar_value)
        self.day_label.configure(textvariable=self.day_label_value)
        self.pause_button.configure(textvariable=self.pause_button_label)

        self.pause_button.configure(command=self.pause)
        self.quit_button.configure(command=self.quit_click)
        self.paused = False
        self.pause_button_label.set("Pause")

        self.day_label.configure(background=cfg.get('colors', 'text'))
        self.day_label.configure(foreground=cfg.get('colors', 'sub_text'))
        self.day_label.configure(highlightbackground=cfg.get('colors', 'border'))
        self.day_label.configure(highlightthickness=int(cfg.get('layout', 'border_width')))
        self.day_label.configure(font=(cfg.get('font', 'face'), int(cfg.get('font', 'size'))))


    def quit_click(self):
        self.quit()

    def pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button_label.set('Unpause')
        else:
            self.pause_button_label.set('Pause')

    def update(self, current_datetime):
        percent_elapsed_value = percent_elapsed(current_datetime)
        self.day_bar_value.set(percent_elapsed_value)
        self.day_label_value.set(str(percent_elapsed_value))


class ThreadedClient(threading.Thread):
    """
    Handles the repeated calls to the datetime.
    """
    def __init__(self, parent=None):
        super(ThreadedClient, self).__init__()
        self.parent = parent

    def run(self):
        while True:
            try:
                self.parent.wm_state()
            except RuntimeError:
                break
            if not self.parent.paused:
                self.parent.update(datetime.now())
            sleep(1)

if __name__ == "__main__":
    app = GuiPart()
    app.mainloop()
