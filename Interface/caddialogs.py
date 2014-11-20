#!/usr/bin/env python
#
# Copyright (c) 2010 Matteo Boscolo, Carlo Pavan
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
# This  module PROVIDE ALL GLOBAL VARIABLE NEEDE TO THE SCENE
#

from PyQt5 import QtCore, QtGui, QtWidgets
from Kernel.initsetting import *

class ConfigDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ConfigDialog, self).__init__()
        self.setWindowTitle("Preferences")
        
        self.exec_()

        