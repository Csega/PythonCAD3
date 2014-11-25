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
# generic dimension classes
#

import math
import sys
import types

from GeoEntity.text import text
from GeoEntity.point import point
from GeoEntity.arc import arc
from GeoUtil.util import util
from GeoUtil.tolerance import tolerance

_dtr = math.pi / 180.0
_rtd = 180.0 / math.pi

class DimString(text.TextBlock):
    """A class for the visual presentation of the dimensional value.

The DimString class is used to present the numerical display for
the dimension. A DimString object is derived from the text.TextBlock
class, so it shares all of that classes methods and attributes.

The DimString class has the following additional properties:

prefix: A prefix prepended to the dimension text
suffix: A suffix appended to the dimension text
units: The units the dimension text will display
precision: The displayed dimension precision
print_zero: Displayed dimensions will have a leading 0 if needed
print_decimal: Displayed dimensions will have a trailing decimal point

The DimString class has the following additional methods:

{get/set}Prefix(): Get/Set the text preceding the dimension value.
{get/set}Suffix(): Get/Set the text following the dimension value.
{get/set}Units(): Define what units the dimension will be in.
{get/set}Precision(): Get/Set how many fractional digits are displayed.
{get/set}PrintZero(): Get/Set whether or not a dimension less than one
                      unit long should have a leading 0 printed
{get/set}PrintDecimal(): Get/Set whether or not a dimension with 0
                         fractional digits prints out the decimal point.
{get/set}Dimension(): Get/Set the dimension using the DimString

The DimString class has the following classmethods:

{get/set}DefaultTextStyle(): Get/Set the default TextStyle for the class.
    """

    __defstyle = None

    __messages = {
        'prefix_changed' : True,
        'suffix_changed' : True,
        'units_changed' : True,
        'precision_changed' : True,
        'print_zero_changed' : True,
        'print_decimal_changed' : True,
        'dimension_changed' : True,
        }

    def __init__(self, x, y, **kw):
        """Initialize a DimString object

ds = DimString(x, y, **kw)

Arguments 'x' and 'y' should be floats. Various keyword arguments can
also be used:

text: Displayed text
textstyle: The default textstyle
family: Font family
style: Font style
weight: Font weight
color: Text color
size: Text size
angle: Text angle
align: Text alignment
prefix: Default prefix
suffix: Default suffix
units: Displayed units
precision: Displayed precision of units
print_zero: Boolean to print a leading '0'
print_decimal: Boolean to print a leading '.'

By default, a DimString object has the following values ...

prefix: Empty string
suffix: Empty string
unit: Millimeters
precision: 3 decimal places
print zero: True
print decimal: True
        """
        _text = u''
        if 'text' in kw:
            _text = kw['text']
        _tstyle = self.getDefaultTextStyle()
        if 'textstyle' in kw:
            _tstyle = kw['textstyle']
            del kw['textstyle']
        _prefix = u''
        if 'prefix' in kw:
            _prefix = kw['prefix']
            if not isinstance(_prefix, types.StringTypes):
                raise TypeError, "Invalid prefix type: " + `type(_prefix)`
        _suffix = u''
        if 'suffix' in kw:
            _suffix = kw['suffix']
            if not isinstance(_suffix, types.StringTypes):
                raise TypeError, "Invalid suffix type: " + `type(_suffix)`
        _unit = units.MILLIMETERS
        if 'units' in kw:
            _unit = kw['units']
        _prec = 3
        if 'precision' in kw:
            _prec = kw['precision']
            if not isinstance(_prec, int):
                raise TypeError, "Invalid precision type: " + `type(_prec)`
            if _prec < 0 or _prec > 15:
                raise ValueError, "Invalid precision: %d" % _prec
        _pz = True
        if 'print_zero' in kw:
            _pz = kw['print_zero']
            util.test_boolean(_pz)
        _pd = True
        if 'print_decimal' in kw:
            _pd = kw['print_decimal']
            util.test_boolean(_pd)
        super(DimString, self).__init__(x, y, _text, textstyle=_tstyle, **kw)
        self.__prefix = _prefix
        self.__suffix = _suffix
        self.__unit = units.Unit(_unit)
        self.__precision = _prec
        self.__print_zero = _pz
        self.__print_decimal = _pd
        self.__dim = None

    def getDefaultTextStyle(cls):
        if cls.__defstyle is None:
            _s = text.TextStyle(u'Default Dimension Text Style',
                                color=color.Color(0xffffff),
                                align=text.TextStyle.ALIGN_CENTER)
            cls.__defstyle = _s
        return cls.__defstyle

    getDefaultTextStyle = classmethod(getDefaultTextStyle)

    def setDefaultTextStyle(cls, s):
        if not isinstance(s, text.TextStyle):
            raise TypeError, "Invalid TextStyle: " + `type(s)`
        cls.__defstyle = s

    setDefaultTextStyle = classmethod(setDefaultTextStyle)

    def finish(self):
        """Finalization for  DimString instances.

finish()
        """
        if self.__dim is not None:
            self.__dim = None
        super(DimString, self).finish()

    def getValues(self):
        """Return values comprising the DimString.

getValues()

This method extends the TextBlock::getValues() method.
        """
        _data = super(DimString, self).getValues()
        _data.setValue('type', 'dimstring')
        _data.setValue('prefix', self.__prefix)
        _data.setValue('suffix', self.__suffix)
        _data.setValue('units', self.__unit.getStringUnit())
        _data.setValue('precision', self.__precision)
        _data.setValue('print_zero', self.__print_zero)
        _data.setValue('print_decimal', self.__print_decimal)
        return _data

    def getParent(self):
        """Get the entity containing the DimString.

getParent()

This method overrides the Entity::getParent() call.
        """
        _parent = None
        if self.__dim is not None:
            _parent = self.__dim.getParent()
        return _parent
    
    def setLocation(self, x, y):
        """Set the location of the DimString.

setLocation(x, y)

Arguments 'x' and 'y' should be floats. This method extends
the TextBlock::setLocation() method.
        """
        #
        # the DimString location is defined in relation to
        # the position defined by the Dimension::setLocation()
        # call, so don't bother sending out 'moved' or 'modified'
        # messages
        #
        self.mute()
        try:
            super(DimString, self).setLocation(x, y)
        finally:
            self.unmute()

    def getPrefix(self):
        """Return the prefix for the DimString object.

getPrefix()
        """
        return self.__prefix

    def setPrefix(self, prefix=None):
        """Set the prefix for the DimString object.

setPrefix([prefix])

Invoking this method without arguments sets the prefix
to an empty string, or to the DimStyle value in the associated
Dimension if one is set for the DimString. When an argument
is passed, the argument should be a Unicode string.
        """
        if self.isLocked():
            raise RuntimeError, "Setting prefix not allowed - object locked."
        _p = prefix
        if _p is None:
            _p = u''
            if self.__dim is not None:
                _p = self.__dim.getStyleValue(self, 'prefix')
        if not isinstance(_p, unicode):
            _p = unicode(prefix)
        _op = self.__prefix
        if _op != _p:
            self.startChange('prefix_changed')
            self.__prefix = _p
            self.endChange('prefix_changed')
            self.setBounds()
            self.sendMessage('prefix_changed', _op)
            self.modified()

    prefix = property(getPrefix, setPrefix, None, 'Dimension string prefix')

    def getSuffix(self):
        """Return the suffix for the DimString object.

getSuffix()
        """
        return self.__suffix

    def setSuffix(self, suffix=None):
        """Set the suffix for the DimString object.

setSuffix([suffix])

Invoking this method without arguments sets the suffix
to an empty string, or to the DimStyle value in the associated
Dimension if one is set for the DimString.. When an argument
is passed, the argument should be a Unicode string.
        """
        if self.isLocked():
            raise RuntimeError, "Setting suffix not allowed - object locked."
        _s = suffix
        if _s is None:
            _s = u''
            if self.__dim is not None:
                _s = self.__dim.getStyleValue(self, 'suffix')
        if not isinstance(_s, unicode):
            _s = unicode(suffix)
        _os = self.__suffix
        if _os != _s:
            self.startChange('suffix_changed')
            self.__suffix = _s
            self.endChange('suffix_changed')
            self.setBounds()
            self.sendMessage('suffix_changed', _os)
            self.modified()

    suffix = property(getSuffix, setSuffix, None, 'Dimension string suffix')

    def getPrecision(self):
        """Return the number of decimal points used for the DimString.

getPrecision()
        """
        return self.__precision

    def setPrecision(self, precision=None):
        """Set the number of decimal points used for the DimString.

setPrecision([p])

The valid range of p is 0 <= p <= 15. Invoking this method without
arguments sets the precision to 3, or to the DimStyle value in the
associated Dimension if one is set for the DimString..
        """
        if self.isLocked():
            raise RuntimeError, "Setting precision not allowed - object locked."
        _p = precision
        if _p is None:
            _p = 3
            if self.__dim is not None:
                _p = self.__dim.getStyleValue(self, 'precision')
        if not isinstance(_p, int):
            raise TypeError, "Invalid precision type: " + `type(_p)`
        if _p < 0 or _p > 15:
            raise ValueError, "Invalid precision: %d" % _p
        _op = self.__precision
        if _op != _p:
            self.startChange('precision_changed')
            self.__precision = _p
            self.endChange('precision_changed')
            self.setBounds()
            self.sendMessage('precision_changed', _op)
            self.modified()

    precision = property(getPrecision, setPrecision, None,
                         'Dimension precision')

    def getUnits(self):
        """Return the current units used in the DimString().

getUnits()
        """
        return self.__unit.getUnit()

    def setUnits(self, unit=None):
        """The the units for the DimString.

setUnits([unit])

The value units are given in the units module. Invoking this
method without arguments sets the units to millimeters, or
to the DimStyle value of the associated Dimension if one
is set for the DimString.
        """
        _u = unit
        if _u is None:
            _u = units.MILLIMETERS
            if self.__dim is not None:
                _u = self.__dim.getStyleValue(self, 'units')
        _ou = self.__unit.getUnit()
        if _ou != _u:
            self.startChange('units_changed')
            self.__unit.setUnit(_u)
            self.endChange('units_changed')
            self.setBounds()
            self.sendMessage('units_changed', _ou)
            self.modified()

    units = property(getUnits, setUnits, None, 'Dimensional units.')

    def getPrintZero(self):
        """Return whether or not a leading 0 is printed for the DimString.

getPrintZero()
        """
        return self.__print_zero

    def setPrintZero(self, print_zero=None):
        """Set whether or not a leading 0 is printed for the DimString.

setPrintZero([pz])

Invoking this method without arguments sets the value to True,
or to the DimStyle value of the associated Dimension if one is
set for the DimString. If called with an argument, the argument
should be either True or False.
        """
        _pz = print_zero
        if _pz is None:
            _pz = True
            if self.__dim is not None:
                _pz = self.__dim.getStyleValue(self, 'print_zero')
        util.test_boolean(_pz)
        _flag = self.__print_zero
        if _flag is not _pz:
            self.startChange('print_zero_changed')
            self.__print_zero = _pz
            self.endChange('print_zero_changed')
            self.setBounds()
            self.sendMessage('print_zero_changed', _flag)
            self.modified()

    print_zero = property(getPrintZero, setPrintZero, None,
                          'Print a leading 0 for decimal dimensions')

    def getPrintDecimal(self):
        """Return whether or not the DimString will print a trailing decimal.

getPrintDecimal()
        """
        return self.__print_decimal

    def setPrintDecimal(self, print_decimal=None):
        """Set whether or not the DimString will print a trailing decimal.

setPrintDecimal([pd])

Invoking this method without arguments sets the value to True, or
to the DimStyle value of the associated Dimension if one is set
for the DimString. If called with an argument, the argument should
be either True or False.
        """
        _pd = print_decimal
        if _pd is None:
            _pd = True
            if self.__dim is not None:
                _pd = self.__dim.getStyleValue(self, 'print_decimal')
        util.test_boolean(_pd)
        _flag = self.__print_decimal
        if _flag is not _pd:
            self.startChange('print_decimal_changed')
            self.__print_decimal = _pd
            self.endChange('print_decimal_changed')
            self.setBounds()
            self.sendMessage('print_decimal_changed', _flag)
            self.modified()

    print_decimal = property(getPrintDecimal, setPrintDecimal, None,
                             'Print a decimal point after the dimension value')

    def getDimension(self):
        """Return the dimension using the Dimstring.

getDimension()

This method can return None if there is not Dimension association set
for the DimString.
        """
        return self.__dim

    def setDimension(self, dim, adjust):
        """Set the dimension using this DimString.

setDimension(dim, adjust)

Argument 'dim' must be a Dimension or None, and argument
'adjust' must be a Boolean. Argument 'adjust' is only used
if a Dimension is passed for the first argument.
        """
        _dim = dim
        if _dim is not None and not isinstance(_dim, Dimension):
            raise TypeError, "Invalid dimension: " + `type(_dim)`
        util.test_boolean(adjust)
        _d = self.__dim
        if _d is not _dim:
            self.startChange('dimension_changed')
            self.__dim = _dim
            self.endChange('dimension_changed')
            if _dim is not None and adjust:
                self.setPrefix()
                self.setSuffix()
                self.setPrecision()
                self.setUnits()
                self.setPrintZero()
                self.setPrintDecimal()
                self.setFamily()
                self.setStyle()
                self.setWeight()
                self.setColor()
                self.setSize()
                self.setAngle()
                self.setAlignment()
            self.sendMessage('dimension_changed', _d)
            self.modified()
        if self.__dim is not None:
            self.setParent(self.__dim.getParent())

#
# extend the TextBlock set methods to use the values
# found in a DimStyle if one is available
#

    def setFamily(self, family=None):
        """Set the font family for the DimString.

setFamily([family])

Calling this method without an argument will set the
family to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _family = family
        if _family is None and self.__dim is not None:
            _family = self.__dim.getStyleValue(self, 'font_family')
        super(DimString, self).setFamily(_family)

    def setStyle(self, style=None):
        """Set the font style for the DimString.

setStyle([style])

Calling this method without an argument will set the
font style to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _style = style
        if _style is None and self.__dim is not None:
            _style = self.__dim.getStyleValue(self, 'font_style')
        super(DimString, self).setStyle(_style)

    def setWeight(self, weight=None):
        """Set the font weight for the DimString.

setWeight([weight])

Calling this method without an argument will set the
font weight to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _weight = weight
        if _weight is None and self.__dim is not None:
            _weight = self.__dim.getStyleValue(self, 'font_weight')
        super(DimString, self).setWeight(_weight)

    def setColor(self, color=None):
        """Set the font color for the DimString.

setColor([color])

Calling this method without an argument will set the
font color to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _color = color
        if _color is None and self.__dim is not None:
            _color = self.__dim.getStyleValue(self, 'color')
        super(DimString, self).setColor(_color)

    def setSize(self, size=None):
        """Set the text size for the DimString.

setSize([size])

Calling this method without an argument will set the
text size to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _size = size
        if _size is None and self.__dim is not None:
            _size = self.__dim.getStyleValue(self, 'size')
        super(DimString, self).setSize(_size)

    def setAngle(self, angle=None):
        """Set the text angle for the DimString.

setAngle([angle])

Calling this method without an argument will set the
text angle to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _angle = angle
        if _angle is None and self.__dim is not None:
            _angle = self.__dim.getStyleValue(self, 'angle')
        super(DimString, self).setAngle(_angle)

    def setAlignment(self, align=None):
        """Set the text alignment for the DimString.

setAlignment([align])

Calling this method without an argument will set the
text alignment to that given in the DimStyle of the associated
Dimension if one is set for this DimString.
        """
        _align = align
        if _align is None and self.__dim is not None:
            _align = self.__dim.getStyleValue(self, 'alignment')
        super(DimString, self).setAlignment(_align)

    def setText(self, text):
        """Set the text in the DimString.

This method overrides the setText method in the TextBlock.
        """
        pass

    def formatDimension(self, dist):
        """Return a formatted numerical value for a dimension.

formatDimension(dist)

The argument 'dist' should be a float value representing the
distance in millimeters. The returned value will have the
prefix prepended and suffix appended to the numerical value
that has been formatted with the precision.
        """
        _d = abs(util.get_float(dist))
        _fmtstr = u"%%#.%df" % self.__precision
        _dstr = _fmtstr % self.__unit.fromMillimeters(_d)
        if _d < 1.0 and self.__print_zero is False:
            _dstr = _dstr[1:]
        if _dstr.endswith('.') and self.__print_decimal is False:
            _dstr = _dstr[:-1]
        _text = self.__prefix + _dstr + self.__suffix
        #
        # don't send out 'text_changed' or 'modified' messages
        #
        self.mute()
        try:
            super(DimString, self).setText(_text)
        finally:
            self.unmute()
        return _text

    def sendsMessage(self, m):
        if m in DimString.__messages:
            return True
        return super(DimString, self).sendsMessage(m)

class DimBar(entity.Entity):
    """The class for the dimension bar.

A dimension bar leads from the point the dimension references
out to, and possibly beyond, the point where the dimension
text bar the DimBar to another DimBar. Linear,
horizontal, vertical, and angular dimension will have two
dimension bars; radial dimensions have none.

The DimBar class has the following methods:

getEndpoints(): Get the x/y position of the DimBar start and end
{get/set}FirstEndpoint(): Get/Set the starting x/y position of the DimBar.
{get/set}SecondEndpoint(): Get/Set the ending x/y position of the DimBar.
getAngle(): Get the angle at which the DimBar slopes
getSinCosValues(): Get trig values used for transformation calculations.
    """

    __messages = {
        'attribute_changed' : True,
        }
        
    def __init__(self, x1=0.0, y1=0.0, x2=0.0, y2=0.0, **kw):
        """Initialize a DimBar.

db = DimBar([x1, y1, x2, y2])

By default all the arguments are 0.0. Any arguments passed to this
method should be float values.
        """
        _x1 = util.get_float(x1)
        _y1 = util.get_float(y1)
        _x2 = util.get_float(x2)
        _y2 = util.get_float(y2)
        super(DimBar, self).__init__(**kw)
        self.__ex1 = _x1
        self.__ey1 = _y1
        self.__ex2 = _x2
        self.__ey2 = _y2

    def getEndpoints(self):
        """Return the coordinates of the DimBar endpoints.

getEndpoints()

This method returns two tuples, each containing two float values.
The first tuple gives the x/y coordinates of the DimBar start,
the second gives the coordinates of the DimBar end.
        """
        _ep1 = (self.__ex1, self.__ey1)
        _ep2 = (self.__ex2, self.__ey2)
        return _ep1, _ep2

    def setFirstEndpoint(self, x, y):
        """Set the starting coordinates for the DimBar

setFirstEndpoint(x, y)

Arguments x and y should be float values.
        """
        if self.isLocked():
            raise RuntimeError, "Setting endpoint not allowed - object locked."
        _x = util.get_float(x)
        _y = util.get_float(y)
        _sx = self.__ex1
        _sy = self.__ey1
        if abs(_sx - _x) > 1e-10 or abs(_sy - _y) > 1e-10:
            self.__ex1 = _x
            self.__ey1 = _y
            self.sendMessage('attribute_changed', 'endpoint', _sx, _sy,
                             self.__ex2, self.__ey2)
            self.modified()

    def getFirstEndpoint(self):
        """Return the starting coordinates of the DimBar.

getFirstEndpoint()

This method returns a tuple giving the x/y coordinates.
        """
        return self.__ex1, self.__ey1

    def setSecondEndpoint(self, x, y):
        """Set the ending coordinates for the DimBar

setSecondEndpoint(x, y)

Arguments x and y should be float values.
        """
        if self.isLocked():
            raise RuntimeError, "Setting endpoint not allowed - object locked."
        _x = util.get_float(x)
        _y = util.get_float(y)
        _sx = self.__ex2
        _sy = self.__ey2
        if abs(_sx - _x) > 1e-10 or abs(_sy - _y) > 1e-10:
            self.__ex2 = _x
            self.__ey2 = _y
            self.sendMessage('attribute_changed', 'endpoint',
                             self.__ex1, self.__ey1, _sx, _sy)
            self.modified()

    def getSecondEndpoint(self):
        """Return the ending coordinates of the DimBar.

getSecondEndpoint()

This method returns a tuple giving the x/y coordinates.
        """
        return self.__ex2, self.__ey2

    def getAngle(self):
        """Return the angle at which the DimBar lies.

getAngle()

This method returns a float value giving the angle of inclination
of the DimBar.

The value returned will be a positive value less than 360.0.
        """
        _x1 = self.__ex1
        _y1 = self.__ey1
        _x2 = self.__ex2
        _y2 = self.__ey2
        if abs(_x2 - _x1) < 1e-10 and abs(_y2 - _y1) < 1e-10:
            raise ValueError, "Endpoints are equal"
        if abs(_x2 - _x1) < 1e-10: # vertical
            if _y2 > _y1:
                _angle = 90.0
            else:
                _angle = 270.0
        elif abs(_y2 - _y1) < 1e-10: # horizontal
            if _x2 > _x1:
                _angle = 0.0
            else:
                _angle = 180.0
        else:
            _angle = _rtd * math.atan2((_y2 - _y1), (_x2 - _x1))
            if _angle < 0.0:
                _angle = _angle + 360.0
        return _angle

    def getSinCosValues(self):
        """Return sin()/cos() values based on the DimBar slope

getSinCosValues()

This method returns a tuple of two floats. The first value is
the sin() value, the second is the cos() value.
        """
        _x1 = self.__ex1
        _y1 = self.__ey1
        _x2 = self.__ex2
        _y2 = self.__ey2
        if abs(_x2 - _x1) < 1e-10: # vertical
            _cosine = 0.0
            if _y2 > _y1:
                _sine = 1.0
            else:
                _sine = -1.0
        elif abs(_y2 - _y1) < 1e-10: # horizontal
            _sine = 0.0
            if _x2 > _x1:
                _cosine = 1.0
            else:
                _cosine = -1.0
        else:
            _angle = math.atan2((_y2 - _y1), (_x2 - _x1))
            _sine = math.sin(_angle)
            _cosine = math.cos(_angle)
        return _sine, _cosine

    def sendsMessage(self, m):
        if m in DimBar.__messages:
            return True
        return super(DimBar, self).sendsMessage(m)

class DimCrossbar(DimBar):
    """The class for the Dimension crossbar.

The DimCrossbar class is drawn between two DimBar objects for
horizontal, vertical, and generic linear dimensions. The dimension
text is place over the DimCrossbar object. Arrow heads, circles, or
slashes can be drawn at the intersection of the DimCrossbar and
the DimBar if desired. These objects are called markers.

The DimCrossbar class is derived from the DimBar class so it shares
all the methods of that class. In addition the DimCrossbar class has
the following methods:

{set/get}FirstCrossbarPoint(): Set/Get the initial location of the crossbar.
{set/get}SecondCrossbarPoint(): Set/Get the ending location of the crossbar.
getCrossbarPoints(): Get the location of the crossbar endpoints.
clearMarkerPoints(): Delete the stored coordintes of the dimension markers.
storeMarkerPoint(): Save a coordinate pair of the dimension marker.
getMarkerPoints(): Return the coordinates of the dimension marker.
    """
    __messages = {}
    
    def __init__(self, **kw):
        """Initialize a DimCrossbar object.

dcb = DimCrossbar()

This method takes no arguments.
        """
        super(DimCrossbar, self).__init__(**kw)
        self.__mx1 = 0.0
        self.__my1 = 0.0
        self.__mx2 = 0.0
        self.__my2 = 0.0
        self.__mpts = []

    def setFirstCrossbarPoint(self, x, y):
        """Store the initial endpoint of the DimCrossbar.

setFirstCrossbarPoint(x, y)

Arguments x and y should be floats.
        """
        if self.isLocked():
            raise RuntimeError, "Setting crossbar point not allowed - object locked."
        _x = util.get_float(x)
        _y = util.get_float(y)
        _sx = self.__mx1
        _sy = self.__my1
        if abs(_sx - _x) > 1e-10 or abs(_sy - _y) > 1e-10:
            self.__mx1 = _x
            self.__my1 = _y
            self.sendMessage('attribute_changed', 'barpoint', _sx, _sy,
                             self.__mx2, self.__my2)
            self.modified()

    def getFirstCrossbarPoint(self):
        """Return the initial coordinates of the DimCrossbar.

getFirstCrossbarPoint()

This method returns a tuple of two floats giving the x/y coordinates.
        """
        return self.__mx1, self.__my1

    def setSecondCrossbarPoint(self, x, y):
        """Store the terminal endpoint of the DimCrossbar.

setSecondCrossbarPoint(x, y)

Arguments 'x' and 'y' should be floats.
        """
        if self.isLocked():
            raise RuntimeError, "Setting crossbar point not allowed - object locked"
        _x = util.get_float(x)
        _y = util.get_float(y)
        _sx = self.__mx2
        _sy = self.__my2
        if abs(_sx - _x) > 1e-10 or abs(_sy - _y) > 1e-10:
            self.__mx2 = _x
            self.__my2 = _y
            self.sendMessage('attribute_changed', 'barpoint',
                             self.__mx1, self.__my1, _sx, _sy)
            self.modified()

    def getSecondCrossbarPoint(self):
        """Return the terminal coordinates of the DimCrossbar.

getSecondCrossbarPoint()

This method returns a tuple of two floats giving the x/y coordinates.
        """
        return self.__mx2, self.__my2

    def getCrossbarPoints(self):
        """Return the endpoints of the DimCrossbar.

getCrossbarPoints()

This method returns two tuples, each tuple containing two float
values giving the x/y coordinates.
        """
        _mp1 = (self.__mx1, self.__my1)
        _mp2 = (self.__mx2, self.__my2)
        return _mp1, _mp2

    def clearMarkerPoints(self):
        """Delete the stored location of any dimension markers.

clearMarkerPoints()
        """
        del self.__mpts[:]

    def storeMarkerPoint(self, x, y):
        """Save a coordinate pair of the current dimension marker.

storeMarkerPoint(x, y)

Arguments 'x' and 'y' should be floats. Each time this method is invoked
the list of stored coordinates is appended with the values given as
arguments.
        """
        _x = util.get_float(x)
        _y = util.get_float(y)
        self.__mpts.append((_x, _y))

    def getMarkerPoints(self):
        """Return the stored marker coordinates.

getMarkerPoints()

This method returns a list of coordinates stored with storeMarkerPoint().
Each item in the list is a tuple holding two float values - the x/y
coordinate of the point.
        """
        return self.__mpts[:]

    def sendsMessage(self, m):
        if m in DimCrossbar.__messages:
            return True
        return super(DimCrossbar, self).sendsMessage(m)

class DimCrossarc(DimCrossbar):
    """The class for specialized crossbars for angular dimensions.

The DimCrossarc class is meant to be used only with angular dimensions.
As an angular dimension has two DimBar objects that are connected
with an arc. The DimCrossarc class is derived from the DimCrossbar
class so it shares all the methods of that class. The DimCrossarc
class has the following additional methods:

{get/set}Radius(): Get/Set the radius of the arc.
{get/set}StartAngle(): Get/Set the arc starting angle.
{get/set}EndAngle(): Get/Set the arc finishing angle.
    """

    __messages = {
        'arcpoint_changed' : True,
        'radius_changed' : True,
        'start_angle_changed' : True,
        'end_angle_changed' : True,
        }
        
    def __init__(self, radius=0.0, start=0.0, end=0.0, **kw):
        """Initialize a DimCrossarc object.

dca = DimCrossarc([radius, start, end])

By default the arguments are all 0.0. Any arguments passed to
this method should be floats.
        """
        super(DimCrossarc, self).__init__(**kw)
        _r = util.get_float(radius)
        if _r < 0.0:
            raise ValueError, "Invalid radius: %g" % _r
        _start = util.make_c_angle(start)
        _end = util.make_c_angle(end)
        self.__radius = _r
        self.__start = _start
        self.__end = _end

    def getRadius(self):
        """Return the radius of the arc.

getRadius()

This method returns a float value.
        """
        return self.__radius

    def setRadius(self, radius):
        """Set the radius of the arc.

setRadius(radius)

Argument 'radius' should be a float value greater than 0.0.
        """
        if self.isLocked():
            raise RuntimeError, "Setting radius not allowed - object locked."
        _r = util.get_float(radius)
        if _r < 0.0:
            raise ValueError, "Invalid radius: %g" % _r
        _sr = self.__radius
        if abs(_sr - _r) > 1e-10:
            self.startChange('radius_changed')
            self.__radius = _r
            self.endChange('radius_changed')
            self.sendMessage('radius_changed', _sr)
            self.modified()

    def getStartAngle(self):
        """Return the arc starting angle.

getStartAngle()

This method returns a float.
        """
        return self.__start

    def setStartAngle(self, angle):
        """Set the starting angle of the arc.

setStartAngle(angle)

Argument angle should be a float value.
        """
        if self.isLocked():
            raise RuntimeError, "Setting start angle not allowed - object locked."
        _sa = self.__start
        _angle = util.make_c_angle(angle)
        if abs(_sa - _angle) > 1e-10:
            self.startChange('start_angle_changed')
            self.__start = _angle
            self.endChange('start_angle_changed')
            self.sendMessage('start_angle_changed', _sa)
            self.modified()

    def getEndAngle(self):
        """Return the arc ending angle.

getEndAngle()

This method returns a float.
        """
        return self.__end

    def setEndAngle(self, angle):
        """Set the ending angle of the arc.

setEndAngle(angle)

Argument angle should be a float value.
        """
        if self.isLocked():
            raise RuntimeError, "Setting end angle not allowed - object locked."
        _ea = self.__end
        _angle = util.make_c_angle(angle)
        if abs(_ea - _angle) > 1e-10:
            self.startChange('end_angle_changed')
            self.__end = _angle
            self.endChange('end_angle_changed')
            self.sendMessage('end_angle_changed', _ea)
            self.modified()

    def getAngle(self):
        pass # override the DimBar::getAngle() method

    def getSinCosValues(self):
        pass # override the DimBar::getSinCosValues() method

    def sendsMessage(self, m):
        if m in DimCrossarc.__messages:
            return True
        return super(DimCrossarc, self).sendsMessage(m)

class Dimension(entity.Entity):
    """The base class for Dimensions

A Dimension object is meant to be a base class for specialized
dimensions.

Every Dimension object holds two DimString objects, so any
dimension can be displayed with two separate formatting options
and units.

A Dimension has the following methods

{get/set}DimStyle(): Get/Set the DimStyle used for this Dimension.
getPrimaryDimstring(): Return the DimString used for formatting the
                       Primary dimension.
getSecondaryDimstring(): Return the DimString used for formatting the
                         Secondary dimension.
{get/set}EndpointType(): Get/Set the type of endpoints used in the Dimension
{get/set}EndpointSize(): Get/Set the size of the dimension endpoints
{get/set}DualDimMode(): Get/Set whether or not to display both the Primary
                        and Secondary DimString objects
{get/set}Offset(): Get/Set how far from the dimension endpoints to draw
                   dimension lines at the edges of the dimension.
{get/set}Extension(): Get/Set how far past the dimension crossbar line
                      to draw.
{get/set}Position(): Get/Set where the dimensional values are placed on the
                     dimension cross bar.
{get/set}Color(): Get/Set the color used to draw the dimension lines.
{get/set}Location(): Get/Set where to draw the dimensional values.
{get/set}PositionOffset(): Get/Set the dimension text offset when the text is
                           above or below the crossbar/crossarc
{get/set}DualModeOffset(): Get/Set the text offset for spaceing the two
                           dimension strings above and below the bar
                           separating the two dimensions
{get/set}Thickness(): Get/Set the Dimension thickness.
{get/set}Scale(): Get/Set the Dimension scaling factor.
getStyleValue(): Return the DimStyle value for some option
getDimensions(): Return the formatted dimensional values in this Dimension.
inRegion(): Return if the dimension is visible within some are.
calcDimValues(): Calculate the dimension lines endpoints.
mapCoords(): Return the coordinates on the dimension within some point.
onDimension(): Test if an x/y coordinate pair hit the dimension lines.
getBounds(): Return the minma and maximum locations of the dimension.

The Dimension class has the following classmethods:

{get/set}DefaultDimStyle(): Get/Set the default DimStyle for the class.
getEndpointTypeAsString(): Return the endpoint type as a string for a value.
getEndpointTypeFromString(): Return the endpoint type value given a string.
getEndpointTypeStrings(): Get the endpoint types values as strings.
getEndpointTypeValues(): Get the endpoint type values.
getPositionAsString(): Return the text position as a string for a value.
getPositionFromString(): Return the text postion value given a string.
getPositionStrings(): Get the text position values as strings.
getPositionValues(): Get the text position values.

    """
    #
    # Endpoint
    #
    DIM_ENDPT_NONE= 0
    DIM_ENDPT_ARROW = 1
    DIM_ENDPT_FILLED_ARROW = 2
    DIM_ENDPT_SLASH = 3
    DIM_ENDPT_CIRCLE = 4

    #
    # Dimension position on dimline
    #
    DIM_TEXT_POS_SPLIT = 0
    DIM_TEXT_POS_ABOVE = 1
    DIM_TEXT_POS_BELOW = 2

    __defstyle = None

    __messages = {
        'dimstyle_changed' : True,
        'endpoint_type_changed' : True,
        'endpoint_size_changed' : True,
        'dual_mode_changed' : True,
        'offset_changed' : True,
        'extension_changed' : True,
        'position_changed' : True,
        'position_offset_changed' : True,
        'dual_mode_offset_changed' : True,
        'color_changed' :  True,
        'thickness_changed' : True,
        'scale_changed' : True,
        'location_changed' : True,
        'dimstring_changed' : True,
        'moved' : True,
        }
        
    def __init__(self, x, y, dimstyle=None, **kw):
        """Initialize a Dimension object

dim = Dimension(x, y[, ds])

Arguments 'x' and 'y' should be float values. Optional argument
'ds' should be a DimStyle instance. A default DimStyle is used
of the optional argument is not used.
        """
        _x = util.get_float(x)
        _y = util.get_float(y)
        _ds = dimstyle
        if _ds is None:
            _ds = self.getDefaultDimStyle()
        if not isinstance(_ds, DimStyle):
            raise TypeError, "Invalid DimStyle type: " + `type(_ds)`
        _ddm = None
        if 'dual-mode' in kw:
            _ddm = kw['dual-mode']
        if _ddm is not None:
            util.test_boolean(_ddm)
            if _ddm is _ds.getValue('DIM_DUAL_MODE'):
                _ddm = None
        _offset = None
        if 'offset' in kw:
            _offset = util.get_float(kw['offset'])
        if _offset is not None:
            if _offset < 0.0:
                raise ValueError, "Invalid dimension offset: %g" % _offset
            if abs(_offset - _ds.getValue('DIM_OFFSET')) < 1e-10:
                _offset = None
        _extlen = None
        if 'extlen' in kw:
            _extlen = util.get_float(kw['extlen'])
            if _extlen < 0.0:
                raise ValueError, "Invalid dimension extension: %g" % _extlen
            if abs(_extlen - _ds.getValue('DIM_EXTENSION')) < 1e-10:
                _extlen = None
        _textpos = None
        if 'textpos' in kw:
            _textpos = kw['textpos']
            if (_textpos != Dimension.DIM_TEXT_POS_SPLIT and
                _textpos != Dimension.DIM_TEXT_POS_ABOVE and
                _textpos != Dimension.DIM_TEXT_POS_BELOW):
                raise ValueError, "Invalid dimension text position: '%s'" % str(_textpos)
            if _textpos == _ds.getValue('DIM_POSITION'):
                _textpos = None
        _poffset = None
        if 'poffset' in kw:
            _poffset = util.get_float(kw['poffset'])
            if _poffset < 0.0:
                raise ValueError, "Invalid text offset length %g" % _poffset
            if abs(_poffset - _ds.getValue('DIM_POSITION_OFFSET')) < 1e-10:
                _poffset = None
        _dmoffset = None
        if 'dmoffset' in kw:
            _dmoffset = util.get_float(kw['dmoffset'])
            if _dmoffset < 0.0:
                raise ValueError, "Invalid dual mode offset length %g" % _dmoffset
            if abs(_dmoffset - _ds.getValue('DIM_DUAL_MODE_OFFSET')) < 1e-10:
                _dmoffset = None
        _eptype = None
        if 'eptype' in kw:
            _eptype = kw['eptype']
            if (_eptype != Dimension.DIM_ENDPT_NONE and
                _eptype != Dimension.DIM_ENDPT_ARROW and
                _eptype != Dimension.DIM_ENDPT_FILLED_ARROW and
                _eptype != Dimension.DIM_ENDPT_SLASH and
                _eptype != Dimension.DIM_ENDPT_CIRCLE):
                raise ValueError, "Invalid endpoint: '%s'" % str(_eptype)
            if _eptype == _ds.getValue('DIM_ENDPOINT'):
                _eptype = None
        _epsize = None
        if 'epsize' in kw:
            _epsize = util.get_float(kw['epsize'])
            if _epsize < 0.0:
                raise ValueError, "Invalid endpoint size %g" % _epsize
            if abs(_epsize - _ds.getValue('DIM_ENDPOINT_SIZE')) < 1e-10:
                _epsize = None
        _color = None
        if 'color' in kw:
            _color = kw['color']
            if not isinstance(_color, color.Color):
                raise TypeError, "Invalid color type: " + `type(_color)`
            if _color == _ds.getValue('DIM_COLOR'):
                _color = None
        _thickness = None
        if 'thickness' in kw:
            _thickness = util.get_float(kw['thickness'])
            if _thickness < 0.0:
                raise ValueError, "Invalid thickness: %g" % _thickness
            if abs(_thickness - _ds.getValue('DIM_THICKNESS')) < 1e-10:
                _thickness = None
        _scale = 1.0
        if 'scale' in kw:
            _scale = util.get_float(kw['scale'])
            if not _scale > 0.0:
                raise ValueError, "Invalid scale: %g" % _scale
        #
        # dimstrings
        #
        # the setDimension() call will adjust the values in the
        # new DimString instances if they get created
        #
        _ds1 = _ds2 = None
        _ds1adj = _ds2adj = True
        if 'ds1' in kw:
            _ds1 = kw['ds1']
            if not isinstance(_ds1, DimString):
                raise TypeError, "Invalid DimString type: " + `type(_ds1)`
            _ds1adj = False
        if _ds1 is None:
            _ds1 = DimString(_x, _y)
        #
        if 'ds2' in kw:
            _ds2 = kw['ds2']
            if not isinstance(_ds2, DimString):
                raise TypeError, "Invalid DimString type: " + `type(_ds2)`
            _ds2adj = False
        if _ds2 is None:
            _ds2 = DimString(_x, _y)
        #
        # finally ...
        #
        super(Dimension, self).__init__(**kw)
        self.__dimstyle = _ds
        self.__ddm = _ddm
        self.__offset = _offset
        self.__extlen = _extlen
        self.__textpos = _textpos
        self.__poffset = _poffset
        self.__dmoffset = _dmoffset
        self.__eptype = _eptype
        self.__epsize = _epsize
        self._color = _color
        self.__thickness = _thickness
        self.__scale = _scale
        self.__dimloc = (_x, _y)
        self.__ds1 = _ds1
        self.__ds2 = _ds2
        self.__ds1.setDimension(self, _ds1adj)
        self.__ds2.setDimension(self, _ds2adj)
        _ds1.connect('change_pending', self.__dimstringChangePending)
        _ds1.connect('change_complete', self.__dimstringChangeComplete)
        _ds2.connect('change_pending', self.__dimstringChangePending)
        _ds2.connect('change_complete', self.__dimstringChangeComplete)

    def getDefaultDimStyle(cls):
        if cls.__defstyle is None:
            cls.__defstyle = DimStyle(u'Default DimStyle')
        return cls.__defstyle

    getDefaultDimStyle = classmethod(getDefaultDimStyle)

    def setDefaultDimStyle(cls, s):
        if not isinstance(s, DimStyle):
            raise TypeError, "Invalid DimStyle: " + `type(s)`
        cls.__defstyle = s

    setDefaultDimStyle = classmethod(setDefaultDimStyle)

    def finish(self):
        self.__ds1.disconnect(self)
        self.__ds2.disconnect(self)
        self.__ds1.finish()
        self.__ds2.finish()
        self.__ds1 = self.__ds2 = None
        super(Dimension, self).finish()

    def getValues(self):
        """Return values comprising the Dimension.

getValues()

This method extends the Entity::getValues() method.
        """
        _data = super(Dimension, self).getValues()
        _data.setValue('location', self.__dimloc)
        if self.__offset is not None:
            _data.setValue('offset', self.__offset)
        if self.__extlen is not None:
            _data.setValue('extension', self.__extlen)
        if self.__textpos is not None:
            _data.setValue('position', self.__textpos)
        if self.__eptype is not None:
            _data.setValue('eptype', self.__eptype)
        if self.__epsize is not None:
            _data.setValue('epsize', self.__epsize)
        if self._color is not None:
            _data.setValue('color', self._color.getColors())
        if self.__ddm is not None:
            _data.setValue('dualmode', self.__ddm)
        if self.__poffset is not None:
            _data.setValue('poffset', self.__poffset)
        if self.__dmoffset is not None:
            _data.setValue('dmoffset', self.__dmoffset)
        if self.__thickness is not None:
            _data.setValue('thickness', self.__thickness)
        _data.setValue('ds1', self.__ds1.getValues())
        _data.setValue('ds2', self.__ds2.getValues())
        _data.setValue('dimstyle', self.__dimstyle.getValues())
        return _data

    def getDimStyle(self):
        """Return the DimStyle used in this Dimension.

getDimStyle()
        """
        return self.__dimstyle

    def setDimStyle(self, ds):
        """Set the DimStyle used for this Dimension.

setDimStyle(ds)

After setting the DimStyle, the values stored in it
are applied to the DimensionObject.
        """
        if self.isLocked():
            raise RuntimeError, "Changing dimstyle not allowed - object locked."
        if not isinstance(ds, DimStyle):
            raise TypeError, "Invalid DimStyle type: " + `type(ds)`
        _sds = self.__dimstyle
        if ds is not _sds:
            _opts = self.getValues()
            self.startChange('dimstyle_changed')
            self.__dimstyle = ds
            self.endChange('dimstyle_changed')
            #
            # call the various methods without arguments
            # so the values given in the new DimStyle are used
            #
            self.setOffset()
            self.setExtension()
            self.setPosition()
            self.setEndpointType()
            self.setEndpointSize()
            self.setColor()
            self.setThickness()
            self.setDualDimMode()
            self.setPositionOffset()
            self.setDualModeOffset()
            #
            # set the values in the two DimString instances
            #
            _d = self.__ds1
            _d.setPrefix(ds.getValue('DIM_PRIMARY_PREFIX'))
            _d.setSuffix(ds.getValue('DIM_PRIMARY_SUFFIX'))
            _d.setPrecision(ds.getValue('DIM_PRIMARY_PRECISION'))
            _d.setUnits(ds.getValue('DIM_PRIMARY_UNITS'))
            _d.setPrintZero(ds.getValue('DIM_PRIMARY_LEADING_ZERO'))
            _d.setPrintDecimal(ds.getValue('DIM_PRIMARY_TRAILING_DECIMAL'))
            _d.setFamily(ds.getValue('DIM_PRIMARY_FONT_FAMILY'))
            _d.setWeight(ds.getValue('DIM_PRIMARY_FONT_WEIGHT'))
            _d.setStyle(ds.getValue('DIM_PRIMARY_FONT_STYLE'))
            _d.setColor(ds.getValue('DIM_PRIMARY_FONT_COLOR'))
            _d.setSize(ds.getValue('DIM_PRIMARY_TEXT_SIZE'))
            _d.setAngle(ds.getValue('DIM_PRIMARY_TEXT_ANGLE'))
            _d.setAlignment(ds.getVaue('DIM_PRIMARY_TEXT_ALIGNMENT'))
            _d = self.__ds2
            _d.setPrefix(ds.getValue('DIM_SECONDARY_PREFIX'))
            _d.setSuffix(ds.getValue('DIM_SECONDARY_SUFFIX'))
            _d.setPrecision(ds.getValue('DIM_SECONDARY_PRECISION'))
            _d.setUnits(ds.getValue('DIM_SECONDARY_UNITS'))
            _d.setPrintZero(ds.getValue('DIM_SECONDARY_LEADING_ZERO'))
            _d.setPrintDecimal(ds.getValue('DIM_SECONDARY_TRAILING_DECIMAL'))
            _d.setFamily(ds.getValue('DIM_SECONDARY_FONT_FAMILY'))
            _d.setWeight(ds.getValue('DIM_SECONDARY_FONT_WEIGHT'))
            _d.setStyle(ds.getValue('DIM_SECONDARY_FONT_STYLE'))
            _d.setColor(ds.getValue('DIM_SECONDARY_FONT_COLOR'))
            _d.setSize(ds.getValue('DIM_SECONDARY_TEXT_SIZE'))
            _d.setAngle(ds.getValue('DIM_SECONDARY_TEXT_ANGLE'))
            _d.setAlignment(ds.getVaue('DIM_SECONDARY_TEXT_ALIGNMENT'))
            self.sendMessage('dimstyle_changed', _sds, _opts)
            self.modified()

    dimstyle = property(getDimStyle, setDimStyle, None,
                        "Dimension DimStyle object.")

    def getEndpointTypeAsString(cls, ep):
        """Return a text string for the dimension endpoint type.

getEndpointTypeAsString(ep)

This classmethod returns 'none', 'arrow', or 'filled-arrow', 'slash',
or 'circle'.
        """
        if not isinstance(ep, int):
            raise TypeError, "Invalid argument type: " + `type(ep)`
        if ep == Dimension.DIM_ENDPT_NONE:
            _str = 'none'
        elif ep == Dimension.DIM_ENDPT_ARROW:
            _str = 'arrow'
        elif ep == Dimension.DIM_ENDPT_FILLED_ARROW:
            _str = 'filled-arrow'
        elif ep == Dimension.DIM_ENDPT_SLASH:
            _str = 'slash'
        elif ep == Dimension.DIM_ENDPT_CIRCLE:
            _str = 'circle'
        else:
            raise ValueError, "Unexpected endpoint type value: %d" % ep
        return _str

    getEndpointTypeAsString = classmethod(getEndpointTypeAsString)

    def getEndpointTypeFromString(cls, s):
        """Return the dimension endpoint type given a string argument.

getEndpointTypeFromString(ep)

This classmethod returns a value based on the string argument:

'none' -> Dimension.DIM_ENDPT_NONE
'arrow' -> Dimension.DIM_ENDPT_ARROW
'filled-arrow' -> Dimension.DIM_ENDPT_FILLED_ARROW
'slash' -> Dimension.DIM_ENDPT_SLASH
'circle' -> Dimension.DIM_ENDPT_CIRCLE

If the string is not listed above a ValueError execption is raised.
        """
        if not isinstance(s, str):
            raise TypeError, "Invalid argument type: " + `type(s)`
        _ls = s.lower()
        if _ls == 'none':
            _v = Dimension.DIM_ENDPT_NONE
        elif _ls == 'arrow':
            _v = Dimension.DIM_ENDPT_ARROW
        elif (_ls == 'filled-arrow' or _ls == 'filled_arrow'):
            _v = Dimension.DIM_ENDPT_FILLED_ARROW
        elif _ls == 'slash':
            _v = Dimension.DIM_ENDPT_SLASH
        elif _ls == 'circle':
            _v = Dimension.DIM_ENDPT_CIRCLE
        else:
            raise ValueError, "Unexpected endpoint type string: " + s
        return _v

    getEndpointTypeFromString = classmethod(getEndpointTypeFromString)

    def getEndpointTypeStrings(cls):
        """Return the endpoint types as strings.

getEndpointTypeStrings()

This classmethod returns a list of strings.
        """
        return [_('None'),
                _('Arrow'),
                _('Filled-Arrow'),
                _('Slash'),
                _('Circle')
                ]

    getEndpointTypeStrings = classmethod(getEndpointTypeStrings)

    def getEndpointTypeValues(cls):
        """Return the endpoint type values.

getEndpointTypeValues()

This classmethod returns a list of values.
        """
        return [Dimension.DIM_ENDPT_NONE,
                Dimension.DIM_ENDPT_ARROW,
                Dimension.DIM_ENDPT_FILLED_ARROW,
                Dimension.DIM_ENDPT_SLASH,
                Dimension.DIM_ENDPT_CIRCLE
                ]

    getEndpointTypeValues = classmethod(getEndpointTypeValues)
    
    def getEndpointType(self):
        """Return what type of endpoints the Dimension uses.

getEndpointType()
        """
        _et = self.__eptype
        if _et is None:
            _et = self.__dimstyle.getValue('DIM_ENDPOINT')
        return _et

    def setEndpointType(self, eptype=None):
        """Set what type of endpoints the Dimension will use.

setEndpointType([e])

The argument 'e' should be one of the following

dimension.NO_ENDPOINT => no special marking at the dimension crossbar ends
dimension.ARROW => an arrowhead at the dimension crossbar ends
dimension.FILLED_ARROW => a filled arrohead at the dimension crossbar ends
dimension.SLASH => a slash mark at the dimension crossbar ends
dimension.CIRCLE => a filled circle at the dimension crossbar ends

If this method is called without an argument, the endpoint type is set
to that given in the DimStyle.
        """
        if self.isLocked():
            raise RuntimeError, "Changing endpoint type allowed - object locked."
        _ep = eptype
        if _ep is not None:
            if (_ep != Dimension.DIM_ENDPT_NONE and
                _ep != Dimension.DIM_ENDPT_ARROW and
                _ep != Dimension.DIM_ENDPT_FILLED_ARROW and
                _ep != Dimension.DIM_ENDPT_SLASH and
                _ep != Dimension.DIM_ENDPT_CIRCLE):
                raise ValueError, "Invalid endpoint value: '%s'" % str(_ep)
        _et = self.getEndpointType()
        if ((_ep is None and self.__eptype is not None) or
            (_ep is not None and _ep != _et)):
            self.startChange('endpoint_type_changed')
            self.__eptype = _ep
            self.endChange('endpoint_type_changed')
            self.calcDimValues()
            self.sendMessage('endpoint_type_changed', _et)
            self.modified()

    endpoint = property(getEndpointType, setEndpointType,
                        None, "Dimension endpoint type.")

    def getEndpointSize(self):
        """Return the size of the Dimension endpoints.

getEndpointSize()
        """
        _es = self.__epsize
        if _es is None:
            _es = self.__dimstyle.getValue('DIM_ENDPOINT_SIZE')
        return _es

    def setEndpointSize(self, size=None):
        """Set the size of the Dimension endpoints.

setEndpointSize([size])

Optional argument 'size' should be a float greater than or equal to 0.0.
Calling this method without an argument sets the endpoint size to that
given in the DimStle.
        """
        if self.isLocked():
            raise RuntimeError, "Changing endpoint type allowed - object locked."
        _size = size
        if _size is not None:
            _size = util.get_float(_size)
            if _size < 0.0:
                raise ValueError, "Invalid endpoint size: %g" % _size
        _es = self.getEndpointSize()
        if ((_size is None and self.__epsize is not None) or
            (_size is not None and abs(_size - _es) > 1e-10)):
            self.startChange('endpoint_size_changed')
            self.__epsize = _size
            self.endChange('endpoint_size_changed')
            self.calcDimValues()
            self.sendMessage('endpoint_size_changed', _es)
            self.modified()

    def getDimstrings(self):
        """Return both primary and secondry dimstrings.

getDimstrings()
        """
        return self.__ds1, self.__ds2

    def getPrimaryDimstring(self):
        """ Return the DimString used for formatting the primary dimension.

getPrimaryDimstring()
        """
        return self.__ds1

    def getSecondaryDimstring(self):
        """Return the DimString used for formatting the secondary dimension.

getSecondaryDimstring()
        """
        return self.__ds2

    def getDualDimMode(self):
        """Return if the Dimension is displaying primary and secondary values.

getDualDimMode(self)
        """
        _mode = self.__ddm
        if _mode is None:
            _mode = self.__dimstyle.getValue('DIM_DUAL_MODE')
        return _mode

    def setDualDimMode(self, mode=None):
        """Set the Dimension to display both primary and secondary values.

setDualDimMode([mode])

Optional argument 'mode' should be either True or False.
Invoking this method without arguments will set the dual dimension
value display mode to that given from the DimStyle
        """
        if self.isLocked():
            raise RuntimeError, "Changing dual mode not allowed - object locked."
        _mode = mode
        if _mode is not None:
            util.test_boolean(_mode)
        _ddm = self.getDualDimMode()
        if ((_mode is None and self.__ddm is not None) or
            (_mode is not None and _mode is not _ddm)): 
            self.startChange('dual_mode_changed')
            self.__ddm = _mode
            self.endChange('dual_mode_changed')
            self.__ds1.setBounds()
            self.__ds2.setBounds()
            self.calcDimValues()
            self.sendMessage('dual_mode_changed', _ddm)
            self.modified()

    dual_mode = property(getDualDimMode, setDualDimMode, None,
                         "Display both primary and secondary dimensions")

    def getOffset(self):
        """Return the current offset value for the Dimension.

getOffset()
        """
        _offset = self.__offset
        if _offset is None:
            _offset = self.__dimstyle.getValue('DIM_OFFSET')
        return _offset

    def setOffset(self, offset=None):
        """Set the offset value for the Dimension.

setOffset([offset])

Optional argument 'offset' should be a positive float.
Calling this method without arguments sets the value to that
given in the DimStyle.
        """
        if self.isLocked():
            raise RuntimeError, "Setting offset not allowed - object locked."
        _o = offset
        if _o is not None:
            _o = util.get_float(_o)
            if _o < 0.0:
                raise ValueError, "Invalid dimension offset length: %g" % _o
        _off = self.getOffset()
        if ((_o is None and self.__offset is not None) or
            (_o is not None and abs(_o - _off) > 1e-10)):
            _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
            self.startChange('offset_changed')
            self.__offset = _o
            self.endChange('offset_changed')
            self.calcDimValues()
            self.sendMessage('offset_changed', _off)
            self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    offset = property(getOffset, setOffset, None, "Dimension offset.")

    def getExtension(self):
        """Get the extension length of the Dimension.

getExtension()
        """
        _ext = self.__extlen
        if _ext is None:
            _ext = self.__dimstyle.getValue('DIM_EXTENSION')
        return _ext

    def setExtension(self, ext=None):
        """Set the extension length of the Dimension.

setExtension([ext])

Optional argument 'ext' should be a positive float value.
Calling this method without arguments set the extension length
to that given in the DimStyle.
        """
        if self.isLocked():
            raise RuntimeError, "Setting extension not allowed - object locked."
        _e = ext
        if _e is not None:
            _e = util.get_float(_e)
            if _e < 0.0:
                raise ValueError, "Invalid dimension extension length: %g" % _e
        _ext = self.getExtension()
        if ((_e is None and self.__extlen is not None) or
            (_e is not None and abs(_e - _ext) > 1e-10)):
            _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
            self.startChange('extension_changed')
            self.__extlen = _e
            self.endChange('extension_changed')
            self.calcDimValues()
            self.sendMessage('extension_changed', _ext)
            self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    extension = property(getExtension, setExtension, None,
                         "Dimension extension length.")

    def getPositionAsString(cls, p):
        """Return a text string for the dimension text position.

getPositionAsString(p)

This classmethod returns 'split', 'above', or 'below'
        """
        if not isinstance(p, int):
            raise TypeError, "Invalid argument type: " + `type(p)`
        if p == Dimension.DIM_TEXT_POS_SPLIT:
            _str = 'split'
        elif p == Dimension.DIM_TEXT_POS_ABOVE:
            _str = 'above'
        elif p == Dimension.DIM_TEXT_POS_BELOW:
            _str = 'below'
        else:
            raise ValueError, "Unexpected position value: %d" % p
        return _str

    getPositionAsString = classmethod(getPositionAsString)

    def getPositionFromString(cls, s):
        """Return the dimension text position given a string argument.

getPositionFromString(s)

This classmethod returns a value based on the string argument:

'split' -> Dimension.DIM_TEXT_POS_SPLIT
'above' -> Dimension.DIM_TEXT_POS_ABOVE
'below' -> Dimension.DIM_TEXT_POS_BELOW

If the string is not listed above a ValueError execption is raised.

        """
        if not isinstance(s, str):
            raise TypeError, "Invalid argument type: " + `type(s)`
        _ls = s.lower()
        if _ls == 'split':
            _v = Dimension.DIM_TEXT_POS_SPLIT
        elif _ls == 'above':
            _v = Dimension.DIM_TEXT_POS_ABOVE
        elif _ls == 'below':
            _v = Dimension.DIM_TEXT_POS_BELOW
        else:
            raise ValueError, "Unexpected position string: " + s
        return _v

    getPositionFromString = classmethod(getPositionFromString)

    def getPositionStrings(cls):
        """Return the position values as strings.

getPositionStrings()

This classmethod returns a list of strings.
        """
        return [_('Split'),
                _('Above'),
                _('Below')
                ]

    getPositionStrings = classmethod(getPositionStrings)

    def getPositionValues(cls):
        """Return the position values.

getPositionValues()

This classmethod reutrns a list of values.
        """
        return [Dimension.DIM_TEXT_POS_SPLIT,
                Dimension.DIM_TEXT_POS_ABOVE,
                Dimension.DIM_TEXT_POS_BELOW
                ]

    getPositionValues = classmethod(getPositionValues)
    
    def getPosition(self):
        """Return how the dimension text intersects the crossbar.

getPosition()
        """
        _pos = self.__textpos
        if _pos is None:
            _pos = self.__dimstyle.getValue('DIM_POSITION')
        return _pos

    def setPosition(self, pos=None):
        """Set where the dimension text should be placed at the crossbar.

setPosition([pos])

Choices for optional argument 'pos' are:

dimension.SPLIT => In the middle of the crossbar.
dimension.ABOVE => Beyond the crossbar from the dimensioned objects.
dimension.BELOW => Between the crossbar and the dimensioned objects.

Calling this method without arguments sets the position to that given
in the DimStyle.
        """
        if self.isLocked():
            raise RuntimeError, "Setting position not allowed - object locked."
        _pos = pos
        if (_pos != Dimension.DIM_TEXT_POS_SPLIT and
            _pos != Dimension.DIM_TEXT_POS_ABOVE and
            _pos != Dimension.DIM_TEXT_POS_BELOW):
            raise ValueError, "Invalid dimension text position: '%s'" % str(_pos)
        _dp = self.getPosition()
        if ((_pos is None and self.__textpos is not None) or
            (_pos is not None and _pos != _dp)):
            self.startChange('position_changed')
            self.__textpos = _pos
            self.endChange('position_changed')
            self.__ds1.setBounds()
            self.__ds2.setBounds()
            self.sendMessage('position_changed', _dp)
            self.modified()

    position = property(getPosition, setPosition, None,
                        "Dimension text position")

    def getPositionOffset(self):
        """Get the offset for the dimension text and the crossbar/crossarc.

getPositionOffset()
        """
        _po = self.__poffset
        if _po is None:
            _po = self.__dimstyle.getValue('DIM_POSITION_OFFSET')
        return _po

    def setPositionOffset(self, offset=None):
        """Set the separation between the dimension text and the crossbar.

setPositionOffset([offset])

If this method is called without arguments, the text offset
length is set to the value given in the DimStyle.
If the argument 'offset' is supplied, it should be a positive float value.
        """
        if self.isLocked():
            raise RuntimeError, "Setting text offset length not allowed - object locked."
        _o = offset
        if _o is not None:
            _o = util.get_float(_o)
            if _o < 0.0:
                raise ValueError, "Invalid text offset length: %g" % _o
        _to = self.getPositionOffset()
        if ((_o is None and self.__poffset is not None) or
            (_o is not None and abs(_o - _to) > 1e-10)):
            _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
            self.startChange('position_offset_changed')
            self.__poffset = _o
            self.endChange('position_offset_changed')
            self.__ds1.setBounds()
            self.__ds2.setBounds()
            self.calcDimValues()
            self.sendMessage('position_offset_changed', _to)
            self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    position_offset = property(getPositionOffset, setPositionOffset, None,
                               "Text offset from crossbar/crossarc distance.")

    def getDualModeOffset(self):
        """Get the offset for the dimension text when displaying two dimensions.

getDualModeOffset()
        """
        _dmo = self.__dmoffset
        if _dmo is None:
            _dmo = self.__dimstyle.getValue('DIM_DUAL_MODE_OFFSET')
        return _dmo

    def setDualModeOffset(self, offset=None):
        """Set the separation between the dimensions and the dual mode dimension divider.

setDualModeOffset([offset])

If this method is called without arguments, the dual mode offset
length is set to the value given in the DimStyle.
If the argument 'offset' is supplied, it should be a positive float value.
        """
        if self.isLocked():
            raise RuntimeError, "Setting dual mode offset length not allowed - object locked."
        _o = offset
        if _o is not None:
            _o = util.get_float(_o)
            if _o < 0.0:
                raise ValueError, "Invalid dual mode offset length: %g" % _o
        _dmo = self.getDualModeOffset()
        if ((_o is None and self.__dmoffset is not None) or
            (_o is not None and abs(_o - _dmo) > 1e-10)):
            _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
            self.startChange('dual_mode_offset_changed')
            self.__dmoffset = _o
            self.endChange('dual_mode_offset_changed')
            self.__ds1.setBounds()
            self.__ds2.setBounds()
            self.calcDimValues()
            self.sendMessage('dual_mode_offset_changed', _dmo)
            self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    dual_mode_offset = property(getDualModeOffset, setDualModeOffset, None,
                                "Text offset from dimension splitting bar when displaying two dimensions.")

    def getColor(self):
        """Return the color of the dimension lines.

getColor()
        """
        _col = self._color
        if _col is None:
            _col = self.__dimstyle.getValue('DIM_COLOR')
        return _col

    def setColor(self, c=None):
        """Set the color of the dimension lines.

setColor([c])

Optional argument 'c' should be a Color instance. Calling this
method without an argument sets the color to the value given
in the DimStyle.
        """
        if self.isLocked():
            raise RuntimeError, "Setting object color not allowed - object locked."
        _c = c
        if _c is not None:
            if not isinstance(_c, color.Color):
                raise TypeError, "Invalid color type: " + `type(_c)`
        _oc = self.getColor()
        if ((_c is None and self._color is not None) or
            (_c is not None and _c != _oc)):
            self.startChange('color_changed')
            self._color = _c
            self.endChange('color_changed')
            self.sendMessage('color_changed', _oc)
            self.modified()

    color = property(getColor, setColor, None, "Dimension Color")

    def getThickness(self):
        """Return the thickness of the dimension bars.

getThickness()

This method returns a float.
        """
        _t = self.__thickness
        if _t is None:
            _t = self.__dimstyle.getValue('DIM_THICKNESS')
        return _t

    def setThickness(self, thickness=None):
        """Set the thickness of the dimension bars.

setThickness([thickness])

Optional argument 'thickness' should be a float value. Setting the
thickness to 0 will display and print the lines with the thinnest
value possible. Calling this method without arguments resets the
thickness to the value defined in the DimStyle.
        """
        if self.isLocked():
            raise RuntimeError, "Setting thickness not allowed - object locked."
        _t = thickness
        if _t is not None:
            _t = util.get_float(_t)
            if _t < 0.0:
                raise ValueError, "Invalid thickness: %g" % _t
        _ot = self.getThickness()
        if ((_t is None and self.__thickness is not None) or
            (_t is not None and abs(_t - _ot) > 1e-10)):
            self.startChange('thickness_changed')
            self.__thickness = _t
            self.endChange('thickness_changed')
            self.sendMessage('thickness_changed', _ot)
            self.modified()

    thickness = property(getThickness, setThickness, None,
                         "Dimension bar thickness.")

    def getScale(self):
        """Return the Dimension scale factor.

getScale()
        """
        return self.__scale

    def setScale(self, scale=None):
        """Set the Dimension scale factor.

setScale([scale])

Optional argument 's' should be a float value greater than 0. If
no argument is supplied the default scale factor of 1 is set. 
        """
        if self.isLocked():
            raise RuntimeError, "Setting scale not allowed - object locked."
        _s = scale
        if _s is None:
            _s = 1.0
        _s = util.get_float(_s)
        if not _s > 0.0:
            raise ValueError, "Invalid scale factor: %g" % _s
        _os = self.__scale
        if abs(_os - _s) > 1e-10:
            self.startChange('scale_changed')
            self.__scale = _s
            self.endChange('scale_changed')
            self.sendMessage('scale_changed', _os)
            self.modified()

    scale = property(getScale, setScale, None, "Dimension scale factor.")

    def getLocation(self):
        """Return the location of the dimensional text values.

getLocation()
        """
        return self.__dimloc

    def setLocation(self, x, y):
        """Set the location of the dimensional text values.

setLocation(x, y)

The 'x' and 'y' arguments should be float values. The text is
centered around that point.
        """
        if self.isLocked():
            raise RuntimeError, "Setting location not allowed - object locked."
        _x = util.get_float(x)
        _y = util.get_float(y)
        _ox, _oy = self.__dimloc
        if abs(_ox - _x) > 1e-10 or abs(_oy - _y) > 1e-10:
            _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
            self.startChange('location_changed')
            self.__dimloc = (_x, _y)
            self.endChange('location_changed')
            self.__ds1.setBounds()
            self.__ds2.setBounds()
            self.calcDimValues()
            self.sendMessage('location_changed', _ox, _oy)
            self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    location = property(getLocation, setLocation, None,
                        "Dimension location")

    def move(self, dx, dy):
        """Move a Dimension.

move(dx, dy)

The first argument gives the x-coordinate displacement,
and the second gives the y-coordinate displacement. Both
values should be floats.
        """
        if self.isLocked():
            raise RuntimeError, "Moving not allowed - object locked."
        _dx = util.get_float(dx)
        _dy = util.get_float(dy)
        if abs(_dx) > 1e-10 or abs(_dy) > 1e-10:
            _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
            _x, _y = self.__dimloc
            self.startChange('location_changed')
            self.__dimloc = ((_x + _dx), (_y + _dy))
            self.endChange('location_changed')
            self.__ds1.setBounds()
            self.__ds2.setBounds()
            self.calcDimValues()
            self.sendMessage('location_changed', _x, _y)
            self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    def getStyleValue(self, ds, opt):
        """Get the value in the DimStyle for some option

getStyleValue(ds, opt)

Argument 'ds' should be one of the DimString objects in
the Dimension, and argument 'opt' should be a string.
Valid choices for 'opt' are 'prefix', 'suffix', 'precision',
'units', 'print_zero', 'print_decimal', 'font_family',
'font_style', 'font_weight', 'size', 'color', 'angle',
and 'alignment'.
        """
        if not isinstance(ds, DimString):
            raise TypeError, "Invalid DimString type: " + `type(ds)`
        if not isinstance(opt, str):
            raise TypeError, "Invalid DimStyle option type: " + `type(opt)`
        _key = None
        if ds is self.__ds1:
            if opt == 'prefix':
                _key = 'DIM_PRIMARY_PREFIX'
            elif opt == 'suffix':
                _key = 'DIM_PRIMARY_SUFFIX'
            elif opt == 'precision':
                _key = 'DIM_PRIMARY_PRECISION'
            elif opt == 'units':
                _key = 'DIM_PRIMARY_UNITS'
            elif opt == 'print_zero':
                _key = 'DIM_PRIMARY_LEADING_ZERO'
            elif opt == 'print_decimal':
                _key = 'DIM_PRIMARY_TRAILING_DECIMAL'
            elif opt == 'font_family':
                _key = 'DIM_PRIMARY_FONT_FAMILY'
            elif opt == 'font_weight':
                _key = 'DIM_PRIMARY_FONT_WEIGHT'
            elif opt == 'font_style':
                _key = 'DIM_PRIMARY_FONT_STYLE'
            elif opt == 'size':
                _key = 'DIM_PRIMARY_TEXT_SIZE'
            elif opt == 'color':
                _key = 'DIM_PRIMARY_FONT_COLOR'
            elif opt == 'angle':
                _key = 'DIM_PRIMARY_TEXT_ANGLE'
            elif opt == 'alignment':
                _key = 'DIM_PRIMARY_TEXT_ALIGNMENT'
            else:
                raise ValueError, "Unexpected option: %s" % opt
        elif ds is self.__ds2:
            if opt == 'prefix':
                _key = 'DIM_SECONDARY_PREFIX'
            elif opt == 'suffix':
                _key = 'DIM_SECONDARY_SUFFIX'
            elif opt == 'precision':
                _key = 'DIM_SECONDARY_PRECISION'
            elif opt == 'units':
                _key = 'DIM_SECONDARY_UNITS'
            elif opt == 'print_zero':
                _key = 'DIM_SECONDARY_LEADING_ZERO'
            elif opt == 'print_decimal':
                _key = 'DIM_SECONDARY_TRAILING_DECIMAL'
            elif opt == 'font_family':
                _key = 'DIM_SECONDARY_FONT_FAMILY'
            elif opt == 'font_weight':
                _key = 'DIM_SECONDARY_FONT_WEIGHT'
            elif opt == 'font_style':
                _key = 'DIM_SECONDARY_FONT_STYLE'
            elif opt == 'size':
                _key = 'DIM_SECONDARY_TEXT_SIZE'
            elif opt == 'color':
                _key = 'DIM_SECONDARY_FONT_COLOR'
            elif opt == 'angle':
                _key = 'DIM_SECONDARY_TEXT_ANGLE'
            elif opt == 'alignment':
                _key = 'DIM_SECONDARY_TEXT_ALIGNMENT'
            else:
                raise ValueError, "Unexpected option: %s" % opt
        else:
            raise ValueError, "DimString not used in this Dimension: " + `ds`
        if _key is None:
            raise ValueError, "Unexpected option: %s" % opt
        return self.__dimstyle.getValue(_key)

    def getDimensions(self, dimlen):
        """Return the formatted dimensional values.

getDimensions(dimlen)

The argument 'dimlen' should be the length in millimeters.

This method returns a list of the primary and secondary
dimensional values.
        """
        _dl = util.get_float(dimlen)
        dims = []
        dims.append(self.__ds1.formatDimension(_dl))
        dims.append(self.__ds2.formatDimension(_dl))
        return dims

    def calcDimValues(self, allpts=True):
        """Recalculate the values for dimensional display

calcDimValues([allpts])

This method is meant to be overriden by subclasses.
        """
        pass

    def inRegion(self, xmin, ymin, xmax, ymax, fully=False):
        """Return whether or not a Dimension exists with a region.

isRegion(xmin, ymin, xmax, ymax[, fully])

The first four arguments define the boundary. The optional
fifth argument 'fully' indicates whether or not the Dimension
must be completely contained within the region or just pass
through it.

This method should be overriden in classes derived from Dimension.
        """
        return False

    def getBounds(self):
        """Return the minimal and maximal locations of the dimension

getBounds()

This method returns a tuple of four values - xmin, ymin, xmax, ymax.
These values give the mimimum and maximum coordinates of the dimension
object.

This method should be overriden in classes derived from Dimension.
        """
        _xmin = _ymin = -float(sys.maxint)
        _xmax = _ymax = float(sys.maxint)
        return _xmin, _ymin, _xmax, _ymax

    def copyDimValues(self, dim):
        """This method adjusts one Dimension to match another Dimension

copyDimValues(dim)

Argument 'dim' must be a Dimension instance
        """
        if not isinstance(dim, Dimension):
            raise TypeError, "Invalid Dimension type: " + `type(dim)`
        self.setDimStyle(dim.getDimStyle())
        self.setOffset(dim.getOffset())
        self.setExtension(dim.getExtension())
        self.setEndpointType(dim.getEndpointType())
        self.setEndpointSize(dim.getEndpointSize())
        self.setColor(dim.getColor())
        self.setThickness(dim.getThickness())
        self.setDualDimMode(dim.getDualDimMode())
        self.setPositionOffset(dim.getPositionOffset())
        self.setDualModeOffset(dim.getDualModeOffset())
        #
        _ds1, _ds2 = dim.getDimstrings()
        #
        _ds = self.__ds1
        _ds.setTextStyle(_ds1.getTextStyle())
        _ds.setPrefix(_ds1.getPrefix())
        _ds.setSuffix(_ds1.getSuffix())
        _ds.setPrecision(_ds1.getPrecision())
        _ds.setUnits(_ds1.getUnits())
        _ds.setPrintZero(_ds1.getPrintZero())
        _ds.setPrintDecimal(_ds1.getPrintDecimal())
        _ds.setFamily(_ds1.getFamily())
        _ds.setWeight(_ds1.getWeight())
        _ds.setStyle(_ds1.getStyle())
        _ds.setColor(_ds1.getColor())
        _ds.setSize(_ds1.getSize())
        _ds.setAngle(_ds1.getAngle())
        _ds.setAlignment(_ds1.getAlignment())
        #
        _ds = self.__ds2
        _ds.setTextStyle(_ds2.getTextStyle())
        _ds.setPrefix(_ds2.getPrefix())
        _ds.setSuffix(_ds2.getSuffix())
        _ds.setPrecision(_ds2.getPrecision())
        _ds.setUnits(_ds2.getUnits())
        _ds.setPrintZero(_ds2.getPrintZero())
        _ds.setPrintDecimal(_ds2.getPrintDecimal())
        _ds.setFamily(_ds2.getFamily())
        _ds.setWeight(_ds2.getWeight())
        _ds.setStyle(_ds2.getStyle())
        _ds.setColor(_ds2.getColor())
        _ds.setSize(_ds2.getSize())
        _ds.setAngle(_ds2.getAngle())
        _ds.setAlignment(_ds2.getAlignment())
        
    def __dimstringChangePending(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        _arg = args[0]
        if _arg == 'moved':
            self.startChange(_arg)
        elif (_arg == 'textstyle_changed' or
              _arg == 'font_family_changed' or
              _arg == 'font_style_changed' or
              _arg == 'font_weight_changed' or
              _arg == 'font_color_changed' or
              _arg == 'text_size_changed' or
              _arg == 'text_angle_changed' or
              _arg == 'text_alignment_changed' or
              _arg == 'prefix_changed' or
              _arg == 'suffix_changed' or
              _arg == 'units_changed' or
              _arg == 'precision_changed' or
              _arg == 'print_zero_changed' or
              _arg == 'print_decimal_changed'):
            self.startChange('dimstring_changed')
        else:
            pass

    def __dimstringChangeComplete(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        _arg = args[0]
        if _arg == 'moved':
            self.endChanged(_arg)
        elif (_arg == 'textstyle_changed' or
              _arg == 'font_family_changed' or
              _arg == 'font_style_changed' or
              _arg == 'font_weight_changed' or
              _arg == 'font_color_changed' or
              _arg == 'text_size_changed' or
              _arg == 'text_angle_changed' or
              _arg == 'text_alignment_changed' or
              _arg == 'prefix_changed' or
              _arg == 'suffix_changed' or
              _arg == 'units_changed' or
              _arg == 'precision_changed' or
              _arg == 'print_zero_changed' or
              _arg == 'print_decimal_changed'):
            self.endChange('dimstring_changed')
        else:
            pass
            
    def sendsMessage(self, m):
        if m in Dimension.__messages:
            return True
        return super(Dimension, self).sendsMessage(m)

#
# class stuff for dimension styles
#

class DimStyle(object):
    """A class storing preferences for Dimensions

The DimStyle class stores a set of dimension parameters
that will be used when creating dimensions when the
particular style is active.

A DimStyle object has the following methods:

getName(): Return the name of the DimStyle.
getOption(): Return a single value in the DimStyle.
getOptions(): Return all the options in the DimStyle.
getValue(): Return the value of one of the DimStyle options.

getOption() and getValue() are synonymous.

The DimStyle class has the following classmethods:

getDimStyleOptions(): Return the options defining a DimStyle.
getDimStyleDefaultValue(): Return the default value for a DimStyle option.
    """

    #
    # the default values for the DimStyle class
    #
    __deftextcolor = color.Color('#ffffff')
    __defdimcolor = color.Color(255,165,0)
    __defaults = {
        'DIM_PRIMARY_FONT_FAMILY' : 'Sans',
        'DIM_PRIMARY_TEXT_SIZE' : 1.0,
        'DIM_PRIMARY_FONT_WEIGHT' : text.TextStyle.FONT_NORMAL,
        'DIM_PRIMARY_FONT_STYLE' : text.TextStyle.FONT_NORMAL,
        'DIM_PRIMARY_FONT_COLOR' : __deftextcolor,
        'DIM_PRIMARY_TEXT_ANGLE' : 0.0,
        'DIM_PRIMARY_TEXT_ALIGNMENT' : text.TextStyle.ALIGN_CENTER,
        'DIM_PRIMARY_PREFIX' : u'',
        'DIM_PRIMARY_SUFFIX' : u'',
        'DIM_PRIMARY_PRECISION' : 3,
        'DIM_PRIMARY_UNITS' : units.MILLIMETERS,
        'DIM_PRIMARY_LEADING_ZERO' : True,
        'DIM_PRIMARY_TRAILING_DECIMAL' : True,
        'DIM_SECONDARY_FONT_FAMILY' : 'Sans',
        'DIM_SECONDARY_TEXT_SIZE' : 1.0,
        'DIM_SECONDARY_FONT_WEIGHT' : text.TextStyle.FONT_NORMAL,
        'DIM_SECONDARY_FONT_STYLE' : text.TextStyle.FONT_NORMAL,
        'DIM_SECONDARY_FONT_COLOR' : __deftextcolor,
        'DIM_SECONDARY_TEXT_ANGLE' : 0.0,
        'DIM_SECONDARY_TEXT_ALIGNMENT' : text.TextStyle.ALIGN_CENTER,
        'DIM_SECONDARY_PREFIX' : u'',
        'DIM_SECONDARY_SUFFIX' : u'',
        'DIM_SECONDARY_PRECISION' : 3,
        'DIM_SECONDARY_UNITS' : units.MILLIMETERS,
        'DIM_SECONDARY_LEADING_ZERO' : True,
        'DIM_SECONDARY_TRAILING_DECIMAL' : True,
        'DIM_OFFSET' : 1.0,
        'DIM_EXTENSION' : 1.0,
        'DIM_COLOR' : __defdimcolor,
        'DIM_THICKNESS' : 0.0,
        'DIM_POSITION' : Dimension.DIM_TEXT_POS_SPLIT,
        'DIM_ENDPOINT' : Dimension.DIM_ENDPT_NONE,
        'DIM_ENDPOINT_SIZE' : 1.0,
        'DIM_DUAL_MODE' : False,
        'DIM_POSITION_OFFSET' : 0.0,
        'DIM_DUAL_MODE_OFFSET' : 1.0,
        'RADIAL_DIM_PRIMARY_PREFIX' : u'',
        'RADIAL_DIM_PRIMARY_SUFFIX' : u'',
        'RADIAL_DIM_SECONDARY_PREFIX' : u'',
        'RADIAL_DIM_SECONDARY_SUFFIX' : u'',
        'RADIAL_DIM_DIA_MODE' : False,
        'ANGULAR_DIM_PRIMARY_PREFIX' : u'',
        'ANGULAR_DIM_PRIMARY_SUFFIX' : u'',
        'ANGULAR_DIM_SECONDARY_PREFIX' : u'',
        'ANGULAR_DIM_SECONDARY_SUFFIX' : u'',
        }

    def __init__(self, name, keywords={}):
        """Instantiate a DimStyle object.

ds = DimStyle(name, keywords)

The argument 'name' should be a unicode name, and the
'keyword' argument should be a dict. The keys should
be the same keywords used to set option values, such
as DIM_OFFSET, DIM_EXTENSION, etc, and the value corresponding
to each key should be set appropriately.
        """
        super(DimStyle, self).__init__()
        _n = name
        if not isinstance(_n, types.StringTypes):
            raise TypeError, "Invalid DimStyle name type: "+ `type(_n)`
        if isinstance(_n, str):
            _n = unicode(_n)
        if not isinstance(keywords, dict):
            raise TypeError, "Invalid keywords argument type: " + `type(keywords)`
        from PythonCAD.Generic.options import test_option
        self.__opts = baseobject.ConstDict(str)
        self.__name = _n
        for _kw in keywords:
            if _kw not in DimStyle.__defaults:
                raise KeyError, "Unknown DimStyle keyword: " + _kw
            _val = keywords[_kw]            
            _valid = test_option(_kw, _val)
            self.__opts[_kw] = _val

    def __eq__(self, obj):
        """Test a DimStyle object for equality with another DimStyle.
        """
        if not isinstance(obj, DimStyle):
            return False
        if obj is self:
            return True
        if self.__name != obj.getName():
            return False
        _val = True
        for _key in DimStyle.__defaults.keys():
            _sv = self.getOption(_key)
            _ov = obj.getOption(_key)
            if ((_key == 'DIM_PRIMARY_TEXT_SIZE') or
                (_key == 'DIM_PRIMARY_TEXT_ANGLE') or
                (_key == 'DIM_SECONDARY_TEXT_SIZE') or
                (_key == 'DIM_SECONDARY_TEXT_ANGLE') or
                (_key == 'DIM_OFFSET') or
                (_key == 'DIM_EXTENSION') or
                (_key == 'DIM_THICKNESS') or
                (_key == 'DIM_ENDPOINT_SIZE') or
                (_key == 'DIM_POSITION_OFFSET') or
                (_key == 'DIM_DUAL_MODE_OFFSET')):
                if abs(_sv - _ov) > 1e-10:
                    _val = False
            else:
                if _sv != _ov:
                    _val = False
            if _val is False:
                break
        return _val

    def __ne__(self, obj):
        """Test a DimStyle object for inequality with another DimStyle.
        """
        return not self == obj

    def getDimStyleOptions(cls):
        """Return the options used to define a DimStyle instance.

getDimStyleOptions()

This classmethod returns a list of strings.
        """
        return cls.__defaults.keys()

    getDimStyleOptions = classmethod(getDimStyleOptions)

    def getDimStyleDefaultValue(cls, key):
        """Return the default value for a DimStyle option.

getDimStyleValue(key)

Argument 'key' must be one of the options given in getDimStyleOptions().
        """
        return cls.__defaults[key]

    getDimStyleDefaultValue = classmethod(getDimStyleDefaultValue)

    def getName(self):
        """Return the name of the DimStyle.

getName()
        """
        return self.__name

    name = property(getName, None, None, "DimStyle name.")

    def getKeys(self):
        """Return the non-default options within the DimStyle.

getKeys()
        """
        return self.__opts.keys()

    def getOptions(self):
        """Return all the options stored within the DimStyle.

getOptions()
        """
        _keys = self.__opts.keys()
        for _key in DimStyle.__defaults:
            if _key not in self.__opts:
                _keys.append(_key)
        return _keys

    def getOption(self, key):
        """Return the value of a particular option in the DimStyle.

getOption(key)

The key should be one of the strings returned from getOptions. If
there is no value found in the DimStyle for the key, the value None
is returned.
        """
        if key in self.__opts:
            _val = self.__opts[key]
        elif key in DimStyle.__defaults:
            _val = DimStyle.__defaults[key]
        else:
            raise KeyError, "Unexpected DimStyle keyword: '%s'" % key
        return _val

    def getValue(self, key):
        """Return the value of a particular option in the DimStyle.

getValue(key)

The key should be one of the strings returned from getOptions. This
method raises a KeyError exception if the key is not found.

        """
        if key in self.__opts:
            _val = self.__opts[key]
        elif key in DimStyle.__defaults:
            _val = DimStyle.__defaults[key]
        else:
            raise KeyError, "Unexpected DimStyle keyword: '%s'" % key
        return _val

    def getValues(self):
        """Return values comprising the DimStyle.

getValues()
        """
        _vals = {}
        _vals['name'] = self.__name
        for _opt in self.__opts:
            _val = self.__opts[_opt]
            if ((_opt == 'DIM_PRIMARY_FONT_COLOR') or
                (_opt == 'DIM_SECONDARY_FONT_COLOR') or
                (_opt == 'DIM_COLOR')):
                _vals[_opt] = _val.getColors()
            else:
                _vals[_opt] = _val
        return _vals

class LinearDimension(Dimension):
    """A class for Linear dimensions.

The LinearDimension class is derived from the Dimension
class, so it shares all of those methods and attributes.
A LinearDimension should be used to display the absolute
distance between two Point objects.

A LinearDimension object has the following methods:

{get/set}P1(): Get/Set the first Point for the LinearDimension.
{get/set}P2(): Get/Set the second Point for the LinearDimension.
getDimPoints(): Return the two Points used in this dimension.
getDimLayers(): Return the two Layers holding the Points.
getDimXPoints(): Get the x-coordinates of the dimension bar positions.
getDimYPoints(): Get the y-coordinates of the dimension bar positions.
getDimMarkerPoints(): Get the locaiton of the dimension endpoint markers.
calcMarkerPoints(): Calculate the coordinates of any dimension marker objects.
    """

    __messages = {
        'point_changed' : True,
        }

    def __init__(self, p1, p2, x, y, ds=None, **kw):
        """Instantiate a LinearDimension object.

ldim = LinearDimension(p1, p2, x, y, ds)

p1: A Point contained in a Layer
p2: A Point contained in a Layer
x: The x-coordinate of the dimensional text
y: The y-coordinate of the dimensional text
ds: The DimStyle used for this Dimension.
        """
        if not isinstance(p1, point.Point):
            raise TypeError, "Invalid point type: " + `type(p1)`
        if p1.getParent() is None:
            raise ValueError, "Point P1 not stored in a Layer!"
        if not isinstance(p2, point.Point):
            raise TypeError, "Invalid point type: " + `type(p2)`
        if p2.getParent() is None:
            raise ValueError, "Point P2 not stored in a Layer!"
        super(LinearDimension, self).__init__(x, y, ds, **kw)
        self.__p1 = p1
        self.__p2 = p2
        self.__bar1 = DimBar()
        self.__bar2 = DimBar()
        self.__crossbar = DimCrossbar()
        p1.storeUser(self)
        p1.connect('moved', self.__movePoint)
        p1.connect('change_pending', self.__pointChangePending)
        p1.connect('change_complete', self.__pointChangeComplete)
        p2.storeUser(self)
        p2.connect('moved', self.__movePoint)
        p2.connect('change_pending', self.__pointChangePending)
        p2.connect('change_complete', self.__pointChangeComplete)
        self.calcDimValues()

    def __eq__(self, ldim):
        """Test two LinearDimension objects for equality.
        """
        if not isinstance(ldim, LinearDimension):
            return False
        _lp1 = self.__p1.getParent()
        _lp2 = self.__p2.getParent()
        _p1, _p2 = ldim.getDimPoints()
        _l1 = _p1.getParent()
        _l2 = _p2.getParent()
        if (_lp1 is _l1 and
            _lp2 is _l2 and
            self.__p1 == _p1 and
            self.__p2 == _p2):
            return True
        if (_lp1 is _l2 and
            _lp2 is _l1 and
            self.__p1 == _p2 and
            self.__p2 == _p1):
            return True
        return False

    def __ne__(self, ldim):
        """Test two LinearDimension objects for equality.
        """
        if not isinstance(ldim, LinearDimension):
            return True
        _lp1 = self.__p1.getParent()
        _lp2 = self.__p2.getParent()
        _p1, _p2 = ldim.getDimPoints()
        _l1 = _p1.getParent()
        _p2 = self.__p2
        _l2 = _p2.getParent()
        if (_lp1 is _l1 and
            _lp2 is _l2 and
            self.__p1 == _p1 and
            self.__p2 == _p2):
            return False
        if (_lp1 is _l2 and
            _lp2 is _l1 and
            self.__p1 == _p2 and
            self.__p2 == _p1):
            return False
        return True

    def finish(self):
        self.__p1.disconnect(self)
        self.__p1.freeUser(self)
        self.__p2.disconnect(self)
        self.__p2.freeUser(self)
        self.__bar1 = self.__bar2 = self.__crossbar = None
        self.__p1 = self.__p2 = None
        super(LinearDimension, self).finish()

    def getValues(self):
        """Return values comprising the LinearDimension.

getValues()

This method extends the Dimension::getValues() method.
        """
        _data = super(LinearDimension, self).getValues()
        _data.setValue('type', 'ldim')
        _data.setValue('p1', self.__p1.getID())
        _layer = self.__p1.getParent()
        _data.setValue('l1', _layer.getID())
        _data.setValue('p2', self.__p2.getID())
        _layer = self.__p2.getParent()
        _data.setValue('l2', _layer.getID())
        return _data

    def getP1(self):
        """Return the first Point of a LinearDimension.

getP1()
        """
        return self.__p1

    def setP1(self, p):
        """Set the first Point of a LinearDimension.

setP1(p)

There is one required argument for this method:

p: A Point contained in a Layer
        """
        if self.isLocked():
            raise RuntimeError, "Setting point not allowed - object locked."
        if not isinstance(p, point.Point):
            raise TypeError, "Invalid point type: " + `type(p)`
        if p.getParent() is None:
            raise ValueError, "Point not stored in a Layer!"
        _pt = self.__p1
        if _pt is not p:
            _pt.disconnect(self)
            _pt.freeUser(self)
            self.startChange('point_changed')
            self.__p1 = p
            self.endChange('point_changed')
            self.sendMessage('point_changed', _pt, p)
            p.storeUser(self)
            p.connect('moved', self.__movePoint)
            p.connect('change_pending', self.__pointChangePending)
            p.connect('change_complete', self.__pointChangeComplete)
            if abs(_pt.x - p.x) > 1e-10 or abs(_pt.y - p.y) > 1e-10:
                _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
                self.calcDimValues()
                self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    p1 = property(getP1, None, None, "Dimension first point.")

    def getP2(self):
        """Return the second point of a LinearDimension.

getP2()
        """
        return self.__p2

    def setP2(self, p):
        """Set the second Point of a LinearDimension.

setP2(p)

There is one required argument for this method:

p: A Point contained in a Layer
        """
        if self.isLocked():
            raise RuntimeError, "Setting point not allowed - object locked."
        if not isinstance(p, point.Point):
            raise TypeError, "Invalid point type: " + `type(p)`
        if p.getParent() is None:
            raise ValueError, "Point not stored in a Layer!"
        _pt = self.__p2
        if _pt is not p:
            _pt.disconnect(self)
            _pt.freeUser(self)
            self.startChange('point_changed')
            self.__p2 = p
            self.endChange('point_changed')
            self.sendMessage('point_changed', _pt, p)
            p.storeUser(self)
            p.connect('moved', self.__movePoint)
            p.connect('change_pending', self.__pointChangePending)
            p.connect('change_complete', self.__pointChangeComplete)
            if abs(_pt.x - p.x) > 1e-10 or abs(_pt.y - p.y) > 1e-10:
                _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
                self.calcDimValues()
                self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)
            self.modified()

    p2 = property(getP2, None, None, "Dimension second point.")

    def getDimPoints(self):
        """Return both points used in the LinearDimension.

getDimPoints()

The two points are returned in a tuple.
        """
        return self.__p1, self.__p2

    def getDimBars(self):
        """Return the dimension boundary bars.

getDimBars()
        """
        return self.__bar1, self.__bar2

    def getDimCrossbar(self):
        """Return the dimension crossbar.

getDimCrossbar()
        """
        return self.__crossbar

    def getDimLayers(self):
        """Return both layers used in the LinearDimension.

getDimLayers()

The two layers are returned in a tuple.
        """
        _l1 = self.__p1.getParent()
        _l2 = self.__p2.getParent()
        return _l1, _l2

    def calculate(self):
        """Determine the length of this LinearDimension.

calculate()
        """
        return self.__p1 - self.__p2

    def inRegion(self, xmin, ymin, xmax, ymax, fully=False):
        """Return whether or not a LinearDimension exists within a region.

isRegion(xmin, ymin, xmax, ymax[, fully])

The four arguments define the boundary of an area, and the
function returns True if the LinearDimension lies within that
area. If the optional argument fully is used and is True,
then the dimension points and the location of the dimension
text must lie within the boundary. Otherwise, the function
returns False.
        """
        _xmin = util.get_float(xmin)
        _ymin = util.get_float(ymin)
        _xmax = util.get_float(xmax)
        if _xmax < _xmin:
            raise ValueError, "Illegal values: xmax < xmin"
        _ymax = util.get_float(ymax)
        if _ymax < _ymin:
            raise ValueError, "Illegal values: ymax < ymin"
        util.test_boolean(fully)
        _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
        if ((_dxmin > _xmax) or
            (_dymin > _ymax) or
            (_dxmax < _xmin) or
            (_dymax < _ymin)):
            return False
        if fully:
            if ((_dxmin > _xmin) and
                (_dymin > _ymin) and
                (_dxmax < _xmax) and
                (_dymax < _ymax)):
                return True
            return False
        _dx, _dy = self.getLocation()
        if _xmin < _dx < _xmax and _ymin < _dy < _ymax: # dim text
            return True
        #
        # bar at p1
        #
        _ep1, _ep2 = self.__bar1.getEndpoints()
        _x1, _y1 = _ep1
        _x2, _y2 = _ep2
        if util.in_region(_x1, _y1, _x2, _y2, _xmin, _ymin, _xmax, _ymax):
            return True
        #
        # bar at p2
        #
        _ep1, _ep2 = self.__bar2.getEndpoints()
        _x1, _y1 = _ep1
        _x2, _y2 = _ep2
        if util.in_region(_x1, _y1, _x2, _y2, _xmin, _ymin, _xmax, _ymax):
            return True
        #
        # crossbar
        #
        _ep1, _ep2 = self.__crossbar.getEndpoints()
        _x1, _y1 = _ep1
        _x2, _y2 = _ep2
        return util.in_region(_x1, _y1, _x2, _y2, _xmin, _ymin, _xmax, _ymax)

    def calcDimValues(self, allpts=True):
        """Recalculate the values for dimensional display.

calcDimValues([allpts])

This method calculates where the points for the dimension
bars and crossbar are located. The argument 'allpts' is
optional. By default it is True. If the argument is set to
False, then the coordinates of the dimension marker points
will not be calculated.
        """
        _allpts = allpts
        util.test_boolean(_allpts)
        _p1, _p2 = self.getDimPoints()
        _bar1 = self.__bar1
        _bar2 = self.__bar2
        _crossbar = self.__crossbar
        _p1x, _p1y = _p1.getCoords()
        _p2x, _p2y = _p2.getCoords()
        _dx, _dy = self.getLocation()
        _offset = self.getOffset()
        _ext = self.getExtension()
        #
        # see comp.graphics.algorithms.faq section on calcuating
        # the distance between a point and line for info about
        # the following equations ...
        #
        _dpx = _p2x - _p1x
        _dpy = _p2y - _p1y
        _rnum = ((_dx - _p1x) * _dpx) + ((_dy - _p1y) * _dpy)
        _snum = ((_p1y - _dy) * _dpx) - ((_p1x - _dx) * _dpy)
        _den = pow(_dpx, 2) + pow(_dpy, 2)
        _r = _rnum/_den
        _s = _snum/_den
        _sep = abs(_s) * math.sqrt(_den)
        if abs(_dpx) < 1e-10: # vertical
            if _p2y > _p1y:
                _slope = math.pi/2.0
            else:
                _slope = -math.pi/2.0
        elif abs(_dpy) < 1e-10: # horizontal
            if _p2x > _p1x:
                _slope = 0.0
            else:
                _slope = -math.pi
        else:
            _slope = math.atan2(_dpy, _dpx)
        if _s < 0.0: # dim point left of p1-p2 line
            _angle = _slope + (math.pi/2.0)
        else: # dim point right of p1-p2 line (or on it)
            _angle = _slope - (math.pi/2.0)
        _sin_angle = math.sin(_angle)
        _cos_angle = math.cos(_angle)
        _x = _p1x + (_offset * _cos_angle)
        _y = _p1y + (_offset * _sin_angle)
        _bar1.setFirstEndpoint(_x, _y)
        if _r < 0.0:
            _px = _p1x + (_r * _dpx)
            _py = _p1y + (_r * _dpy)
            _x = _px + (_sep * _cos_angle)
            _y = _py + (_sep * _sin_angle)
        else:
            _x = _p1x + (_sep * _cos_angle)
            _y = _p1y + (_sep * _sin_angle)
        _crossbar.setFirstEndpoint(_x, _y)
        _x = _p1x + (_sep * _cos_angle)
        _y = _p1y + (_sep * _sin_angle)
        _crossbar.setFirstCrossbarPoint(_x, _y)
        _x = _p1x + ((_sep + _ext) * _cos_angle)
        _y = _p1y + ((_sep + _ext) * _sin_angle)
        _bar1.setSecondEndpoint(_x, _y)
        _x = _p2x + (_offset * _cos_angle)
        _y = _p2y + (_offset * _sin_angle)
        _bar2.setFirstEndpoint(_x, _y)
        if _r > 1.0:
            _px = _p1x + (_r * _dpx)
            _py = _p1y + (_r * _dpy)
            _x = _px + (_sep * _cos_angle)
            _y = _py + (_sep * _sin_angle)
        else:
            _x = _p2x + (_sep * _cos_angle)
            _y = _p2y + (_sep * _sin_angle)
        _crossbar.setSecondEndpoint(_x, _y)
        _x = _p2x + (_sep * _cos_angle)
        _y = _p2y + (_sep * _sin_angle)
        _crossbar.setSecondCrossbarPoint(_x, _y)
        _x = _p2x + ((_sep + _ext) * _cos_angle)
        _y = _p2y + ((_sep + _ext) * _sin_angle)
        _bar2.setSecondEndpoint(_x, _y)
        if _allpts:
            self.calcMarkerPoints()

    def calcMarkerPoints(self):
        """Calculate and store the dimension endpoint markers coordinates.

calcMarkerPoints()
        """
        _type = self.getEndpointType()
        _crossbar = self.__crossbar
        _crossbar.clearMarkerPoints()
        if _type == Dimension.DIM_ENDPT_NONE or _type == Dimension.DIM_ENDPT_CIRCLE:
            return
        _size = self.getEndpointSize()
        _p1, _p2 = _crossbar.getCrossbarPoints()
        _x1, _y1 = _p1
        _x2, _y2 = _p2
        # print "x1: %g" % _x1
        # print "y1: %g" % _y1
        # print "x2: %g" % _x2
        # print "y2: %g" % _y2
        _sine, _cosine = _crossbar.getSinCosValues()
        if _type == Dimension.DIM_ENDPT_ARROW or _type == Dimension.DIM_ENDPT_FILLED_ARROW:
            _height = _size/5.0
            # p1 -> (x,y) = (size, _height)
            _mx = (_cosine * _size - _sine * _height) + _x1
            _my = (_sine * _size + _cosine * _height) + _y1
            _crossbar.storeMarkerPoint(_mx, _my)
            # p2 -> (x,y) = (size, -_height)
            _mx = (_cosine * _size - _sine *(-_height)) + _x1
            _my = (_sine * _size + _cosine *(-_height)) + _y1
            _crossbar.storeMarkerPoint(_mx, _my)
            # p3 -> (x,y) = (-size, _height)
            _mx = (_cosine * (-_size) - _sine * _height) + _x2
            _my = (_sine * (-_size) + _cosine * _height) + _y2
            _crossbar.storeMarkerPoint(_mx, _my)
            # p4 -> (x,y) = (-size, -_height)
            _mx = (_cosine * (-_size) - _sine *(-_height)) + _x2
            _my = (_sine * (-_size) + _cosine *(-_height)) + _y2
            _crossbar.storeMarkerPoint(_mx, _my)
        elif _type == Dimension.DIM_ENDPT_SLASH:
            _angle = 30.0 * _dtr # slope of slash
            _height = 0.5 * _size * math.sin(_angle)
            _length = 0.5 * _size * math.cos(_angle)
            # p1 -> (x,y) = (-_length, -_height)
            _sx1 = (_cosine * (-_length) - _sine * (-_height))
            _sy1 = (_sine * (-_length) + _cosine * (-_height))
            # p2 -> (x,y) = (_length, _height)
            _sx2 = (_cosine * _length - _sine * _height)
            _sy2 = (_sine * _length + _cosine * _height)
            #
            # shift the calculate based on the location of the
            # marker point
            #
            _mx = _sx1 + _x2
            _my = _sy1 + _y2
            _crossbar.storeMarkerPoint(_mx, _my)
            _mx = _sx2 + _x2
            _my = _sy2 + _y2
            _crossbar.storeMarkerPoint(_mx, _my)
            _mx = _sx1 + _x1
            _my = _sy1 + _y1
            _crossbar.storeMarkerPoint(_mx, _my)
            _mx = _sx2 + _x1
            _my = _sy2 + _y1
            _crossbar.storeMarkerPoint(_mx, _my)
        else:
            raise ValueError, "Unexpected endpoint type: '%s'" % str(_type)

    def mapCoords(self, x, y, tol=tolerance.TOL):
        """Test an x/y coordinate pair if it could lay on the dimension.

mapCoords(x, y[, tol])

This method has two required parameters:

x: The x-coordinate
y: The y-coordinate

These should both be float values.

There is an optional third parameter tol giving the maximum distance
from the dimension bars that the x/y coordinates may lie.
        """
        _x = util.get_float(x)
        _y = util.get_float(y)
        _t = tolerance.toltest(tol)
        _ep1, _ep2 = self.__bar1.getEndpoints()
        #
        # test p1 bar
        #
        _mp = util.map_coords(_x, _y, _ep1[0], _ep1[1], _ep2[0], _ep2[1], _t)
        if _mp is not None:
            return _mp
        #
        # test p2 bar
        #
        _ep1, _ep2 = self.__bar2.getEndpoints()
        _mp = util.map_coords(_x, _y, _ep1[0], _ep1[1], _ep2[0], _ep2[1], _t)
        if _mp is not None:
            return _mp
        #
        # test crossbar
        #
        _ep1, _ep2 = self.__crossbar.getEndpoints()
        return util.map_coords(_x, _y, _ep1[0], _ep1[1], _ep2[0], _ep2[1], _t)

    def onDimension(self, x, y, tol=tolerance.TOL):
        return self.mapCoords(x, y, tol) is not None

    def getBounds(self):
        """Return the minimal and maximal locations of the dimension

getBounds()

This method overrides the Dimension::getBounds() method
        """
        _dx, _dy = self.getLocation()
        _dxpts = []
        _dypts = []
        _ep1, _ep2 = self.__bar1.getEndpoints()
        _dxpts.append(_ep1[0])
        _dypts.append(_ep1[1])
        _dxpts.append(_ep2[0])
        _dypts.append(_ep2[1])
        _ep1, _ep2 = self.__bar2.getEndpoints()
        _dxpts.append(_ep1[0])
        _dypts.append(_ep1[1])
        _dxpts.append(_ep2[0])
        _dypts.append(_ep2[1])
        _ep1, _ep2 = self.__crossbar.getEndpoints()
        _dxpts.append(_ep1[0])
        _dypts.append(_ep1[1])
        _dxpts.append(_ep2[0])
        _dypts.append(_ep2[1])
        _xmin = min(_dx, min(_dxpts))
        _ymin = min(_dy, min(_dypts))
        _xmax = max(_dx, max(_dxpts))
        _ymax = max(_dy, max(_dypts))
        return _xmin, _ymin, _xmax, _ymax

    def clone(self):
        _p1 = self.__p1
        _p2 = self.__p2
        _x, _y = self.getLocation()
        _ds = self.getDimStyle()
        _ldim = LinearDimension(_p1, _p2, _x, _y, _ds)
        _ldim.copyDimValues(self)
        return _ldim
        
    def __pointChangePending(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        if args[0] == 'moved':
            self.startChange('moved')

    def __pointChangeComplete(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        if args[0] == 'moved':
            self.endChange('moved')

    def __movePoint(self, p, *args):
        _alen = len(args)
        if _alen < 2:
            raise ValueError, "Invalid argument count: %d" % _alen
        if p is not self.__p1 and p is not self.__p2:
            raise ValueError, "Unexpected dimension point: " + `p`
        _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
        self.calcDimValues(True)
        self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)

    def sendsMessage(self, m):
        if m in LinearDimension.__messages:
            return True
        return super(LinearDimension, self).sendsMessage(m)

class HorizontalDimension(LinearDimension):
    """A class representing Horizontal dimensions.

This class is derived from the LinearDimension class, so
it shares all those attributes and methods of its parent.
    """
    def __init__(self, p1, p2, x, y, ds=None, **kw):
        """Initialize a Horizontal Dimension.

hdim = HorizontalDimension(p1, p2, x, y, ds)

p1: A Point contained in a Layer
p2: A Point contained in a Layer
x: The x-coordinate of the dimensional text
y: The y-coordinate of the dimensional text
ds: The DimStyle used for this Dimension.
        """
        super(HorizontalDimension, self).__init__(p1, p2, x, y, ds, **kw)

    def getValues(self):
        """Return values comprising the HorizontalDimension.

getValues()

This method extends the LinearDimension::getValues() method.
        """
        _data = super(HorizontalDimension, self).getValues()
        _data.setValue('type', 'hdim')
        return _data

    def calculate(self):
        """Determine the length of this HorizontalDimension.

calculate()
        """
        _p1, _p2 = self.getDimPoints()
        return abs(_p1.x - _p2.x)

    def calcDimValues(self, allpts=True):
        """Recalculate the values for dimensional display.

calcDimValues([allpts])

This method overrides the LinearDimension::calcDimValues() method.
        """
        _allpts = allpts
        util.test_boolean(_allpts)
        _p1, _p2 = self.getDimPoints()
        _bar1, _bar2 = self.getDimBars()
        _crossbar = self.getDimCrossbar()
        _p1x, _p1y = _p1.getCoords()
        _p2x, _p2y = _p2.getCoords()
        _dx, _dy = self.getLocation()
        _offset = self.getOffset()
        _ext = self.getExtension()
        _crossbar.setFirstEndpoint(_p1x, _dy)
        _crossbar.setSecondEndpoint(_p2x, _dy)
        if _dx < min(_p1x, _p2x) or _dx > max(_p1x, _p2x):
            if _p1x < _p2x:
                if _dx < _p1x:
                    _crossbar.setFirstEndpoint(_dx, _dy)
                if _dx > _p2x:
                    _crossbar.setSecondEndpoint(_dx, _dy)
            else:
                if _dx < _p2x:
                    _crossbar.setSecondEndpoint(_dx, _dy)
                if _dx > _p1x:
                    _crossbar.setFirstEndpoint(_dx, _dy)
        _crossbar.setFirstCrossbarPoint(_p1x, _dy)
        _crossbar.setSecondCrossbarPoint(_p2x, _dy)
        if _dy < min(_p1y, _p2y):
            _bar1.setFirstEndpoint(_p1x, (_p1y - _offset))
            _bar1.setSecondEndpoint(_p1x, (_dy - _ext))
            _bar2.setFirstEndpoint(_p2x, (_p2y - _offset))
            _bar2.setSecondEndpoint(_p2x, (_dy - _ext))
        elif _dy > max(_p1y, _p2y):
            _bar1.setFirstEndpoint(_p1x, (_p1y + _offset))
            _bar1.setSecondEndpoint(_p1x, (_dy + _ext))
            _bar2.setFirstEndpoint(_p2x, (_p2y + _offset))
            _bar2.setSecondEndpoint(_p2x, (_dy + _ext))
        else:
            if _dy > _p1y:
                _bar1.setFirstEndpoint(_p1x, (_p1y + _offset))
                _bar1.setSecondEndpoint(_p1x, (_dy + _ext))
            else:
                _bar1.setFirstEndpoint(_p1x, (_p1y - _offset))
                _bar1.setSecondEndpoint(_p1x, (_dy - _ext))
            if _dy > _p2y:
                _bar2.setFirstEndpoint(_p2x, (_p2y + _offset))
                _bar2.setSecondEndpoint(_p2x, (_dy + _ext))
            else:
                _bar2.setFirstEndpoint(_p2x, (_p2y - _offset))
                _bar2.setSecondEndpoint(_p2x, (_dy - _ext))
        if _allpts:
            self.calcMarkerPoints()

    def clone(self):
        _p1, _p2 = self.getDimPoints()
        _x, _y = self.getLocation()
        _ds = self.getDimStyle()
        _hdim = HorizontalDimension(_p1, _p2, _x, _y, _ds)
        _hdim.copyDimValues(self)
        return _hdim

class VerticalDimension(LinearDimension):
    """A class representing Vertical dimensions.

This class is derived from the LinearDimension class, so
it shares all those attributes and methods of its parent.
    """

    def __init__(self, p1, p2, x, y, ds=None, **kw):
        """Initialize a Vertical Dimension.

vdim = VerticalDimension(p1, p2, x, y, ds)

p1: A Point contained in a Layer
p2: A Point contained in a Layer
x: The x-coordinate of the dimensional text
y: The y-coordinate of the dimensional text
ds: The DimStyle used for this Dimension.
        """
        super(VerticalDimension, self).__init__(p1, p2, x, y, ds, **kw)

    def getValues(self):
        """Return values comprising the VerticalDimension.

getValues()

This method extends the LinearDimension::getValues() method.
        """
        _data = super(VerticalDimension, self).getValues()
        _data.setValue('type', 'vdim')
        return _data

    def calculate(self):
        """Determine the length of this VerticalDimension.

calculate()
        """
        _p1, _p2 = self.getDimPoints()
        return abs(_p1.y - _p2.y)

    def calcDimValues(self, allpts=True):
        """Recalculate the values for dimensional display.

calcDimValues([allpts])

This method overrides the LinearDimension::calcDimValues() method.
        """
        _allpts = allpts
        util.test_boolean(_allpts)
        _p1, _p2 = self.getDimPoints()
        _bar1, _bar2 = self.getDimBars()
        _crossbar = self.getDimCrossbar()
        _p1x, _p1y = _p1.getCoords()
        _p2x, _p2y = _p2.getCoords()
        _dx, _dy = self.getLocation()
        _offset = self.getOffset()
        _ext = self.getExtension()
        _crossbar.setFirstEndpoint(_dx, _p1y)
        _crossbar.setSecondEndpoint(_dx, _p2y)
        if _dy < min(_p1y, _p2y) or _dy > max(_p1y, _p2y):
            if _p1y < _p2y:
                if _dy < _p1y:
                    _crossbar.setFirstEndpoint(_dx, _dy)
                if _dy > _p2y:
                    _crossbar.setSecondEndpoint(_dx, _dy)
            if _p2y < _p1y:
                if _dy < _p2y:
                    _crossbar.setSecondEndpoint(_dx, _dy)
                if _dy > _p1y:
                    _crossbar.setFirstEndpoint(_dx, _dy)
        _crossbar.setFirstCrossbarPoint(_dx, _p1y)
        _crossbar.setSecondCrossbarPoint(_dx, _p2y)
        if _dx < min(_p1x, _p2x):
            _bar1.setFirstEndpoint((_p1x - _offset), _p1y)
            _bar1.setSecondEndpoint((_dx - _ext), _p1y)
            _bar2.setFirstEndpoint((_p2x - _offset), _p2y)
            _bar2.setSecondEndpoint((_dx - _ext), _p2y)
        elif _dx > max(_p1x, _p2x):
            _bar1.setFirstEndpoint((_p1x + _offset), _p1y)
            _bar1.setSecondEndpoint((_dx + _ext), _p1y)
            _bar2.setFirstEndpoint((_p2x + _offset), _p2y)
            _bar2.setSecondEndpoint((_dx + _ext), _p2y)
        else:
            if _dx > _p1x:
                _bar1.setFirstEndpoint((_p1x + _offset), _p1y)
                _bar1.setSecondEndpoint((_dx + _ext), _p1y)
            else:
                _bar1.setFirstEndpoint((_p1x - _offset), _p1y)
                _bar1.setSecondEndpoint((_dx - _ext), _p1y)
            if _dx > _p2x:
                _bar2.setFirstEndpoint((_p2x + _offset), _p2y)
                _bar2.setSecondEndpoint((_dx + _ext), _p2y)
            else:
                _bar2.setFirstEndpoint((_p2x - _offset), _p2y)
                _bar2.setSecondEndpoint((_dx - _ext), _p2y)
        if _allpts:
            self.calcMarkerPoints()

    def clone(self):
        _p1, _p2 = self.getDimPoints()
        _x, _y = self.getLocation()
        _ds = self.getDimStyle()
        _vdim = VerticalDimension(_p1, _p2, _x, _y, _ds)
        _vdim.copyDimValues(self)
        return _vdim

class RadialDimension(Dimension):
    """A class for Radial dimensions.

The RadialDimension class is derived from the Dimension
class, so it shares all of those methods and attributes.
A RadialDimension should be used to display either the
radius or diamter of a Circle object.

A RadialDimension object has the following methods:

{get/set}DimCircle(): Get/Set the measured circle object.
getDimLayer(): Return the layer containing the measured circle.
{get/set}DiaMode(): Get/Set if the RadialDimension should return diameters.
getDimXPoints(): Get the x-coordinates of the dimension bar positions.
getDimYPoints(): Get the y-coordinates of the dimension bar positions.
getDimMarkerPoints(): Get the locaiton of the dimension endpoint markers.
getDimCrossbar(): Get the DimCrossbar object of the RadialDimension.
calcDimValues(): Calculate the endpoint of the dimension line.
mapCoords(): Return coordinates on the dimension near some point.
onDimension(): Test if an x/y coordinate pair fall on the dimension line.
    """
    __messages = {
        'dimobj_changed' : True,
        'dia_mode_changed' : True,
        }
        
    def __init__(self, cir, x, y, ds=None, **kw):
        """Initialize a RadialDimension object.

rdim = RadialDimension(cir, x, y, ds)

cir: A Circle or Arc object
x: The x-coordinate of the dimensional text
y: The y-coordinate of the dimensional text
ds: The DimStyle used for this Dimension.
        """
        super(RadialDimension, self).__init__(x, y, ds, **kw)
        if not isinstance(cir, (circle.Circle, arc.Arc)):
            raise TypeError, "Invalid circle/arc type: " + `type(cir)`
        if cir.getParent() is None:
            raise ValueError, "Circle/Arc not found in Layer!"
        self.__circle = cir
        self.__crossbar = DimCrossbar()
        self.__dia_mode = False
        cir.storeUser(self)
        _ds = self.getDimStyle()
        _pds, _sds = self.getDimstrings()
        _pds.mute()
        try:
            _pds.setPrefix(_ds.getValue('RADIAL_DIM_PRIMARY_PREFIX'))
            _pds.setSuffix(_ds.getValue('RADIAL_DIM_PRIMARY_SUFFIX'))
        finally:
            _pds.unmute()
        _sds.mute()
        try:
            _sds.setPrefix(_ds.getValue('RADIAL_DIM_SECONDARY_PREFIX'))
            _sds.setSuffix(_ds.getValue('RADIAL_DIM_SECONDARY_SUFFIX'))
        finally:
            _sds.unmute()
        self.setDiaMode(_ds.getValue('RADIAL_DIM_DIA_MODE'))
        cir.connect('moved', self.__moveCircle)
        cir.connect('radius_changed', self.__radiusChanged)
        cir.connect('change_pending', self.__circleChangePending)
        cir.connect('change_complete', self.__circleChangeComplete)
        self.calcDimValues()

    def __eq__(self, rdim):
        """Compare two RadialDimensions for equality.
        """
        if not isinstance(rdim, RadialDimension):
            return False
        _val = False
        _layer = self.__circle.getParent()
        _rc = rdim.getDimCircle()
        _rl = _rc.getParent()
        if _layer is _rl and self.__circle == _rc:
            _val = True
        return _val

    def __ne__(self, rdim):
        """Compare two RadialDimensions for inequality.
        """
        if not isinstance(rdim, RadialDimension):
            return True
        _val = True
        _layer = self.__circle.getParent()
        _rc = rdim.getDimCircle()
        _rl = _rc.getParent()
        if _layer is _rl and self.__circle == _rc:
            _val = False
        return _val

    def finish(self):
        self.__circle.disconnect(self)
        self.__circle.freeUser(self)
        self.__circle = self.__crossbar = None
        super(RadialDimension, self).finish()

    def getValues(self):
        """Return values comprising the RadialDimension.

getValues()

This method extends the Dimension::getValues() method.
        """
        _data = super(RadialDimension, self).getValues()
        _data.setValue('type', 'rdim')
        _data.setValue('circle', self.__circle.getID())
        _layer = self.__circle.getParent()
        _data.setValue('layer', _layer.getID())
        _data.setValue('dia_mode', self.__dia_mode)
        return _data

    def getDiaMode(self):
        """Return if the RadialDimension will return diametrical values.

getDiaMode()

This method returns True if the diameter value is returned,
and False otherwise.
        """
        return self.__dia_mode

    def setDiaMode(self, mode=False):
        """Set the RadialDimension to return diametrical values.

setDiaMode([mode])

Calling this method without an argument sets the RadialDimension
to return radial measurements. If the argument "mode" is supplied,
it should be either True or False.

If the RadialDimension is measuring an arc, the returned value
will always be set to return a radius.
        """
        util.test_boolean(mode)
        if not isinstance(self.__circle, arc.Arc):
            _m = self.__dia_mode
            if _m is not mode:
                self.startChange('dia_mode_changed')
                self.__dia_mode = mode
                self.endChange('dia_mode_changed')
                self.sendMessage('dia_mode_changed', _m)
                self.calcDimValues()
                self.modified()

    dia_mode = property(getDiaMode, setDiaMode, None,
                        "Draw the Dimension as a diameter")

    def getDimLayer(self):
        """Return the Layer object holding the Circle for this RadialDimension.

getDimLayer()
        """
        return self.__circle.getParent()

    def getDimCircle(self):
        """Return the Circle object this RadialDimension is measuring.

getDimCircle()
        """
        return self.__circle

    def setDimCircle(self, c):
        """Set the Circle object measured by this RadialDimension.

setDimCircle(c)

The argument for this method is:

c: A Circle/Arc contained in a Layer
        """
        if self.isLocked():
            raise RuntimeError, "Setting circle/arc not allowed - object locked."
        if not isinstance(c, (circle.Circle, arc.Arc)):
            raise TypeError, "Invalid circle/arc type: " + `type(c)`
        if c.getParent() is None:
            raise ValueError, "Circle/Arc not found in a Layer!"
        _circ = self.__circle
        if _circ is not c:
            _circ.disconnect(self)
            _circ.freeUser(self)
            self.startChange('dimobj_changed')
            self.__circle = c
            self.endChange('dimobj_changed')
            c.storeUser(self)
            self.sendMessage('dimobj_changed', _circ, c)
            c.connect('moved', self.__moveCircle)
            c.connect('radius_changed', self.__radiusChanged)
            c.connect('change_pending', self.__circleChangePending)
            c.connect('change_complete', self.__circleChangeComplete)
            self.calcDimValues()
            self.modified()

    circle = property(getDimCircle, None, None,
                      "Radial dimension circle object.")

    def getDimCrossbar(self):
        """Get the DimCrossbar object used by the RadialDimension.

getDimCrossbar()
        """
        return self.__crossbar

    def calcDimValues(self, allpts=True):
        """Recalculate the values for dimensional display.

calcDimValues([allpts])

The optional argument 'allpts' is by default True. Calling
this method with the argument set to False will skip the
calculation of any dimension endpoint marker points.
        """
        _allpts = allpts
        util.test_boolean(_allpts)
        _c = self.__circle
        _dimbar = self.__crossbar
        _cx, _cy = _c.getCenter().getCoords()
        _rad = _c.getRadius()
        _dx, _dy = self.getLocation()
        _dia_mode = self.__dia_mode
        _sep = math.hypot((_dx - _cx), (_dy - _cy))
        _angle = math.atan2((_dy - _cy), (_dx - _cx))
        _sx = _rad * math.cos(_angle)
        _sy = _rad * math.sin(_angle)
        if isinstance(_c, arc.Arc):
            assert _dia_mode is False, "dia_mode for arc radial dimension"
            _sa = _c.getStartAngle()
            _ea = _c.getEndAngle()
            _angle = _rtd * _angle
            if _angle < 0.0:
                _angle = _angle + 360.0
            if not _c.throughAngle(_angle):
                _ep1, _ep2 = _c.getEndpoints()
                if _angle < _sa:
                    _sa = _dtr * _sa
                    _sx = _rad * math.cos(_sa)
                    _sy = _rad * math.sin(_sa)
                    if _sep > _rad:
                        _dx = _cx + (_sep * math.cos(_sa))
                        _dy = _cy + (_sep * math.sin(_sa))
                if _angle > _ea:
                    _ea = _dtr * _ea
                    _sx = _rad * math.cos(_ea)
                    _sy = _rad * math.sin(_ea)
                    if _sep > _rad:
                        _dx = _cx + (_sep * math.cos(_ea))
                        _dy = _cy + (_sep * math.sin(_ea))
        if _dia_mode:
            _dimbar.setFirstEndpoint((_cx - _sx), (_cy - _sy))
            _dimbar.setFirstCrossbarPoint((_cx - _sx), (_cy - _sy))
        else:
            _dimbar.setFirstEndpoint(_cx, _cy)
            _dimbar.setFirstCrossbarPoint(_cx, _cy)
        if _sep > _rad:
            _dimbar.setSecondEndpoint(_dx, _dy)
        else:
            _dimbar.setSecondEndpoint((_cx + _sx), (_cy + _sy))
        _dimbar.setSecondCrossbarPoint((_cx + _sx), (_cy + _sy))
        if not _allpts:
            return
        #
        # calculate dimension endpoint marker coordinates
        #
        _type = self.getEndpointType()
        _dimbar.clearMarkerPoints()
        if _type == Dimension.DIM_ENDPT_NONE or _type == Dimension.DIM_ENDPT_CIRCLE:
            return
        _size = self.getEndpointSize()
        _x1, _y1 = _dimbar.getFirstCrossbarPoint()
        _x2, _y2 = _dimbar.getSecondCrossbarPoint()
        _sine, _cosine = _dimbar.getSinCosValues()
        if _type == Dimension.DIM_ENDPT_ARROW or _type == Dimension.DIM_ENDPT_FILLED_ARROW:
            _height = _size/5.0
            # p1 -> (x,y) = (size, _height)
            _mx = (_cosine * _size - _sine * _height) + _x1
            _my = (_sine * _size + _cosine * _height) + _y1
            _dimbar.storeMarkerPoint(_mx, _my)
            # p2 -> (x,y) = (size, -_height)
            _mx = (_cosine * _size - _sine *(-_height)) + _x1
            _my = (_sine * _size + _cosine *(-_height)) + _y1
            _dimbar.storeMarkerPoint(_mx, _my)
            # p3 -> (x,y) = (-size, _height)
            _mx = (_cosine * (-_size) - _sine * _height) + _x2
            _my = (_sine * (-_size) + _cosine * _height) + _y2
            _dimbar.storeMarkerPoint(_mx, _my)
            # p4 -> (x,y) = (-size, -_height)
            _mx = (_cosine * (-_size) - _sine *(-_height)) + _x2
            _my = (_sine * (-_size) + _cosine *(-_height)) + _y2
            _dimbar.storeMarkerPoint(_mx, _my)
        elif _type == Dimension.DIM_ENDPT_SLASH:
            _angle = 30.0 * _dtr # slope of slash
            _height = 0.5 * _size * math.sin(_angle)
            _length = 0.5 * _size * math.cos(_angle)
            # p1 -> (x,y) = (-_length, -_height)
            _sx1 = (_cosine * (-_length) - _sine * (-_height))
            _sy1 = (_sine * (-_length) + _cosine * (-_height))
            # p2 -> (x,y) = (_length, _height)
            _sx2 = (_cosine * _length - _sine * _height)
            _sy2 = (_sine * _length + _cosine * _height)
            #
            # shift the calculate based on the location of the
            # marker point
            #
            _mx = _sx1 + _x1
            _my = _sy1 + _y1
            _dimbar.storeMarkerPoint(_mx, _my)
            _mx = _sx2 + _x1
            _my = _sy2 + _y1
            _dimbar.storeMarkerPoint(_mx, _my)
            _mx = _sx1 + _x2
            _my = _sy1 + _y2
            _dimbar.storeMarkerPoint(_mx, _my)
            _mx = _sx2 + _x2
            _my = _sy2 + _y2
            _dimbar.storeMarkerPoint(_mx, _my)
        else:
            raise ValueError, "Unexpected endpoint type: '%s'" % str(_type)

    def calculate(self):
        """Return the radius or diamter of this RadialDimension.

calculate()

By default, a RadialDimension will return the radius of the
circle. The setDiaMode() method can be called to set the
returned value to corresponed to a diameter.
        """
        _val = self.__circle.getRadius()
        if self.__dia_mode is True:
            _val = _val * 2.0
        return _val

    def inRegion(self, xmin, ymin, xmax, ymax, fully=False):
        """Return whether or not a RadialDimension exists within a region.

isRegion(xmin, ymin, xmax, ymax[, fully])

The four arguments define the boundary of an area, and the
function returns True if the RadialDimension lies within that
area. If the optional argument 'fully' is used and is True,
then the dimensioned circle and the location of the dimension
text must lie within the boundary. Otherwise, the function
returns False.
        """
        _xmin = util.get_float(xmin)
        _ymin = util.get_float(ymin)
        _xmax = util.get_float(xmax)
        if _xmax < _xmin:
            raise ValueError, "Illegal values: xmax < xmin"
        _ymax = util.get_float(ymax)
        if _ymax < _ymin:
            raise ValueError, "Illegal values: ymax < ymin"
        util.test_boolean(fully)
        _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
        if ((_dxmin > _xmax) or
            (_dymin > _ymax) or
            (_dxmax < _xmin) or
            (_dymax < _ymin)):
            return False
        if fully:
            if ((_dxmin > _xmin) and
                (_dymin > _ymin) and
                (_dxmax < _xmax) and
                (_dymax < _ymax)):
                return True
            return False
        _dx, _dy = self.getLocation()
        if _xmin < _dx < _xmax and _ymin < _dy < _ymax: # dim text
            return True
        _p1, _p2 = self.__crossbar.getEndpoints()
        _x1, _y1 = _p1
        _x2, _y2 = _p2
        return util.in_region(_x1, _y1, _x2, _y2, _xmin, _ymin, _xmax, _ymax)

    def mapCoords(self, x, y, tol=tolerance.TOL):
        """Test an x/y coordinate pair if it could lay on the dimension.

mapCoords(x, y[, tol])

This method has two required parameters:

x: The x-coordinate
y: The y-coordinate

These should both be float values.

There is an optional third parameter, 'tol', giving
the maximum distance from the dimension bars that the
x/y coordinates may sit.
        """
        _x = util.get_float(x)
        _y = util.get_float(y)
        _t = tolerance.toltest(tol)
        _p1, _p2 = self.__crossbar.getEndpoints()
        _x1, _y1 = _p1
        _x2, _y2 = _p2
        return util.map_coords(_x, _y, _x1, _y1, _x2, _y2, _t)

    def onDimension(self, x, y, tol=tolerance.TOL):
        return self.mapCoords(x, y, tol) is not None

    def getBounds(self):
        """Return the minimal and maximal locations of the dimension

getBounds()

This method overrides the Dimension::getBounds() method
        """
        _p1, _p2 = self.__crossbar.getEndpoints()
        _x1, _y1 = _p1
        _x2, _y2 = _p2
        _xmin = min(_x1, _x2)
        _ymin = min(_y1, _y2)
        _xmax = max(_x1, _x2)
        _ymax = max(_y1, _y2)
        return _xmin, _ymin, _xmax, _ymax

    def clone(self):
        _c = self.__circle
        _x, _y = self.getLocation()
        _ds = self.getDimStyle()
        _rdim = RadialDimension(_c, _x, _y, _ds)
        _rdim.copyDimValues(self)
        _rdim.setDiaMode(self.getDiaMode())
        return _rdim

    def __circleChangePending(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        if args[0] == 'moved' or args[0] =='radius_changed':
            self.startChange('moved')

    def __circleChangeComplete(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        if args[0] == 'moved' or args[0] =='radius_changed':
            self.endChange('moved')

    def __moveCircle(self, circ, *args):
        _alen = len(args)
        if _alen < 3:
            raise ValueError, "Invalid argument count: %d" % _alen
        if circ is not self.__circle:
            raise ValueError, "Unexpected sender: " + `circ`
        _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
        self.calcDimValues()
        self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)

    def __radiusChanged(self, circ, *args):
        self.calcDimValues()
        
    def sendsMessage(self, m):
        if m in RadialDimension.__messages:
            return True
        return super(RadialDimension, self).sendsMessage(m)

class AngularDimension(Dimension):
    """A class for Angular dimensions.

The AngularDimension class is derived from the Dimension
class, so it shares all of those methods and attributes.

AngularDimension objects have the following methods:

{get/set}VertexPoint(): Get/Set the vertex point for the AngularDimension.
{get/set}P1(): Get/Set the first Point for the AngularDimension.
{get/set}P2(): Get/Set the second Point for the AngularDimension.
getDimPoints(): Return the two Points used in this dimension.
getDimLayers(): Return the two Layers holding the Points.
getDimXPoints(): Get the x-coordinates of the dimension bar positions.
getDimYPoints(): Get the y-coordinates of the dimension bar positions.
getDimAngles(): Get the angles at which the dimension bars should be drawn.
getDimMarkerPoints(): Get the locaiton of the dimension endpoint markers.
calcDimValues(): Calculate the endpoint of the dimension line.
mapCoords(): Return coordinates on the dimension near some point.
onDimension(): Test if an x/y coordinate pair fall on the dimension line.
invert(): Switch the endpoints used to measure the dimension
    """

    __messages = {
        'point_changed' : True,
        'inverted' : True,
        }
        
    def __init__(self, vp, p1, p2, x, y, ds=None, **kw):
        """Initialize an AngularDimension object.

adim = AngularDimension(vp, p1, p2, x, y, ds)

vp: A Point contained in a Layer
p1: A Point contained in a Layer
p2: A Point contained in a Layer
x: The x-coordinate of the dimensional text
y: The y-coordinate of the dimensional text
ds: The DimStyle used for this Dimension.
        """
        super(AngularDimension, self).__init__(x, y, ds, **kw)
        if not isinstance(vp, point.Point):
            raise TypeError, "Invalid point type: " + `type(vp)`
        if vp.getParent() is None:
            raise ValueError, "Vertex Point not found in a Layer!"
        if not isinstance(p1, point.Point):
            raise TypeError, "Invalid point type: " + `type(p1)`
        if p1.getParent() is None:
            raise ValueError, "Point P1 not found in a Layer!"
        if not isinstance(p2, point.Point):
            raise TypeError, "Invalid point type: " + `type(p2)`
        if p2.getParent() is None:
            raise ValueError, "Point P2 not found in a Layer!"
        self.__vp = vp
        self.__p1 = p1
        self.__p2 = p2
        self.__bar1 = DimBar()
        self.__bar2 = DimBar()
        self.__crossarc = DimCrossarc()
        _ds = self.getDimStyle()
        _pds, _sds = self.getDimstrings()
        _pds.mute()
        try:
            _pds.setPrefix(_ds.getValue('ANGULAR_DIM_PRIMARY_PREFIX'))
            _pds.setSuffix(_ds.getValue('ANGULAR_DIM_PRIMARY_SUFFIX'))
        finally:
            _pds.unmute()
        _sds.mute()
        try:
            _sds.setPrefix(_ds.getValue('ANGULAR_DIM_SECONDARY_PREFIX'))
            _sds.setSuffix(_ds.getValue('ANGULAR_DIM_SECONDARY_SUFFIX'))
        finally:
            _sds.unmute()
        vp.storeUser(self)
        vp.connect('moved', self.__movePoint)
        vp.connect('change_pending', self.__pointChangePending)
        vp.connect('change_complete', self.__pointChangeComplete)
        p1.storeUser(self)
        p1.connect('moved', self.__movePoint)
        p1.connect('change_pending', self.__pointChangePending)
        p1.connect('change_complete', self.__pointChangeComplete)
        p2.storeUser(self)
        p2.connect('moved', self.__movePoint)
        p2.connect('change_pending', self.__pointChangePending)
        p2.connect('change_complete', self.__pointChangeComplete)
        self.calcDimValues()

    def __eq__(self, adim):
        """Compare two AngularDimensions for equality.
        """
        if not isinstance(adim, AngularDimension):
            return False
        _val = False
        _lvp = self.__vp.getParent()
        _lp1 = self.__p1.getParent()
        _lp2 = self.__p2.getParent()
        _vl, _l1, _l2 = adim.getDimLayers()
        _vp, _p1, _p2 = adim.getDimPoints()
        if (_lvp is _vl and
            self.__vp == _vp and
            _lp1 is _l1 and
            self.__p1 == _p1 and
            _lp2 is _l2 and
            self.__p2 == _p2):
            _val = True
        return _val

    def __ne__(self, adim):
        """Compare two AngularDimensions for inequality.
        """
        if not isinstance(adim, AngularDimension):
            return True
        _val = True
        _lvp = self.__vp.getParent()
        _lp1 = self.__p1.getParent()
        _lp2 = self.__p2.getParent()
        _vl, _l1, _l2 = adim.getDimLayers()
        _vp, _p1, _p2 = adim.getDimPoints()
        if (_lvp is _vl and
            self.__vp == _vp and
            _lp1 is _l1 and
            self.__p1 == _p1 and
            _lp2 is _l2 and
            self.__p2 == _p2):
            _val = False
        return _val

    def finish(self):
        self.__vp.disconnect(self)
        self.__vp.freeUser(self)
        self.__p1.disconnect(self)
        self.__p1.freeUser(self)
        self.__p2.disconnect(self)
        self.__p2.freeUser(self)
        self.__bar1 = self.__bar2 = self.__crossarc = None
        self.__vp = self.__p1 = self.__p2 = None
        super(AngularDimension, self).finish()

    def getValues(self):
        """Return values comprising the AngularDimension.

getValues()

This method extends the Dimension::getValues() method.
        """
        _data = super(AngularDimension, self).getValues()
        _data.setValue('type', 'adim')
        _data.setValue('vp', self.__vp.getID())
        _layer = self.__vp.getParent()
        _data.setValue('vl', _layer.getID())
        _data.setValue('p1', self.__p1.getID())
        _layer = self.__p1.getParent()
        _data.setValue('l1', _layer.getID())
        _data.setValue('p2', self.__p2.getID())
        _layer = self.__p2.getParent()
        _data.setValue('l2', _layer.getID())
        return _data

    def getDimLayers(self):
        """Return the layers used in an AngularDimension.

getDimLayers()
        """
        _vl = self.__vp.getParent()
        _l1 = self.__p1.getParent()
        _l2 = self.__p2.getParent()
        return _vl, _l1, _l2

    def getDimPoints(self):
        """Return the points used in an AngularDimension.

getDimPoints()
        """
        return self.__vp, self.__p1, self.__p2

    def getVertexPoint(self):
        """Return the vertex point used in an AngularDimension.

getVertexPoint()
        """
        return self.__vp

    def setVertexPoint(self, p):
        """Set the vertex point for an AngularDimension.

setVertexPoint(p)

There is one required argument for this method:

p: A Point contained in Layer
        """
        if self.isLocked():
            raise RuntimeError, "Setting vertex point allowed - object locked."
        if not isinstance(p, point.Point):
            raise TypeError, "Invalid point type: " + `type(p)`
        if p.getParent() is None:
            raise ValueError, "Point not found in a Layer!"
        _vp = self.__vp
        if _vp is not p:
            _vp.disconnect(self)
            _vp.freeUser(self)
            self.startChange('point_changed')
            self.__vp = p
            self.endChange('point_changed')
            p.storeUser(self)
            p.connect('moved', self.__movePoint)
            p.connect('change_pending', self.__pointChangePending)
            p.connect('change_complete', self.__pointChangeComplete)
            self.sendMessage('point_changed', _vp, p)
            self.calcDimValues()
            if abs(_vp.x - p.x) > 1e-10 or abs(_vp.y - p.y) > 1e-10:
                _x1, _y1 = self.__p1.getCoords()
                _x2, _y2 = self.__p2.getCoords()
                _dx, _dy = self.getLocation()
                self.sendMessage('moved', _vp.x, _vp.y, _x1, _y1,
                                 _x2, _y2, _dx, _dy)
            self.modified()

    vp = property(getVertexPoint, None, None,
                  "Angular Dimension vertex point.")

    def getP1(self):
        """Return the first angle point used in an AngularDimension.

getP1()
        """
        return self.__p1

    def setP1(self, p):
        """Set the first Point for an AngularDimension.

setP1(p)

There is one required argument for this method:

p: A Point contained in a Layer.
        """
        if self.isLocked():
            raise RuntimeError, "Setting vertex point allowed - object locked."
        if not isinstance(p, point.Point):
            raise TypeError, "Invalid point type: " + `type(p)`
        if p.getParent() is None:
            raise ValueError, "Point not found in a Layer!"
        _p1 = self.__p1
        if _p1 is not p:
            _p1.disconnect(self)
            _p1.freeUser(self)
            self.startChange('point_changed')
            self.__p1 = p
            self.endChange('point_changed')
            p.storeUser(self)
            p.connect('moved', self.__movePoint)
            p.connect('change_pending', self.__pointChangePending)
            p.connect('change_complete', self.__pointChangeComplete)
            self.sendMessage('point_changed', _p1, p)
            self.calcDimValues()
            if abs(_p1.x - p.x) > 1e-10 or abs(_p1.y - p.y) > 1e-10:
                _vx, _vy = self.__vp.getCoords()
                _x2, _y2 = self.__p2.getCoords()
                _dx, _dy = self.getLocation()
                self.sendMessage('moved', _vx, _vy, _p1.x, _p1.y,
                                 _x2, _y2, _dx, _dy)
            self.modified()

    p1 = property(getP1, None, None, "Dimension first point.")

    def getP2(self):
        """Return the second angle point used in an AngularDimension.

getP2()
        """
        return self.__p2

    def setP2(self, p):
        """Set the second Point for an AngularDimension.

setP2(p)

There is one required argument for this method:

l: The layer holding the Point p
p: A point in Layer l
        """
        if self.isLocked():
            raise RuntimeError, "Setting vertex point allowed - object locked."
        if not isinstance(p, point.Point):
            raise TypeError, "Invalid point type: " + `type(p)`
        if p.getParent() is None:
            raise ValueError, "Point not found in a Layer!"
        _p2 = self.__p2
        if _p2 is not p:
            _p2.disconnect(self)
            _p2.freeUser(self)
            self.startChange('point_changed')
            self.__p2 = p
            self.endChange('point_changed')
            p.storeUser(self)
            p.connect('moved', self.__movePoint)
            p.connect('change_pending', self.__pointChangePending)
            p.connect('change_complete', self.__pointChangeComplete)
            self.sendMessage('point_changed', _p2, p)
            self.calcDimValues()
            if abs(_p2.x - p.x) > 1e-10 or abs(_p2.y - p.y) > 1e-10:
                _vx, _vy = self.__vp.getCoords()
                _x1, _y1 = self.__p1.getCoords()
                _dx, _dy = self.getLocation()
                self.sendMessage('moved', _vx, _vy, _x1, _y1,
                                 _p2.x, _p2.y, _dx, _dy)
            self.modified()


    p2 = property(getP2, None, None, "Dimension second point.")

    def getDimAngles(self):
        """Get the array of dimension bar angles.

geDimAngles()
        """
        _angle1 = self.__bar1.getAngle()
        _angle2 = self.__bar2.getAngle()
        return _angle1, _angle2

    def getDimRadius(self):
        """Get the radius of the dimension crossarc.

getDimRadius()
        """
        return self.__crossarc.getRadius()

    def getDimBars(self):
        """Return the dimension boundary bars.

getDimBars()
        """
        return self.__bar1, self.__bar2

    def getDimCrossarc(self):
        """Get the DimCrossarc object used by the AngularDimension.

getDimCrossarc()
        """
        return self.__crossarc

    def invert(self):
        """Switch the endpoints used in this object.

invert()

Invoking this method on an AngularDimension will result in
it measuring the opposite angle than what it currently measures.
        """
        _pt = self.__p1
        self.startChange('inverted')
        self.__p1 = self.__p2
        self.__p2 = _pt
        self.endChange('inverted')
        self.sendMessage('inverted')
        self.calcDimValues()
        self.modified()

    def calculate(self):
        """Find the value of the angle measured by this AngularDimension.

calculate()
        """
        _vx, _vy = self.__vp.getCoords()
        _p1x, _p1y = self.__p1.getCoords()
        _p2x, _p2y = self.__p2.getCoords()
        _a1 = _rtd * math.atan2((_p1y - _vy), (_p1x - _vx))
        if _a1 < 0.0:
            _a1 = _a1 + 360.0
        _a2 = _rtd * math.atan2((_p2y - _vy), (_p2x - _vx))
        if _a2 < 0.0:
            _a2 = _a2 + 360.0
        _val = _a2 - _a1
        if _a1 > _a2:
            _val = _val + 360.0
        return _val

    def inRegion(self, xmin, ymin, xmax, ymax, fully=False):
        """Return whether or not an AngularDimension exists within a region.

isRegion(xmin, ymin, xmax, ymax[, fully])

The four arguments define the boundary of an area, and the
function returns True if the RadialDimension lies within that
area. If the optional argument 'fully' is used and is True,
then the dimensioned circle and the location of the dimension
text must lie within the boundary. Otherwise, the function
returns False.
        """
        _xmin = util.get_float(xmin)
        _ymin = util.get_float(ymin)
        _xmax = util.get_float(xmax)
        if _xmax < _xmin:
            raise ValueError, "Illegal values: xmax < xmin"
        _ymax = util.get_float(ymax)
        if _ymax < _ymin:
            raise ValueError, "Illegal values: ymax < ymin"
        util.test_boolean(fully)
        _vx, _vy = self.__vp.getCoords()
        _dx, _dy = self.getLocation()
        _pxmin, _pymin, _pxmax, _pymax = self.getBounds()
        _val = False
        if ((_pxmin > _xmax) or
            (_pymin > _ymax) or
            (_pxmax < _xmin) or
            (_pymax < _ymin)):
            return False
        if _xmin < _dx < _xmax and _ymin < _dy < _ymax:
            return True
        #
        # bar on vp-p1 line
        #
        _ep1, _ep2 = self.__bar1.getEndpoints()
        _ex1, _ey1 = _ep1
        _ex2, _ey2 = _ep2
        if util.in_region(_ex1, _ey1, _ex2, _ey2, _xmin, _ymin, _xmax, _ymax):
            return True
        #
        # bar at vp-p2 line
        #
        _ep1, _ep2 = self.__bar2.getEndpoints()
        _ex1, _ey1 = _ep1
        _ex2, _ey2 = _ep2
        if util.in_region(_ex1, _ey1, _ex2, _ey2, _xmin, _ymin, _xmax, _ymax):
            return True
        #
        # dimension crossarc
        #
        _val = False
        _r = self.__crossarc.getRadius()
        _d1 = math.hypot((_xmin - _vx), (_ymin - _vy))
        _d2 = math.hypot((_xmin - _vx), (_ymax - _vy))
        _d3 = math.hypot((_xmax - _vx), (_ymax - _vy))
        _d4 = math.hypot((_xmax - _vx), (_ymin - _vy))
        _dmin = min(_d1, _d2, _d3, _d4)
        _dmax = max(_d1, _d2, _d3, _d4)
        if _xmin < _vx < _xmax and _ymin < _vy < _ymax:
            _dmin = -1e-10
        else:
            if _vx > _xmax and _ymin < _vy < _ymax:
                _dmin = _vx - _xmax
            elif _vx < _xmin and _ymin < _vy < _ymax:
                _dmin = _xmin - _vx
            elif _vy > _ymax and _xmin < _vx < _xmax:
                _dmin = _vy - _ymax
            elif _vy < _ymin and _xmin < _vx < _xmax:
                _dmin = _ymin - _vy
        if _dmin < _r < _dmax:
            _da = _rtd * math.atan2((_ymin - _vy), (_xmin - _vx))
            if _da < 0.0:
                _da = _da + 360.0
            _val = self._throughAngle(_da)
            if _val:
                return _val
            _da = _rtd * math.atan2((_ymin - _vy), (_xmax - _vx))
            if _da < 0.0:
                _da = _da + 360.0
            _val = self._throughAngle(_da)
            if _val:
                return _val
            _da = _rtd * math.atan2((_ymax - _vy), (_xmax - _vx))
            if _da < 0.0:
                _da = _da + 360.0
            _val = self._throughAngle(_da)
            if _val:
                return _val
            _da = _rtd * math.atan2((_ymax - _vy), (_xmin - _vx))
            if _da < 0.0:
                _da = _da + 360.0
            _val = self._throughAngle(_da)
        return _val

    def _throughAngle(self, angle):
        """Test if the angular crossarc exists at a certain angle.

_throughAngle()

This method is private to the AngularDimension class.
        """
        _crossarc = self.__crossarc
        _sa = _crossarc.getStartAngle()
        _ea = _crossarc.getEndAngle()
        _val = True
        if abs(_sa - _ea) > 1e-10:
            if _sa > _ea:
                if angle > _ea and angle < _sa:
                    _val = False
            else:
                if angle > _ea or angle < _sa:
                    _val = False
        return _val

    def calcDimValues(self, allpts=True):
        """Recalculate the values for dimensional display.

calcDimValues([allpts])

The optional argument 'allpts' is by default True. Calling
this method with the argument set to False will skip the
calculation of any dimension endpoint marker points.
        """
        _allpts = allpts
        util.test_boolean(_allpts)
        _vx, _vy = self.__vp.getCoords()
        _p1x, _p1y = self.__p1.getCoords()
        _p2x, _p2y = self.__p2.getCoords()
        _dx, _dy = self.getLocation()
        _offset = self.getOffset()
        _ext = self.getExtension()
        _bar1 = self.__bar1
        _bar2 = self.__bar2
        _crossarc = self.__crossarc
        _dv1 = math.hypot((_p1x - _vx), (_p1y - _vy))
        _dv2 = math.hypot((_p2x - _vx), (_p2y - _vy))
        _ddp = math.hypot((_dx - _vx), (_dy - _vy))
        _crossarc.setRadius(_ddp)
        #
        # first dimension bar
        #
        _angle = math.atan2((_p1y - _vy), (_p1x - _vx))
        _sine = math.sin(_angle)
        _cosine = math.cos(_angle)
        _deg = _angle * _rtd
        if _deg < 0.0:
            _deg = _deg + 360.0
        _crossarc.setStartAngle(_deg)
        _ex = _vx + (_ddp * _cosine)
        _ey = _vy + (_ddp * _sine)
        _crossarc.setFirstCrossbarPoint(_ex, _ey)
        _crossarc.setFirstEndpoint(_ex, _ey)
        if _ddp > _dv1: # dim point is radially further to vp than p1
            _x1 = _p1x + (_offset * _cosine)
            _y1 = _p1y + (_offset * _sine)
            _x2 = _vx + ((_ddp + _ext) * _cosine)
            _y2 = _vy + ((_ddp + _ext) * _sine)
        else: # dim point is radially closer to vp than p1
            _x1 = _p1x - (_offset * _cosine)
            _y1 = _p1y - (_offset * _sine)
            _x2 = _vx + ((_ddp - _ext) * _cosine)
            _y2 = _vy + ((_ddp - _ext) * _sine)
        _bar1.setFirstEndpoint(_x1, _y1)
        _bar1.setSecondEndpoint(_x2, _y2)
        #
        # second dimension bar
        #
        _angle = math.atan2((_p2y - _vy), (_p2x - _vx))
        _sine = math.sin(_angle)
        _cosine = math.cos(_angle)
        _deg = _angle * _rtd
        if _deg < 0.0:
            _deg = _deg + 360.0
        _crossarc.setEndAngle(_deg)
        _ex = _vx + (_ddp * _cosine)
        _ey = _vy + (_ddp * _sine)
        _crossarc.setSecondCrossbarPoint(_ex, _ey)
        _crossarc.setSecondEndpoint(_ex, _ey)
        if _ddp > _dv2: # dim point is radially further to vp than p2
            _x1 = _p2x + (_offset * _cosine)
            _y1 = _p2y + (_offset * _sine)
            _x2 = _vx + ((_ddp + _ext) * _cosine)
            _y2 = _vy + ((_ddp + _ext) * _sine)
        else: # dim point is radially closers to vp than p2
            _x1 = _p2x - (_offset * _cosine)
            _y1 = _p2y - (_offset * _sine)
            _x2 = _vx + ((_ddp - _ext) * _cosine)
            _y2 = _vy + ((_ddp - _ext) * _sine)
        _bar2.setFirstEndpoint(_x1, _y1)
        _bar2.setSecondEndpoint(_x2, _y2)
        #
        # test if the DimString lies outside the measured angle
        # and if it does adjust either the crossarc start or end angle
        #
        _deg = _rtd * math.atan2((_dy - _vy), (_dx - _vx))
        if _deg < 0.0:
            _deg = _deg + 360.0
        _csa = _crossarc.getStartAngle()
        _cea = _crossarc.getEndAngle()
        if ((_csa > _cea) and (_cea < _deg < _csa)):
            if abs(_csa - _deg) < abs(_deg - _cea): # closer to start
                _crossarc.setStartAngle(_deg)
            else:
                _crossarc.setEndAngle(_deg)
        elif ((_cea > _csa) and ((_csa > _deg) or (_cea < _deg))):
            if _deg > _cea:
                _a1 = _deg - _cea
                _a2 = 360.0 - _deg + _csa
            else:
                _a1 = 360.0 - _cea + _deg
                _a2 = _csa - _deg
            if abs(_a1) > abs(_a2): # closer to start
                _crossarc.setStartAngle(_deg)
            else:
                _crossarc.setEndAngle(_deg)
        else:
            pass
        if not _allpts:
            return
        #
        # calculate dimension endpoint marker coordinates
        #
        _type = self.getEndpointType()
        _crossarc.clearMarkerPoints()
        if _type == Dimension.DIM_ENDPT_NONE or _type == Dimension.DIM_ENDPT_CIRCLE:
            return
        _size = self.getEndpointSize()
        _a1 = _bar1.getAngle() - 90.0
        _a2 = _bar2.getAngle() - 90.0
        # print "a1: %g" % _a1
        # print "a2: %g" % _a2
        _mp1, _mp2 = _crossarc.getCrossbarPoints()
        _x1, _y1 = _mp1
        _x2, _y2 = _mp2
        # print "x1: %g" % _x1
        # print "y1: %g" % _y1
        # print "x2: %g" % _x2
        # print "y2: %g" % _y2
        _sin1 = math.sin(_dtr * _a1)
        _cos1 = math.cos(_dtr * _a1)
        _sin2 = math.sin(_dtr * _a2)
        _cos2 = math.cos(_dtr * _a2)
        if _type == Dimension.DIM_ENDPT_ARROW or _type == Dimension.DIM_ENDPT_FILLED_ARROW:
            _height = _size/5.0
            # p1 -> (x,y) = (size, _height)
            _mx = (_cos1 * (-_size) - _sin1 * _height) + _x1
            _my = (_sin1 * (-_size) + _cos1 * _height) + _y1
            _crossarc.storeMarkerPoint(_mx, _my)
            # p2 -> (x,y) = (size, -_height)
            _mx = (_cos1 * (-_size) - _sin1 *(-_height)) + _x1
            _my = (_sin1 * (-_size) + _cos1 *(-_height)) + _y1
            _crossarc.storeMarkerPoint(_mx, _my)
            # p3 -> (x,y) = (size, _height)
            _mx = (_cos2 * _size - _sin2 * _height) + _x2
            _my = (_sin2 * _size + _cos2 * _height) + _y2
            _crossarc.storeMarkerPoint(_mx, _my)
            # p4 -> (x,y) = (size, -_height)
            _mx = (_cos2 * _size - _sin2 *(-_height)) + _x2
            _my = (_sin2 * _size + _cos2 *(-_height)) + _y2
            _crossarc.storeMarkerPoint(_mx, _my)
        elif _type == Dimension.DIM_ENDPT_SLASH:
            _angle = 30.0 * _dtr # slope of slash
            _height = 0.5 * _size * math.sin(_angle)
            _length = 0.5 * _size * math.cos(_angle)
            # p1 -> (x,y) = (-_length, -_height)
            _mx = (_cos1 * (-_length) - _sin1 * (-_height)) + _x1
            _my = (_sin1 * (-_length) + _cos1 * (-_height)) + _y1
            _crossarc.storeMarkerPoint(_mx, _my)
            # p2 -> (x,y) = (_length, _height)
            _mx = (_cos1 * _length - _sin1 * _height) + _x1
            _my = (_sin1 * _length + _cos1 * _height) + _y1
            _crossarc.storeMarkerPoint(_mx, _my)
            # p3 -> (x,y) = (-_length, -_height)
            _mx = (_cos2 * (-_length) - _sin2 * (-_height)) + _x2
            _my = (_sin2 * (-_length) + _cos2 * (-_height)) + _y2
            _crossarc.storeMarkerPoint(_mx, _my)
            # p4 -> (x,y) = (_length, _height)
            _mx = (_cos2 * _length - _sin2 * _height) + _x2
            _my = (_sin2 * _length + _cos2 * _height) + _y2
            _crossarc.storeMarkerPoint(_mx, _my)
        else:
            raise ValueError, "Unexpected endpoint type: '%s'" % str(_type)

    def mapCoords(self, x, y, tol=tolerance.TOL):
        """Test an x/y coordinate pair hit the dimension lines and arc.

mapCoords(x, y[, tol])

This method has two required parameters:

x: The x-coordinate
y: The y-coordinate

These should both be float values.

There is an optional third parameter, 'tol', giving
the maximum distance from the dimension bars that the
x/y coordinates may sit.
        """
        _x = util.get_float(x)
        _y = util.get_float(y)
        _t = tolerance.toltest(tol)
        #
        # test vp-p1 bar
        #
        _ep1, _ep2 = self.__bar1.getEndpoints()
        _ex1, _ey1 = _ep1
        _ex2, _ey2 = _ep2
        _mp = util.map_coords(_x, _y, _ex1, _ey1, _ex2, _ey2, _t)
        if _mp is not None:
            return _mp
        #
        # test vp-p2 bar
        #
        _ep1, _ep2 = self.__bar2.getEndpoints()
        _mp = util.map_coords(_x, _y, _ex1, _ey1, _ex2, _ey2, _t)
        if _mp is not None:
            return _mp
        #
        # test the arc
        #
        _vx, _vy = self.__vp.getCoords()
        _psep = math.hypot((_vx - _x), (_vy - y))
        _dx, _dy = self.getLocation()
        _dsep = math.hypot((_vx - _dx), (_vy - _dy))
        if abs(_psep - _dsep) < _t:
            _crossarc = self.__crossarc
            _sa = _crossarc.getStartAngle()
            _ea = _crossarc.getEndAngle()
            _angle = _rtd * math.atan2((_y - _vy), (_x - _vx))
            _val = True
            if abs(_sa - _ea) > 1e-10:
                if _sa < _ea:
                    if _angle < _sa or  _angle > _ea:
                        _val = False
                else:
                    if _angle > _ea or _angle < _sa:
                        _val = False
            if _val:
                _xoff = _dsep * math.cos(_angle)
                _yoff = _dsep * math.sin(_angle)
                return (_vx + _xoff), (_vy + _yoff)
        return None

    def onDimension(self, x, y, tol=tolerance.TOL):
        return self.mapCoords(x, y, tol) is not None

    def getBounds(self):
        """Return the minimal and maximal locations of the dimension

getBounds()

This method overrides the Dimension::getBounds() method
        """
        _vx, _vy = self.__vp.getCoords()
        _dx, _dy = self.getLocation()
        _dxpts = []
        _dypts = []
        _ep1, _ep2 = self.__bar1.getEndpoints()
        _dxpts.append(_ep1[0])
        _dypts.append(_ep1[1])
        _dxpts.append(_ep2[0])
        _dypts.append(_ep2[1])
        _ep1, _ep2 = self.__bar2.getEndpoints()
        _dxpts.append(_ep1[0])
        _dypts.append(_ep1[1])
        _dxpts.append(_ep2[0])
        _dypts.append(_ep2[1])
        _rad = self.__crossarc.getRadius()
        if self._throughAngle(0.0):
            _dxpts.append((_vx + _rad))
        if self._throughAngle(90.0):
            _dypts.append((_vy + _rad))
        if self._throughAngle(180.0):
            _dxpts.append((_vx - _rad))
        if self._throughAngle(270.0):
            _dypts.append((_vy - _rad))
        _xmin = min(_dx, min(_dxpts))
        _ymin = min(_dy, min(_dypts))
        _xmax = max(_dx, max(_dxpts))
        _ymax = max(_dy, max(_dypts))
        return _xmin, _ymin, _xmax, _ymax

    def clone(self):
        _vp = self.__vp
        _p1 = self.__p1
        _p2 = self.__p2
        _x, _y = self.getLocation()
        _ds = self.getDimStyle()
        _adim = AngularDimension(_vp, _p1, _p2, _x, _y, _ds)
        _adim.copyDimValues(self)
        return _adim

    def __movePoint(self, p, *args):
        _alen = len(args)
        if _alen < 2:
            raise ValueError, "Invalid argument count: %d" % _alen
        if ((p is not self.__vp) and
            (p is not self.__p1) and
            (p is not self.__p2)):
            raise ValueError, "Unexpected dimension point: " + `p`
        _dxmin, _dymin, _dxmax, _dymax = self.getBounds()
        self.calcDimValues()
        self.sendMessage('moved', _dxmin, _dymin, _dxmax, _dymax)

    def __pointChangePending(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        if args[0] == 'moved':
            self.startChange('moved')

    def __pointChangeComplete(self, p, *args):
        _alen = len(args)
        if _alen < 1:
            raise ValueError, "Invalid argument count: %d" % _alen
        if args[0] == 'moved':
            self.endChange('moved')

    def sendsMessage(self, m):
        if m in AngularDimension.__messages:
            return True
        return super(AngularDimension, self).sendsMessage(m)

