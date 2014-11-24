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
# You should have received a copy of the GNU General Public Licensesegmentcmd.py
# along with PythonCAD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#This module provide a class for the arc command
#
import math

from exception import *
from Command.basecommand import *
from GeoEntity.arc import Arc

class ArcCommand(BaseCommand):
    """
        this class rappresent the arc command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception = [ExcPoint, ExcLenght, ExcAngle, ExcAngle]
        self.defaultValue =[None, 10, 0, math.pi * 2]
        self.message = ["Give Me the center Point", 
                        "Give Me the radius", 
                        "Give Me the start Angle (Could Be None)", 
                        "Give Me the span Angle (Could Be None)"]
        
    def applyCommand(self):
        if len(self.value) < 2:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        self.applyDefault()
        arg = {"ARC_0": self.value[0], 
                "ARC_1": self.value[1], 
                "ARC_2": self.value[2], 
                "ARC_3": self.value[3]
                }    
        arc = Arc(arg)
        self.document.saveEntity(arc)
