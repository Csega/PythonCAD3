#
# Copyright (c) 2009 Matteo Boscolo
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the termscl_bo of the GNU General Public License as published by
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
#
# This code is written by Yagnesh Desai
#

dxfDebug = False


import math  # added to handle arc start and end point defination
import re  # added to handle Mtext

from initsetting import cgcol

from GeoEntity.point import Point
from GeoEntity.segment import Segment
from GeoEntity.arc import Arc
from GeoEntity.text import Text
from GeoEntity.ellipse import Ellipse

def ChangeColor(x):
    try:
        newcolor = cgcol[x]
    except:
        newcolor = 256
    return newcolor

def changeColorFromDxf(col):
    if col == '256':
        newcol = layerColor[col]  # Work in progress layerColor captured under readLayer needs to be used
    else:
        newcol = ChangeColor(col)
    return newcol
    
class DrawingFile(object):
    """
        This Class provide base capability to read write a  file
    """
    def __init__(self, fileName):
        """
            Base Constructor
        """
        dPrint("Debug: DrawingFile constructor")
        self.__fn = fileName
        self.__fb = None
        self.__errors = []
        self.__reading = False
        self.__writing = False
        self.__lineNumber = 0

    def readAsci(self):
        """
            Read a generic file
        """
        dPrint("Debug: Read asci File")
        self.__fb = open(self.__fn, 'r')
        self.__reading = True
        self.__writing = False

    def createAsci(self):
        """
            create the new file
        """
        self.__fb = open(self.__fn, 'w')
        self.__reading = False
        self.__writing = True

    def fileObject(self):
        """
            Return the file opened
        """
        dPrint("Debug: GetFileObject")
        if self.__fb is not None:
          dPrint("Debug: Return file object")
          return self.__fb
        else:
          dPrint("Debug: None")
          return None

    def readLine(self):
        """
            read a line and return it
        """
        if self.__reading:
            self.__lineNumber = self.__lineNumber + 1
            return self.__fb.readline()
        else:
            raise("Unable to perfor reading operation")

    def writeLine(self, line):
        """
            write a line to the file
        """
        if self.__writing:
            self.__fb.write(line)
        else:
            raise("Unable to perfor writing operation")

    def writeError(self, functionName, msg):
        """
            Add an Error to the Collection
        """
        _msg = u'Error on line %s function Name: %s Message %s \n' % (str(self.__lineNumber), functionName,msg)
        self.__errors.append(_msg)

    def getError(self):
        """
        get the import export error
        """
        if len(self.__errors) > 0:
            return self.__errors
        else:
            return None

    def close(self):
        """
        close the active fileObject
        """
        if not self.__fb is None:
            self.__fb.close()
    
    def getFileName(self):
        """
            Return The active file Name
        """
        return self.__fn


class Dxf(DrawingFile):
    """
        this class provide dxf reading/writing capability
    """
    def __init__(self, kernel, fileName):
        """
            Default Constructor
        """
        dPrint( "Debug: Dxf constructor")
        DrawingFile.__init__(self, fileName)
        self.__kernel = kernel
        self.__dxfLayer = None

    def exportEntitis(self):
        """
            export The current file in dxf format
        """
        #TODO : Implements this part with the new kernel
        pass
        _fo = self.createAsci()  # open the file for writing
        _layersEnts = self.getAllEntitis()  # get all the entities from the file
        self.writeLine("999\nExported from Pythoncad\nSECTION\n  2\nENTITIES\n")  # header section for entities
        for _key in _layersEnts:  #Looping at all layer
            # create header section#
            for _obj in _layersEnts[_key]:  # looping at all entities in the layer
                if isinstance(_obj, Segment):  # if it's segment
                    self.writeSegment(_obj)  # ad it at the dxf drawing
                if isinstance(_obj, Circle):
                    self.writeCircle(_obj)
                if isinstance(_obj, Arc):
                    self.writeArc(_obj)
                if isinstance(_obj, Polyline):
                    self.writePolyline(_obj)
                if isinstance(_obj, TextBlock):
                    self.writeText(_obj)
                # go on end implements the other case arc circle ...
        self.writeLine("  0\nENDSEC\n  0\nEOF")  # writing End Of File
        self.close()

    def getAllEntitis(self):
        """
            retrive all the entitys from the drawing
        """
        # TODO : implement this part with the new kernel
        _outLayers = {}
        _layers = [self.__image.getActiveLayer()]
        while len(_layers):
            _layerEnts = []
            _layer = _layers.pop()
            _layerName = _layer.getName()
            _objs = _layer.getAllEntitys()
            for _o in _objs:
                _layerEnts.append(_o)
            _outLayers[_layerName] = _layerEnts
        return _outLayers

    def writeSegment(self, e):
        """
           write segment to the dxf file
        """
        x1,y1 = e.getP1().getCoords()
        x2,y2 = e.getP2().getCoords()
        _c = e.getColor()
        _c = str(_c)
        _c = ChangeColor(_c)
        dPrint("debug line color are %s" % str( _c)) # TODO : replace the dprint with the logging
        self.writeLine("  0\nLINE\n100\nAcdbLine\n")
        self.writeLine(" 62\n" + str(_c) + "\n")
        self.writeLine(" 10\n" + str(x1) + "\n")
        self.writeLine(" 20\n" + str(y1) + "\n 30\n0.0\n")
        self.writeLine(" 11\n" + str(x2) + "\n")
        self.writeLine(" 21\n" + str(y2) + "\n 31\n0.0\n")

    def writeCircle(self, e):
        """
           Write Circle to the dxf file
        """
        x1, y1 = e.getCenter().getCoords()
        r = e.getRadius()
        _c = e.getColor()
        _c = str(_c)
        _c = ChangeColor(_c)
        dPrint(" circle color are %s" % str(_c)) # TODO : replace the dprint with the logging
        self.writeLine("  0\nCIRCLE\n100\nAcDbCircle\n")
        self.writeLine(" 62\n" + str(_c) + "\n")
        self.writeLine(" 10\n" + str(x1) + "\n")
        self.writeLine(" 20\n" + str(y1) + "\n 30\n0.0\n")
        self.writeLine(" 40\n" + str(r) + "\n")
    
    def writeArc(self, e):
        """
           Write Arc to the dxf file
        """
        x1,y1 = e.getCenter().getCoords()
        r = e.getRadius()
        sa = e.getStartAngle()
        ea = e.getEndAngle()
        _c = e.getColor()
        _c = str(_c)
        _c = ChangeColor(_c)
        dprint("debug Arc color are %s " % str( _c))
        self.writeLine("  0\nARC\n100\nAcDbCircle\n")
        self.writeLine(" 62\n" + str(_c) + "\n")
        self.writeLine(" 10\n" + str(x1) + "\n")
        self.writeLine(" 20\n" + str(y1) + "\n 30\n0.0\n")
        self.writeLine(" 40\n" + str(r) + "\n")
        self.writeLine(" 50\n" + str(sa) + "\n 51\n"+str(ea)+"\n")
    
    def writePolyline(self, e):
        """
           Write Polyline to the dxf file
        """
        _c = e.getColor()
        _c = str(_c)
        _c = ChangeColor(_c)
        dprint( "debug Arc color are %s" % str(_c))
        self.writeLine("  0\nLWPOLYLINE\n100\nAcDbPolyline\n")
        self.writeLine(" 62\n" + str(_c) + "\n")
        count = e.getNumPoints()
        self.writeLine(" 90\n" + str(count) + "\n")
        self.writeLine(" 70\n0\n")
        self.writeLine(" 43\n0\n")
        c = 0
        points = []
        while c < count:
            x1,y1 = e.getPoint(c).getCoords()
            self.writeLine(" 10\n" + str(x1) + "\n")
            self.writeLine(" 20\n" + str(y1) + "\n")
            c = c + 1
    
    def writeText(self, e):
        """
           Write Text to the dxf file
        """
        x1,y1 = e.getLocation()
        h = e.getSize()
        _c = e.getColor()
        _c = str(_c)
        _c = ChangeColor(_c)
        dprint("debug Text color are %s " % str( _c))
        txt = e.getText()
        txt = txt.replace(' ', '\~')
        txt = txt.replace('\n', '\P')
        self.writeLine("  0\nMTEXT\n100\nAcDbMText\n")
        self.writeLine(" 62\n" + str(_c) + "\n")
        self.writeLine(" 10\n" + str(x1) + "\n")
        self.writeLine(" 20\n" + str(y1) + "\n 30\n0.0\n")
        self.writeLine(" 40\n" + str(h) + "\n")
        self.writeLine("  1\n" + str(txt) + "\n")

    def importEntitis(self):
        """
            Open The file and create The entity in pythonCad
        """
        dPrint("Debug: import entitys") 
        self.readAsci();
        #_layerName,_ext=os.path.splitext(os.path.basename(self.getFileName()))
        #_layerName="Imported_"+_layerName
        #_dxfLayer=Layer(_layerName)
        #self.__image.addLayer(_dxfLayer) # TODO : when we have the layer
        #self.__dxfLayer=_dxfLayer
        try:
            self.__kernel.startMassiveCreation()
            while True:
                _k = self.readLine()
                if not _k: break
                else:
                    ##print  "debug: readline", _k # TODO : replace the dprint with the logging
                    #dPrint( "Debug: Read Line line = [%s]"%str(_k)) # TODO : replace the dprint with the logging
                    if _k[0:5] == 'TABLE':
                        _k = self.readLine() # for tag "  2"
                        _k = self.readLine() # for table name
                        ##print "debug TABLE found" # TODO : replace the dprint with the logging
                        if _k[0:5] == 'LAYER':
                            self.readLayer()
                            #print "debug LAYER found" # TODO : replace the dprint with the logging
                        continue
                    if _k[0:4] == 'LINE':
                        self.createLineFromDxf()
                        ##print "debug line found" # TODO : replace the dprint with the logging
                        continue
                    if _k[0:6] == 'CIRCLE':
                        self.createCircleFromDxf()
                        continue
                    if _k[0:5] == 'MTEXT':
                        self.createTextFromDxf()
                        continue
                    if _k[0:4] == 'TEXT':
                        #self.createTextFromDxf()
                        continue
                    if _k[0:3] == 'ARC':
                        self.createArcFromDxf()
                        ##print "debug arc found"
                        continue
                    if _k[0:10] == 'LWPOLYLINE':
                        #self.createPolylineFromDxf()
                        continue
                    if _k[0:8] == 'POLYLINE':
                        #self.createPolylineFromDxf()
                        continue
                    if not _k : break
            self.__kernel.performCommit()
        finally:
            self.__kernel.stopMassiveCreation()
    
    def readLayer(self):
        """
        Reading the data in the dxf file under TABLE section
        it collects the information regarding the
        Layers, Colors and Linetype
        WORK IN PROGRESS
        """
        ##print 'debug Layer found !'
        layerColor = {}
        dxfColor = 0
        layerName = '0'
        #_k = self.readLine()
        while True:
            _k = self.readLine()
            if _k[0:6] == 'ENDTAB':
                break
            if _k[0:3] == '  2':
                _k = self.readLine()
                layerName = _k.replace('\n', '')
                #print "Debug New LayerName=", layerName
            if _k[0:3] == ' 62':
                _k = self.readLine()
                dxfColor = _k.replace('\n', '')
                #print "Debug new dxfColor = ", dxfColor
            layerColor[layerName] = dxfColor
        return layerColor

    def createLineFromDxf(self):
        """
            read the line dxf section and create the line
        """
        dPrint( "Debug createLineFromDxf" )# TODO : replace the dprint with the logging
        x1 = None
        y1 = None
        x2 = None
        y2 = None
        g = 0 # start counter to read lines
        c = 0
        while g < 18:
            ##print "Debug g =", g
            ##print "Debug: Read line  g = %s Value = %s "%(str(g),str(line))
            _k = self.readLine()
            ##print "Debug: Read line g = %s k =  %s "%(str(g),str(k))
            #dPrint( "line value k="+_k)
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                dPrint("debug 10" + _k)
                # this line of file contains start point"X" co ordinate
                ##print "Debug: Convert To flot x1: %s" % str(k[0:-1])
                _k = self.readLine()
                x1 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 20':# this line of file contains start point "Y" co ordinate
                ##print "Debug: Convert To flot y1: %s" % str(k[0:-1])
                _k = self.readLine()
                y1 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 30':# this line of file contains start point "Z" co ordinate
                ##print "Debug: Convert To flot z1: %s" % str(k[0:-1])
                _k = self.readLine()
                z1 = (float(_k[0:-1]))
                continue
                # Z co ordinates are not used in PythonCAD we can live without this line
            if _k[0:3] == ' 11':# this line of file contains End point "X" co ordinate
                ##print "Debug: Convert To flot x2: %s" % str(k[0:-1])
                _k = self.readLine()
                x2 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 21':# this line of file contains End point "Y" co ordinate
                ##print "Debug: Convert To flot y2: %s" % str(k[0:-1])
                _k = self.readLine()
                y2 = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 31':# this line of file contains End point "Z" co ordinate
                ##print "Debug: Convert To flot z2: %s" % str(k[0:-1])
                _k = self.readLine()
                z2 = (float(_k[0:-1]))
                g = 119
                continue
                #Z co ordinates are not used in PythonCAD we can live without this line
        if c == None:
            c = 7
        if not ( x1 == None or y1 == None or
           x2 == None or y2 == None ):
            self.createLine(x1, y1, x2, y2, c)
        else:
            _msg = u'Read parameter from file x1: [%s] y1: [%s] x2: [%s] y2: [%s]' % (str(x1), str(y1), str(x2), str(y2))
            self.writeError('createLineFromDxf', _msg)

    def createLine(self, x1, y1, x2, y2, c):
        """
          Create the line into the current drawing
          In this implementation all the lines gose to the active layer and use the global settings of pythoncad
          Feauture implementation could be :
          1) Create a new layer(ex: Dxf Import)
          2) Read dxf import style propertis and set it to the line
        """
        ##print "debug c=", c
        #dPrint( "Debug Creatre line %s,%s,%s,%s"%(str(x1),str(y1),str(x2),str(y2)) ) # TODO : replace the dprint with the logging
        #_active_layer = self.__dxfLayer
        #_p1 = Point(x1, y1)
        #_active_layer.addObject(_p1)
        #_p2 = Point(x2, y2)
        #_active_layer.addObject(_p2)
        #_s = self.__image.getOption('LINE_STYLE')
        #_seg = Segment(_p1, _p2, _s)
        args = {"SEGMENT_0": Point(x1, y1), "SEGMENT_1": Point(x2, y2)}
        _seg = Segment(args)
        #_l = self.__image.getOption('LINE_TYPE')
        #if _l != _s.getLinetype():
        #  _seg.setLinetype(_l)
        #_c = changeColorFromDxf(int(c))
        #_c = self.__image.getOption('LINE_COLOR')
        #if _c != _s.getColor():
        #  _seg.setColor(_c)
        ##print _c
        #_t = self.__image.getOption('LINE_THICKNESS')
        #if abs(_t - _s.getThickness()) > 1e-10:
        #  _seg.setThickness(_t)
        #_active_layer.addObject(_seg)
        self.__kernel.saveEntity(_seg)

    def createCircleFromDxf(self):
        """
            Read and create the Circle into drawing
        """
        dPrint( "Debug createCircleFromDxf" )
        g = 0 # reset g
        c = 0
        while g < 1:
            _k = self.readLine()
            dPrint( "line value k="+ _k)
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                _k = self.readLine()
                x = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 20':
                _k = self.readLine()
                y = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 40':
                _k = self.readLine()
                r = (float(_k[0:-1]))
                g = 10  # g > 1 for break
                'I need a "create Circle code" here to append the segment to image'
        if c == None:
            c = 7
        self.createArc(x, y, r, c)


    def createTextFromDxf(self):
        """
            Read and create the Text into drawing
        """
        dPrint( "Debug createTextFromDxf" )
        g = 0 # reset g
        x = None
        y = None
        h = None
        _t= ''
        while g < 1:
            _k = self.readLine()
            dPrint("line value k=" + _k)
            #if _k[0:3] == ' 62':# COLOR
            #    _k = self.readLine()
            #    c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                _k = self.readLine()
                x = (float(_k[0:-1]))
                ##print "Text Loc x =", x
                continue
            if _k[0:3] == ' 20':
                _k = self.readLine()
                y = (float(_k[0:-1]))
                #rint "Text Loc y =", y
                continue
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z = (float(_k[0:-1]))
                ##print "Text Loc z =", z
                continue
            if _k[0:3] == ' 40':
                _k = self.readLine()
                h = (float(_k[0:-1]))
                dPrint("Text Height =%s"%str(h))
                continue
            if _k[0:3] == '  1':
                _k = self.readLine()
                _t = _k.replace('\~', ' ')
                _t = _t.replace('\P', '\n')
                ##print "Text itself is ", x, y, z, 'height', h, _t#
                g = 10 # g > 1 for break
                continue
        if not (x is None or y is None or h is None):
            self.createText(x,y,h,_t)
        else:
            _msg = "Read parameter from file x: [%s] y: [%s] h: [%s] t: [%s]" % (str(x), str(y), str(h), str(_t))
            self.writeError("createTextFromDxf",_msg)

    def createArcFromDxf(self):
        """
            Read and create the ARC into drawing
        """
        g = 0 # reset g
        c = 0
        while g < 1:
            _k = self.readLine()
            if _k[0:3] == ' 62':# COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                _k = self.readLine()
                x = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 20':
                _k = self.readLine()
                y = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z = (float(_k[0:-1]))
            if _k[0:3] == ' 40':
                _k = self.readLine()
                r = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 50':
                _k = self.readLine()
                sa = (float(_k[0:-1]))
                continue
            if _k[0:3] == ' 51':
                _k = self.readLine()
                ea = (float(_k[0:-1]))
                g = 10 # g > 1 for break\\
                continue
        if c == None:
                c = 7
        self.createArc(x, y, r, c, sa, ea)

    def createArc(self, x, y, r, color = None, sa = None, ea = None):
        """
            Create a Arc entitys into the current drawing
        """
        #_active_layer = self.__dxfLayer
        _center = Point(x, y)
        #_active_layer.addObject(_center)
        #_s = self.__image.getOption('LINE_STYLE')
        if sa is None or ea is None:
            sa = ea = 0  # This is the case of circle
        else:
            sa = (sa * math.pi) / 180.
            ea = (ea * math.pi) / 180.
            ea = ea - sa
        #ex = x + r*math.cos(sa)
        #ey = y + r*math.sin(sa)
        #lpx = x + r*math.cos(ea)
        #lpy = y + r*math.sin(ea)
        #ep = Point(ex, ey)
        #lp = Point(lpx, lpy)
        #_active_layer.addObject(ep)
        #_active_layer.addObject(lp)
        args = {"ARC_0": _center, "ARC_1": r, "ARC_2": sa, "ARC_3": ea}
        _arc = Arc(args)
        #_l = self.__image.getOption('LINE_TYPE')
        #if _l != _s.getLinetype():
        #    _arc.setLinetype(_l)
        #_c = changeColorFromDxf(color)
        #_c = self.__image.getOption('LINE_COLOR')
        #if _c != _s.getColor():
        #    _arc.setColor(_c)
        #_t = self.__image.getOption('LINE_THICKNESS')
        #if abs(_t - _s.getThickness()) > 1e-10:
        #    _arc.setThickness(_t)
        #_active_layer.addObject(_arc)
        self.__kernel.saveEntity(_arc)

    def createText(self, x, y, h, t):
        """
            Create a Text entitys into the current drawing
        """
        #_active_layer = self.__dxfLayer
        try:
            _text = t.replace('\x00', '').decode('utf8', 'ignore').encode('utf8')
        except:
            self.writeError("createText", "Debug Error Converting in unicode [%s]" % t)
            _text ='Unable to convert in unicode'
        _p = Point(x, y)
        #_ts = self.__image.getOption('TEXT_STYLE')
        args = {"TEXT_0": _p, "TEXT_1": _text, "TEXT_2": 0.0, "TEXT_3": ""}
        _tb = Text(args)

        #_f = self.__image.getOption('FONT_FAMILY')
        #if _f != _ts.getFamily():
        #    _tb.setFamily(_f)

        #_s = self.__image.getOption('FONT_STYLE')
        #if _s != _ts.getStyle():
        #    _tb.setStyle(_s)

        #_w = self.__image.getOption('FONT_WEIGHT')
        #if _w != _ts.getWeight():
        #    _tb.setWeight(_w)
        #_c = changeColorFromDxf(c)
        #_c = self.__image.getOption('FONT_COLOR')
        #if _c != _ts.getColor():
        #    _tb.setColor(_c)
        #_sz = h
        #if abs(_sz - _ts.getSize()) > 1e-10:
        #    _tb.setSize(_sz)
        #_a = self.__image.getOption('TEXT_ANGLE')
        #if abs(_a - _ts.getAngle()) > 1e-10:
        #_tb.setAngle(_a)
        #_al = self.__image.getOption('TEXT_ALIGNMENT')
        #if _al != _ts.getAlignment():
        #    _tb.setAlignment(_al)
        #_active_layer.addObject(_tb)
        self.__kernel.saveEntity(_tb)

    def createPolylineFromDxf(self):
        """
        Polyline creation read the line dxf section and create the line
        """
        dPrint("Exec createPolylineFromDxf")
        c = 0
        while True:
            _k = self.readLine()
            if _k[0:3] == ' 62':  # COLOR
                _k = self.readLine()
                c = (int(_k[0:-1]))
            if _k[0:3] == ' 10':
                break
        points = []
        p = ()
        t = 0
        while True:
            # this line of file contains start point"X" co ordinate
            # #print "Debug: Convert To flot x1: %s" % str(k[0:-1])
            _k = self.readLine()
            x = (float(_k[0:-1]))
            _k = self.readLine()#pass for k[0:3] == ' 20'
            _k = self.readLine()
            y = (float(_k[0:-1]))
            p = (x, y)
            points.append(p)
            dPrint(str(points))
            _k = self.readLine()
            if _k[0:3] == ' 30':
                _k = self.readLine()
                z1 = (float(_k[0:-1]))
                _k = self.readLine()
                continue
            if _k[0:3] != ' 10':
                break
            continue
        if c == None:
                c = 7
        if len(points) > 1:
            self.createPolyline(points, c)

    def createPolyline(self, points, c):
        """
            Crate poliline into Pythoncad
        """
        dPrint("Exec createPolyline")
        _active_layer = self.__dxfLayer
        _x = 0.0
        _y = 0.0
        _pts = []
        for _x, _y in points:
            dPrint(_x)
            dPrint(_y)
            _p = Point(_x, _y)
            _active_layer.addObject(_p)
            _pts.append(_p)
        dPrint("Exec createPolyline lenPts(%s)" % str(len(_pts)))
        _s = self.__image.getOption('LINE_STYLE')
        _pline = Polyline(_pts, _s)
        _l = self.__image.getOption('LINE_TYPE')
        if _l != _s.getLinetype():
          _pline.setLinetype(_l)
        _c = changeColorFromDxf(c)
        #_c = self.__image.getOption('LINE_COLOR')
        if _c != _s.getColor():
          _pline.setColor(_c)
        _t = self.__image.getOption('LINE_THICKNESS')
        if abs(_t - _s.getThickness()) > 1e-10:
          _pline.setThickness(_t)
        _active_layer.addObject(_pline)

def dPrint(msg):
    """
        Debug function for the dxf file
    """
    if dxfDebug :
        print("Debug: %s " % str(msg))
