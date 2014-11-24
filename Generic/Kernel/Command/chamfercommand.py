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
#This module provide a class for the champfer command
#
from exception import *
from composedentity import ComposedEntity
from Command.basecommand import *
from GeoComposedEntity.chamfer import Chamfer
from GeoEntity.segment import Segment
from GeoUtil.util import getIdPoint

class ChamferCommand(BaseCommand):
    """
        this class rappresent the champfer command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception = [ExcEntityPoint,
                        ExcEntityPoint, 
                        ExcText , 
                        ExcLenght, 
                        ExcLenght 
                        ]
        self.defaultValue = [None, None, "BOTH", 10, 10]
        self.message = [  "Select the First entity or give me a the keyword Text As: (4@10,20)", 
                        "Select the Second entity or give me a the keyword Text As: (4@10,20)", 
                        "Give me trim Mode (FIRST,SECOND,BOTH,NO_TRIM)", 
                        "Give me the first Lenght", 
                        "Give me the second Lenght", 
                        ]
    
    def getEntsToSave(self):
        """
            get the chamfer segments
        """
        id0, p0 = self.value[0]
        id1, p1 = self.value[1]
       
        objEnt = []
        ent1 = self.document.getEntity(id0)
        ent2 = self.document.getEntity(id1)
        
        cel1 = ent1.getConstructionElements()
        seg1 = Segment(cel1)
        
        cel2 = ent2.getConstructionElements()
        seg2 = Segment(cel2)
        arg = {
             "OBJECTJOINT_0": seg1,
             "OBJECTJOINT_1": seg2,  
             "OBJECTJOINT_2": p0, 
             "OBJECTJOINT_3": p1, 
             "OBJECTJOINT_4": self.value[2], 
             "OBJECTJOINT_5": self.value[3], 
             "OBJECTJOINT_6": self.value[4]
             }

        cmf = Chamfer(arg)
        seg1Mod, seg2Mod, chamferSegment = cmf.getReletedComponent()
        
        _cElements1, entityType = self.document._getCelements(seg1Mod)
        _cElements2, entityType = self.document._getCelements(seg2Mod)
       
        ent1.setConstructionElements(_cElements1)
        ent2.setConstructionElements(_cElements2)
        
        objEnt.append(ent1)
        objEnt.append(ent2)
        objEnt.append(chamferSegment)
        return objEnt
        
    def applyCommand(self):
        """
            apply the champfer command
        """
        if len(self.value) != 5:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        
        try:
            self.document.startMassiveCreation()
            for _ent in self.getEntsToSave():
                self.document.saveEntity(_ent)
        finally:
            self.document.stopMassiveCreation()
       