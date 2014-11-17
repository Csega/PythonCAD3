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
# This module provide basic operation for the Relation in the pythoncad database
#

import cPickle as pickle

from Kernel.entity          import Entity
from Kernel.Db.basedb       import BaseDb

class RelationDb(BaseDb):
    """
        this class provide the besic operation for the relation
    """
    def __init__(self,dbConnection=None):
        BaseDb.__init__(self)
        if dbConnection is None:
            self.createConnection()
        else:
            self.setConnection(dbConnection)

        _sqlCheck="""select * from sqlite_master where name like 'pycadrel'"""
        _table=self.makeSelect(_sqlCheck).fetchone()
        if _table is None:
            _sqlCreation="""CREATE TABLE pycadrel(
                    "pycad_id" INTEGER PRIMARY KEY,
                    "pycad_parent_id" INTEGER,
                    "pycad_child_id" INTEGER
                    )"""
            self.makeUpdateInsert(_sqlCreation)

    def saveRelation(self,parentEntObj,childEntObj):
        """
            This method save the Relation in the db
            TODO  : THE RELATION MAST BE UNIVOC ...
        """
        _parentEntityId=parentEntObj.getId()
        _childEntityId=childEntObj.getId()
        _sqlInsert="""INSERT INTO pycadrel (
                      pycad_parent_id,
                      pycad_child_id
                      ) VALUES
                      (%s,"%s")"""%(
                    str(_parentEntityId),
                    str(_childEntityId))
        self.makeUpdateInsert(_sqlInsert)

    def getChildrenIds(self,entityParentId):
        """
            Get the children id of a relation
        """
        _outObj=[]
        _sqlGet="""SELECT pycad_child_id
                FROM pycadrel
                WHERE pycad_parent_id=%s"""%str(entityParentId)
        _rows=self.makeSelect(_sqlGet)
        _dbEntRow=self.makeSelect(_sqlGet)
        if _dbEntRow is not None:
            for _row in _dbEntRow:
                _outObj.append(_row[0])
        return _outObj

    def getAllChildrenType(self, parent, childrenType=None):
        """
            get all the children entity of type childrenType
        """
        _outObj=[]
        if not childrenType:
            childrenType='%'
        if childrenType=='ALL':
            childrenType='%'
        _sqlSelect="""SELECT pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_style_id,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible
                            FROM pycadent
                            WHERE pycad_entity_id IN
                                (
                                    SELECT pycad_child_id
                                    FROM pycadrel
                                    WHERE pycad_parent_id =%s
                                )
                            AND pycad_entity_state NOT LIKE "DELETE"
                            AND pycad_object_type LIKE '%s'
                            AND pycad_undo_visible=1
                            """%(str(parent.getId()), str(childrenType))
        _dbEntRow=self.makeSelect(_sqlSelect)
        for _row in _dbEntRow:
            _style=_row[3]
            _dumpObj=pickle.loads(str(_row[2]))
            _objEnt=Entity(_row[1],_dumpObj,_style,_row[0])
            _objEnt.state=_row[4]
            _objEnt.index=_row[5]
            _objEnt.visible=_row[6]
            _objEnt.updateBBox()
            _outObj.append(_objEnt)
        return _outObj

    def getParentEnt(self,entity):
        """
            get the parent entity
            TODO: To be tested
        """
        _sqlSelect="""SELECT pycad_entity_id,
                            pycad_object_type,
                            pycad_object_definition,
                            pycad_style_id,
                            pycad_entity_state,
                            pycad_index,
                            pycad_visible
                            FROM pycadent
                            WHERE pycad_entity_id IN
                                (
                                    SELECT pycad_parent_id
                                    FROM pycadrel
                                    WHERE pycad_child_id =%s
                                )
                            AND pycad_entity_state NOT LIKE "DELETE"
                            AND pycad_object_type LIKE '%s'
                            AND pycad_undo_visible=1
                            """%(str(parent.getId()))
        _dbEntRow=self.makeSelect(_sqlSelect)
        for _row in _dbEntRow:
            _style=_row[3]
            _dumpObj=pickle.loads(str(_row[2]))
            _objEnt=Entity(_row[1],_dumpObj,_style,_row[0])
            _objEnt.state=_row[4]
            _objEnt.index=_row[5]
            _objEnt.visible=_row[6]
            _objEnt.updateBBox()
            return _objEnt
        return None

    def deleteFromParent(self,entityObj):
        """
            Delete the entity from db
        """
        _entityId=entityObj.getId()
        _sqlDelete="""DELETE FROM pycadrel
            WHERE pycad_parent_id='%s'"""%str(_entityId)
        self.makeUpdateInsert(_sqlDelete)

    def deleteFromChild(self,entityObj):
        """
            Delete the entity from db
        """
        _entityId=entityObj.getId()
        _sqlDelete="""DELETE FROM pycadrel
            WHERE pycad_child_id='%s'"""%str(_entityId)
        self.makeUpdateInsert(_sqlDelete)

    def deleteRelation(self,entityObjParent,entityObjChild):
        """
            delete the relation from parent and child
        """
        _parentId=entityObjParent.getId()
        _childId=entityObjChild.getId()
        _sqlDelete="""DELETE FROM pycadrel
            WHERE pycad_parent_id='%s' and pycad_child_id='%s'and """%(str(_parentId),str(_childId))
        self.makeUpdateInsert(_sqlDelete)

    def relationExsist(self, parentId, childId):
        """
            check if the given parent child id exsist or not
        """
        _sqlSelect="""SELECT COUNT(*)
                    FROM pycadrel
                    WHERE pycad_parent_id='%s' and pycad_child_id='%s'
                    """%(str(parentId),str(childId))
        res=self.fetchOneRow(_sqlSelect)
        return res

"""
    TODO TEST deleteFromChild
    TODO TEST deleteRelation
"""
