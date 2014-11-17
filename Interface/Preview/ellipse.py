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
# EllipsePreview object
#
import math

from Interface.Preview.base         import *

class QtEllipseItem(BaseQtPreviewItem):
    def __init__(self, command):
        super(QtEllipseItem, self).__init__(command)
        # get the geometry
    
    def drawGeometry(self, painter,option,widget):
        """
            overloading of the paint method
        """
        if self.center:
            xc=self.center.x()
            yc=self.center.y()
            painter.drawEllipse(xc-(self.major/2.0),yc-(self.minor/2.0),self.major ,self.minor)
    
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        if self.center:
            xc=self.center.x()
            yc=self.center.y()
            painterPath.drawEllipse(xc-(self.major/2.0),yc-(self.minor/2.0),self.major ,self.minor)
    
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        if self.center:
            xc=self.center.x()
            yc=self.center.y()
            return QtCore.QRectF(xc-(self.major/2.0),yc- (self.minor/2.0) ,self.major ,self.minor )
        return QtCore.QRectF(0,0 ,0.1,0.1)
        
    @property
    def center(self):
        return self.value[0]
    @center.setter
    def center(self, value):
        self.value[0]=value
        self.update(self.boundingRect())
    @property
    def major(self):
        return self.value[1]
    @major.setter
    def major(self, value):
        self.value[1] =value
        self.update(self.boundingRect())
    @property
    def minor(self):
        return self.value[2]
    @minor.setter
    def minor(self, value):
        self.value[2]=value
        self.update(self.boundingRect())
