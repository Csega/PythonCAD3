#
# Copyright (c) 2003, 2004, 2005, 2006 Art Haas
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
# class stuff for ellipses
#
# Ellipse info:
# http://mathworld.wolfram.com/Ellipse.html
# http://astronomy.swin.edu.au/~pbourke/geometry/ellipsecirc/
#

import math


from Kernel.GeoUtil.tolerance import *
from Kernel.GeoUtil.util import *
from .point import Point
from .segment import Segment
from .cline import CLine
from .geometricalentity import *

class Ellipse(GeometricalEntity):
    """
        A base class for Ellipses
        An ellipse has the following attributes:
        center: A _point object
        horizontalRadius_axis:
        verticalRadius_axis:
    """
    def __init__(self, kw):
        """
            Initialize a Arc/Circle.
            kw['ELLIPSE_0'] center must be a point 
            kw['ELLIPSE_1'] hradius ax
            kw['ELLIPSE_2'] vradius ax
        """
        argDescription={
                        "ELLIPSE_0": Point,
                        "ELLIPSE_1": (float, int), 
                        "ELLIPSE_2": (float, int)
                        }
        _horizontalRadius = kw['ELLIPSE_1']
        _verticalRadius = kw['ELLIPSE_2']
        #if _verticalRadius > _horizontalRadius:
        #    kw['ELLIPSE_2'] = get_float(_horizontalRadius)
        #    kw['ELLIPSE_1'] = get_float(_verticalRadius)
        GeometricalEntity.__init__(self, kw, argDescription)
    
    @property
    def info(self):
        return "Ellipse: Center: %s, horizontalRadius: %s, verticalRadius:%s "%(str(self.center), str(self.horizontalRadius), str(self.verticalRadius))        
    
    def __eq__(self, obj):
        """
            Compare one ellipse to another for equality.
        """
        if not isinstance(obj, Ellipse):
            return False
        if obj is self:
            return True
        return (self.center == obj.getCenter() and
                abs(self.horizontalRadius - obj.gethorizontalRadiusAxis()) < 1e-10 and
                abs(self.verticalRadius - obj.getverticalRadiusAxis()) < 1e-10 
                )

    def __ne__(self, obj):
        """
            Compare one ellipse to another for equality.
        """
        return not self == object

    def getCenter(self):
        """
            Return the center _Point of the Ellipse.
        """
        return self['ELLIPSE_0']

    def setCenter(self, point):
        """
            Set the center _Point of the Ellipse.
            The argument must be a _Point or a tuple containing
            two float values.
        """
        self['ELLIPSE_0'] = point

    center = property(getCenter, setCenter, None, "Ellipse center")

    def gethorizontalRadiusAxis(self):
        """
            Return the horizontalRadius axis value of the Ellipse.
            This method returns a float.
        """
        return self['ELLIPSE_1']

    def sethorizontalRadiusAxis(self, val):
        """
            Set the horizontalRadius axis of the Ellipse.
            Argument 'val' must be a float value greater than 0.
        """
        _val = get_float(val)
        if _val < 0.0:
            raise ValueError("Invalid horizontalRadius axis value: %g" % _val)
        if _val < self.verticalRadius:
            self.self['ELLIPSE_1'] = self.verticalRadius
            self.verticalRadius = _val
        else:
            self['ELLIPSE_1'] = _val
            
    horizontalRadius = property(gethorizontalRadiusAxis, sethorizontalRadiusAxis, None,
                          "Ellipse horizontalRadius axis")

    def getverticalRadiusAxis(self):
        """
            Return the verticalRadius axis value of the Ellipse.
            This method returns a float.
        """
        return self['ELLIPSE_2']

    def setverticalRadiusAxis(self, val):
        """
            Set the verticalRadius axis of the Ellipse.
            Argument 'val' must be a float value greater than 0.
        """
        _val = get_float(val)
        if _val < 0.0:
            raise ValueError("Invalid verticalRadius axis value: %g" % _val)
        if _val > self.horizontalRadius:
            self['ELLIPSE_2'] = self.horizontalRadius
            self.horizontalRadius = _val
        else:
            self['ELLIPSE_2'] = _val
            
    verticalRadius = property(getverticalRadiusAxis, setverticalRadiusAxis, None,
                          "Ellipse verticalRadius axis")


    def eccentricity(self):
        """
            Return the eccecntricity of the Ellipse.
            This method returns a float value.
        """
        _horizontalRadius = self.horizontalRadius
        _verticalRadius = self.verticalRadius
        if abs(_horizontalRadius - _verticalRadius) < 1e-10: # circular
            _e = 0.0
        else:
            _e = math.sqrt(1.0 - ((_verticalRadius * _verticalRadius)/(_horizontalRadius * _horizontalRadius)))
        return _e

    def area(self):
        """
            Return the area of the Ellipse.
            This method returns a float value.
        """
        return math.pi * self.horizontalRadius * self.verticalRadius

    def circumference(self):
        """
            Return the circumference of an ellipse.
            This method returns a float.
            The algorithm below is taken from
            http://astronomy.swin.edu.au/~pbourke/geometry/ellipsecirc/
            Ramanujan, Second Approximation
        """
        _a = self.horizontalRadius
        _b = self.verticalRadius
        _h = math.pow((_a - _b), 2) / math.pow((_a + _b), 2)
        _3h = 3.0 * _h
        return math.pi * (_a + _b) * (1.0 + _3h / (10.0 + math.sqrt(4.0 - _3h)))

#
# measure r from focus
#
# x = c + r * cos(theta)
# y = r * sin(theta)
#
# c = sqrt(a^2 - b^2)
#
# r = a*(1-e)/(1 + e*cos(theta))

    def clone(self):
        """
            Make a copy of an Ellipse.
            This method returns a new Ellipse object
        """
        return Ellipse(self.getConstructionElements())

    def getSympy(self):
        """
            get the sympy object in this case a ellipse
        """
        _cp = self.center.getSympy()
        return geoSympy.Ellipse(_cp, mainSympy.Rational(str(self.horizontalRadius * .5)), mainSympy.Rational(str(self.verticalRadius * .5)))
        
    def setFromSympy(self, sympyEllipse):    
        """
            update the points cord from a sympyobject only avaiable for circle
        """
        self.center.setFromSympy(sympyEllipse[0])
        self.horizontalRadius = float(sympyEllipse[1])
        self.verticalRadius = float(sympyEllipse[2])
        
    def __str__(self):
        msg = "Ellipse: Center %s , horizontalRadius Axi = %s, Mino Axi = %s"%(
            str(self.center), str(self.horizontalRadius), str(self.verticalRadius))
        return msg
        
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        if not isinstance(mirrorRef, (CLine, Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")
        #
        self.center.mirror(mirrorRef)
