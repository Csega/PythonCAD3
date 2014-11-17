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
# code for base for Bisector
#

from Kernel.GeoComposedEntity.objoint import *
from Kernel.GeoUtil.geolib import Vector
import math

class Bisector(ObjectJoint):
    """
        A Bisector class 
    """
    def __init__(self, kw):
        """
            "OBJECTJOINT_0" obj1             :(Segment ,ACLine,Arc,CCircle)
            "OBJECTJOINT_1" obj2             :(Segment ,ACLine,Arc,CCircle)
            "OBJECTJOINT_2" pointClick1      :Clicked point from the u.i near the obj1
            "OBJECTJOINT_3" pointClick2      :Clicked point from the u.i near the obj2
            "OBJECTJOINT_4" str              :Fixed Value "NO_TRIM" not needed
            "OBJECTJOINT_5" lengh            :Bisector lengh from intersection point
        """
        kw["OBJECTJOINT_4"]="NO_TRIM"
        argDes={"OBJECTJOINT_5":(float, int, None)}
        ObjectJoint.__init__(self, kw, argDes)
        if not kw["OBJECTJOINT_5"]:
            self["OBJECTJOINT_5"]=self.getDefaultLeng()
        self._UpdateBisector()

    def _UpdateBisector(self):
        """
            Update the segment base on the imput value
        """
        v1=self.getAngledVector(self.obj1, self.pointClick1)
        v2=self.getAngledVector(self.obj2, self.pointClick2)
        ang=v1.ang(v2)/2.0
        if v1.absAng==0 or v2.absAng==0:
            if v2.point.y<0:
                bisecVector=v2.mag()
            elif v1.point.y<0:
                bisecVector=v1.mag()
            else:
                if v1.absAng>v2.absAng:
                    bisecVector=v2.mag()
                else:
                    bisecVector=v1.mag()
        else:
            v1v2Ang=abs(v1.absAng-v2.absAng)
            if v1.absAng>v2.absAng:
                if v1v2Ang>math.pi:
                    bisecVector=v1.mag()
                else:
                    bisecVector=v2.mag()
            else:
                if v1v2Ang>math.pi:
                    bisecVector=v2.mag()
                else:
                    bisecVector=v1.mag()
        bisecVector.mult(self.lengh)
        bisecVector.rotate(ang)
        newPoint=self.intersection[0]+bisecVector.point
        arg={"SEGMENT_0":self.intersection[0], "SEGMENT_1":newPoint}
        self.bisector=Segment(arg)
        
    @property
    def lengh(self):
        """
            Second object of the bisector
        """
        return self['OBJECTJOINT_5']

    @lengh.setter
    def lengh(self, value):
        if value:
            self['OBJECTJOINT_5'] = value
        else:
            self.getDefaultLeng()

    @property
    def bisector(self):
        """
            Bisector segment object
        """
        return self.__bisector
    @bisector.setter
    def bisector(self, value):
        self.__bisector=value
        
    def getDefaultLeng(self):
        """
            get the default bisector lengh
        """
        pp1=obj1.projection(pointClick1.getSympy())
        pp2=obj2.projection(pointClick2.getSympy())
        ppi.self.intersection[0].getSympy()
        import sympy.geometry   as geoSympy
        t=geoSympy.Triangle(pp1,pp1,ppi)
        return float(t.bisectors[ppi].length)
        
    def clone(self):
        """
            Clone the Chamfer .. 
            I do not why somone whant to clone a chamfer ..
            But Tis is the functionality .. :-)
        """
        newChamfer=Chamfer(self._obj1 , 
                    self._obj2 ,

                    self.pointClick1, 
                    self.pointClick2)
        return newChamfer

    def getReletedComponent(self):
        """
            return the element to be written in the db and used for renderin
        """
        return self.bisector
    
        
