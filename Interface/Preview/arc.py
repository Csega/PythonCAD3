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
# SegmentPreview object
#
import math

from Interface.Preview.base         import *

class QtArcItem(BaseQtPreviewItem):
    def __init__(self, command):
        super(QtArcItem, self).__init__(command)
        # get the geometry
    
    def drawGeometry(self, painter,option,widget):
        """
            overloading of the paint method
        """
        if self.center and self.radius:
            # By default, the span angle is 5760 (360 * 16, a full circle).
            # From pythoncad the angle are in radiant ..
            startAngle=(self.startAngle*180.0/math.pi)*16.0
            spanAngle=(self.spanAngle*180.0/math.pi)*16.0 
            xc=self.center.x()-self.radius
            yc=self.center.y()-self.radius
            h=self.radius*2.0
            painter.drawArc(xc,yc ,h ,h ,startAngle,  spanAngle)
            #first angle segment
            x=self.center.x()
            y=self.center.y()
            xsP=self.radius*math.cos(self.startAngle)
            ysP=self.radius*math.sin(self.startAngle)*-1.0
            painter.drawLine(self.center, QtCore.QPointF(xsP+x, ysP+y))
            #second angle segment
            secondAngle=self.startAngle+self.spanAngle
            xsP=self.radius*math.cos(secondAngle)
            ysP=self.radius*math.sin(secondAngle)*-1.0
            painter.drawLine(self.center, QtCore.QPointF(xsP+x, ysP+y))

    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        
        painterPath.arcTo(self.boundingRect(),self.startAngle,self.spanAngle) 
    
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        if self.center and self.radius:
            _s=self.radius
            xc=self.center.x()-_s
            yc=self.center.y()-_s
            _h=(_s*2.0)
            #print "boundingRect ", xc,yc,_h ,_h
            return QtCore.QRectF(xc,yc,_h ,_h)
        return QtCore.QRectF(0,0 ,0.1,0.1)
        
    @property
    def center(self):
        return self.value[0]
    @center.setter
    def center(self, value):
        self.value[0]=value
        self.update(self.boundingRect())
    @property
    def radius(self):    
        return self.value[1]
    @radius.setter
    def radius(self, value):
        self.value[1]=value
        self.update(self.boundingRect())
    @property
    def startAngle(self):
        return self.value[2]
    @startAngle.setter
    def startAngle(self, value):
        self.value[2] =value
        self.update(self.boundingRect())
    @property
    def spanAngle(self):
        return self.value[3]
    @spanAngle.setter
    def spanAngle(self, value):
        self.value[3]=value
        self.update(self.boundingRect())
