#
# Copyright (c) 2010 Matteo Boscolo, Gertwin Groen
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PythonCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# This module the graphics scene class
#
#

import math

from PyQt5 import QtCore, QtGui, QtWidgets
from Kernel.pycadevent import PyCadEvent

class DinamicEntryLine(QtWidgets.QLineEdit):
    def __init__(self):
        super(DinamicEntryLine, self).__init__()
        self.hide()
        self.h = 20
        self.w = 60
        self.onEnter = PyCadEvent()
        
    def setPos(self, x, y):
        self.setGeometry(x, y, self.w, self.h)
    
    @property
    def text(self):
        return super(DinamicEntryLine, self).text()
    
    @text.setter
    def text(self, value):
        super(DinamicEntryLine, self).settext(value)
        
    def show(self):
        self.setFocus(7)
        super(DinamicEntryLine, self).show()  
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            self.onEnter()
            super(DinamicEntryLine, self).hide()  
        super(DinamicEntryLine, self).keyPressEvent(event)
