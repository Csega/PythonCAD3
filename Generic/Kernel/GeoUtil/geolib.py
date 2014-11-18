#
# Copyright (c) 2009 Matteo Boscolo
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
# This module provide class to manage geometrical vector operation
#

import math

from Kernel.GeoEntity.point import Point

class Vector:
    """
        Provide a full 2d vector operation and definition
    """
    def __init__(self,p1,p2):
        """
            Default Constructor
        """
        if(not isinstance(p1, Point)):
          raise TypeError("Invalid Argument p1: Point Required")
        if(not isinstance(p2, Point)):
          raise TypeError("Invalid Argument p2: Point Required")
        x, y = p1.getCoords()
        x1, y1 = p2.getCoords()
        self.X = x1 - x
        self.Y = y1 - y
        
    def mag(self):
        """
            Get the versor
        """
        _a = self.absAng
        p1 = Point(0, 0)
        p2 = Point(math.cos(_a), math.sin(_a))
        return Vector(p1, p2)

    @property    
    def norm(self):
        """
          Get The Norm Of the vector
        """
        return math.sqrt(pow(self.X, 2) + pow(self.Y, 2))
    
    def __eq__(self, vector):
        """
            the 2 vector are equal
        """ 
        if(not isinstance(vector, Vector)):
          raise TypeError("Invalid Argument vector: Vector Required")
        if(self.point == vector.point):
            return True             
        else:
            return False
    
    @property
    def point(self):
        """
              Return The Point 
        """
        return Point(self.X, self.Y)
    
    @property
    def x(self):
        """
            return the x value of the vector
        """
        return self.X
    
    @property
    def y(self):
        """
            return the y value of the vector
        """
        return self.Y
    
    def dot(self, vector):
        """
            Compute The Dot Product
        """
        if(not isinstance(vector, Vector)):
            raise TypeError("Invalid Argument vector: Vector Required")
        v0 = self.point.getCoords()
        v1 = vector.point.getCoords()
        som = 0
        for a, b in zip(v0, v1):
          som += a * b
        return som  
        
    def cross(self, vector):
        """
            Compute The Cross Product
        """
        if(not isinstance(vector, Vector)):
            raise TypeError("Invalid Argument vector: Vector Required")
        x1, y1 = self.point.getCoords()
        x2, y2 = vector.point.getCoords()
        cros = x1 * y2 - y1 * x2
        return cros
        
    def ang(self, vector):
        """
            Calculate the angle Between the two vector
        """
        if(not isinstance(vector, Vector)):
            raise TypeError("Invalid Argument vector: Vector Required")
        vself = self.mag()
        vvector = vector.mag()
        dot = vself.dot(vvector)
        if(dot < -1):
            dot = -1
        if(dot > 1):
            dot = 1
        ang = math.acos(dot)
        return ang
    
    @property
    def absAng(self):
        """
            return the angle from the cartesian reference
        """
        _y = self.point.y
        ang = math.atan2(float(_y), float(self.point.x))
        if _y < 0:
            ang = ang + 2 * math.pi
        return ang
        
    def mult(self, scalar):
        """
            Multiplae the vector for a scalar value
        """
        self.X = scalar * self.norm * math.cos(self.absAng)
        self.Y = scalar * self.norm * math.sin(self.absAng)

    
    def map(self, pPro):
        """
            Get a vector for the mapping point
        """
        p0 = Point(0, 0)
        vProj = Vector(p0, pPro)
        ang = self.ang(vProj)
        vProjNorm = vProj.norm
        projectionUnitDistance = vProjNorm * math.cos(ang)
        vSelfMag = self.mag()
        vSelfMag.mult(projectionUnitDistance)
        return vSelfMag    
    
    def rotate(self, angle):
        """
            rotate the vector of a given angle
        """
        _a = self.absAng + angle
        _norm = self.norm
        self.X = _norm * math.cos(_a)
        self.Y = _norm * math.sin(_a)

    def invert(self):
        """
            Invert the vector
        """
        self.rotate(math.pi)
		
    def __str__(self):    
        """
            print the vector
        """
        msg = "Vector :(%s,%s),Norm: %s"%(self.point.x, self.point.y, self.norm)
        return msg
