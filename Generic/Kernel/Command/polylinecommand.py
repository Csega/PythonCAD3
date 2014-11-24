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
#This module provide a class for the polyline command
#

from exception import *
from Command.basecommand import *
from GeoEntity.polyline import Polyline
from GeoEntity.point import Point

class PolylineCommand(BaseCommand):
    """
        this class rappresent the ellips command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception = [ExcPoint]
        self.defaultValue = [None]
        self.message = ["Give Me A Point"]
        self.raiseStop = False
        self.automaticApply = False #In case of polyline we need to stop the automatic apply
    
    def __setitem__(self, key, value):
        """
            overwrite the command to perform the stop operation
        """
        value = self.translateCmdValue(value)
        if isinstance(value, Point):
            self.value.append(value) 
            self.exception.append(ExcPoint)
            self.message.append("Give Me A Point")
            self.defaultValue.append(None)
        else:
           self.raiseStop = True 

    def applyCommand(self):
        """
            perform the write of the entity
        """
        i = 0
        args = {}
        for k in self.value:
           args["POLYLINE_%s" % str(i)] = k
           i += 1 
        pline = Polyline(args)
        self.document.saveEntity(pline)
