
from datetime import datetime
from time import sleep
from PySide import QtGui, QtCore
from os import sys, path
sys.path.append(path.join(path.dirname(path.dirname(path.abspath(__file__))), "common"))
from common_functionality import *

cfg = read_config()


class GuiPart(QtGui.QWidget):
    """
    Defines the GUI.
    """
    def __init__(self):
        super(GuiPart, self).__init__()
        self.paused = False
        self.thread = ThreadedClient(self)
        self.thread.current_time.connect(self.update_gui)
        self.thread.start()
        self.background_qtcolor = QtGui.QColor()
        # python 2 does not support get item for configparser, use get instead
        self.background_qtcolor.setNamedColor(cfg.get('colors', 'background'))
        self.main_layout = QtGui.QGridLayout()
        p = self.palette()
        p.setColor(self.backgroundRole(), self.background_qtcolor)
        self.setPalette(p)
        self.day_bar = QtGui.QProgressBar(self)
        self.day_box = QtGui.QLabel(self)
        self.pause_button = QtGui.QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause)
        self.quit_button = QtGui.QPushButton("Quit", self)
        self.quit_button.clicked.connect(self.quit_click)
        program_label = QtGui.QLabel(self)
        self.main_layout.addWidget(program_label, 0, 0, 1, 1)
        self.main_layout.addWidget(self.day_box, 1, 0, 1, 1)
        self.main_layout.addWidget(self.day_bar, 0, 1, 2, 1)
        self.main_layout.addWidget(self.pause_button, 2, 0, 1, 1)
        self.main_layout.addWidget(self.quit_button, 2, 1, 1, 1)
        day_barp = self.day_bar.palette()
        day_barp.setColor(self.day_bar.backgroundRole(),
         self.background_qtcolor)
        self.day_bar.setPalette(day_barp)
        self.day_bar.setOrientation(QtCore.Qt.Vertical)
        self.day_bar.setMaximum(100)
        self.day_bar.setFormat("%v")
        self.setLayout(self.main_layout)
        self.setWindowTitle('Day Monitor')
        self.showFullScreen()
        self.show()

    def pause(self):
        self.paused = not self.paused

    def quit_click(self):
        self.thread.quit()
        self.close()

    @QtCore.Slot(datetime)
    def update_gui(self, current_datetime):
        percent_elapsed_value = percent_elapsed(current_datetime)
        self.day_bar.setValue(percent_elapsed_value)
        self.day_box.setText(str(percent_elapsed_value))


class ThreadedClient(QtCore.QThread):
    """
    Handles the repeated calls to the datetime.
    """
    current_time = QtCore.Signal(datetime)

    def __init__(self, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.parent = parent

    def run(self):
        while True:
            if not self.parent.paused:
                self.current_time.emit(datetime.now())
            sleep(1)


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    testing_gui = GuiPart()

    sys.exit(app.exec_())