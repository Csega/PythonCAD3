#!/usr/bin/env python

import sys
import os
import platform

import sqlite3 as sqlite

    
# This is needed for me to use unpickle objects
sys.path.append(os.path.join(os.getcwd(), 'Generic', 'Kernel'))    
    
from random import random
from Generic.Kernel.document import *
from Generic.application import Application
from Generic.Kernel.GeoEntity.point import Point
from Generic.Kernel.GeoEntity.style import Style
from Generic.Kernel.GeoComposedEntity.chamfer import Chamfer

def printId(kernel, obj):
    """
        print the id of the obj
    """
    print("Save Entity: %s" % str(type(obj)))
    
def testSinglePoint(kernel):
    """
        test single point operation
    """
    startTime = time.clock()
    print("Create a single point")
    basePoint = Point(10, 1)
    print("singlePoint ", type(basePoint))
    kernel.saveEntity(basePoint)
    endTime = time.clock() - startTime
    print("Time for saving  a single point   %ss" % str(endTime))
    
def testMultiPoints(kernel, nPoint):
    """
        test the point operatoin
    """
    startTime = time.clock()
    kernel.startMassiveCreation()
    for i in range(nPoint):
        basePoint = Point(10, i)
        kernel.saveEntity(basePoint)
    kernel.performCommit()
    endTime = time.clock() - startTime
    print("Create n: %s entity in : %ss" % (str(nPoint ), str(endTime)))

def testMultiSegments(kernel, nSegments):
    """
        create a single segment
    """    
    startTime = time.clock()
    kernel.startMassiveCreation()
    for i in range(nSegments):
        _p1 = Point(10, i)
        _p2 = Point(10, i)
        _s = Segment(_p1, _p2)
        kernel.saveEntity(_s)
    kernel.performCommit()
    endTime = time.clock() - startTime
    print("Create n: %s entity in : %ss" % (str(nSegments ), str(endTime)))
    
def testSingleSegment(kernel):
    """
        create a single segment
    """    
    _p1 = Point(10, 10)
    _p2 = Point(10, 20)
    _s = Segment(_p1, _p2)
    kernel.saveEntity(_s)

def testGetLayerEnt(kernel):
    """
        get layer dictionary of all the id child
    """
    startTime = time.clock()
    ids = kernel.getLayerChild('ROOT')
    nids = len(ids)
    endTime = time.clock()-startTime
    print("Get n: %s layer entity in : %ss" % (str(nids ), str(endTime)))

def testPerformanceInCreation(kr):
    print("Points:")
    testMultiPoints(kr, 1)
    #testMultiPoints(kr,10)
    #testMultiPoints(kr,100)
    #testMultiPoints(kr,1000)
    #testMultiPoints(kr,10000)
    #testMultiPoints(kr,100000)
    print("Segments:")
    testMultiSegments(kr, 1)
    #testMultiSegments(kr,10)
    #testMultiSegments(kr,100)
    #testMultiSegments(kr,1000)
    #testMultiSegments(kr,10000)
    #testMultiSegments(kr,100000)
    testGetLayerEnt(kr)

def createSegment(kernel):
    """
        create a single segment
    """    
    _p1 = Point(10, 10)
    _p2 = Point(10, 20)
    _s = Segment(_p1, _p2)
    return kernel.saveEntity(_s)

def CreateModifieEntity(kr):
    """
        test for create and modifie an entity
    """
    ent = createSegment(kr)
    celement = {'POINT_1': Point(100, 100), 'POINT_2': Point(200, 200)}
    ent.setConstructionElement(celement)
    kr.saveEntity(ent)
 
def deleteTable(tableName):
    """
    delete the table name 
    """
    #import sqlite3 as sql
    # sqlite + R*Tree module
    from pysqlite2 import dbapi2 as sql

    dbPath = 'pythoncad.pdr'
    dbConnection = sql.connect(dbPath)
    statment ="drop table pycadrel"
    _cursor = dbConnection.cursor()
    _rows = _cursor.execute(statment)
    dbConnection.commit()
    dbConnection.close()

def testPointDb(nLoop):
    """
    Test point creation 
    """
    # import sqlite3 as sql
    # sqlite + R*Tree module
    from pysqlite2 import dbapi2 as sql
    import cPickle as pickle
    
    dbConnection = sql.connect(":memory:")
    cursor = dbConnection.cursor()
    _sqlCreation = """CREATE TABLE pycadent(
                    pycad_id INTEGER PRIMARY KEY,
                    pycad_entity_id INTEGER,
                    pycad_object_type TEXT,
                    pycad_object_definition TEXT,
                    pycad_style_id INTEGER,
                    pycad_security_id INTEGER,
                    pycad_undo_id INTEGER,
                    pycad_entity_state TEXT,
                    pycad_date NUMERIC,
                    pycad_visible INTEGER,
                    pycad_undo_visible INTEGER,
                    pycad_locked INTEGER,
                    pycad_bbox_xmin REAL,
                    pycad_bbox_ymin REAL,
                    pycad_bbox_xmax REAL,
                    pycad_bbox_ymax REAL)"""
    cursor.execute(_sqlCreation)
    dic = [(x, y) for x in range(20) for y in range(1)]
    dbConnection.commit()
    startTime = time.clock()
    for i in range(nLoop):
        dumpDic = pickle.dumps(dic)
        sql = """insert into pycadent (pycad_entity_id,pycad_object_definition) values(1,"%s")""" % str(dumpDic)
        cursor.execute(sql)
    dbConnection.commit()
    endTime = time.clock() - startTime
    everage = endTime / nLoop
    print("End time for nLoop %s in %s everage %s " % (str(nLoop), str(endTime), str(everage)))

def testPointDb1(nLoop):
    """
    Test point creation 
    """
    # import sqlite3 as sql
    # sqlite + R*Tree module
    from pysqlite2 import dbapi2 as sql
    import pickle
    
    dbConnection = sql.connect(":memory:")
    cursor = dbConnection.cursor()
    _sqlCreation = """CREATE TABLE pycadent(
                    pycad_X REAL,
                    pycad_Y REAL)"""
    cursor.execute(_sqlCreation)
    dbConnection.commit()    
    dic = [(x,y) for x in range(20) for y in range(1)]
    startTime = time.clock()
    for i in range(nLoop):
        for x,y in dic:
            _sql = """INSERT INTO pycadent (pycad_X,pycad_Y) 
                VALUES (%s,%s)""" % (str(x),str(y))
            cursor.execute(_sql)
    dbConnection.commit()   
    endTime = time.clock() - startTime
    everage = endTime / nLoop
    print("End time for nLoop %s in %s everage %s " % (str(nLoop), str(endTime), str(everage)))

def TestcPickleSql():
    for i in [10,100, 1000, 1000, 10000, 100000]:
        print(">>print Test with %s entitys" % str(i))
        testPointDb(i)
        testPointDb1(i)

def getAllSegment(kr):
    """
        get all the segments
    """
    print(">>Looking for segment")
    ent = kr.getEntityFromType('SEGMENT')
    for e in ent:
        print("e >>>>", e.eType)
       
def test():
    print(">>Create pycad object")
    kr = PyCadDbKernel()
    #CreateModifieEntity(kr)
    #print "Add creation event"
    #kr.saveEntityEvent+=printId
    redo(kr)
    getAllSegment(kr)


class ioKernel(object):
    """
        This class provide a simple interface for using 
        PythonCad Kernel
    """
    def __init__(self):
        startTime = time.clock()
        self.__kr = PyCadDbKernel()
        endTime = time.clock() - startTime    
        print("Inizialize kernel object in : %s" % str(endTime))
        self.__command = {}
        # Basic Command
        self.__command['H'] = self.help
        self.__command['Esc'] = self.endApplication
        self.__command['Import'] = self.importExt
        self.__command['SetCurrentLayer'] = self.setCurrentLayer
        # Creatio Command
        self.__command['NewSegment'] = self.newSegment
        self.__command['NewArc'] = self.newArc
        self.__command['AddLayer'] = self.addLayer
        # Delete Command
        self.__command['Delete'] = self.delete
        self.__command['DeleteLayer'] = self.deleteLayer
        # Get Command
        self.__command['GetCurrentLayer'] = self.getCurrentLayerName
        self.__command['GetEntType'] = self.getEntType
        self.__command['GetLayers'] = self.getLayers
        self.__command['GetDrwEnt'] = self.getDrawingEntity
        # Edit Command
        self.__command['UnDo'] = self.unDo
        self.__command['ReDo'] = self.reDo
        # WorkFlow Command
        self.__command['Relese'] = self.release
        # View Command
        self.__command['Hide'] = self.hideEntity
        self.__command['UnHide'] = self.unHideEntity
        self.__kr.handledError = self.printError
        
    def printError(self, **args):
        """
            print the error/warning caming from the kernel
        """    
        # if args.has_key('error'):
        if 'error' in args:
            if args['error'] == 'DxfReport':
                print("dxfReport")  # todo : improve this system
            elif args['error'] == 'DxfUnsupportedFormat':
                print("DxfUnsupportedFormat")  # todo : improve this system
                
    def mainLoop(self):
        """
            mainLoop operation
        """
        while 1:
            input_str = input("Insert a command (H for Help)>> :")
            # if self.__command.has_key(imputstr):
            if input_str in self.__command.keys():
                self.__command[input_str]()
            else:
                print("Wrong Command !!")
    
    def help(self):
        """
            print the help
        """
        print("*" * 10)
        print("PyCadIOInterface Help")
        kmd = self.__command.keys()
        kmd.sort()
        for s in kmd:
            print("command :" , s)
        print("*"*10)
        
    def newSegment(self):
        """
            create a new segment
        """
        try:
            val = (input("-->Get First Point x,y :"))
            p1 = Point(val[0], val[1])
            val = (input("-->Get Second Point x,y :"))
            p2 = Point(val[0], val[1])
            _s = Segment(p1,p2)
            self.__kr.saveEntity(_s)
        except:
            print("---->Error on point creation !!")
            
    def getDrawingEntity(self):        
        """
            get all the drawing entity
        """
        print("--<< Looking for All entitys")
        startTime = time.clock()
        ents = self.__kr.getAllDrawingEntity()
        endTime = time.clock() - startTime       
        printEntity(ents)
        print("Exec query get %s ent in %s s" % (str(len(ents)), str(endTime)))
        print("********************************")

    def reDo(self):
        """
            perform the redo command
        """
        try:
            print("-->>Perform Redo")
            self.__kr.reDo()  
        except UndoDb:
            print("----<<Err>>No more redo to perform")

    def unDo(self):
        """
            perform the undo command
        """
        try:
            print("-->>Perform unDo")
            self.__kr.unDo()  
        except UndoDb:
            print("----<<Err>>No more unDo to perform")
    
    def delete(self):
        """
            Delete the entity
        """
        try:
            val = (input("-->Write entityId :"))
            self.__kr.deleteEntity(val)
        except:
            print("----<<Err>>Enable to delete the entity")

    def hideEntity(self):
        """
            hide an entity
        """
        entId = raw_input("-->Insert the id to hide :")
        try:
            self.__kr.hideEntity(entityId=entId)
        except:
            print("----<<Err>>On Hide the id : %s " % entId)

    def unHideEntity(self):
        """
            unhide an entity
        """
        entId = raw_input("-->Insert the id to Unhide :")
        try:
            self.__kr.unHideEntity(entityId=entId)
        except:
            print("----<<Err>>On unHide the id : %s " % entId)
        
    def endApplication(self):
        """
            close the application
        """
        sys.exit(0)
        
    def release(self):
        """
            release the current drawing
        """
        self.__kr.release()
    
    def getLayers(self):
        """
            get all layer
        """
        try:
            print(">>** Layer Tree ****")
            layersTree = self.__kr.getLayerTree().getLayerTree()
            printTree(layersTree, 1)
            print("<<** Layer Tree ****")
        except:
            print("----<<Err>>On getLayers ")
    
    def addLayer(self):
        """
            add a new layer
        """
        layerName = input("-->Insert LayerName :")
        try:
            activeLayer = self.__kr.getLayerTree().getActiveLater()
            newLayer = Layer(layerName)
            dbLayer = self.__kr.saveEntity(newLayer)
            self.__kr.getLayerTree().insert(dbLayer,activeLayer)
            
        except:
            print("----<<Err>>Unable to create the layer : %s " % layerName)
    
    def setCurrentLayer(self):
        """
            set the current layer
        """
        LayerName = input("-->Layer Id :")
        try:
            self.__kr.getLayerTree().setActiveLayer(LayerName)
        except:
            print("----<<Err>>Unable to create the layer : %s " % LayerName)
            
    def getCurrentLayerName(self):
        """
            get the current layer name
        """
        try:
            activeLayer = self.__kr.getLayerTree().getActiveLater()
            ce = self.__kr.getLayerTree()._getLayerConstructionElement(activeLayer)
            print("Layer Name", ce.name)
        except:
            print("----<<Err>>unable to get the current layer name ")

    def importExt(self):
        """
            import an external file into pythoncad
        """
        fileName = input("-->insert The file name to import :")
        try:
            self.__kr.importExternalFormat(fileName)
        except:
            print("----<<Err>> importExt the  : %s we get en error " % fileName)
            
    def deleteLayer(self):
        """
            Delete the layer
        """
        layerId = input("-->insert The id layer to delete :")
        try:
            self.__kr.getLayerTree().delete(layerId)
        except:
            print("----<<Err>> deleteLayer id : %s we get en error " % layerId)
    
    def newArc(self):
        """
            Create a new arc
        """ 
        radius = input("-->Insert the radius :")
        val = input("-->insert The center position x,y:")
        xy = val.split(',')
        if len(xy) == 2:
            center = Point(xy[0], xy[1])
        else:
            #print("Errore valore incorretto inserire un valore 10,20 in questo formato")
            print("Incorrectly entered value, please use the format 10,20")
            return
            
        start_angle = input("-->insert startAngle [Empty in case of circle]:")
        if start_angle:
            end_angle = input("-->insert The end Angle :")
        else:
            start_angle = end_angle = 0
        arc = Arc(center, float(radius), float(start_angle), float(end_angle))
        self.__kr.saveEntity(arc)
    
    def getEntType(self):
        """
            get all the entity from a specifie type
        """
        type = input("-->Witch Type ? :")
        if not type:
            type = "ALL"
        startTime = time.clock()
        ents = self.__kr.getEntityFromType(type)
        endTime = time.clock() - startTime       
        printEntity(ents)
        print("Exec query get %s ent in %s s" % (str(len(ents)), str(endTime)))
        print("********************************")
        
def printEntity(ents):
    """
        print a query result
    """
    i = 0
    for e in ents:
        print("----<< Entity Type %s id %s " % (str(e.eType), str(e.getId())))
        if i > 100:
            print("There are more then 100 entitys in the select so i stop printing")
            break
        i += 1

def printTree(cls, indent):
    """
        print the tree structure
    """  
    if cls:
        for l in cls:
            parent, childs = cls[l]
            print('.' * indent + 'Layer Id: %s Name : %s' % (str(l) , str(parent.name)))
            printTree(childs, indent + 1)

class textApplication(object):
    def __init__(self):
        self.__command = {}
        self.__applicationCommand = {}
        # Application Command
        self.__applicationCommand['Open'] = self.openFile
        self.__applicationCommand['Close'] = self.closeFile
        self.__applicationCommand['New'] = self.newDoc
        self.__applicationCommand['Documents'] = self.showDocuments
        self.__applicationCommand['CreateStyle'] = self.createStyle
        self.__applicationCommand['SetActive'] = self.setActiveDoc
        self.__applicationCommand['GetActive'] = self.getActiveDoc
        self.__applicationCommand['GetEnts'] = self.getEnts
        self.__applicationCommand['Esc'] = self.endApplication
        self.__applicationCommand['?'] = self.printHelp
        self.__applicationCommand['Test'] = self.featureTest
        self.__applicationCommand['ETest'] = self.easyTest
        # Document Commandf
        self.__pyCadApplication = Application()
        for command in self.__pyCadApplication.getCommandList():
            self.__command[command] = self.performCommand

    def mainLoop(self):
        """
            mainLoop operation
        """
        while 1:
            input_str = self.inputMsg("Insert a command (? for Help)")
            try:
                # if self.__command.has_key(imputstr):
                if input_str in self.__command:
                    self.__command[input_str](input_str)
                # elif self.__applicationCommand.has_key(imputstr):
                elif input_str in self.__applicationCommand:
                    self.__applicationCommand[input_str]()
                else:
                    self.outputMsg("Wrong Command !!")
            except EntityMissing as err:
                self.outputMsg("Application Error %s " % str(err))
                
    def printHelp(self):            
        """
            print the command list
        """
        self.outputMsg("*****************************Drawing")
        for commandName in self.__command:
            self.outputMsg("Comand : %s "%str(commandName))
        self.outputMsg("**************************Application Command")
        for commandName in self.__applicationCommand:
            self.outputMsg("Comand : %s "%str(commandName))
    
    def getEnts(self):
        """
            get database entitys
        """
        try:
            type = self.inputMsg("Witch Type ?")
            if not type:
                type = "ALL"
            startTime = time.clock()
            activeDoc = self.__pyCadApplication.getActiveDocument()
            if activeDoc == None:
                self.outputMsg("No Object opened")
                return
                
            ents = activeDoc.getEntityFromType(type)
            endTime = time.clock() - startTime       
            self.printEntity(ents)
            self.outputMsg("Exec query get %s ent in %s s" % (str(len(ents)), str(endTime)))
            self.outputMsg("********************************")
        except:
            self.outputMsg("Unable To Perform the getEnts")   

        
    def printEntity(self, ents):
        """
            print a query result
        """
        i = 0
        for e in ents:
            self.outputMsg("Entity Type %s id %s " % (str(e.eType), str(e.getId())))
            if i > 100:
                self.outputMsg("There are more then 100 entitys in the select so i stop printing")
                break
            i += 1

    def newDoc(self):
        """
            create a new document
        """
        try:
            self.__pyCadApplication.newDocument(None)
        except (IOError, EmptyFile):
            self.outputMsg("Unable To open the file %s" % str(filePath))
    
    def createStyle(self):        
        """
            create a new style object
        """
        styleName = self.inputMsg("Write style name")
        stl = Style(styleName)
        doc = self.__pyCadApplication.getActiveDocument()
        doc.saveEntity(stl);
        
    def getActiveDoc(self):            
        """
            print the active document
        """ 
        try:
            doc = self.__pyCadApplication.getActiveDocument()
            self.outputMsg("Active Document is %s" % str(doc.dbPath))
        except:
            self.outputMsg("Unable To Perform the getActiveDoc") 
   
    def setActiveDoc(self):
        """
            set the active docuement
        """
        try:
            lookIndex = self.inputMsg("Write the number of doc that you are looking for")
            i = 0
            docs = self.__pyCadApplication.getDocuments()
            if len(docs) < int(lookIndex):
                self.outputMsg("No such a document")
                return
            for key in docs:
                if i == int(lookIndex):
                    self.__pyCadApplication.setActiveDocument(docs[key])
                    return
                i += 1
            else:
                self.outputMsg("Document not found") 
        except:
            self.outputMsg("Unable To Perform the setActiveDoc") 
            
    def showDocuments(self):
        """
            show The list of documents
        """
        try:
            self.outputMsg("Documents in the curret application")
            i = 0
            for key in self.__pyCadApplication.getDocuments():
                self.outputMsg("%s File %s" % (str(i), str(key)))
                i += 1
            self.outputMsg("***********************************")
        except:
            self.outputMsg("Unable To Perform the GetDocuments")
    
    def closeFile(self):
        """
            close the active Document
        """
        try:
            acDoc = self.__pyCadApplication.getActiveDocuemnt()
            self.__pyCadApplication.closeDocument(acDoc.dbFile)
        except:
            self.outputMsg("Unable To close the active document")

    def openFile(self):
        """
            open a new document
        """
        try:
            filePath = self.inputMsg("File Path")
            self.__pyCadApplication.openDocument(filePath)
        except IOError:
            self.outputMsg("Unable To open the file %s" % str(filePath))

    def endApplication(self):
        """
            close the application
        """
        self.outputMsg("Bye")
        sys.exit(0)

    def performCommand(self, name):
        """
            Perform a Command
        """
        try:
            cmd_Key = str(name).upper()
            cObject = self.__pyCadApplication.getCommand(cmd_Key)
            for iv in cObject:
                exception, message = iv
                try:
                    raise exception(None)
                except ExcPoint:
                    cObject[iv] = self.imputPoint(message)                    
                except (ExcLenght, ExcAngle):
                    cObject[iv] = self.inputFloat(message)
                except (ExText):
                    cObject[iv] = self.inputMsg(message)
                except (ExEntity):
                    cObject[iv] = self.inputInt(message)
                except:
                    print("Bad error !!")
                    raise 
            else:
                cObject.applyCommand()
        except PyCadWrongCommand:
            self.outputMsg("Wrong Command")
            
    def featureTest(self):
        """
            this function make a basic test
        """
        self.outputMsg("Create a new document 1")
        doc1 = self.__pyCadApplication.newDocument()
        self.outputMsg("Create a new document 2")
        doc2 = self.__pyCadApplication.newDocument()
        self.outputMsg("Set Current p1")
        self.__pyCadApplication.setActiveDocument(doc1)
        self.outputMsg("Create Point")
        self.performCommandRandomly("POINT")
        self.outputMsg("Create Segment")
        self.performCommandRandomly("SEGMENT")
        self.outputMsg("Create Arc")
        self.performCommandRandomly("ARC")
        self.__pyCadApplication.setActiveDocument(doc2)
        self.outputMsg("Create Ellipse")
        self.performCommandRandomly("ELLIPSE")
        self.outputMsg("Create Polyline")
        self.performCommandRandomly("POLYLINE")
        self.outputMsg("Create ACLine")
        self.performCommandRandomly("ACLINE")
        
        self.outputMsg("Get Entitys for doc 1")
        self.__pyCadApplication.setActiveDocument(doc1)
        activeDoc = self.__pyCadApplication.getActiveDocument()
        ents = activeDoc.getEntityFromType("ALL")
        self.printEntity(ents)
        self.outputMsg("Get Entitys for doc 2")
        self.__pyCadApplication.setActiveDocument(doc2)
        activeDoc = self.__pyCadApplication.getActiveDocument()
        ents = activeDoc.getEntityFromType("ALL")
        self.printEntity(ents)
        # Working with styles
        self.outputMsg("Create NewStyle")
        stl = Style("NewStyle")
        self.outputMsg("Save in document")
        activeDoc.saveEntity(stl)
        activeDoc.setActiveStyle(name='NewStyle')
        self.outputMsg("Create Segment")
        self.performCommandRandomly("SEGMENT")
        self.outputMsg("Create Arc")
        self.performCommandRandomly("ARC")
        
        self.outputMsg("Create NewStyle1")
        stl1 = Style("NewStyle1")
        self.__pyCadApplication.setApplicationStyle(stl1)
        stl11 = self.__pyCadApplication.getApplicationStyle(name='NewStyle1')
        styleDic = stl11.getConstructionElements()
        styleDic[styleDic.keys()[0]].setStyleProp('entity_color', (255, 215, 000))
        self.__pyCadApplication.setApplicationStyle(stl11)
        activeDoc.saveEntity(stl11)
        self.outputMsg("Create Segment")
        self.performCommandRandomly("SEGMENT")
        self.outputMsg("Create Arc")
        self.performCommandRandomly("ARC")
        
        self.outputMsg("Create NewStyle2 ")
        stl1 = Style("NewStyle2")
        stl12 = activeDoc.saveEntity(stl1)
        styleDic = stl11.getConstructionElements()
        styleDic[styleDic.keys()[0]].setStyleProp('entity_color', (255, 215, 000))
        self.outputMsg("Update NewStyle2")
        activeDoc.saveEntity(stl12)
        self.outputMsg("Done")
        # Test  Geometrical chamfer ent
        self.GeotestChamfer()
        # Test Chamfer Command 
        self.testChamferCommand()
        
    def testGeoChamfer(self):    
        self.outputMsg("Test Chamfer")
        p1 = Point(0.0, 0.0)
        p2 = Point(10.0, 0.0)
        p3 = Point(0.0, 10.0)
        s1 = Segment(p1, p2)
        s2 = Segment(p1, p3)
        cmf = Chamfer(s1, s2, 2.0, 2.0)
        cl = cmf.getLength()
        self.outputMsg("Chamfer Lengh %s" % str(cl))
        s1, s2, s3 = cmf.getReletedComponent()
        if s3:
            for p in s3.getEndpoints():
                x, y = p.getCoords()
                self.outputMsg("P1 Cords %s, %s" % (str(x), str(y)))
        else:
            self.outputMsg("Chamfer segment in None")
    
    def testChamferCommand(self):
        """
            this function is usefoul for short test
            as soon it works copy the code into featureTest
        """
        newDoc = self.__pyCadApplication.newDocument()
        intPoint = Point(0.0, 0.0)
        
        s1 = Segment(intPoint, Point(10.0, 0.0))
        s2 = Segment(intPoint, Point(0.0, 10.0))
        
        ent1 = newDoc.saveEntity(s1)
        ent2 = newDoc.saveEntity(s2)
       
        cObject = self.__pyCadApplication.getCommand("CHAMFER")
        keys = cObject.keys()
        cObject[keys[0]] = ent1
        cObject[keys[1]] = ent2
        cObject[keys[2]] = 2
        cObject[keys[3]] = 2
        cObject[keys[4]] = None
        cObject[keys[5]] = None
        cObject.applyCommand()
    
    def easyTest(self):
        """
            this function is usefoul for short test
            as soon it works copy the code into featureTest
        """
        pass
        newDoc = self.__pyCadApplication.newDocument()
        intPoint = Point(2.0, 2.0)
        
        # a = {'SEGMENT_0': intPoint, 'SEGMENT_1': Point(10.0, 0.0)}
        s1 = Segment(intPoint, Point(10.0, 0.0))
        # s1 = Segment(a)
        s2 = Segment(intPoint, Point(0.0, 10.0))
        
        ent1 = newDoc.saveEntity(s1)
        ent2 = newDoc.saveEntity(s2)
       
        cObject = self.__pyCadApplication.getCommand("CHAMFER")
        keys = cObject.keys()
        cObject[keys[0]] = ent1
        cObject[keys[1]] = ent2
        cObject[keys[2]] = 2
        cObject[keys[3]] = 2
        cObject[keys[4]] = None
        cObject[keys[5]] = None
        cObject.applyCommand()
        
    def performCommandRandomly(self, commandName, andLoop=10):
        """
            set some random Value at the command input
        """
        self.outputMsg("Start Command %s" % str(commandName))
        i = 0
        cObject = self.__pyCadApplication.getCommand(commandName)
        for iv in cObject:
            exception, message = iv
            try:
                raise exception(None)
            except ExcPoint:
                self.outputMsg("Add Point")
                if i >= andLoop:
                    cObject[iv] = None
                else:
                    cObject[iv] = self.getRandomPoint()
            except (ExcLenght, ExcAngle):
                self.outputMsg("Add Lengh/Angle")
                cObject[iv] = 100
            except:
                self.outputMsg("Bad error !!")
                raise 
            i += 1
        else:
            # if cObject.message[0] == "Give Me the Point":
            #     cObject.value = [self.getRandomPoint()]
            self.outputMsg("Apply Command")
            cObject.applyCommand()
            
    def getRandomPoint(self):
        """
            get a random point
        """
        x = random() * 1000
        y = random() * 1000
        return Point(x, y)
    
    def inputInt(self, msg):   
        """
            return an int from user
        """        
        value = self.inputMsg(msg)
        if value:
            return int(value)
        return None
        
    def inputFloat(self, msg):
        """
            return a float number
        """
        value = self.inputMsg(msg)
        if value:
            return float(value)
        return None
        
    def imputPoint(self, msg):
        """
            ask at the user to imput a point 
        """
        msg = msg + " x,y "
        value = self.inputMsg(msg)
        if value:
            coords = value.split(',')
            x = float(coords[0])
            y = float(coords[1])
            return Point(x, y)
        return None
        
    def outputMsg(self, msg):
        """
            print an output message
        """
        print("""<PythonCad> %s""" % (str(msg)))
        
    def inputMsg(self, msg):
        """
            print and ask for a value
        """
        msg = """<PythonCad> %s >>>""" % (str(msg))
        return input(msg)

if __name__=='__main__':
    ta = textApplication()
    ta.mainLoop()
    #test()
    #io=ioKernel()
    #io.mainLoop()
    #print "bye"


