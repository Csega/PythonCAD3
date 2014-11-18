#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas
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
#
# arc class
#

from __future__ import generators

import math

from Kernel.GeoEntity.point                import Point
from Kernel.GeoEntity.segment              import Segment
from Kernel.GeoEntity.cline                import CLine
from Kernel.GeoUtil.geolib                 import Vector
from Kernel.GeoEntity.geometricalentity    import *
from Kernel.GeoUtil.util                   import *

_dtr = math.pi/180.0
_rtd = 180.0/math.pi

pi_2=math.pi*2.0
pi2=math.pi/2.0

class Arc(GeometricalEntity):
    """
        A class for Arcs.
        An Arc has four attributes:
        center: A Point object
        radius: The Arc's radius
        startAngle: The start angle
        endAngle: The end angle

        An Arc has the following methods:
    """
    def __init__(self,kw):
        """
            Initialize a Arc/Circle.
            kw['ARC_0'] center must be a point 
            kw['ARC_1'] radius must be a valid float
            kw['ARC_2'] startAngle must be a valid radiant float value
            kw['ARC_3'] endAngle   must be a valid radiant float value
        """
        argDescription={
                        "ARC_0":Point,
                        "ARC_1":(float, int), 
                        "ARC_2":(float, int), 
                        "ARC_3":(float, int)
                        }
        GeometricalEntity.__init__(self,kw, argDescription)
        __isCircle=False
        if self.startAngle ==None or self.endAngle==None:
            self.startAngle=0
            self.endAngle=pi_2
            __isCircle=True
        if not get_float(self.radius) > 0.0:
            raise ValueError("Invalid radius" )
        
        self.startAngle = self.startAngle
        self.endAngle= self.endAngle
        
    def isCircle(self):
        """
            return if the arc isa circle
        """
        return self.__isCircle
    @property
    def info(self):
        return "Arc: Center: %s, Radius:%s ,StartAngle: %s,EndAngle: %s"%(str(self.center), str(self.radius), str(self.startAngle), str(self.endAngle))
    def __eq__(self, obj):
        """
            Compare a Arc to another for equality.
        """
        if not isinstance(obj, Arc):
            return False
        if obj is self:
            return True
        return ((self.center == obj.center) and
                (abs(self.radius - obj.radius) < 1e-10) and
                (abs(self.startAngle - obj.startAngle) < 1e-10) and
                (abs(self.endAngle - obj.endAngle) < 1e-10))

    def __ne__(self, obj):
        """
            Compare a Arc to another for inequality.
        """
        if not isinstance(obj, Arc):
            return True
        if obj is self:
            return False
        return ((self.center != obj.center) or
                (abs(self.radius - obj.radius) > 1e-10) or
                (abs(self.startAngle - obj.startAngle) > 1e-10) or
                (abs(self.endAngle - obj.endAngle) > 1e-10))                   
        
        
    def getCenter(self):
        """
            Return the center Point of the Arc.
        """
        return self['ARC_0']

    def setCenter(self, point):
        """
            Set the center Point of the Arc.
        """
        if not isinstance(point, self.arguments['ARC_0'] ):
            raise TypeError("Wrong argument type Need a Point")
        self['ARC_0']=point

    center = property(getCenter, setCenter, None, "Arc center")

    def getRadius(self):
        """
            Return the radius of the the Arc.
        """
        return self['ARC_1']

    def setRadius(self, radius):
        """
            Set the radius of the Arc.
            The argument must be float value greater than 0.
        """
        _r = get_float(radius)
        if not _r > 0.0:
            raise ValueError("Invalid radius: %g" % _r)
        self['ARC_1']=_r

    radius = property(getRadius, setRadius, None, "Arc radius")

    def getStartAngle(self):
        """
            Return the startAngle for the Arc.
        """
        return self['ARC_2']

    def setStartAngle(self, angle):
        """
            Set the startAngle for the Arc.
            The argument angle should be a float.
        """
        self['ARC_2'] = angle

    startAngle = property(getStartAngle, setStartAngle, None,
                           "Start angle for the Arc.")

    def getEndAngle(self):
        """
            Return the endAngle for the Arc.
        """
        return self['ARC_3']

    def setEndAngle(self, angle):
        """
            Set the endAngle for the Arc.
            The argument angle should be a float.
        """
        self['ARC_3'] = angle

    endAngle = property(getEndAngle, setEndAngle, None,
                         "End angle for the Arc.")

    def getAngle(self):
        """
            Return the angular sweep of the Arc.
        """
        if abs(self.endAngle - self.startAngle) < 1e-10:
            _angle = pi_2
        elif self.endAngle > self.startAngle:
            _angle =self.endAngle - self.startAngle
        else:
            _angle = pi_2 - self.startAngle + self.endAngle
        return _angle

    def throughAngle(self, angle):
        """
            Return True if an arc passes through some angle
            The argument angle should be a float value. This method returns
            True if the arc exists at that angle, otherwise the method returns False.
        """
        _angle = math.fmod(get_float(angle), pi_2)
        if _angle < 0.0:
            _angle = _angle + pi_2
        _sa = self.__sa
        _ea = self.__ea
        _val = True
        if abs(_sa - _ea) > 1e-10:
            if _sa > _ea:
                if _angle > _ea and _angle < _sa:
                    _val = False
            else:
                if _angle > _ea or _angle < _sa:
                    _val = False
        return _val

    def getEndpoints(self):
        """
            Return where the two endpoints for the arc-segment lie.
            This function returns two Points, each containing the x-y coordinates
            of the arc endpoints. The first Point corresponds to the endpoint at
            the startAngle, the second to the endpoint at the endAngle.
        """
        _cx, _cy = self.center.getCoords()
        _r = self.radius
        _sa = self.startAngle
        _sax = _cx + _r * math.cos(_sa )
        _say = _cy + _r * math.sin(_sa)
        _ea = self.endAngle+_sa
        
        _eax = _cx + _r * math.cos(_ea )
        _eay = _cy + _r * math.sin(_ea )
        return Point(_sax, _say), Point(_eax, _eay)

    def length(self):
        """
            Return the length of the Arc.
        """
        
        return self.radius*self.getAngle()

    def area(self):
        """
            Return the area enclosed by the Arc.
        """
        return pow(self.radius, 2) * (self.getAngle()/2)

    def GetTangentPoint(self,x,y,outx,outy):
        """
            Get the tangent from an axternal point
            args:
                x,y is a point near the circle
                xout,yout is a point far from the circle
            return:
                a tuple(x,y,x1,xy) that define the tangent line
        """
        firstPoint=Point(x,y)
        fromPoint=Point(outx,outy)
        twoPointDistance=self.center.dist(fromPoint)
        if(twoPointDistance<self.radius):
            return None,None
        originPoint=Point(0.0,0.0)
        tanMod=math.sqrt(pow(twoPointDistance,2)-pow(self.radius,2))
        tgAngle=math.asin(self.radius/twoPointDistance)
        #Compute the x versor
        xPoint=Point(1.0,0.0)
        xVector=Vector(originPoint,xPoint)
        twoPointVector=Vector(fromPoint,self.center)
        rightAngle=twoPointVector.ang(xVector)
        cx,cy=self.center.getCoords()
        if(outy>cy): # stupid situation
            rightAngle=-rightAngle
        posAngle=rightAngle+tgAngle
        negAngle=rightAngle-tgAngle
        # Compute the Positive Tangent
        xCord=math.cos(posAngle)
        yCord=math.sin(posAngle)
        dirPoint=Point(xCord,yCord) # Versor that point at the tangentPoint
        ver=Vector(originPoint,dirPoint)
        ver.mult(tanMod)
        tangVectorPoint=ver.Point()
        posPoint=Point(tangVectorPoint+(outx,outy))
        # Compute the Negative Tangent
        xCord=math.cos(negAngle)
        yCord=math.sin(negAngle)
        dirPoint=Point(xCord,yCord)#Versor that point at the tangentPoint
        ver=Vector(originPoint,dirPoint)
        ver.mult(tanMod)
        tangVectorPoint=ver.point()
        negPoint=Point(tangVectorPoint+(outx,outy))
        if(firstPoint.dist(posPoint)<firstPoint.dist(negPoint)):
            return posPoint.getCoords()
        else:
            return negPoint.getCoords()

    def GetRadiusPointFromExt(self,x,y):
        """
            get The intersecrion point from the line(x,y,cx,cy) and the circle
        """
        _cx, _cy = self.center.getCoords()
        _r = self.radius
        centerPoint=Point(_cx,_cy)
        outPoint=Point(x,y)
        vector=Vector(outPoint,centerPoint)
        vNorm=vector.norm()
        newNorm=abs(vNorm-_r)
        magVector=vector.mag()
        magVector.mult(newNorm)
        newPoint=magVector.point()
        intPoint=Point(outPoint+newPoint)
        return intPoint.getCoords()

    def inRegion(self, xmin, ymin, xmax, ymax, fully=False):
        """
            Return whether or not an Arc exists within a region.
            The first four arguments define the boundary. The optional
            fifth argument fully indicates whether or not the Arc
            must be completely contained within the region or just pass
            through it.
        """
        #TODO : May be we need to delete this ...
        _xmin = get_float(xmin)
        _ymin = get_float(ymin)
        _xmax = get_float(xmax)
        if _xmax < _xmin:
            raise ValueError("Illegal values: xmax < xmin")
        _ymax = get_float(ymax)
        if _ymax < _ymin:
            raise ValueError("Illegal values: ymax < ymin")
        test_boolean(fully)
        _xc, _yc = self.center.getCoords()
        _r = self.radius
        #
        # cheap test to see if arc cannot be in region
        #
        _axmin, _aymin, _axmax, _aymax = self.getBounds()
        if ((_axmin > _xmax) or
            (_aymin > _ymax) or
            (_axmax < _xmin) or
            (_aymax < _ymin)):
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
            # arc must be visible - the center is in
            # the region and is more than the radius from
            # each edge
            #
            _val = True
        else:
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
            # if all bits are set then distance from arc center
            # to region endpoints is less than radius - arc
            # entirely outside the region
            #
            _val = not ((_bits == 0xff) or fully)
            #
            # if the test value is still true, check that the
            # arc boundary can overlap with the region
            #
            if _val:
                _ep1, _ep2 = self.getEndpoints()
                _axmin = min(_xc, _ep1[0], _ep2[0])
                if self.throughAngle(180.0):
                    _axmin = _xc - _r
                if _axmin > _xmax:
                    return False
                _aymin = min(_yc, _ep1[1], _ep2[1])
                if self.throughAngle(270.0):
                    _aymin = _yc - _r
                if _aymin > _ymax:
                    return False
                _axmax = max(_xc, _ep1[0], _ep2[0])
                if self.throughAngle(0.0):
                    _axmax = _xc + _r
                if _axmax < _xmin:
                    return False
                _aymax = max(_yc, _ep1[1], _ep2[1])
                if self.throughAngle(90.0):
                    _aymax = _yc + _r
                if _aymax < _ymin:
                    return False
        return _val

    def getBounds(self):
        _ep1, _ep2 = self.getEndpoints()
        _xc, _yc = self.center.getCoords()
        _r = self.radius
        _xmin = min(_xc, _ep1[0], _ep2[0])
        _ymin = min(_yc, _ep1[1], _ep2[1])
        _xmax = max(_xc, _ep1[0], _ep2[0])
        _ymax = max(_yc, _ep1[1], _ep2[1])
        if self.throughAngle(0.0):
            _xmax = _xc + _r
        if self.throughAngle(90.0):
            _ymax = _yc + _r
        if self.throughAngle(180.0):
            _xmin = _xc - _r
        if self.throughAngle(270.0):
            _ymin = _yc - _r
        return _xmin, _ymin, _xmax, _ymax

    def clone(self):
        """
            Create an identical copy of a Arc
            clone()
        """
        return Arc(self.getConstructionElements())
    
    def getSympy(self):
        """
            get the sympy object in this case a circle
        """
        _cp=self.center.getSympy()
        return geoSympy.Circle(_cp, mainSympy.Rational(str(self.radius)))
        
    def setFromSympy(self, sympyCircle):    
        """
            update the points cord from a sympyobject only avaiable for circle
        """
        self.center.setFromSympy(sympyCircle[0])
        self.radius=float(sympyCircle[1])
        
    def __str__(self):
        msg="Arc\Circle: Center %s , Radius %s , StartAngle=%s, EndAngle=%s"%(
            str(self.center), str(self.radius), str(self.startAngle), str(self.endAngle))
        return msg
        
    def test_angle(s, e, a):
        """
            Returns if an angle lies between the start and end angle of an arc.
            s: arc start angle
            e: arc end angle
            a: angle being tested
        """
        _val = False
        if ((abs(e - s) < 1e-10) or
            ((s > e) and
             ((s <= a <= math.pi) or (0.0 <= a <= e))) or
            (s <= a <= e)):
            _val = True
        return _val
    
    def rotate(self, rotationPoint, angle):
        """
            rotate the arc
        """
        self.startAngle+=angle
        self.center.rotate(rotationPoint, angle)
        
        
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        if not isinstance(mirrorRef, (CLine, Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")
        #
        startPoint, endPoint=self.getEndpoints()
        self.center.mirror(mirrorRef)
        endMirror=mirrorRef.getProjection(endPoint)
        vEnd=Vector( endPoint, endMirror)
        newStart=endMirror+vEnd.point
        self.startAngle=Vector(self.center, newStart).absAng
    
    def getQuadrant(self):
        """
            Return the circle intersection with the line x,y passing through the
            center
        """
        print("call getQuadrant")
        x, y=self.center.getCoords()
        p1=Point(x, y+self.radius)
        p2=Point(x-self.radius, y)
        p3=Point(x, y-self.radius)
        p4=Point(x+self.radius, y)
        return [p1, p2, p3, p4]
