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
#This module provide a class for the move command
#
from Kernel.exception               import *
from Kernel.Command.basecommand     import *
from Kernel.GeoEntity.arc import Arc

class CopyCommand(BaseCommand):
    """
        this class rappresent the Move command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception=[ExcMultiEntity,
                        ExcPoint, 
                        ExcPoint]
        self.defaultValue=[None, None,None]
        self.message=[  "Select the entity to copy [or give me a the keyword Text As: (10,20,30,...)]", 
                        "Give me the base point",
                        "Give me the destination point"]
    
    def getEntsToSave(self):
        """
           get entity to save
        """
        updEnts=[]
        for id in str(self.value[0]).split(','):
            dbEnt=self.document.getEntity(id)
            geoEnt=self.document.convertToGeometricalEntity(dbEnt)
            geoEnt.move(self.value[1], self.value[2])
            updEnts.append(geoEnt)
        return updEnts
        
    def applyCommand(self):
        """
            apply the champfer command
        """
        if len(self.value)!=3:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        try:
            self.document.startMassiveCreation()
            for _ent in self.getEntsToSave():
                self.document.saveEntity(_ent)
        finally:
            self.document.stopMassiveCreation()
       
