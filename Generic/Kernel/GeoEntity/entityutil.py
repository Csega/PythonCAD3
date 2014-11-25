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
# This module provide some utility  for the entity 
#
import math

import sympy as mainSympy
import sympy.geometry as geoSympy

from GeoEntity.point import Point
from GeoEntity.segment import Segment
from GeoEntity.arc import Arc
from GeoEntity.ellipse import Ellipse


#    "Ray",
#    "Line",
#    "Triangle",
#    "RegularPolygon",
#    "Polygon",
#    "Curve"
    
def getEntityEntity(sympyEntity):
    """
        convert sympy object into PyCAD object
    """
    if isinstance(sympyEntity, geoSympy.Circle):
        arg = {"ARC_0": Point(0.0, 0.0), 
             "ARC_1": 1, 
             "ARC_2": None, 
             "ARC_3": None
             }    
        arc = Arc(arg)
        arc.setFromSympy(sympyEntity)
        return arc
    elif isinstance(sympyEntity, geoSympy.Point):
        p = Point(0.0, 0.0)
        p.setFromSympy(sympyEntity)
        return p
    elif isinstance(sympyEntity, geoSympy.Segment):
        segArg = {"SEGMENT_0": Point(0.0, 0.0), "SEGMENT_1": Point(1.0, 1.0)}
        seg = Segment(segArg)
        seg.setFromSympy(sympyEntity)
        return seg
    elif isinstance(sympyEntity, geoSympy.Ellipse):
        arg = {"ELLIPSE_0": Point(0.0, 0.0), "ELLIPSE_1": 1.0, "ELLIPSE_2": 2.0}
        e = Ellipse(arg)
        e.setFromSympy(sympyEntity)
        return e
    else:
        raise "not supported entity"
