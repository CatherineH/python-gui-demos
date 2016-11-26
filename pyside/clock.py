
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
        self.setStyleSheet("QWidget { "
                           "background-color: \""+cfg.get('colors', 'background')+"\";"
                           "font-family:"+cfg.get('font', 'face')+"; "
                           "font-size: "+cfg.get('font', 'size')+"pt;"
                           "color: \""+cfg.get('colors', 'text')+"\";"
                           "}")


        self.thread = ThreadedClient(self)

        self.thread.start()

        self.main_layout = QtGui.QGridLayout()
        self.day_bar = QtGui.QProgressBar(self)
        self.day_label = QtGui.QLabel(self)
        self.pause_button = QtGui.QPushButton("Pause", self)
        self.quit_button = QtGui.QPushButton("Quit", self)
        program_label = QtGui.QLabel(cfg.get("variables", "main_label"), self)
        self.main_layout.addWidget(program_label, 0, 0, 1, 1)
        self.main_layout.addWidget(self.day_label, 1, 0, 1, 1)
        self.main_layout.addWidget(self.day_bar, 0, 1, 2, 1)
        self.main_layout.addWidget(self.pause_button, 2, 0, 1, 1)
        self.main_layout.addWidget(self.quit_button, 2, 1, 1, 1)
        self.setLayout(self.main_layout)
        self.day_bar.setOrientation(QtCore.Qt.Vertical)
        self.day_bar.setMaximum(100)
        self.day_bar.setFormat("")
        self.thread.current_time.connect(self.update)
        self.quit_button.clicked.connect(self.quit_click)
        self.pause_button.clicked.connect(self.pause)

        self.day_label.setStyleSheet("QLabel { "
                           "background-color: \""+cfg.get('colors', 'text')+"\";"
                           "color: \""+cfg.get('colors', 'sub_text')+"\";"
                           "border: "+cfg.get('layout', 'border_width')+"px solid \""+cfg.get('colors', 'border')+"\";"
                           "}")
        self.day_bar.setStyleSheet("QProgressBar{ "
                                   "background-color: \""+cfg.get('colors', 'text')+"\";"
                                   "border: "+cfg.get('layout', 'border_width')+"px solid \""+cfg.get('colors', 'border')+"\";"
                                   " } "
                                   "QProgressBar::chunk {    "
                                   " background-color: \""+cfg.get('colors', 'sub_text')+"\";} ")


        self.setWindowTitle('Day Monitor')
        self.showFullScreen()
        self.show()

    def pause(self):
        self.paused = not self.paused
        if self.paused:
            self.pause_button.setText("Unpause")
        else:
            self.pause_button.setText("Pause")

    def quit_click(self):
        self.thread.quit()
        self.close()

    @QtCore.Slot(datetime)
    def update(self, current_datetime):
        percent_elapsed_value = percent_elapsed(current_datetime)
        self.day_bar.setValue(percent_elapsed_value)
        self.day_label.setText(str(percent_elapsed_value))


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