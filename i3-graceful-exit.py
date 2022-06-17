#!/bin/python

import subprocess
import sys
import time
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from Xlib import display, X

def closeAllWindowsGracefully():
    subprocess.run(["sh", "-c", "\"echo \"$(xdotool search \"\" | while IFS= read -r line ; do wmctrl -ci \"$line\"; done)\"\""])

def exitI3():
    subprocess.run(["i3-msg", "exit"])

def getOpenWindows():
    d = display.Display()
    root = d.screen().root

    query = root.query_tree()

    ret = []
    for c in query.children:
        name = c.get_wm_name()
        if name:
            print(name)
            if (name.startswith("[i3 con]") or name == "i3-graceful-exit"):
                continue
            ret.append(name)
    return ret

class WaitingDialog(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.text = QtWidgets.QLabel(self)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText("Force Quit")
        self.cancelBtn = QtWidgets.QPushButton(self)
        self.cancelBtn.setText("Cancel")
        container = QtWidgets.QWidget(self)
        container.setLayout(QtWidgets.QHBoxLayout())
        container.layout().addWidget(self.btn)
        container.layout().addWidget(self.cancelBtn)
        self.layout().addWidget(self.text)
        self.layout().addWidget(container)
        self.btn.clicked.connect(self.onPressSkip)
        self.cancelBtn.clicked.connect(self.onPressCancel)
        self.onTimer()

    def setWaitingWindows(self, wnds):
        self.text.setText("Waiting for " + str(wnds) + " to close")
    
    def onTimer(self):
        value = getOpenWindows()
        if len(value) == 0:
            self.doExit = True
            QtCore.QCoreApplication.instance().quit()
        self.setWaitingWindows(value)
        QtCore.QTimer.singleShot(250, self.onTimer)

    def onPressSkip(self):
        self.doExit = True
        QtCore.QCoreApplication.instance().quit()

    def onPressCancel(self):
        QtCore.QCoreApplication.instance().quit()

    doExit = False

def main():
    closeAllWindowsGracefully()
    time.sleep(1)
    app = QtWidgets.QApplication(sys.argv)
    window = WaitingDialog()
    window.show()
    app.exec()
    if window.doExit == True:
        exitI3()

main()