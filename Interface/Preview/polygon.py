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
from Kernel.GeoUtil.geolib          import Vector
from Kernel.GeoEntity.point         import Point


class QtPolygonItem(BaseQtPreviewItem):
    def __init__(self, command):
        super(QtPolygonItem, self).__init__(command)
        self.command=command
        # get the geometry
    @property
    def polygonPoint(self):
        """
            get the poligon points
        """
        if self.side<=0:
            self.side=6
        deltaAngle=(math.pi*2)/self.side
        cPoint=Point(self.center.x(), self.center.y())
        vPoint=Point(self.vertex.x(), self.vertex.y())
        vertexVector=Vector(cPoint, vPoint)
        radius=vertexVector.norm
        angle=vertexVector.absAng
        pol=QtGui.QPolygonF()
        pFirst=None
        for i in range(0, int(self.side)):
            angle=deltaAngle+angle
            xsP=cPoint.x+radius*math.cos(angle)*-1.0
            ysP=cPoint.y+radius*math.sin(angle)*-1.0
            p=QtCore.QPointF(xsP,ysP)
            pol.append(p)
            if not pFirst:
                pFirst=p
        if pFirst:        
            pol.append(pFirst)
        return pol
        
    def drawGeometry(self, painter,option,widget):
        """
            overloading of the paint method
        """
        if self.center and self.vertex:
            painter.drawPolyline(self.polygonPoint)
    
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        if self.center and self.vertex:
            painter.drawPolyline(self.polygonPoint)
    
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        if self.center and self.vertex:
            return self.polygonPoint.boundingRect() 
        return QtCore.QRectF(0,0 ,0.1,0.1)
        
    @property
    def center(self):
        return self.value[0]
    @center.setter
    def center(self, value):
        self.value[0]=value
        self.update(self.boundingRect())
    @property
    def vertex(self):    
        return self.value[1]
    @vertex.setter
    def vertex(self, value):
        self.value[1]=value
        self.update(self.boundingRect())
    @property
    def side(self):
        return self.value[2]
        
