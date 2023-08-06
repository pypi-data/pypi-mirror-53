#!/usr/bin/env python

"""
display one or more EPICS PVs in a PyDM GUI window as a table

EXAMPLE:

    pvview.py xxx:m1.DESC xxx:m1.RBV xxx:m1.VAL xxx:m1.DMOV &
"""

import os
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QApplication, QFrame
from PyQt5.QtGui import QFont
from pydm.widgets.label import PyDMLabel


class PVView(QWidget):
    ''' '''
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.db = {}

        name_label  = QLabel("PV Name")
        value_label = QLabel("PV Value")
        self.formatWidget(name_label, QFrame.Raised, bold=True)
        self.formatWidget(value_label, QFrame.Raised, bold=True)

        self.grid = QGridLayout()
        self.grid.addWidget(name_label,   0, 0)
        self.grid.addWidget(value_label,  0, 1)
        self.grid.setColumnStretch(0, 0)
        self.grid.setColumnStretch(1, 1)

        self.setLayout(self.grid)
        self.setWindowTitle("EPICS PV View")

    def add(self, pvname):
        '''add a PV to the table'''
        if pvname in self.db:
            return
        row = len(self.db) + 1
        label = QLabel(pvname)
        widget = PyDMLabel(init_channel=f"ca://{pvname}")
        widget.useAlarmState = True
        self.formatWidget(label)
        self.formatWidget(widget)
        self.db[pvname] = widget
        self.grid.addWidget(label, row, 0)
        self.grid.addWidget(widget, row, 1)

    def formatWidget(self, widget, shadow=None, bold=False):
        """apply some styles to the widget"""
        shadow = shadow or QFrame.Sunken
        widget.setFrameShape(QFrame.Panel)
        widget.setFrameShadow(shadow)
        widget.setLineWidth(2)
        if bold:
            myFont=QFont()
            myFont.setBold(True)
            widget.setFont(myFont)

def main():
    app = QApplication(sys.argv)
    probe = PVView()
    if len(sys.argv) < 2:
        raise RuntimeError("Need one or more EPICS PVs on command line")
    pvnames = sys.argv[1:]
    for pvname in pvnames:
        probe.add(pvname)
    probe.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
