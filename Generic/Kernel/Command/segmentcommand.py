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
#This module provide a class for the segment command
#
from exception import *
from Command.basecommand import *
from GeoEntity.segment import Segment
from GeoEntity.point import Point

class SegmentCommand(BaseCommand):
    """
        this class rappresent the segment command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception = [ExcPoint, ExcPoint]
        self.message = ["Give Me the first Point", "Give Me The Second Point"]
        self.defaultValue = [None, None]
        
    def applyCommand(self):
        if len(self.value) != 2:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        segArg = {"SEGMENT_0": self.value[0], "SEGMENT_1": self.value[1]}
        seg = Segment(segArg)
        self.document.saveEntity(seg)
        