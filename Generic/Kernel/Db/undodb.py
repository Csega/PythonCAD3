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
# This  module provide access to the undo part of the pythoncad database
#

import sys

from Kernel.Db.basedb import BaseDb
from Kernel.exception import UndoDbExc

class UndoDb(BaseDb):
    """
        this Class Provide all the basic operation to be made on the
        undo
    """
    def __init__(self, dbConnection):
        BaseDb.__init__(self)
        if dbConnection is None:
            self.createConnection()
        else:
            self.setConnection(dbConnection)
        _sqlCheck = """select * from sqlite_master where name like 'pycadundo'"""
        _pycadundoTableRow = self.fetchOneRow(_sqlCheck)
        if _pycadundoTableRow is None:
            _sqlCreation = """CREATE TABLE "pycadundo" (
                                "pycad_id" INTEGER PRIMARY KEY,
                                "pycad_incremental_id" INTEGER
                                )
                                """
            self.makeUpdateInsert(_sqlCreation)
            self.__lastUndo = 1
        else:
            self.__lastUndo = self.getMaxUndoIndex()
        self.__activeUndo = self.getLastUndoIndex()

    def getMaxUndoIndex(self):
        """
            get the gretest undo index from database
        """
        _sqlCheck = "select max(pycad_incremental_id) from pycadundo"
        _row = self.fetchOneRow(_sqlCheck)
        if _row is None:            # no entity in the table
            _sqlInser = """INSERT INTO pycadundo (pycad_incremental_id) VALUES (1)"""
            self.makeUpdateInsert(_sqlInser)
            return 1
        return _row # get the max index of the table

    def getLastUndoIndex(self):
        """
            get the active undo index from database
        """
        _sqlCheck = "select pycad_incremental_id from pycadundo where pycad_id=(select max(pycad_id) from pycadundo)"
        _row = self.fetchOneRow(_sqlCheck)
        if _row is None:            # no entity in the table
            _sqlInser = """INSERT INTO pycadundo (pycad_incremental_id) VALUES (1)"""
            self.makeUpdateInsert(_sqlInser)
            return 1
        return _row # get the max index of the table

    def dbUndo(self):
        """
            performe the undo operation
        """
        _id = self.__activeUndo - 1
        while _id > 0:
            if self.undoIdExsist(_id):
                self.__activeUndo = _id
                break
            else:
                _id -= 1
        if _id > 0:
            _sqlInsert = """INSERT INTO pycadundo
                        (pycad_incremental_id) VALUES (%s)""" % str(_id)
            self.makeUpdateInsert(_sqlInsert)
            self.__activeUndo = _id
            return self.__activeUndo
        else:
            raise UndoDbExc("The undo are finished Unable to perform the undo")

    def dbRedo(self):
        """
            perform the redo operation
        """
        _id = self.__activeUndo + 1
        while _id < self.__lastUndo:
            if self.undoIdExsist(_id):
                self.__activeUndo = _id
                break
            else:
                _id += 1
        if _id <= self.__lastUndo:
            _sqlInsert = """INSERT INTO pycadundo (pycad_incremental_id) VALUES (%s)""" % str(_id)
            self.makeUpdateInsert(_sqlInsert)
            self.__activeUndo = _id
            return self.__activeUndo
        else:
            raise UndoDbExc("The undo are finished Unable to perform the redo")

    def undoIdExsist(self, undoId):
        """
            check is the undo id exsist
        """
        _sqlSelect = """SELECT pycad_incremental_id FROM pycadundo WHERE pycad_incremental_id = %s""" % str(undoId)
        return not self.fetchOneRow(_sqlSelect) is None

    def getNewUndo(self):
        """
            get the next undo index pycadundo
        """
        try:
            self.suspendCommit()        #suspend commit operation
            self.__lastUndo += 1
            self.__activeUndo = self.__lastUndo
            _sqlInser = """INSERT INTO pycadundo (pycad_incremental_id) VALUES (%s)""" % str(self.__lastUndo)
            self.makeUpdateInsert(_sqlInser)
            self.performCommit()
            return self.__lastUndo
        except:
            self.reactiveCommit()
            print("Unable to make insert into pycadundo:", sys.exc_info()[0])
            raise
        finally:
            self.reactiveCommit()

    def clearUndoTable(self):
        """
            Clear all the undo created
        """
        _sqlDelete = """DELETE FROM pycadundo"""
        self.makeUpdateInsert(_sqlDelete)

    def deleteUndo(self, undoId):
        """
            delete the undo index
        """
        _sqlDelete = """DELETE FROM pycadundo WHERE (pycad_incremental_id) VALUES (%s)""" % str(undoId)
        self.makeUpdateInsert(_sqlDelete)

    def getMaxUndoId(self):
        """
            return the undo id
        """
        return self.__lastUndo

    def getActiveUndoId(self):
        """
            return the active undo id
        """
        return self.__activeUndo

def test():
    print("*" * 10)
    _undo = PyCadUndoDb(None)
    print("Clear db Table")
    _undo.clearUndoTable()
    print("create 10 undo ")
    for i in range(10):
        _undo.getNewUndo()
    print("Undo")
    for i in range(11):
        _undo.dbUndo()
    print("redo")
    _undo.dbRedo()
