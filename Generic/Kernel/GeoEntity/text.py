#
# Copyright (c) 2002, 2003, 2004, 2005, 2006 Art Haas
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
# basic text functionality
#

from geometricalentity import GeometricalEntity


from Kernel.GeoUtil.util import *
from Kernel.GeoEntity.point import Point
#
# Text
#
class Text(GeometricalEntity):
    """
        A class representing text in a drawing.
        A Text instance has the following attributes:
    """
    def __init__(self, kw):
        """
            Initialize a Arc/Circle.
            kw['TEXT_0'] position point must be a point 
            kw['TEXT_1'] text must be a valid text
            kw['TEXT_2'] angle must be a valid radiant float value or None
            kw['TEXT_3'] position of the text refered to the position point must be a valid string value or None
        """
        argDescription={
                        "TEXT_0": Point,
                        "TEXT_1": (float, str, unicode), 
                        "TEXT_2": (float, int), 
                        "TEXT_3": (str, unicode)
                        }
        
        if kw['TEXT_2'] == None:
            kw['TEXT_2'] = 0
        
        from Kernel.initsetting import TEXT_POSITION
        if kw['TEXT_3'] == None:
            kw['TEXT_3'] = 'sw'
        else:
            if not kw['TEXT_3'] in TEXT_POSITION:
                kw['TEXT_3'] = 'sw'
                #if kw['TEXT_3']=='':
                #    kw['TEXT_3'] = 'sw'
                #else:
                #    raise TypeError, "Argument for TEXT_3 not supported"

        GeometricalEntity.__init__(self, kw, argDescription)
        
    def __eq__(self, objTest):
        if isistance(objTest,Text):
            if(self.text == objTest.text and
                self.angle == objTest.angle and
                self.location == objTest.location and
                self.pointPosition == objTest.pointPosition):
                return True
            else:
                return False
        else:
            raise TypeError("obj must be of type Text")
    
    @property
    def info(self):
        return "Text: %s"%str(self.location) 

    @property            
    def text(self):
        """
            Get the current text within the Text.
        """
        return self['TEXT_1']
    
    @text.setter
    def text(self, text):
        """
            Set the text within the Text.
        """
        if not isinstance(text, str):
            raise TypeError("Invalid text data: " + str(text))
        self['TEXT_1'] = text
    
    @property
    def location(self):
        """
            Return the Text spatial position.
        """
        return self['TEXT_0']
    
    @location.setter
    def location(self, x, y):
        """
            Store the spatial position of the Text.
        """
        _x = get_float(x)
        _y = get_float(y)
        self['TEXT_0'] = Point(_x, _y)
    
    @property
    def angle(self):
        """
            Return the angle at which the text is drawn.
        """
        return self['TEXT_2']
    
    @angle.setter
    def angle(self, angle = None):
        """
            Set the angle at which the text block should be drawn.
        """
        self['TEXT_2']= get_float(angle)
    
    @property
    def pointPosition(self):
        """
            return the position of the textrefered to the point 
        """
        return self['TEXT_3']
    
    @pointPosition.setter
    def pointPosition(self, position):
        """
            set the position of the textrefered to the point 
        """
        from Kernel.initsetting import TEXT_POSITION
        from Kernel.exception import PythopnCadWarning
        if position in TEXT_POSITION:
            self['TEXT_3' ]= position
        raise TypeError("bad Point position")
    def getLineCount(self):
        """
            Return the number of lines of text in the Text
        """
        #
        # ideally Python itself would provide a linecount() method
        # so the temporary list would not need to be created ...
        #
        return len(self.text.splitlines())
    
    def clone(self):
        """
            Return an identical copy of a Text.
        """
        _x, _y = self.getLocation().getCoords()
        _text = self.getText()
        _tb = Text(_x, _y, _text)
        _tb.angle = self.getAngle()
        _tb.pointPosition = self.pointPosition
        return _tb
   
    def mirror(self, mirrorRef):
        """
            perform the mirror of the line
        """
        # TODO Look at the qt text implementation to understand better the text 
        # mirror 
        pass
        if not isinstance(mirrorRef, ( Segment)):
            raise TypeError("mirrorObject must be Cline Segment or a tuple of points")

        pl = self.getLocation()
        pl.mirror(mirrorRef)
    
    def rotate(self, rotationPoint, angle):
        """
            overloading of the rotate base method 
        """
        GeometricalEntity.rotate(self, rotationPoint, angle)
        self.angle = self.angle - angle
        
