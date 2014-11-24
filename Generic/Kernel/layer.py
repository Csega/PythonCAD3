#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas 2009 Matteo Boscolo
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
# classes that describe the layer 
#

class Layer(object):
    """
        this class manage a single layer
    """
    def __init__(self, layerName = None):
        """
            name            = name of the layer
            parentLayerObj  = parent layer object
            styleObj        = styleObject
        """
        self.name = layerName

    def getName(self):
        """
            get the layer name
        """
        return self.__name

    def setName(self, layerName):
        """
            set the layer name
        """
        if len(layerName) == 0:
            raise ValueError("You mast provide a name for the layer")
        
        self.__name = layerName
    
    name = property(getName, setName, None, "Get/Set The layer name")
