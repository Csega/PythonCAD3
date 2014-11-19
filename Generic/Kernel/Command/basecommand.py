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
#This module provide basic command function
#
from Kernel.exception import *
from Kernel.unitparser import *
from Kernel.GeoEntity.point import Point

class BaseCommand(object):
    """
        this class provide a base command
    """
    def __init__(self, document):
        """
            kernel is a PyCadKernel object
        """
        self.exception = []
        self.value = []
        self.message = []
        self.defaultValue = []
        self.index = 0
        self.document = document
        self.automaticApply = True
    
    def __iter__(self):
        return self
    
    def __setitem__(self, key, value):
        """
            set the value of the command
        """
        if not isinstance(value, tuple) or len(value) != 5:
            raise PyCadWrongImputData("BaseCommand : Wrong value provide a good tuple (point,entity,distance)")
        print("BaseCommand add command value", [str(x) for x in value])
        value = self.translateCmdValue(value)
        if value == None:
            print("BaseCommand.__setitem__ exept")
            raise PyCadWrongImputData("BaseCommand : Wrong imput parameter for the command")
        self.value.append(value)    
        
    def resetToDefault(self): 
        """
            Reset the command to default value
        """   
        self.value = []
        for val in self.defaultValue:
            self.value.append(val)
            
    def applyDefault(self):
        i = 0
        for value in self.value:
            if self.value[i] == None:
                self.value[i] = self.defaultValue[i]
            i += 1
        for i in range(i, self.lenght):
            self.value.append(self.defaultValue[i])
            
    def reset(self):
        """
            reset the command 
        """
        self.index=0
        self.value=[]
    
    @property
    def valueIndex(self):    
        """
            get the index of the insert value in the command
        """
        return len(self.value)
    
    def next(self):
        """
            go on with the iteration
        """
        self.index += 1
        TotNIter = len(self.exception)
        if self.index >= TotNIter:
            raise StopIteration
        return (self.exception[self.index],self.message[self.index])
    
    def activeException(self):
        """
            Return the active exception
        """
        return self.exception[self.index]

    @property
    def activeMessage(self):
        """
            get Active message
        """
        if len(self.message) > self.index:
            return self.message[self.index]
        else:
            return "Press enter to ececute the command"

    def activeDefaultValue(self):
        """
            Return the active default value
        """
        return self.defaultValue[self.index]
    
    def getActiveDefaultValue(self):
        """
            get the default value for the active command input
        """
        if self.index >= 0 and self.index <= len(self.defaultValue) - 1:
            return self.defaultValue[self.index]
        else:
            return None   

    def previus(self):
        """
            came back with the iteration
        """
        self.index -= 1
        if self.index < 0:
            self.index = 0
        return (self.exception[self.index],self.message[self.index])       
    
    def keys(self):
        """
            return all the exception key
        """
        return self.exception
        

    
    @property
    def lenght(self):
        """
            get the number of command imput value that the user have to provide
        """
        return len(self.exception)
    
    def applyCommand(self):
        """
            this method here must be defined
        """
        pass
        
    def translateCmdValue(self, value):
        """
            translate the imput value based on exception
        """
        point, entitys, distance, angle , text = value
        exitValue = None
        print("Try to except ", self.activeException())
        try:
            raise self.activeException()(None)
        except ExcPoint:
            exitValue = point
        except ExcEntity:
            if entitys:
                exitValue = str(entitys[0].ID)
        except ExcMultiEntity:
            exitValue = self.getIdsString(entitys)
        except ExcEntityPoint:
            if entitys:
                exitValue = (str(entitys[0].ID), point)
        except (ExcLenght):
            if distance:
                exitValue = self.convertToFloat(distance)
        except(ExcAngle):
            if angle:
                exitValue = convertAngle(angle)
            elif distance:
                exitValue = distance
            else:
                p0 = Point(0.0, 0.0)
                x, y = point.getCoords()
                p1 = Point(x, y)
                exitValue = Vector(p0, p1).absAng
        except(ExcInt):
            exitValue = self.convertToInt(distance)
        except(ExcText):
            exitValue = text
            if text == None:
                exitValue = ""
        except(ExcBool):
            if text == "TRUE":
                exitValue = True    
            else:
                exitValue = False
        except:
            raise PyCadWrongImputData("BaseCommand : Wrong imput parameter for the command")
        finally: return exitValue
        
    def getIdsString(self, selectedItems):
        """
            get the selected entity in terms of ids
        """
        text = None
        for ent in selectedItems:
            if not text:
                text = ''
                text += str(ent.ID)
            else:
                text += "," + str(ent.ID)
        return text   
                
    def convertToBool(self, msg):   
        """
            return an int from user
        """        
        if msg == "Yes":
            return True
        else:
            return False

    def convertToInt(self, msg):   
        """
            return an int from user
        """        
        if msg:
            return int(convertLengh(msg))
        return None
        
    def convertToFloat(self, msg):
        """
            return a float number
        """
        if msg:
            return convertLengh(msg)
        return None
        
    def convertToAngle(self, msg):
        """
            convert the angle using sympy
        """
        if msg:
            p = convertAngle(msg)
            return p
        return None
        
    def convertToPoint(self, msg):
        """
            ask at the user to imput a point 
        """
        if msg:
            p = decodePoint(msg)
            return p
        return None
