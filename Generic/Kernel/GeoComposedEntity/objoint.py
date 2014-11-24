#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas
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
# You should have received a copy of the GNU General Public License
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#
# code for base composed object
#

from math import hypot, pi, sin, cos, tan, atan2

from GeoEntity.geometricalentity import *
from GeoUtil.util import *
from GeoUtil.intersection import *
from GeoEntity.segment import Segment
#from GeoEntity.acline import ACLine
from  GeoEntity.arc import Arc
from  GeoEntity.ccircle import CCircle
from  GeoUtil.geolib import Vector


#ALLOW_CHAMFER_ENTITY=(Segment, ACLine)

class ObjectJoint(GeometricalEntityComposed):
    """
        A base class for chamfers and fillets
        A ObjectJoint object has the following methods:
    """
    def __init__(self, kw, argDes = None):
        from Kernel.initsetting import DRAWIN_ENTITY
        classNames = tuple(DRAWIN_ENTITY.keys())
        argDescription = {"OBJECTJOINT_0": classNames, 
                          "OBJECTJOINT_1": classNames, 
                          "OBJECTJOINT_2": (Point, None), 
                          "OBJECTJOINT_3": (Point, None), 
                          "OBJECTJOINT_4": (str, unicode)
                         }
        if argDes:
            for k in argDes:
                argDescription[k] = argDes[k]
                
        self.trimModeKey = {"FIRST": 0, "SECOND": 1, "BOTH": 2, "NO_TRIM": 3}
        GeometricalEntityComposed.__init__(self, kw, argDescription)
        self._externalIntersectio = False
        spoolIntersection = [Point(x, y) for x, y in find_intersections(self.obj1, self.obj2)]
        if len(spoolIntersection) <= 0:  # if not intesection is found extend it on cLine
            spoolIntersection = findSegmentExtendedIntersectionPoint(self.obj1, self.obj2)
            self._externalIntersectio = True
        self._intersectionPoints = spoolIntersection
    
    @property
    def angle(self):
        """
            angle betwin the two entity
        """
        v1 = self.getAngledVector(self.obj1, self.pointClick1)
        v2 = self.getAngledVector(self.obj2, self.pointClick2)
        ang = v1.ang(v2)
        return ang
        
    @property
    def trimMode(self):
        """
            trim mode for the entity
        """
        return self["OBJECTJOINT_4"]
    
    @trimMode.setter
    def trimMode(self, value):
        if value in self.trimModeKey:
            self["OBJECTJOINT_4"] = value
        else:
            raise AttributeError("Bad trim mode use FIRST SECOND BOTH NO_TRIM")
    
    @property
    def obj1(self):    
        """
            First object
        """
        return self["OBJECTJOINT_0"]
    
    @obj1.setter
    def obj1(self, value):
        self["OBJECTJOINT_0"] = value
        
    @property
    def obj2(self):    
        """
           second object
        """
        return self["OBJECTJOINT_1"]
    
    @obj2.setter
    def obj2(self, value):
        self["OBJECTJOINT_1"] = value
        
    @property    
    def pointClick1(self):
        """
            get the clicked point
        """
        return self["OBJECTJOINT_2"]
    
    @pointClick1.setter
    def pointClick1(self, value):
        self["OBJECTJOINT_2"] = value

    @property  
    def pointClick2(self):
        """
            get the clicked point
        """
        return self["OBJECTJOINT_3"]

    @pointClick2.setter
    def pointClick2(self, value):
        self["OBJECTJOINT_3"] = value
        
    @property    
    def intersection(self):
        """
            Return the intersection points of the ObjectJoint Entity Object.

            This method returns an array of intersection point 
            [] no intersection
        """
        return self._intersectionPoints
        
    def getConstructionElements(self):
        """
            Return the two Entity Object joined by the ObjectJoint.
            This method returns a tuple holding the two Entity Object joined
            by the ObjectJoint.
        """
        return self

    
    def getReletedComponent(self):
        """
            return the releted compont of the ObjectJoint
        """
        return self.getConstructionElements()

    def getAngledVector(self, segment,  point):
        """
            calculate the vector use
        """
        pi = self.intersection[0]
        p1, p2 = segment.getEndpoints()
        vs1 = Vector(pi, p1)
        vs2 = Vector(pi, p2)
        if abs(vs1.absAng - vs2.absAng) < 0.00001:
            if pi.dist(p1) > pi.dist(p2):
                return Vector(pi, p1)
            else:
                return Vector(pi, p2)
        else:
            jp = segment.getProjection(point)
            vj = Vector(pi, jp)
            if abs(vj.absAng - vs1.absAng) < 0.00001:
                return Vector(pi, p1)
            else:
                return Vector(pi, p2)  
    