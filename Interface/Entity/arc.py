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
# qt arc class
#

from Interface.Entity.base import *

class Arc(BaseEntity):
    """
        this class define the arcQT object 
    """
    def __init__(self, entity):
        super(Arc, self).__init__(entity)
        geoEnt=self.geoItem  # get the geometry from kernel
        self.startPoint, p2=geoEnt.getEndpoints()     
        self.xc, self.yc=geoEnt.center.getCoords()
        startAngle=geoEnt.startAngle
        self.sa=startAngle
        spanAngle=geoEnt.endAngle
        self.yc=(-1.0*self.yc)- geoEnt.radius
        self.xc=self.xc-geoEnt.radius
        self.h=geoEnt.radius*2
        # By default, the span angle is 5760 (360 * 16, a full circle).
        # From pythoncad the angle are in radiant ..
        startAngle=(startAngle*180/math.pi)*16
        spanAngle=(spanAngle*180/math.pi)*16
        spanAngle=spanAngle
        self.startAngle=startAngle
        self.spanAngle=spanAngle
        return
    
    def arcRect(self):    
        return QtCore.QRectF(self.xc,
                             self.yc,
                             self.h,
                             self.h)

    
    def drawShape(self, painterPath):    
        """
            extending of the shape method 
        """
        x, y=self.startPoint.getCoords()
        painterPath.moveTo(x, y*-1.0)
        painterPath.arcTo(self.arcRect(),self.startAngle/16.0,self.spanAngle/16.0) 
        return
    
    def drawGeometry(self, painter, option, widget):
        """
            extending of the paint method
        """
        #Create Arc/Circle
        
        painter.drawArc(self.arcRect(),self.startAngle,  self.spanAngle)
    
    
    
    
    
    
    
    
  
