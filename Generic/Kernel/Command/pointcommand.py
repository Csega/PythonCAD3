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
#This module provide a class for the point command
#
from Kernel.exception               import *
from Kernel.Command.basecommand     import *
from Kernel.GeoEntity.point         import Point

class PointCommand(BaseCommand):
    """
        this class rappresent the point command
    """
    def __init__(self, kernel):
        BaseCommand.__init__(self, kernel)
        self.exception=[ExcPoint]
        self.defaultValue=[None]
        self.message=["Give Me the Point"]
    def applyCommand(self):
        if len(self.value)!=1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        point=Point(self.value[0])
        self.document.saveEntity(point)
