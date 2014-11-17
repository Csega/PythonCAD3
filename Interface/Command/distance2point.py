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
# This module provide a command to calculate the distance from 2 point
#

import math

from Kernel.exception                  import *
from Kernel.Command.basecommand        import *

class Distance2Point(BaseCommand):
    """
        This class rappresent the distance 2 point command
    """
    def __init__(self, document, iDocument):
        BaseCommand.__init__(self, document)
        self.iDocuemnt=iDocument
        self.exception=[ExcPoint, ExcPoint]
        self.defaultValue=[None, None]
        self.message=["Give Me the first Point", 
                        "Give Me the second Point"]
        
    def applyCommand(self):
        if len(self.value)<1:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        leng=self.value[0].dist(self.value[1])
        msg="Lenght, "+ str(leng)
        self.iDocuemnt.popUpInfo(msg)
