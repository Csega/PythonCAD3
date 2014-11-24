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
from GeoEntity.text import Text

class TextCommand(BaseCommand):
    """
        This class rappresent the segment command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception = [ExcPoint, ExcText, ExcAngle,ExcText ]
        self.defaultValue = [None, "Dummy Text", 0, "sw"]
        self.message = ["Give Me the first Point",
                        "Give Me The Text string",
                        "Give Me The angle", 
                        "Give me the position of the text referred to the point"]

    def applyCommand(self):
        if len(self.value) != 4:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        textArgs = {"TEXT_0": self.value[0], "TEXT_1": self.value[1], "TEXT_2": self.value[2], "TEXT_3": self.value[3]}
        text = Text(textArgs)
        self.document.saveEntity(text)
