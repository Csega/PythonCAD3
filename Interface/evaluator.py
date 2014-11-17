#
# Copyright (c) ,2010 Matteo Boscolo
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
# evaluator Class to manage  command computation
#
from math import *
from Interface.pycadapp import PyCadApp
from sympy.physics import units as u

RESERVED_WORK=['self._print', 'self._error', 'self._ok','self._cadApplication','self.evaluate', 'self._eval', 'self._exec'  ]

class Evaluator(object):
    def __init__(self, printFunction):
        self._print=printFunction
        self._error='*error*'
        self._ok='*Ok*'
        self._cadApplication=PyCadApp
        
    def evaluate(self, value):
        """
            evaluate the string 
        """
        if len(value)<=0:
            return None
        for cmd in RESERVED_WORK:
            if value.count(cmd):
                return self._error + "->Reserved word"
        
            
        if value[0]=='>': # eval
            return self._eval(value[1:])
        if value[0]=='@':
            return self._exec(value[1:])
        else:
            return value
            
    def _eval(self, value):
        """
            evaluate the evaluated value
        """
        try:
            return eval(value)
        except:
            return self._error
            
    def _exec(self, value):
        """
            exec value
        """
        try:
            value=str(value).replace('print', 'self._print')
            value=str(value).replace('pyCad', 'self._cadApplication')
            exec(value)
            return self._ok
        except:
            return self._error
        
