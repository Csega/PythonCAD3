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
#This module provide a class for the Trim command
#
from Kernel.exception               import *
from Kernel.Command.basecommand     import *
from Kernel.GeoEntity               import *
from Kernel.GeoUtil.intersection    import *
from Kernel.GeoUtil.util            import *

class TrimCommand(BaseCommand):
    """
        this class rappresent the Trim command
    """
    def __init__(self, document):
        BaseCommand.__init__(self, document)
        self.exception=[ExcText,
                        ExcText,  
                        ExcText]
        self.defaultValue=[None, None,"BOTH"]
        self.message=[  "Geve me the First entity", 
                        "Give me the Second entity",
                        "Give me a point near the First entity", 
                        "Give me a point near the Second entity", 
                        "Give me The Trim Mode ((FIRST,SECOND,BOTH)"]

    def performTrim(self):
        """
            get the chamfer segments
        """
        updEnts=[]
        dbEnt1=self.document.getEntity(self.value[0])
        geoEnt1=self.document.convertToGeometricalEntity(dbEnt1)
        dbEnt2=self.document.getEntity(self.value[1])
        geoEnt2=self.document.convertToGeometricalEntity(dbEnt2)
        intPoint=findSegmentExtendedIntersectionPoint(geoEnt1, geoEnt2)
        if len(intPoint)<=0:
            raise PythopnCadWarning("No intersection Found") 
        
        if dbEnt1.eType=="SEGMENT":     
            geoEntTrim1=updateSegment(geoEnt1, self.value[2], intPoint[0])
            
        if dbEnt2.eType=="SEGMENT":     
            geoEntTrim2=updateSegment(geoEnt2, self.value[3], intPoint[0])
        
        if self.value[4]=='FIRST':
            dbEnt1.setConstructionElements(geoEntTrim1.getConstructionElements())
            updEnts.append(dbEnt1)
        elif self.value[4]=='SECOND':
            dbEnt2.setConstructionElements(geoEntTrim2.getConstructionElements())
            updEnts.append(dbEnt2)            
        else:
            dbEnt1.setConstructionElements(geoEntTrim1.getConstructionElements())
            updEnts.append(dbEnt1)
            dbEnt2.setConstructionElements(geoEntTrim2.getConstructionElements())
            updEnts.append(dbEnt2) 
        return updEnts
        
    def applyCommand(self):
        """
            apply the trim command
        """
        if len(self.value)!=5:
            raise PyCadWrongImputData("Wrong number of imput parameter")
        try:
            self.document.startMassiveCreation()
            for _ent in self.performTrim():
                self.document.saveEntity(_ent)
        finally:
            self.document.stopMassiveCreation()
       
