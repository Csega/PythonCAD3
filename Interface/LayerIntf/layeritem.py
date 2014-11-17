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
# This module contain a layer item used in the layer tree
#

from PyQt4 import QtCore, QtGui


class LayerItem(object):
    
    def __init__(self, data, parent=None):
        self.parent_item = parent
        self.item_data = data
        self.children = []


    def appendChild(self, item):
        self.children.append(item)


    def child(self, row):
        return self.children[row]


    def childCount(self):
        return len(self.children)


    def columnCount(self):
        return len(self.item_data)


    def data(self, column):
        try:
            return self.item_data[column]
        except IndexError:
            return None


    def parent(self):
        return self.parent_item


    def row(self):
        if self.parent_item:
            return self.parent_item.children.index(self)
        return 0

