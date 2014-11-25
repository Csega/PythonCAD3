#
# Copyright (c) 2002, 2003, 2004, 2005 Art Haas
# Copyright (c) 2009,2010 Matteo Boscolo
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
# classes for points
#

from __future__ import generators

import math

from .geometricalentity import *
from Kernel.GeoUtil.util import *



class Point(GeometricalEntity):
    """
        A 2-D point Class.
    """
    def __init__(self, x, y=None):
        """
            Initialize a Point.
            There are Tree ways to initialize a Point:
            Point(xc,yc) - Two arguments, with both arguments being floats
            Point((xc,yc)) - A single tuple containing two float objects
            Point(Point) - A single Point Object
        """
        GeometricalEntity.__init__(self, None, None)
        if isinstance(x, tuple):
            if y is not None:
                raise SyntaxError("Invalid call to Point()")
            _x, _y = tuple_to_two_floats(x)
        elif y is not None:
            _x = float(x)
            _y = float(y)
        elif isinstance(x, Point):
            _x,_y = x.getCoords()
        else:
            #print("Debug : x[%s] y[%s]"%(str(x),str(y)))
            #print("Debug : type x %s"%str(type(x)))
            raise SyntaxError("Invalid call to Point().")
        self.__x = _x
        self.__y = _y

    def __str__(self):
        return "Point : (%g,%g)" % (self.__x, self.__y)
    
    @property
    def info(self):
        return "Point : (%g,%g)" % (self.__x, self.__y)
    
    def __sub__(self, p):
        """
            Return the separation between two points.
            This function permits the use of '-' to be an easy to read
            way to find the distance between two Point objects.
        """
        if not isinstance(p, Point):
            raise TypeError("Invalid type for Point subtraction: " + str(type(p)))
        _px, _py = p.getCoords()
        return math.hypot((self.__x - _px), (self.__y - _py))

    def __eq__(self, obj):
        """
            Compare a Point to either another Point or a tuple for equality.
        """
        if not isinstance(obj, (Point,tuple)):
            return False
        if isinstance(obj, Point):
            if obj is self:
                return True
            _x, _y = obj.getCoords()
        else:
            _x, _y = tuple_to_two_floats(obj)
        if abs(self.__x - _x) < 1e-10 and abs(self.__y - _y) < 1e-10:
            return True
        return False

    def __ne__(self, obj):
        """
            Compare a Point to either another Point or a tuple for inequality.
        """
        if not isinstance(obj, (Point, tuple)):
            return True
        if isinstance(obj, Point):
            if obj is self:
                return False
            _x, _y = obj.getCoords()
        else:
            _x, _y = tuple_to_two_floats(obj)
        if abs(self.__x - _x) < 1e-10 and abs(self.__y - _y) < 1e-10:
            return False
        return True

    def __add__(self,obj):
        """
            Add two Point
        """
        if not isinstance(obj, Point):
            if isinstance(obj, tuple):
                x, y = tuple_to_two_floats(obj)
            else:
                raise TypeError("Invalid Argument obj: Point or tuple Required")
        else:
            x,y = obj.getCoords()
        return Point(self.__x+x, self.__y+y)

    def getConstructionElements(self):
        """
            Get the construction element of entity..
        """
        return {"POINT_0":self.__x, "POINT_1":self.__y}
    
    def setConstructionElements(self, p1, p2):
        """
            Set the construction element of entity..
        """
        self__x=p1
        self__y=p2
        
    def getx(self):
        """
            Return the x-coordinate of a Point.
            getx()
        """
        return self.__x

    def setx(self, val):
        """
            Set the x-coordinate of a Point
            setx(val)
            The argument 'val' must be a float.
        """
        _v = get_float(val)
        _x = self.__x
        if abs(_x - _v) > 1e-10:
            self.__x = _v

    x = property(getx, setx, None, "x-coordinate value")

    def gety(self):
        """
            Return the y-coordinate of a Point.
        """
        return self.__y

    def sety(self, val):
        """
            Set the y-coordinate of a Point
            The argument 'val' must be a float.
        """
        _v = get_float(val)
        _y = self.__y
        if abs(_y - _v) > 1e-10:
            self.__y = _v

    y = property(gety, sety, None, "y-coordinate value")

    def getCoords(self):
        """
            Return the x and y Point coordinates in a tuple.
        """
        return self.__x, self.__y

    def setCoords(self, x, y):
        """
            Set both the coordinates of a Point.
            Arguments 'x' and 'y' should be float values.
        """
        _x = get_float(x)
        _y = get_float(y)
        _sx = self.__x
        _sy = self.__y
        if abs(_sx - _x) > 1e-10 or abs(_sy - _y) > 1e-10:
            self.__x = _x
            self.__y = _y

    def clone(self):
        """
            Create an identical copy of a Point.
        """
        return Point(self.__x, self.__y)

    def inRegion(self, xmin, ymin, xmax, ymax, fully=True):
        """
            Returns True if the Point is within the bounding values.
            inRegion(xmin, ymin, xmax, ymax)
            The four arguments define the boundary of an area, and the
            function returns True if the Point lies within that area.
            Otherwise, the function returns False.
        """
        _xmin = get_float(xmin)
        _ymin = get_float(ymin)
        _xmax = get_float(xmax)
        if _xmax < _xmin:
            raise ValueError("Illegal values: xmax < xmin")
        _ymax = get_float(ymax)
        if _ymax < _ymin:
            raise ValueError("Illegal values: ymax < ymin")
        test_boolean(fully)
        _x = self.__x
        _y = self.__y
        return not ((_x < _xmin) or
                    (_x > _xmax) or
                    (_y < _ymin) or
                    (_y > _ymax))

    def dist(self,obj):
        """
           Get The Distance From 2 Points
        """
        if not isinstance(obj, Point):
            if isinstance(obj, tuple):
                _x, _y = tuple_to_two_floats(obj)
            else:
                raise TypeError("Invalid Argument point: Point or Tuple Required")
        else:
            x,y=obj.getCoords()
        xDist=x-self.__x
        yDist=y-self.__y
        return math.sqrt(pow(xDist,2)+pow(yDist,2))

    def getSympy(self):
        """
            get the sympy object
        """
        return geoSympy.Point(mainSympy.Rational(str(self.__x)), mainSympy.Rational(str(self.__y)))

    def setFromSympy(self, sympyPoint):
        """
            update the points cord from a sympyobject
        """
        #self.__x=float(sympyPoint[0])
        #self.__y=float(sympyPoint[1])
        self.__x = float(sympyPoint.x)
        self.__y = float(sympyPoint.y)
    
    def move(self,fromPoint, toPoint):
        """
            perform the move operation
        """
        from Kernel.GeoUtil.geolib  import Vector
        v=Vector(fromPoint, toPoint)
        p=self+v.point
        self.__x=p.x
        self.__x=p.y
    
    def rotate(self, rotationPoint, angle):
        """
            this method must be defined for rotation
        """
        from Kernel.GeoUtil.geolib import Vector
        from Kernel.GeoEntity.point import Point
        v=Vector(rotationPoint,self)
        v.rotate(angle)
        p=rotationPoint+v.point    
        self.__x=p.x
        self.__y=p.y
        
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        from Kernel.GeoEntity.cline              import CLine
        from Kernel.GeoEntity.segment            import Segment
        from Kernel.GeoUtil.geolib               import Vector
        if not isinstance(mirrorRef, (CLine, Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")
        #
        centerMirror=mirrorRef.getProjection(self)
        vCenter=Vector(self, centerMirror )
        p=centerMirror+vCenter.point
        self.__x, self.__y=p.getCoords()
