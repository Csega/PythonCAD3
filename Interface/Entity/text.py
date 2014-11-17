#
# Copyright (c) ,2010 Matteo Boscolo
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
# qt text class
#

from Interface.Entity.base import *
from math import degrees
class Text(BaseEntity):
    def __init__(self, entity):
        super(Text, self).__init__(entity)
        geoEnt=self.geoItem
        self.text=geoEnt.text #QtCore.QString(geoEnt.text)
        x, y=geoEnt.location.getCoords()
        self.angle=degrees(geoEnt.angle)
        self.location=QtCore.QPointF(float(x), -1.0*y)
        self.pointPosition=geoEnt.pointPosition
        self.font=QtGui.QFont() #This have to be derived from the geoent as son is implemented
        self.setPos(self.location)
        self.rotate(self.angle)
        return
            
    def drawShape(self, painterPath):    
        """
            overloading of the shape method 
        """
        painterPath.addText(QtCore.QPointF(0.0, 0.0), self.font, self.text)        
        return
        
        
    def drawGeometry(self, painter, option, widget):
        #Create Text
        painter.drawText(self.boundingRect(),QtCore.Qt.AlignCenter,  self.text)
        
        
        
        
