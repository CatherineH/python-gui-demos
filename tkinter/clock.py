from configparser import ConfigParser
from datetime import datetime
from sys import version_info, exit

import threading
from time import sleep

if version_info[0] < 3:
    import Queue as qu
    import Tkinter as tk
else:
    import queue as qu
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
        self.day_bar_value = tk.IntVar()
        self.day_bar = ttk.Progressbar(self, variable=self.day_bar_value,
                                       orient="vertical",
                                       mode="determinate")
        self.day_bar.grid(row=0, column=1, rowspan=2)
        self.day_box_value = tk.StringVar()
        self.day_box = tk.Label(self, textvariable=self.day_box_value)
        self.day_box.grid(row=1, column=0)
        program_label = tk.Label(self, text=cfg.get("variables", "main_label"))
        program_label.grid(row=0, column=0)
        self.pause_button_label = tk.StringVar()
        self.pause_button_label.set("Pause")
        self.pause_button = tk.Button(self, textvariable=self.pause_button_label,
                                      command=self.pause)
        self.pause_button.grid(row=2, column=0)
        self.paused = False
        self.quit_button = tk.Button(self, text="Quit", command=self.quit_click)
        self.quit_button.grid(row=2, column=1)

    def quit_click(self):
        self.quit()

    def pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button_label.set('Unpause')
        else:
            self.pause_button_label.set('Pause')

    def update_gui(self, current_datetime):
        percent_elapsed_value = percent_elapsed(current_datetime)
        self.day_bar_value.set(percent_elapsed_value)
        self.day_box_value.set(str(percent_elapsed_value))


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
                self.parent.update_gui(datetime.now())
            sleep(1)

if __name__ == "__main__":
    app = GuiPart()
    app.mainloop()
