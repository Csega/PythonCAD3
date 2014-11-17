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
# This module provide basic operation for the entity in the pythoncad database
#

import cPickle as pickle

from Kernel.entity              import *
from Kernel.Db.basedb           import BaseDb
from Kernel.initsetting         import *
from Kernel.exception           import *

class EntityDb(BaseDb):
    """
        this class provide the besic operation for the entity
    """
    def __init__(self,dbConnection):
        BaseDb.__init__(self)
        if dbConnection is None:
            self.createConnection()
        else:
            self.setConnection(dbConnection)
        _sqlCheck="""select * from sqlite_master where name like 'pycadent'"""
        _table=self.makeSelect(_sqlCheck).fetchone()
        if _table is None:
            _sqlCreation="""CREATE TABLE pycadent(
                    pycad_id INTEGER PRIMARY KEY,
                    pycad_entity_id INTEGER,
                    pycad_object_type TEXT,
                    pycad_object_definition TEXT,
                    pycad_object_style TEXT,
                    pycad_security_id INTEGER,
                    pycad_undo_id INTEGER,
                    pycad_entity_state TEXT,
                    pycad_index NUMERIC,
                    pycad_visible INTEGER,
                    pycad_undo_visible INTEGER,
                    pycad_locked INTEGER,
                    pycad_bbox_xmin REAL,
                    pycad_bbox_ymin REAL,
                    pycad_bbox_xmax REAL,
                    pycad_bbox_ymax REAL)"""
            self.makeUpdateInsert(_sqlCreation)
        self.__revisionIndex=self.getRevisionIndex()
    
    def getRevisionIndex(self):
        """
            get the revision index from the database
        """
        _sql="""SELECT max(pycad_index) From pycadent"""
        index=self.fetchOneRow(_sql)
        if index is None: return 0
        return index
        
    def increaseRevisionIndex(self):
        """
            increase the relesed index
        """
        self.__revisionIndex+=1

    def decreseRevisionIndex(self):
        """
            decrese the revision index
        """
        self.__revisionIndex-=1

    def saveEntity(self,entityObj,undoId):
        """
            this method save the entity in the db
            entityObj = object that we whant to store
        """
        _entityId=entityObj.getId()
        _entityDump=pickle.dumps(entityObj.getConstructionElements())
        _entityType=entityObj.getEntityType()
        _entityVisible=entityObj.visible
        _styleObject=pickle.dumps(entityObj.style)
        _xMin,_yMin,_xMax,_yMax=entityObj.getBBox()
        _revisionIndex=self.__revisionIndex
        _revisionState=entityObj.state
        _sqlInsert="""INSERT INTO pycadent (
                    pycad_entity_id,
                    pycad_object_type,
                    pycad_object_definition,
                    pycad_object_style,
                    pycad_undo_id,
                    pycad_undo_visible,
                    pycad_bbox_xmin,
                    pycad_bbox_ymin,
                    pycad_bbox_xmax,
                    pycad_bbox_ymax,
                    pycad_entity_state,
                    pycad_index,
                    pycad_visible) VALUES
                    (?,?,?,?,?,1,?,?,?,?,?,?,?)"""
                    
        tupleArg=(
                    _entityId,
                    _entityType,
                    _entityDump,
                    _styleObject,
                    undoId,
                    _xMin,
                    _yMin,
                    _xMax,
                    _yMax, 
                    _revisionState,
                    _revisionIndex, 
                    _entityVisible)
        self.makeUpdateInsert(_sqlInsert, tupleArg)
        
    def getEntityFromTableId(self,entityTableId):
        """
            Get the entity object from the database Univoc id
        """
        _outObj=None
        _sqlGet="""SELECT   pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_object_style,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible
                FROM pycadent
                WHERE pycad_id=%s"""%str(entityTableId)
        _rows=self.makeSelect(_sqlGet)
        if _rows is not None:
            _row=_rows.fetchone()
            if _row is not None:
                _style=pickle.loads(str(_row[3]))
                _dumpObj=pickle.loads(str(_row[2]))
                _outObj=Entity(_row[1],_dumpObj,_style,_row[0])
                _outObj.state=_row[4]
                _outObj.index=_row[5]
                _outObj.visible=_row[6]
                _outObj.updateBBox()
        return _outObj
    
    def getEntityEntityId(self,entityId):
        """
            get all the entity with the entity id
        """
        _outObj=None
        _sqlGet="""SELECT   pycad_id,
                            pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_object_style,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible
                FROM pycadent
                WHERE pycad_entity_id=%s ORDER BY  pycad_id DESC"""%str(entityId)
        _dbEntRow=self.makeSelect(_sqlGet)
        if _dbEntRow is not None:
            _row=_dbEntRow.fetchone()
            _style=pickle.loads(str(_row[4]))
            _dumpObj=pickle.loads(str(_row[3]))
            _entObj=Entity(_row[2],_dumpObj,_style,_row[1])       
            _entObj.state=_row[5]
            _entObj.index=_row[6]
            _entObj.visible=_row[7]
            _entObj.updateBBox()
        return _entObj

    def getEntitysFromStyle(self,styleId):
        """
            return all the entity that match the styleId
        """
        return
        #
        # This function need to be redefined
        # the new style system is changed
        #
        _outObj=[]
        _sqlGet="""SELECT   pycad_id,
                            pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_object_style,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible
                    FROM pycadent
                    WHERE PyCad_Id IN (
                        SELECT max(PyCad_Id) 
                        FROM pycadent  
                        WHERE pycad_undo_visible=1 
                        GROUP BY pycad_entity_id ORDER BY PyCad_Id)
                    AND pycad_object_style=%s"""%str(styleId)
        _dbEntRow=self.makeSelect(_sqlGet)
        for _row in _dbEntRow: 
            _style=_row[4]
            _dumpObj=pickle.loads(_row[3])
            _objEnt=Entity(_row[2],_dumpObj,_style,_row[1])
            _objEnt.state=_row[5]
            _objEnt.index=_row[6]
            _objEnt.visible=_dbEntRow[7]
            _objEnt.updateBBox()            
            _outObj.append(_objEnt)
        return _outObj
    
    def _getEntInVersion(self, versionIndex):
        """
            get entity in version
        """
        #TODO: to be tested
        _sqlGet="""SELECT pycad_id,
                    pycad_entity_id,
                    pycad_object_type,
                    pycad_object_definition,
                    pycad_object_style,
                    pycad_entity_state,
                    pycad_index,
                    pycad_visible
                    FROM pycadent
                    WHERE PyCad_Id IN (
                        SELECT max(PyCad_Id) 
                        FROM pycadent  
                        WHERE pycad_undo_visible=1 
                        GROUP BY pycad_entity_id ORDER BY PyCad_Id)
                    AND pycad_entity_state NOT LIKE "DELETE"
                    AND pycad_index = %s
                    """%str(versionIndex)
        return self.makeSelect(_sqlGet)
        
    def getMultiFilteredEntity(self, visible=1, entityType='ALL', entityTypeArray=None):
        """
            get all visible entity
        """  
        if entityTypeArray:
            isFirst=1
            for t in entityTypeArray:
                if isFirst:
                    entityTypes="""AND (pycad_object_type like '%s'"""%str(t)
                    isFirst=0
                else:
                    entityTypes="""%s OR pycad_object_type like '%s'"""%(str(entityTypes), str(t))
            else:
                entityTypes=entityTypes+")"
        else:
            if entityType=='ALL':
                entityTypes="""AND pycad_object_type like '%'"""
            else:
                entityTypes="""AND pycad_object_type like '%s'"""%str(entityType)
                if not entityType in PY_CAD_ENT:
                    raise TypeError,"Entity type %s not supported from the dbEnt"%str(entityType)  
        _sqlGet="""SELECT pycad_id,
                    pycad_entity_id,
                    pycad_object_type,
                    pycad_object_definition,
                    pycad_object_style,
                    pycad_entity_state,
                    pycad_index,
                    pycad_visible
                    FROM pycadent
                    WHERE PyCad_Id IN (
                        SELECT max(PyCad_Id) 
                        FROM pycadent  
                        WHERE pycad_undo_visible=1  
                        GROUP BY pycad_entity_id ORDER BY PyCad_Id)
                    AND pycad_entity_state NOT LIKE "DELETE"
                    AND pycad_visible =%s
                    %s
                    """%(str(visible), str(entityTypes))
        return self.makeSelect(_sqlGet)   
        
    def getEntityFromType(self,entityType):
        """
            get all the entity from a given type 
        """
        _outObj=[]
        _dbEntRow=self.getMultiFilteredEntity(entityType=entityType)
        for _row in _dbEntRow: 
            _style=pickle.loads(str(_row[4]))
            _dumpObj=pickle.loads(str(_row[3]))
            _objEnt=Entity(_row[2],_dumpObj,_style,_row[1])
            _objEnt.state=_row[5]
            _objEnt.index=_row[6]
            _objEnt.visible=_row[7]
            _objEnt.updateBBox()            
            _outObj.append(_objEnt)
        return _outObj            
    
    def getEntityFromTypeArray(self, typeArray):
        """
            get entitys from an array of type
        """
        _outObj=[]
        _dbEntRow=self.getMultiFilteredEntity(entityTypeArray=typeArray)
        for _row in _dbEntRow: 
            _objEnt=self.convertRowToDbEnt(_row)            
            _outObj.append(_objEnt)
        return _outObj  
        
    def convertRowToDbEnt(self, row):
        """
            this function convert a single db row in a dbEnt Object
            the row mast be a row from the pycadent table with the following column order
            pycad_id,
            pycad_entity_id,
            pycad_object_type,
            pycad_object_definition,
            pycad_object_style,
            pycad_entity_state,
            pycad_index,
            pycad_visible
            FROM pycadent
        """
        _style=pickle.loads(str(row[4]))
        _dumpObj=pickle.loads(str(row[3]))
        _objEnt=Entity(row[2],_dumpObj,_style,row[1])
        _objEnt.state=row[5]
        _objEnt.index=row[6]
        _objEnt.visible=row[7]
        _objEnt.updateBBox()  
        return _objEnt
        
    def exsisting(self, id):    
        """
            check id the entity is new or is olready in the database
        """
        sqlFrase="""
                    SELECT COUNT(*) FROM pycadent 
                    WHERE pycad_entity_id=%s"""%str(id)
        _rows=self.makeSelect(sqlFrase)
        if _rows is not None:
            _row=_rows.fetchone()
            if _row is not None:
                return True
        return False
        
    def haveDrwEntitys(self, drwEntArray):
        """
            check if there is some drawing entity in the db
            drwArray mast be an erray of type entitys
        """
        isFirst=1
        for ent in drwEntArray:
            if isFirst:
                whereCause="where pycad_object_type like '%s'"%str(ent)    
                isFirst=0
            else:
                whereCause="%s or pycad_object_type like '%s'"%(str(whereCause), str(ent))
        else:
            try:
                sqlSelect="""select count(*) from pycadent %s"""%str(whereCause)
            except:
                return 0
            return self.fetchOneRow(sqlSelect)>0
        return 0
        
    def getNewEntId(self):
        """
            get the last id entity 
        """
        _outObj=0
        _sqlSelect="""select max(pycad_entity_id) from pycadent"""
        _rows=self.makeSelect(_sqlSelect)
        if _rows is not None:
            _dbEntRow=_rows.fetchone()
            if _dbEntRow is not None:
                if _dbEntRow[0] is not None:
                    _outObj=int(_dbEntRow[0])
        return _outObj

    def markUndoVisibility(self,undoId,visible):
        """
            set as undo visible all the entity with undoId
        """
        _sqlVisible="""UPDATE pycadent SET pycad_undo_visible=%s
                    WHERE pycad_undo_id=%s"""%(str(visible),str(undoId))
        self.makeUpdateInsert(_sqlVisible)
    
    def markUndoVisibilityFromEntId(self, entityId, visible):
        """
            set the undo visibility to for all the entity
        """
        _sqlVisible="""UPDATE pycadent SET pycad_undo_visible=%s
                    WHERE pycad_entity_id=%s"""%(str(visible),str(entityId))
        try:
            self.makeUpdateInsert(_sqlVisible)
        except:
            # may be the update culd fail in case we create the first entity
            return

    def markEntVisibility(self,entId,visible):
        """
            mark the visibility of the entity
        """
        _tableId="""SELECT MAX(pycad_id) FROM pycadent 
                    WHERE pycad_entity_id=%s"""%str(entId)
        _entId=self.fetchOneRow(_tableId)
        if _entId is None:
            raise EmptyDbSelect, "Unable to find the entity with id %s"%str(entId)
        # Update the entity state
        _sqlVisible="""UPDATE pycadent SET pycad_undo_visible=%s
                    WHERE pycad_id=%s"""%(str(visible),str(_entId))
        self.makeUpdateInsert(_sqlVisible) 
             
    def hideAllEntityIstance(self,entId,visible):
        """
            hide all the row with entId
        """
        _sqlVisible="""UPDATE pycadent SET pycad_undo_visible=%s
                    WHERE pycad_entity_id=%s"""%(str(visible),str(entId))
        self.makeUpdateInsert(_sqlVisible)      
        
    def delete(self,tableId):
        """
            delete the entity from db
        """
        _sqlDelete="""DELETE FROM pycadent 
                        WHERE pycad_id=%s"""%str(tableId)
        self.makeUpdateInsert(_sqlDelete)
    
    def uptateEntity(self, entityObj):
        """
            Update an exsisting entity in the database 
            *************************Attention*********************************
            Remarks : using this function you will loose the undo history.
            Remarks : with this function you will force to update all the value
            so you can update value on released entity .
            Remarks : use this function only internaly at the kernel .
            *******************************************************************
        """    
        #toto : test update function
        _entityId=entityObj.getId()
        _entityDump=pickle.dumps(entityObj.getConstructionElements())
        _entityType=entityObj.getEntityType()
        _entityVisible=entityObj.visible
        _styleObject=pickle.dumps(entityObj.style)
        _xMin,_yMin,_xMax,_yMax=entityObj.getBBox()
        _revisionIndex=entityObj.index
        _revisionState=entityObj.state
        _sqlInsert="""UPDATE pycadent set 
                    pycad_object_type="%s",
                    pycad_object_definition="%s",
                    pycad_object_style=%s,
                    pycad_bbox_xmin=%s,
                    pycad_bbox_ymin=%s,
                    pycad_bbox_xmax=%s,
                    pycad_bbox_ymax=%s,
                    pycad_entity_state="%s",
                    pycad_index=%s,
                    pycad_visible=%s
                    WHERE PyCad_Id IN (
                        SELECT max(PyCad_Id) 
                        FROM pycadent  
                        WHERE pycad_undo_visible=1 
                        GROUP BY pycad_entity_id ORDER BY PyCad_Id) 
                    AND pycad_entity_id=%s
                    """%(
                    str(_entityType),
                    str(_entityDump),
                    str(_styleObject),
                    str(_xMin),
                    str(_yMin),
                    str(_xMax),
                    str(_yMax), 
                    str(_revisionState),
                    str(_revisionIndex), 
                    str(_entityVisible), 
                    str(_entityId))
        #**************************************
        #**************Attention***************
        #**************************************
        #if dose not work conver it with ? insted of %s
        #and use the  self.makeUpdateInsert(_sqlInsert,tupleargs)
        self.makeUpdateInsert(_sqlInsert)
        
    def clearEnt(self):
        """
            perform the clear of all the entity that are not in the release state
        """
        _sql="""
                SELECT pycad_id 
                FROM pycadent
                WHERE pycad_entity_state NOT LIKE "RELEASED"
            """
        _rows=self.makeSelect(_sql)   
        for _row in _rows: 
            self.delete(_row[0])

