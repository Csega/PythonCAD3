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
# This class provide all the style operation for the pythoncadDB
#

from GeoEntity.geometricalentity import GeometricalEntity
from GeoUtil.util import getRandomString

class Style(GeometricalEntity):
        """
            This class rappresent the style in pythoncad
            objID is the object that rappresent the id in the db
        """
        def __init__(self, kw):
            """
                Initialize a Arc/Circle.
                kw['STYLE_0'] 
                kw['STYLE_1'] 
            """
            argDescription = dict([(key, str) for key in kw])
            GeometricalEntity.__init__(self, kw, argDescription)
            
            if 'STYLE_1' in self:
                if self['STYLE_1'] == None:
                    from Kernel.initsetting import getDefaultStyle
                    self.__styleProperty = getDefaultStyle()
            else:
                from Kernel.initsetting import getDefaultStyle
                self['STYLE_1'] = getDefaultStyle()
            #if self.has_key('STYLE_0'):  # old Python 2 syntax
            if 'STYLE_0' in self:
                if self['STYLE_0'] == None:
                    self.name = getRandomString()       
            else:
                self['STYLE_0'] = getRandomString()       
        
        def setName(self, name):
            """
                set the name of the style
            """
            self['STYLE_0'] = name

        def getName(self):
            """
                get the style name
            """
            return self['STYLE_0']
        
        name = property(setName, getName, None, "Style Name")
        
        def getStyleProp(self, name):
            """
                get the style property
            """
            if name in self['STYLE_1']:
                return self['STYLE_1'][name]
            else:
                return None
        
        def setStyleProp(self, name, value):
            """
                set the style property 
            """
            from Kernel.initsetting import PYTHONCAD_STYLE_ATTRIBUTES
            from Kernel.exception import EntityMissing
            if name in PYTHONCAD_STYLE_ATTRIBUTES:
                self['STYLE_1'][name] = value
            else:
                raise EntityMissing("Unable to find the property %s" % str(name))
