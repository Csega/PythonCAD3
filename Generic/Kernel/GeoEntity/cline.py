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
# single point construction lines at an arbitrary angle
#

from __future__ import generators

import math


from Kernel.GeoEntity.geometricalentity    import *
from Kernel.GeoUtil.tolerance              import *
from Kernel.GeoUtil.util                   import *
from Kernel.GeoEntity.point                import Point
from Kernel.GeoUtil.geolib                 import Vector

class CLine(GeometricalEntity):
    """
        A class for single point construction lines From Two points.
    """
    
    def __init__(self, kw):
        """
            Initialize an CLine object.
            kw must be a dict with 2 argument 
            CLINE_0=Point: First Point object where the line passes through
            CLINE_1=Point: Second Point object where the line passes through
        """
        argDescription={"CLINE_0":Point, "CLINE_1":Point}
        GeometricalEntity.__init__(self,kw, argDescription)

    def __str__(self):
        return "Construction line through point %s at %s " % (self.p1, self.p2)   
    @property
    def info(self):
        return "CLine: %s, %s"%(str(self.p1), str(self.p2))
    
    def rotate(self, rotationPoint, angle):
        """
            rotate the acline for a given angle
        """    
        self.p1=GeometricalEntity.rotate(self, rotationPoint,self.p1, angle )
        self.p2=GeometricalEntity.rotate(self, rotationPoint,self.p2, angle )

    def isVertical(self):
        x1, y1=self.p1.getCoords()
        x2, y2=self.p1.getCoords()
        return abs(y1 - y2) < 1e-10

    def isHorizontal(self):
        x1, y1=self.p1.getCoords()
        x2, y2=self.p1.getCoords()
        return abs(x1 - x2) < 1e-10

    def getP1(self):
        return self['CLINE_0']

    def setP1(self, p):
        if not isinstance(p, Point):
            raise TypeError, "Unexpected type for point: " + `type(p)`
        self['CLINE_0']=p
        
    p1=property(getP1, setP1, None, "Set the location of the first point of the line")

    def getP2(self):
        return self['CLINE_1']

    def setP2(self, p):
        if not isinstance(p, Point):
            raise TypeError, "Unexpected type for point: " + `type(p)`
        self['CLINE_1']=p
        
    p2=property(getP2, setP2, None, "Set the location of the first point of the line")

    def getKeypoints(self):
        """
            Return the 2 construction point 
        """
        return p1, p2
        
    def getAngle(self):
        """
            get the getAngle 
        """
        return float(mainSympy.atan(getSympy.slope))
        
    def clone(self):
        """
            Create an identical copy of an CLine.
        """
        return CLine(self)
        
    def getSympy(self):
        """
            get the sympy object
        """
        _sp1=self.p1.getSympy()
        _sp2=self.p2.getSympy()
        return geoSympy.Line(_sp1, _sp2)
        
    def setFromSympy(self, sympySegment):    
        """
            update the points cord from a sympyobject
        """
        self.p1.setFromSympy(sympySegment[0])
        self.p2.setFromSympy(sympySegment[1])
    @property
    def vector(self):
        """
            Get The vector of the CLine
        """
        return Vector(self.p1, self.p2)
    
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        from Kernel.GeoEntity.segment              import Segment
        if not isinstance(mirrorRef, (CLine, Segment)):
            raise TypeError, "mirrorObject must be Cline Segment or a tuple of points"
        #
        self.p1.mirror(mirrorRef)
        self.p2.mirror(mirrorRef)

def intersect_region(acl, xmin, ymin, xmax, ymax):
    if not isinstance(acl, CLine):
        raise TypeError, "Argument not an CLine: " + `type(acl)`
    _xmin = get_float(xmin)
    _ymin = get_float(ymin)
    _xmax = get_float(xmax)
    if _xmax < _xmin:
        raise ValueError, "Illegal values: xmax < xmin"
    _ymax = get_float(ymax)
    if _ymax < _ymin:
        raise ValueError, "Illegal values: ymax < ymin"
    _x, _y = acl.getLocation().getCoords()
    _x1 = _y1 = _x2 = _y2 = None
    if acl.isVertical() and _xmin < _x < _xmax:
        _x1 = _x
        _y1 = _ymin
        _x2 = _x
        _y2 = _ymax
    elif acl.isHorizontal() and _ymin < _y < _ymax:
        _x1 = _xmin
        _y1 = _y
        _x2 = _xmax
        _y2 = _y
    else:
        _angle = acl.getAngle()
        _slope = math.tan(_angle )
        _yint = _y - (_x * _slope)
        _xt = _x + math.cos(_angle)
        _yt = _y + math.sin(_angle)
        #
        # find y for x = xmin
        #
        _yt = (_slope * _xmin) + _yint
        if _ymin < _yt < _ymax:
            # print "hit at y for x=xmin"
            _x1 = _xmin
            _y1 = _yt
        #
        # find y for x = xmax
        #
        _yt = (_slope * _xmax) + _yint
        if _ymin < _yt < _ymax:
            # print "hit at y for x=xmax"
            if _x1 is None:
                _x1 = _xmax
                _y1 = _yt
            else:
                _x2 = _xmax
                _y2 = _yt
        if _x2 is None:
            #
            # find x for y = ymin
            #
            _xt = (_ymin - _yint)/_slope
            if _xmin < _xt < _xmax:
                # print "hit at x for y=ymin"
                if _x1 is None:
                    _x1 = _xt
                    _y1 = _ymin
                else:
                    _x2 = _xt
                    _y2 = _ymin
        if _x2 is None:
            #
            # find x for y = ymax
            #
            _xt = (_ymax - _yint)/_slope
            if _xmin < _xt < _xmax:
                # print "hit at x for y=ymax"
                if _x1 is None:
                    _x1 = _xt
                    _y1 = _ymax
                else:
                    _x2 = _xt
                    _y2 = _ymax
    return _x1, _y1, _x2, _y2

