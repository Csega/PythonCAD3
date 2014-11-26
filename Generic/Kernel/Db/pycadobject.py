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
#
# This module provide basic pythoncadObject
#
from GeoEntity.style import Style

class PyCadObject(object):
    """
        This class provide basic information usefoul for the
        db like id for exsample
    """
    def __init__(self, objId, style, eType):
        from Generic.Kernel.initsetting import OBJECT_STATE
        self.OBJECT_STATE = OBJECT_STATE
        self.__entityId = objId
        self.__state = "MODIFIE"
        self.__index = 0
        self.__visible = 1
        self.__style = style
        self.__entType = eType
        
    def setVisible(self, visible):
        """
            set the visible value
        """
        self.__visible = visible
    
    def getVisible(self):
        """
            get the visible value
        """
        return self.__visible
    visible = property(getVisible, setVisible, None, "Set/Get the entity visibiolity")

    def getId(self):
        """
            get the entity id
        """
        return self.__entityId
    
    def getState(self):
        """
            get the active entity state
        """
        return self.__state
        
    def setState(self, state):
        """
            set the active state
        """ 
        if state in self.OBJECT_STATE:
            self.__state = state
        else:
            print("Wrong argunent")
            raise 
            
    state = property(getState, setState, None, "Get/Set the state of the entity")
    
    def getIndex(self):
        """
            get the index of the revision index of the current object
        """
        return self.__index
    
    def getNewIndex(self):
        """
            Get the new index of the current entity
        """
        if index :
            self.__index += self.__index
            self.__state = self.OBJECT_STATE[0]
        else: 
            self.__index = 0
            self.__state = self.OBJECT_STATE[0]
    
    def setIndex(self, index):
        """
            Set The index of the entity
        """
        if index:
            self.__index = index
    index = property(getIndex, setIndex, "Get The new index of the current entity")
    
    def delete(self):
        """
            mark the entity to delete
        """
        self.__state = 'DELETE'
    
    def relese(self):
        """
            mark the entity as released
        """
        self.__state = 'RELEASED'

    def getStyle(self):
        """
            get the object EntityStyle
        """
        return self.__style

    def setStyle(self,style):
        """
            set/update the entitystyle
        """
        if not isinstance(style, Style):
            raise TypeError('Type error in style')
        self.__style = style

    style = property(getStyle, setStyle, None, "Get/Set the entity style")

    def getInnerStyle(self):
        """
            return the inner style of type Style
        """
        if self.getStyle():
            styleEnt = self.getStyle().getConstructionElements() 
            return styleEnt[list(styleEnt.keys())[0]]
        else:
            return None

    def setEntType(self, type):
        """
            Set the entity type
        """
        self.__entType = type
        
    def getEntityType(self):
        """
            Get the entity type
        """
        return self.__entType

    eType = property(getEntityType, setEntType, None, "Get/Set the etity type ")
