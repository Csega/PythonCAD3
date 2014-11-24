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
#
# This  module all the interface needed to talk with pythoncad database
#
#**************************************************System Import
import os
import sys
import pickle
import logging
import time

#***************************************************Kernel Import
from .pycadevent import PyCadEvent
from .initsetting import *
from Kernel.ExternalFormat.externalformat  import ExtFormat
from Kernel.ExternalFormat.Dxf.dxf  import Dxf
from Kernel.exception import *
from Kernel.settings import *
from Kernel.entity import Entity
from Kernel.composedentity import ComposedEntity
from Kernel.layertree import LayerTree
from Kernel.layer import Layer

#***************************************************Db Import
from Kernel.Db.undodb import UndoDb
from Kernel.Db.entitydb import EntityDb
from Kernel.Db.basedb import BaseDb
from Kernel.Db.relationdb import RelationDb


#****************************************************Entity Import
from Kernel.GeoEntity.geometricalentity import GeometricalEntity, GeometricalEntityComposed
from Kernel.GeoEntity.point import Point
from Kernel.GeoEntity.segment import Segment
from Kernel.GeoEntity.arc import Arc
from Kernel.GeoEntity.ellipse import Ellipse
from Kernel.GeoEntity.polyline import Polyline
from Kernel.GeoEntity.style import Style
from Kernel.GeoEntity.entityutil import *

#   Define the log 
LEVELS = {'PyCad_Debug':    logging.DEBUG,
          'PyCad_Info':     logging.INFO,
          'PyCad_Warning':  logging.WARNING,
          'PyCad_Error':    logging.ERROR,
          'PyCad_Critical': logging.CRITICAL}
#   Set the debug level
level = LEVELS.get('PyCad_Warning', logging.NOTSET)
logging.basicConfig(level=level)
#
class Document(BaseDb):
    """
        This class provide basic operation on the pycad db database
        dbPath: is the path the database if None look in the some directory.
    """
    def __init__(self,dbPath=None):
        """
            init of the kernel
        """
        self.__logger=logging.getLogger('DbKernel')
        self.__logger.debug('__init__')
        BaseDb.__init__(self)
        # set the events
        self.__logger.debug('set events')
        self.saveEntityEvent=PyCadEvent()
        self.deleteEntityEvent=PyCadEvent()
        self.massiveDeleteEvent=PyCadEvent()
        self.showEntEvent=PyCadEvent()
        self.hideEntEvent=PyCadEvent()
        self.updateShowEntEvent=PyCadEvent()
        self.undoRedoEvent=PyCadEvent()
        self.handledErrorEvent=PyCadEvent()
        #create Connection
        self.createConnection(dbPath)
        # inizialize extentionObject
        self.__UndoDb=UndoDb(self.getConnection())
        self.__EntityDb=EntityDb(self.getConnection())
        self.__RelationDb=RelationDb(self.getConnection())
        # Some inizialization parameter
        self.__bulkCommit=False
        self.__bulkUndoIndex=-1     # undo index are alweys positive so we do not breke in case missing entity id
        self.__entId=self.__EntityDb.getNewEntId()
        #   set the default style
        self.__logger.debug('Set Style')
        self.__activeStyleObj=None
        self.__activeStyleObj=self.getMainStyle()
        self.__settings=self.getDbSettingsObject()
        #************************
        #Inizialize Layer structure
        #************************
        self.__logger.debug('Inizialize layer structure')
        try:
            self.__LayerTree=LayerTree(self)
        except StructuralError:
            raise StructuralError('Unable to create LayerTree structure')
        self.__logger.debug('Done inizialization')
    
    def getMainStyle(self):
        """
            get all the db styles
        """
        
        self.__logger.debug('getDbSettingsObject')
        styleEntitys=self.getEntityFromType('STYLE')
        for styleEntity in styleEntitys:
            styles=styleEntity.getConstructionElements()
            for stl in styles:
                if styles[stl].getName()=="Main":
                    return styleEntity
                    break
        else:
            style=Style({"STYLE_0":"Main"})
            return self.saveEntity(style) 
        
    def getDbSettingsObject(self):
        """
            get the pythoncad settings object
        """
        self.__logger.debug('getDbSettingsObject')
        _settingsObjs=self.getEntityFromType('SETTINGS')
        if len(_settingsObjs)<=0:
            _settingsObjs=Settings('MAIN_SETTING')
            self.saveEntity(_settingsObjs)
        else:
            for sto in _settingsObjs:
                _setts=sto.getConstructionElements()
                for i in _setts:
                    if _setts[i].name=='MAIN_SETTING':
                        _settingsObjs=_setts[i]
                        break
        return _settingsObjs

    def startMassiveCreation(self):
        """
            suspend the undo for write operation
        """
        self.__logger.debug('startMassiveCreation')
        self.__bulkCommit=True
        self.__bulkUndoIndex=self.__UndoDb.getNewUndo()

    def stopMassiveCreation(self):
        """
            Reactive the undo trace
        """
        self.__logger.debug('stopMassiveCreation')
        self.__bulkCommit=False
        self.__bulkUndoIndex=-1
        self.performCommit()

    def getEntity(self,entId):
        """
            get the entity from a given id
        """
        self.__logger.debug('getEntity')
        return self.__EntityDb.getEntityEntityId(entId)

    def getEntityFromType(self,entityType):
        """
            get all the entity from a specifie type
            imput :
            type as string "SEGMENT"
            type as list ["SEGMENT","ARC",...   ]
        """
        self.__logger.debug('getEntityFromType')
        if isinstance(entityType,list):
            return self.__EntityDb.getEntityFromTypeArray(entityType)
        else:
            return self.__EntityDb.getEntityFromType(entityType)
        
    def getAllDrawingEntity(self):
        """
            get all drawing entity from the db
        """
        return self.__EntityDb.getEntityFromTypeArray([DRAWIN_ENTITY[key] for key in DRAWIN_ENTITY.keys()])
   
    def getEntInDbTableFormat(self, visible=1, entityType='ALL', entityTypeArray=None):
        """
            return a db table of the entity
            visible:            1=show the visible entity 2= sho the hidden entity
            entityType:         Tipe of Entity that you are looking for "SEGMENT,ARC.."
            entityTypeArray:    an array of element in case we are lookin for all the ARC and SEGMENT
                ['ARC','SEGMENT]
            Remarks if entityTypeArray is not None entityType is ignored
        """
        return self.__EntityDb.getMultiFilteredEntity(visible,entityType , entityTypeArray)

    def convertToGeometricalEntity(self, entity):
        """
            Convert an entity into a geometrical entity
        """ 
        return entity.toGeometricalEntity()
        
    def haveDrawingEntitys(self):
        """
            check if the drawing have some data in it
        """
        return self.__EntityDb.haveDrwEntitys([DRAWIN_ENTITY[key] for key in DRAWIN_ENTITY.keys()])
    
    def saveSympyEnt(self, sympyEnt):
        """
            save the sympy entity
        """
        ent = getEntityEntity(sympyEnt)
        self.saveEntity(ent)
    
    def saveEntity(self, entity):
        """
            save the entity into the database
        """
        self.__logger.debug('saveEntity')
        if not isinstance(entity, SUPPORTED_ENTITYS):
            msg = "SaveEntity : Type %s not supported from pythoncad kernel" % type(entity)
            self.__logger.warning(msg)
            raise TypeError(msg)
        try:
            _obj = None
            # self.__UndoDb.suspendCommit()
            # self.__EntityDb.suspendCommit()
            # self.__RelationDb.suspendCommit()
            BaseDb.commit = False
            if isinstance(entity, GeometricalEntity):
                _obj = self._saveGeometricalEntity(entity)    
            elif isinstance(entity, ComposedEntity):
                _obj = self._saveComposedEntity(entity)
            elif isinstance(entity, Layer):
                _obj = self._saveLayer(entity)
            elif isinstance(entity, Settings):
                _obj = self._saveSettings(entity)
            elif isinstance(entity, Entity):  # This is used if case of update of the entity
                _obj = self._savePyCadEnt(entity)
            else:
                raise StructuralError("Entity %s not allowed to be Saved" % str(type(entity)))
            if not self.__bulkCommit:
                # self.__UndoDb.reactiveCommit()
                # self.__EntityDb.reactiveCommit()
                # self.__RelationDb.reactiveCommit()
                BaseDb.commit = True
                self.performCommit()
            return _obj
        except:
            msg = "Unexpected error: %s " % str(sys.exc_info()[0])
            raise StructuralError(msg)
            
    def _saveComposedEntity(self, entity):
        """
            save all the geometrical entity composed
        """
        relComp=[]
        #Save the releted component
        for e in entity.getChildEnt():
            relComp.append(self.saveEntity(e))
        #save the composedEntity
        _cElements, entityType =self._getCelements(entity)
        _obj=self._saveDbEnt(entType=entityType,constructorElements=_cElements)
        #seve the relation layer compose ent
        self.__RelationDb.saveRelation(self.__LayerTree.getActiveLater(),_obj)
        #seve the relation composed ent ent
        for c in relComp:
            self.__RelationDb.saveRelation(_obj,c)
        return _obj
        
    def _saveGeometricalEntity(self, entity):
        """
            save all the geometrical entity
        """
        if isinstance(entity,Style):
            _obj=self._saveStyle(entity)
        elif isinstance(entity,Entity):
            _obj=self._savePyCadEnt(entity)
        else:
            _obj=self._saveDrwEnt(entity)
        return _obj
        
        
    def _saveDrwEnt(self,entity):
        """
            Save a PythonCad drawing entity
        """
        self.__logger.debug('_saveDrwEnt')

        self.__entId+=1
        _cElements, entityType=self._getCelements(entity)
        _obj=self._saveDbEnt(entityType,_cElements)
        self.__RelationDb.saveRelation(self.__LayerTree.getActiveLater(),_obj)
        return _obj
        
    def getNewId(self):
        """
            get a new id
        """
        self.__entId+=1    
        return self.__entId
        
    def _getCelements(self, entity):
        """
            get an array of construction elements
            entity must be a DRAWIN_ENTITY
        """
        for t in DRAWIN_ENTITY :
            if isinstance(entity, t):
                entityType=DRAWIN_ENTITY[t]
                break
        return entity.getConstructionElements(), entityType
        
    def _saveSettings(self,settingsObj):
        """
            save the settings object
        """
        self.__logger.debug('_saveSettings')
        self.__entId+=1
        _cElements={}
        _cElements['SETTINGS']=settingsObj
        return self._saveDbEnt('SETTINGS',_cElements)
        
    def _saveStyle(self, styleObject):
        """
            save the style object
        """
        self.__logger.debug('_saveStyle')
        self.__entId+=1
        _cElements={}
        _cElements['STYLE']=styleObject
        #-1 is for all the entity style that do not have style :-)
        _newDbEnt=Entity('STYLE',_cElements,None,self.__entId)
        self.__EntityDb.saveEntity(_newDbEnt,self.__UndoDb.getNewUndo())
        self.saveEntityEvent(self,_newDbEnt)
        self.showEntEvent(self,_newDbEnt)
        return _newDbEnt
        
    def _saveLayer(self,layerObj):
        """
            save the layer object
        """
        self.__logger.debug('_saveLayer')
        self.__entId+=1
        _cElements={}
        _cElements['LAYER']=layerObj
        return self._saveDbEnt('LAYER',_cElements)

    def _savePyCadEnt(self, entity):
        """
            save the entity in the database
            if this entity have an id mark pycad_visible = 0
            and then save the entity
        """
        return self._saveDbEnt(entity=entity)

    def _saveDbEnt(self,entType=None,constructorElements=None, entity=None):
        """
            save the DbEnt to db
        """
        self.__logger.debug('_saveDbEnt')
        updateEvent=False
        if entity==None:
            _newDbEnt=Entity(entType,constructorElements,self.__activeStyleObj,self.__entId)
        else:
            if self.entityExsist(entity.getId()):
                updateEvent=True
            _newDbEnt=entity
        if self.__bulkUndoIndex>=0:
            self.__EntityDb.saveEntity(_newDbEnt,self.__bulkUndoIndex)
        else:
            self.__EntityDb.saveEntity(_newDbEnt,self.__UndoDb.getNewUndo())
        self.saveEntityEvent(self,_newDbEnt)
        if updateEvent:
            self.updateShowEntEvent(self,_newDbEnt)
        else:
            self.showEntEvent(self,_newDbEnt)
        return _newDbEnt

    def entityExsist(self, id):
        """
            check id the entity exsist in the database
        """
        return self.__EntityDb.exsisting(id)
        
    def getStyle(self, id=None, name=None):
        """
            get the style object
        """
        self.__logger.debug('getStyle')
        _styleObjs=self.getStyleList()
        if id!=None:
            for sto in _styleObjs:
                if sto.getId()==id:
                    return sto
        else:
            for sto in _styleObjs:
                _styleObj=sto.getConstructionElements()
                stlName=_styleObj[_styleObj.keys()[0]].getName()
                if stlName==name:
                   return sto 
        raise EntityMissing("Miss entity style in db id: <%s> name : <%s>"%(str(id), str(name)))

    def getActiveStyle(self):
        """
            Get the current style
        """
        self.__logger.debug('getActiveStyle')
        if self.__activeStyleObj==None:
            
            self.setActiveStyle(0) # In this case get the first style
            
        return self.__activeStyleObj

    def setActiveStyle(self, id=None, name=None):
        """
            set the current style
        """
        self.__logger.debug('setActiveStyle')
        if id==None and name==None:
            raise EntityMissing("Unable to retive the Style object")
        styleObject=self.getStyle(id, name)
        if styleObject==None:
            raise EntityMissing("Unable to retive the Style object")
        self.__activeStyleObj=styleObject

    def getStyleList(self):
        """
            get all the style from the db
        """
        self.__logger.debug('getStyleList')
        return self.getEntityFromType('STYLE')

    activeStyle=property(getActiveStyle,setActiveStyle)

    def unDo(self):
        """
            perform an undo operation
        """
        self.__logger.debug('unDo')
        try:
            self.__EntityDb.markUndoVisibility(self.__UndoDb.getActiveUndoId(),0)
            _newUndo=self.__UndoDb.dbUndo()
            self.__EntityDb.performCommit()
            self.undoRedoEvent(self, None)
        except UndoDb:
            raise UndoDb("Generical problem to perform undo")

    def reDo(self):
        """
            perform a redo operation
        """
        self.__logger.debug('reDo')
        try:
            _activeRedo=self.__UndoDb.dbRedo()
            self.__EntityDb.markUndoVisibility(_activeRedo, 1)
            self.__EntityDb.performCommit()
            self.undoRedoEvent(self, None)
        except UndoDb:
            raise UndoDb("Generical problem to perform reDo")

    def clearUnDoHistory(self):
        """
            perform a clear history operation
        """
        self.__logger.debug('clearUnDoHistory')
        #:TODO

        #self.__UndoDb.clearUndoTable()
        #compact all the entity
        #self.__EntityDb.compactByUndo()

    def release(self):
        """
            release the current drawing
        """
        try:
            # For Best Performance
            self.startMassiveCreation()
            # Clear the undo table
            self.__UndoDb.clearUndoTable()
            # Relese all the entity
            goodEntity=self.__EntityDb.getEntityFromType('ALL')
            for entity in goodEntity:
                entity.relese()
                self.saveEntity(entity)
            # Clear the old entity
            self.__EntityDb.clearEnt()
            # Increse the revision index
            self.__EntityDb.increaseRevisionIndex()
            # Commit all the change
            self.performCommit()
        except:
            self.__EntityDb.decreseRevisionIndex()
            print("Unable to perform the release operation")
        finally:
            self.stopMassiveCreation()

    def deleteEntity(self,entityId):
        """
            Delete the entity from the database
        """
        self.__logger.debug('deleteEntity')
        entity=self.__EntityDb.getEntityEntityId(entityId)
        entity.delete()
        self.saveEntity(entity)
        self.deleteEntityEvent(self,entity)
        
    def massiveDelete(self, entityIds):
        """
            perform a massive delete more then one entity 
        """
        self.__logger.debug('massiveDelete')
        _delEnity=[]
        try:
            self.startMassiveCreation()
            for entityId in entityIds:
                entity=self.__EntityDb.getEntityEntityId(entityId)
                entity.delete()
                self.saveEntity(entity)
                _delEnity.append(entity)
            else:    
                self.performCommit()    
        finally:
            self.massiveDeleteEvent(self, _delEnity)
            self.stopMassiveCreation()
        
    def hideEntity(self, entity=None, entityId=None):
        """
            Hide an entity
        """
        self._hide(entity, entityId, 0)
        self.hideEntEvent(self, entity) # Event

    def unHideEntity(self, entity=None, entityId=None):
        """
            Unhide an entity
        """
        self._hide(entity, entityId, 1)
        self.showEntEvent(self, entity) #Event

    def _hide(self,entity=None, entityId=None,  visible=0):
        """
            make the hide/unhide of an entity
        """
        if entity is None and entityId is None:
            raise EntityMissing("All function attribut are null")
        activeEnt=None
        if entity != None:
            activeEnt=self.__EntityDb.getEntityEntityId(entity.getId())
        if activeEnt == None and entityId is not None:
            activeEnt=self.__EntityDb.getEntityEntityId(entityId)
        if activeEnt.visible!=visible:
            activeEnt.visible=visible
            self.__EntityDb.uptateEntity(activeEnt)

    def importExternalFormat(self, fileName):
        """
            This method allow you to import a file from an external format
        """
        try:
            extFormat=ExtFormat(self)
            extFormat.openFile(fileName)
        except DxfReport:
            self.__logger.error('DxfReport')
            _err={'object':extFormat, 'error':DxfReport}
            self.handledErrorEvent(self,_err)#todo : test it not sure it works
        except DxfUnsupportedFormat:
            self.__logger.error('UnsupportedFormat')
            _err={'object':extFormat, 'error':DxfUnsupportedFormat}
            self.handledErrorEvent(self,_err)#todo : test it not sure it works

    def getTreeLayer(self):
        """
            retrive the layer from the tree
        """
        return self.__LayerTree

    def getAllChildrenType(self, parentObject, childrenType):
        """
            Get all the entity children from an pyCadDb object
        """
        return self.__RelationDb.getAllChildrenType(parentObject, childrenType)

    def getRelatioObject(self):
        """
            getRelationObject
        """
        return self.__RelationDb
    
    def getName(self):
        """
            get the name of the active document
        """
        return self.dbPath




