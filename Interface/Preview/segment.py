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
#
from Interface.Preview.base         import *
from Kernel.GeoEntity.segment       import Segment as geoSegment
from Kernel.initsetting             import PYTHONCAD_PREVIEW_COLOR
#
class QtSegmentItem(BaseQtPreviewItem):
    def __init__(self,command):
        super(QtSegmentItem, self).__init__(command)
        
    def drawGeometry(self, painter,option,widget):
        """
            Overloading of the paint method
        """
        if self.value[0]!=None and self.value[1]!=None:
            #print "drawLine", self.value[0],self.value[1]
            painter.drawLine(self.value[0],self.value[1])
        
    def boundingRect(self):
        """
            Overloading of the qt bounding rectangle
        """
        if self.value[0]!=None and self.value[1]!=None:
            x=min(self.value[0].x(), self.value[1].x())
            y=min(self.value[0].y(), self.value[1].y())
            d1=abs(self.value[0].x()-self.value[1].x())
            d2=abs(self.value[0].y()-self.value[1].y())
            #print "boundingRect", x, y, d1, d2
            return QtCore.QRectF(x,y ,d1,d2)
        #print "not updated"
        return QtCore.QRectF(0.0,0.0 ,0.1,0.1)
