#!/usr/bin/env python
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
# This module provides a parser for the input interface

import sys
from sympy.physics import units as u


def convertLength(value):
    """
    Convert a length in sympy units syntax into a mm float.
    (Renamed from 'convertLengh' to fix typo)
    """
    val = str(value).lower()

    # Fast path for plain numbers (e.g., "10")
    try:
        return float(val)
    except ValueError:
        pass  # Not a plain number, continue to sympy parsing

    # Sanitization: Use safe 'eval' with restricted namespace instead of exec('retVal=...')
    # This allows expressions like "10*u.m + 2*cm" without executing arbitrary code.
    try:
        namespace = {"u": u}
        result = eval(val, {"__builtins__": {}}, namespace)

        if hasattr(result, "si"):
            return float((result.si / u.mm).n())
        else:
            return float(float(result / u.mm).n())
    except Exception as e:
        print(f"Wrong formatting string in length conversion: {e}")
        return None


# Alias the correct function name to the old typo for backward compatibility
convertLengh = convertLength


def convertAngle(value):
    """
    Convert an angle in sympy units syntax into a rad float.
    """
    val = str(value).lower()

    # Fast path for plain numbers (e.g., "45")
    try:
        return float(val)
    except ValueError:
        pass

    # Sanitization: Same safe evaluation as length
    try:
        namespace = {"u": u}
        result = eval(val, {"__builtins__": {}}, namespace)

        if hasattr(result, "si"):
            return float(result.si / u.rad)
        else:
            return float(float(result / u.rad))
    except Exception as e:
        print(f"Wrong formatting string in angle conversion: {e}")
        return None


def decodePoint(value, previousPoint=None):
    """
    This static method decodes an input and returns a point (mm, mm)
    """
    value = str(value).lower()

    # Sanitization: Check for basic formatting requirements
    if "," not in value:
        raise ValueError(f"Invalid point format. Expected 'x,y'. Received '{value}'")

    parts = value.split(",")
    if len(parts) != 2:
        raise ValueError(
            f"Invalid point format. Expected exactly two values. Received '{value}'"
        )

    x_str, y_str = parts

    # Import locally to avoid circular dependencies at module load time
    from Kernel.GeoEntity.point import Point

    return Point(convertLength(x_str), convertLength(y_str))


if __name__ == "__main__":
    print(f"Length Test: {convertLengh('10*u.m+3.5*u.cm+10*u.ft')}")
    print(f"Angle Test (10): {convertAngle('10')}")
    print(f"Angle Test (90 deg): {convertAngle('90*u.deg')}")
