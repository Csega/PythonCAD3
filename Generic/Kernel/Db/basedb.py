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
# This  module provide access to the basic operation on pythoncad database
#

import os
import sys
import tempfile
import sqlite3 as sql

from Kernel.exception import *

class BaseDb(object):
    """
        this class provide base db operation
    """
    commit=True
    def __init__(self):
        self.__dbConnection=None
        self.dbPath=None
        
    def createConnection(self,dbPath=None):
        """
            create the connection with the database
        """
        if dbPath is None:
            f=tempfile.NamedTemporaryFile(prefix='PyCad_',suffix='.pdr')
            dbPath=f.name
            f.close()
        self.__dbConnection = sql.connect(dbPath)
        self.dbPath=dbPath
        
    def setConnection(self,dbConnection):
        """
            set the connection with the database
        """
        if not self.__dbConnection is None:
            # Todo fire a warning
            self.__dbConnection.close()
        self.__dbConnection=dbConnection

    def getConnection(self):
        """
            Get The active connection
        """
        return self.__dbConnection

    def makeSelect(self,statment):
        """
            perform a select operation
        """
        try:
            _cursor = self.__dbConnection.cursor()
            _rows = _cursor.execute(statment)
        except sql.Error, _e:
            msg="Sql Phrase: %s"%str(statment)+"\nSql Error: %s"%str( _e.args[0] )
            raise StructuralError(msg)
        except :
            for s in sys.exc_info():
                print "Generic Error: %s"%str(s)
            raise StructuralError
        #_cursor.close()
        return _rows

    def fetchOneRow(self,sqlSelect, tupleArgs=None):
        """
            get the first row of the select
        """
        try:
            _cursor = self.__dbConnection.cursor()
            if tupleArgs:
                _rows = _cursor.execute(sqlSelect,tupleArgs )
            else:
                _rows = _cursor.execute(sqlSelect)
        except sql.Error, _e:
            msg="Sql Phrase: %s"%str(sqlSelect)+"\nSql Error: %s"%str( _e.args[0] )
            raise StructuralError, msg
        except :
            for s in sys.exc_info():
                print "Generic Error: %s"%str(s)
            raise StructuralError
        _row=_rows.fetchone()
        _cursor.close()
        if _row is None or _row[0] is None:
            return None
        return _row[0]
            
    def makeUpdateInsert(self,statment, tupleArgs=None):
        """
            make an update Inster operation
        """
        #print "qui1 : sql ",statment
        try:
            _cursor = self.__dbConnection.cursor()
            if tupleArgs:
                _rows = _cursor.execute(statment,tupleArgs )
            else:
                _rows = _cursor.execute(statment)
            #if self.__commit:
            if BaseDb.commit:
                self.performCommit()
                _cursor.close()
        except sql.Error, _e:
            msg="Sql Phrase: %s"%str(statment)+"\nSql Error: %s"%str( _e.args[0] )
            raise sql.Error,msg
        except :
            for s in sys.exc_info():
                print "Generic Error: %s"%str(s)
            raise KeyError

    def close(self):
        """
            close the database connection
        """
        self.__dbConnection.close()

    def suspendCommit(self):
        """
            suspend the commit in the update\insert
        """
        #self.__commit=False
        BaseDb.commit=False

    def reactiveCommit(self):
        """
            reactive the commit in the update\insert
        """
        #self.__commit=True
        BaseDb.commit=True


    def performCommit(self):
        """
            perform a commit
        """
        try:
            self.__dbConnection.commit()
        except:
            print "Error on commit"
