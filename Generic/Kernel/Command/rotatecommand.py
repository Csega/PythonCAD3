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
#This module provide a class for the rotate command
#
import math

from Kernel.exception               import *
from Kernel.Command.basecommand     import *
from Kernel.GeoEntity.point         import Point

class RotateCommand(BaseCommand):
    """
        this class rappresent the rotate command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception=[ExcMultiEntity,
                        ExcPoint, 
                        ExcAngle, 
                        ExcText]
        self.defaultValue=[None, None, math.pi/2, "C"]
        self.message=[  "Select the entity to rotate or give me a the keyword Text As: (10,20,30,...)", 
                        "Give me the reference rotation point", 
                        "Give me the rotation angle[rad]", 
                        "Give me the Mode (M or None ->Move,C ->Copy)"]
              
    def performRotation(self):
        """
            perform the mirror of all the entity selected
        """
        copy=True
        if self.value[3]:
            if self.value[3]=='C':
                copy=False
        updEnts=[]
        for id in str(self.value[0]).split(','):
            dbEnt=self.document.getEntity(id)
            geoEnt=self.document.convertToGeometricalEntity(dbEnt)
            geoEnt.rotate(self.value[1], self.value[2])
            if not copy:
                dbEnt.setConstructionElements(geoEnt.getConstructionElements())
                updEnts.append(dbEnt)
            else:
                updEnts.append(geoEnt)
        return updEnts
        
    def applyCommand(self):
        """
            perform the write of the entity
        """
        if len(self.value)!=4:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        try:
            self.document.startMassiveCreation()
            for _ent in self.performRotation():
                self.document.saveEntity(_ent)
        finally:
            self.document.stopMassiveCreation()
