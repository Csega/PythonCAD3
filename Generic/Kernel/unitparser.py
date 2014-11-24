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
# This module provide a parser for the imput interface
#
from sympy.physics import units as u

def decodePoint(value, previusPoint=None):
    """
        this static method decode an imput and return a point(mm,mm)
    """
    value = str(value).lower()
    from Kernel.GeoEntity.point import Point
    x, y = str(value).split(',')
    return Point(convertLengh(x), convertLengh(y))
    
def convertAngle(value):
    """
        convert a angle in simpy units syntax into a rad float
    """
    value = str(value).lower()
    retVal = None
    try:
        retVal = float(value)
    except:
        try:
            retVal = sympyConvertAngle(value)
        except:
            print("Wrong formatting string")
    finally:
        return retVal

def sympyConvertAngle(value):
    retVal = None
    value = 'retVal=' + value
    exec(value)
    retVal = retVal / u.rad
    return float(retVal)
    
def convertLengh(value):
    """
        convert a lengh in simpy units syntax into a mm float
        return : Float
    """
    value = str(value).lower()
    retVal = None
    try:
        retVal = float(value)
    except:
        try:
            retVal = sympyConvertLeng(value)
        except:
            print("Wrong formatting string")
    finally:
        return retVal

def sympyConvertLeng(value):
    retVal = None
    value = 'retVal=' + value
    exec(value)
    retVal = retVal / u.mm
    return float(retVal.n())

if __name__ == '__main__':
    print(convertLengh('10*u.m+3.5*u.cm+10*u.ft'))
    print(convertAngle('10'))
    print(convertAngle('90*u.deg'))
    print(sympyConvertAngle('10*u.rad+10*u.deg'))
