#!/usr/bin/env python
#
# Copyright (c) 2010 Matteo Boscolo
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
# You should have received a copy of the GNU General Public Licensesegmentcmd.py
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#This module provide a class for the segment command
#
from PyQt4 import QtCore, QtGui

from Kernel.exception       import *
from Kernel.GeoEntity.point import Point as GeoPoint
from Kernel.GeoUtil.geolib  import Vector
from Kernel.initsetting     import PYTHONCAD_PREVIEW_COLOR

class Base(object):
    def __init__(self, command):
        """
            inizialize base preview items
        """
        self._command=command
        self._items=command.lenght
        
    def getPreviewObject(self):
        return None

class BaseQtPreviewItem(QtGui.QGraphicsItem):
    def __init__(self, command):
        super(BaseQtPreviewItem, self).__init__()
        self.updateColor()
        self.value=[]
        for dValue in command.defaultValue:
            val=self.convertToQTObject(dValue)
            self.value.append(val)
        
    def updateColor(self):
        """
            update the preview color 
        """
        r, g, b=PYTHONCAD_PREVIEW_COLOR
        self.color = QtGui.QColor.fromRgb(r, g, b)
        
    def updatePreview(self,  position, distance, kernelCommand):
        """
            update the data at the preview item
        """
        # Assing default values
        for i in range(0, len(kernelCommand.exception)):
            if len(self.value)>i:
                self.value[i]=self.convertToQTObject(kernelCommand.defaultValue[i])
            else:
                self.value.append(self.convertToQTObject(kernelCommand.defaultValue[i]))
        # Assing Command Values
        for i in range(0, len(kernelCommand.exception)):        
            if(i<len(kernelCommand.value)):
                self.value[i]=self.convertToQTObject(kernelCommand.value[i])
        # Assing mouse keyboard values
        index=kernelCommand.valueIndex
        try:
            raise kernelCommand.exception[index](None)
        except(ExcPoint):
            self.value[index]=position
        except(ExcLenght, ExcInt):
            self.value[index]=distance
        except(ExcAngle):
            p1=GeoPoint(0.0, 0.0)
            p2=GeoPoint(position.x(), position.y()*-1.0)
            self.value[index]=Vector(p1, p2).absAng
        except:
            return 
        self.update(self.boundingRect())
    
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        #painter.setPen(QtGui.QPen(self.color, self.lineWith))
        painter.setPen(QtGui.QPen(self.color))
        #draw geometry
        #painter.drawPath(self.shape())
        self.drawGeometry(painter,option,widget)     
       
    def convertToQTObject(self, value):
        """
            convert the imput value in a proper value
        """
        if isinstance(value, (float, int)):
            return value
        elif isinstance(value, tuple):
            return QtCore.QPointF(value[0], value[1])
        elif isinstance(value, GeoPoint):
            return QtCore.QPointF(value.x, value.y*-1.0)
        else:
            return value
