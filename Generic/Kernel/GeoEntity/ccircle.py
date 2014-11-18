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
# construction circle class
#

from __future__ import generators

import math

from Kernel.GeoUtil.tolerance import *
from Kernel.GeoUtil.util import *
from Kernel.GeoEntity.geometricalentity import *
from Kernel.GeoEntity.point import Point
from Kernel.GeoEntity.segment import Segment
from Kernel.GeoEntity.cline import CLine
from Kernel.GeoUtil.geolib import Vector

class CCircle(GeometricalEntity):
    """
        A class for contruction circles

        center: A Point object
        radius: The CCircle's radius
    """
    def __init__(self, kw):
        """
            Initialize a CCircle.
            kw['ARC_0'] center must be a point 
            kw['ARC_1'] radius must be a valid float
        """
        argDescription={
                        "CCIRCLE_0": Point,
                        "CCIRCLE_1": (float, int)
                        }
        GeometricalEntity.__init__(self, kw, argDescription)
        
        if not get_float(self.radius) > 0.0:
            raise ValueError("Invalid radius")
    
    @property
    def info(self):
        return "CCircle: Center: %s, Radius:%ss"%(str(self.center), str(self.radius))
    def __eq__(self, obj):
        """
            Compare a CCircle to another for equality.
        """
        if not isinstance(obj, CCircle):
            return False
        if obj is self:
            return True
        _val = False
        if self.center == obj.center:
            if abs(self.radius - obj.radius) < 1e-10:
                _val = True
        return _val

    def __ne__(self, obj):
        """
            Compare a CCircle to another for inequality.
        """
        if not isinstance(obj, CCircle):
            return True
        if obj is self:
            return False
        _val = True
        if self.center == obj.center:
            if abs(self.radius - obj.radius) < 1e-10:
                _val = False
        return _val
        
    def getConstructionElements(self):
        """
            get construction elements
        """
        return (self.center, self.radius)
        
    def getCenter(self):
        """
            Return the center Point of the CCircle.
        """
        return self['CCIRCLE_0']

    def setCenter(self, point):
        """
            Set the center Point of the CCircle.
            The argument must be a Point or a tuple containing
            two float values.
        """
        if not isinstance(point, Point):
            raise TypeError("Invalid center point: " + str(type(point)))
       
        self['CCIRCLE_0'] = point

    center = property(getCenter, setCenter, None, "CCircle center")

    def getRadius(self):
        """
            Return the radius of the the CCircle.
        """
        return self['CCIRCLE_1']

    def setRadius(self, radius):
        """
            Set the radius of the CCircle.
            The argument must be float value greater than 0.
        """
        _r = get_float(radius)
        if not _r > 0.0:
            raise ValueError("Invalid radius: %g" % _r)
        self['CCIRCLE_1'] = _r

    radius = property(getRadius, setRadius, None, "CCircle radius")

    def circumference(self):
        """
            Return the circumference of the CCircle.
        """
        return 2.0 * math.pi * self.radius

    def area(self):
        """
            Return the area enclosed by the CCircle.
        """
        return math.pi * pow(self.radius, 2)

    def mapCoords(self, x, y, tol = TOL):
        """
            Return the nearest Point on the CCircle to a coordinate pair.
            The function has two required arguments:

            x: A Float value giving the x-coordinate
            y: A Float value giving the y-coordinate

            There is a single optional argument:

            tol: A float value equal or greater than 0.0

            This function is used to map a possibly near-by coordinate pair to
            an actual Point on the CCircle. If the distance between the actual
            Point and the coordinates used as an argument is less than the tolerance,
            the actual Point is returned. Otherwise, this function returns None.
        """
        _x = get_float(x)
        _y = get_float(y)
        _t = toltest(tol)
        _cx, _cy = self.center.getCoords()
        _r = self.radius
        _dist = math.hypot((_x - _cx), (_y - _cy))
        if abs(_dist - _r) < _t:
            _angle = math.atan2((_y - _cy),(_x - _cx))
            _xoff = _r * math.cos(_angle)
            _yoff = _r * math.sin(_angle)
            return (_cx + _xoff), (_cy + _yoff)
        return None
    
    def GetTangentPoint(self, x, y, outx, outy):
        """
            Get the tangent from an axternal point
            args:
                x,y is a point near the circle
                xout,yout is a point far from the circle
            return:
                a tuple(x,y,x1,xy) that define the tangent line
        """
        firstPoint = Point(x, y)
        fromPoint = Point(outx, outy)
        twoPointDistance = self.center.Dist(fromPoint)
        if(twoPointDistance < self.radius):
            return None, None
        originPoint = Point(0.0, 0.0)        
        tanMod = math.sqrt(pow(twoPointDistance, 2) - pow(self.radius, 2))
        tgAngle = math.asin(self.radius / twoPointDistance)
        #Compute the x versor
        xPoint = point.Point(1.0, 0.0)
        xVector = Vector(originPoint, xPoint)
        twoPointVector = Vector(fromPoint, self.center)
        rightAngle = twoPointVector.Ang(xVector)                
        cx, cy = self.center.getCoords()        
        if(outy > cy): #stupid situation 
            rightAngle =- rightAngle
        posAngle = rightAngle + tgAngle
        negAngle = rightAngle - tgAngle
        #Compute the Positive Tangent
        xCord = math.cos(posAngle)
        yCord = math.sin(posAngle)
        dirPoint = Point(xCord, yCord)#Versor that point at the tangentPoint
        ver = Vector(originPoint, dirPoint)
        ver.Mult(tanMod)
        tangVectorPoint = ver.Point()
        posPoint = Point(tangVectorPoint + (outx, outy))
        #Compute the Negative Tangent
        xCord = math.cos(negAngle)
        yCord = math.sin(negAngle)
        dirPoint = Point(xCord, yCord) #Versor that point at the tangentPoint
        ver = Vector(originPoint, dirPoint)
        ver.Mult(tanMod)
        tangVectorPoint = ver.Point()
        negPoint = Point(tangVectorPoint + (outx, outy))
        if firstPoint.Dist(posPoint) < firstPoint.Dist(negPoint):
            return posPoint.getCoords()     
        else:
            return negPoint.getCoords() 
           
    def GetRadiusPointFromExt(self, x, y):
        """
            get The intersecrion point from the line(x,y,cx,cy) and the circle
        """
        _cx, _cy = self.center.getCoords()
        _r = self.radius
        centerPoint = Point(_cx, _cy)
        outPoint = Point(x, y)
        vector = Vector(outPoint, centerPoint)
        vNorm = vector.Norm()
        newNorm = abs(vNorm - _r)
        magVector = vector.Mag()
        magVector.Mult(newNorm)
        newPoint = magVector.Point()
        intPoint = Point(outPoint + newPoint)
        return intPoint.getCoords()  
    
    def inRegion(self, xmin, ymin, xmax, ymax, fully = False):
        """
            Return whether or not an CCircle exists within a region.

        The first four arguments define the boundary. The optional
        fifth argument 'fully' indicates whether or not the CCircle
        must be completely contained within the region or just pass
        through it.
        """
        _xmin = get_float(xmin)
        _ymin = get_float(ymin)
        _xmax = get_float(xmax)
        if _xmax < _xmin:
            raise ValueError("Illegal values: xmax < xmin")
        _ymax = get_float(ymax)
        if _ymax < _ymin:
            raise ValueError("Illegal values: ymax < ymin")
        util.test_boolean(fully)
        _xc, _yc = self.center.getCoords()
        _r = self.radius
        #
        # cheap test to see if ccircle cannot be in region
        #
        if (((_xc - _r) > _xmax) or
            ((_yc - _r) > _ymax) or
            ((_xc + _r) < _xmin) or
            ((_yc + _r) < _ymin)):
            return False
        _val = False
        _bits = 0        
        #
        # calculate distances from center to region boundary
        #
        if abs(_xc - _xmin) < _r: _bits = _bits | 1 # left edge
        if abs(_xc - _xmax) < _r: _bits = _bits | 2 # right edge
        if abs(_yc - _ymin) < _r: _bits = _bits | 4 # bottom edge
        if abs(_yc - _ymax) < _r: _bits = _bits | 8 # top edge
        if _bits == 0:
            #
            # if the ccircle center is in region then the entire
            # ccircle is visible since the distance from the center
            # to any edge is greater than the radius. If the center
            # is not in the region then the ccircle is not visible in
            # the region because the distance to any edge is greater
            # than the radius, and so one of the bits should have been
            # set ...
            #
            if ((_xmin < _xc < _xmax) and (_ymin < _yc < _ymax)):
                _val = True
        else:
            _val = True
            #
            # calculate distance to corners of region
            #
            if math.hypot((_xc - _xmin), (_yc - _ymax)) < _r:
                _bits = _bits | 0x10 # upper left
            if math.hypot((_xc - _xmax), (_yc - _ymin)) < _r:
                _bits = _bits | 0x20 # lower right
            if math.hypot((_xc - _xmin), (_yc - _ymin)) < _r:
                _bits = _bits | 0x40 # lower left
            if math.hypot((_xc - _xmax), (_yc - _ymax)) < _r:
                _bits = _bits | 0x80 # upper right
            #
            # if all bits are set then distance from ccircle center
            # to region endpoints is less than radius - ccircle
            # entirely outside the region
            #
            if _bits == 0xff or fully:
                _val = False
        return _val

    def clone(self):
        """
            Create an identical copy of a CCircle
        """
        return CCircle(self.getConstructionElements())

    def getSympy(self):
        """
            get the sympy object in this case a circle
        """
        _cp=self.center.getSympy()
        return geoSympy.Circle(_cp, mainSympy.Rational(self.radius))
        
    def setFromSympy(self, sympyCircle):    
        """
            update the points cord from a sympyobject only avaiable for circle
        """
        self.center.setFromSympy(sympyCircle[0])
        self.radius = float(sympyCircle[1])
    
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        if not isinstance(mirrorRef, (CLine, Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")
        #
        self.center.mirror(mirrorRef)
        