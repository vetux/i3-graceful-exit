#!/bin/python

import subprocess
import sys
import time
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
from Xlib import display, protocol, X

def closeAllWindowsGracefully():
    subprocess.run(["sh", "-c", "\"echo \"$(xdotool search \"\" | while IFS= read -r line ; do wmctrl -ci \"$line\"; done)\"\""])
    return
    d = display.Display()
    root = d.screen().root
    query = root.query_tree()
    for c in query.children:
        name = c.get_wm_name()
        WM_PROTOCOLS = d.intern_atom('WM_PROTOCOLS')
        WM_DELETE_WINDOW = d.intern_atom('WM_DELETE_WINDOW')
        if name:
            if (name.startswith("[i3 con]") or name == "i3-shutdown"):
                continue
        ev = protocol.event.ClientMessage(window=c, 
                                            client_type=WM_PROTOCOLS, 
                                            data=(32, [WM_DELETE_WINDOW, X.CurrentTime, 0, 0, 0]))
        # Does not send anything for some reason.
        c.send_event(ev)

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
            if (name.startswith("[i3 con]") or name == "i3-shutdown"):
                continue
            ret.append(name)
    return ret

class WaitingDialog(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.text = QtWidgets.QLabel(self)
        self.text.setAlignment(QtCore.Qt.AlignCenter)
        self.text.setWordWrap(True)
        self.btn = QtWidgets.QPushButton(self)
        self.btn.setText("Force Quit")
        self.cancelBtn = QtWidgets.QPushButton(self)
        self.cancelBtn.setText("Cancel")
        self.layout().setSpacing(10)
        container = QtWidgets.QWidget(self)
        container.setLayout(QtWidgets.QHBoxLayout())
        container.layout().addWidget(QtWidgets.QWidget(), 2)
        container.layout().addWidget(self.btn, 1)
        container.layout().addWidget(self.cancelBtn, 1)
        container.layout().addWidget(QtWidgets.QWidget(), 2)
        container.layout().setSpacing(10)
        center = QtWidgets.QWidget(self)
        center.setLayout(QtWidgets.QVBoxLayout())
        center.layout().addWidget(QtWidgets.QWidget(), 1)
        center.layout().addWidget(self.text)
        center.layout().addWidget(container)
        center.layout().addWidget(QtWidgets.QWidget(), 1)
        self.layout().addWidget(center)
        self.btn.clicked.connect(self.onPressSkip)
        self.cancelBtn.clicked.connect(self.onPressCancel)
        self.onTimer()

    def setWaitingWindows(self, wnds):
        self.text.setText("Waiting for " + str(len(wnds)) + " windows to close:\n" + str(wnds))
    
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
    app = QtWidgets.QApplication(sys.argv)
    window = WaitingDialog()
    window.show()
    app.exec()
    if window.doExit == True:
        exitI3()

main()