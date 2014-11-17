#
# Copyright (c) 2002, 2003 Art Haas
# Copyright (c) 2010 Matteo Boscolo
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
# this is a class that keeps a tolerance value. It should
# be used as a class (static) variable for classes that
# will compare instances with a tolerance
#
# a valid tolerance is a float value 0 or greater
#

TOL = 1e-10

class TolObject(object):
    """A class for maintaining a tolerance value.

The tolerance value is a float that must be 0.0 or
greater. Any class using this class as a base class
will have a tolerance value unique to that class.

There are two member functions:

getTolerance(): return the current tolerance
setTolerance(t): set the new tolerance

    """
    def __init__(self, t=None):
        """Initialize a TolObject.

TolObject(t)

Optional argument t must be a float, and it
must be greater than 0. A default tolerance is set
if the function is called without arguments.
        """
        if t is None:
            t = TOL
        tol = t
        if not isinstance(tol, float):
            tol = float(t)
        if tol < 0.0:
            raise ValueError, "Tolerance must be greater than 0: " + `tol`
        self.__tolerance = tol
        
    def setTolerance(self, t=None):
        """Set the tolerance value.

setTolerance(t)

Optional argument t must be a float, and it
must be greater than 0. The default tolerance is
reset if the function is called without arguments.
This function returns the old tolerance value.
        """
        old_tol = self.__tolerance
        if t is None:
            t = TOL
        tol = t
        if not isinstance(tol, float):
            tol = float(t)
        if tol < 0.0:
            raise ValueError, "Tolerance must be greater than 0: " + `tol`
        self.__tolerance = tol
        return old_tol

    def getTolerance(self):
        """Get the tolerance value.

getTolerance()

Return the current tolerance.
        """
        return self.__tolerance

    tolerance = property(getTolerance, setTolerance, None, "Tolerance value")

class StaticTolObject(object):
    """A class for maintaining a tolerance value.

This class is meant to be a base-class for classes
that wish to use a tolerance value for comparing
one instance to another.

There are two class methods:

getTolerance(): return the current tolerance
setTolerance(tol): set the new tolerance

This class stores the tolerance value as a static class
variable, so any classes using this class as a base class
will share the same tolerance value.
    """

    __tolerance = TOL
    
    def setTolerance(cls, t=None):
        """Set the tolerance value.

Optional argument t must be a float, and itmust be
greater than 0. The default tolerance is reset if
the function is called without arguments.

This function returns the old tolerance value.
        """
        old_tol = cls.__tolerance
        if t is None:
            t = TOL
        _t = t
        if not isinstance(_t, float):
            _t = float(t)
        if _t < 0.0:
            raise ValueError, "Tolerance must be greater than 0: " + `_t`
        cls.__tolerance = _t
        return old_tol

    setTolerance = classmethod(setTolerance)
    
    def getTolerance(cls):
        """Get the tolerance value.

Return the current tolerance.
        """
        return cls.__tolerance

    getTolerance = classmethod(getTolerance)

def toltest(tol):
    """Test that a tolerance value is valid.

toltest(tol)

The argument "tol" should be a float.
    """
    _t = tol
    if not isinstance(_t, float):
        _t = float(tol)
    if _t < TOL:
        raise ValueError, "Invalid tolerance: %g" % _t
    return _t
