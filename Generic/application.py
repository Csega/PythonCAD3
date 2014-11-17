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
# This  module provide the main api interface of pythoncad
#
#
import sys
import os
import shutil
#
if __name__=="__main__":
    sys.path.append(os.path.join(os.getcwd(), 'Kernel'))
#
from Kernel.pycadevent          import PyCadEvent
from Kernel.exception           import *
from Kernel.document            import *
from Kernel.Command             import *


class Application(object):
    """
        this class provide the real pythoncad api interface ..
    """
    def __init__(self, **args):
        userDirectory=os.getenv('USERPROFILE') or os.getenv('HOME')
        pyUserDir=os.path.join(userDirectory, "PythonCAD")
        if not os.path.exists(pyUserDir):
            os.makedirs(pyUserDir)
        baseDbName=os.path.join(pyUserDir, 'PythonCAD_Local.pdr')    
        #--
        self.kernel=Document(baseDbName)
        self.__applicationCommand=APPLICATION_COMMAND
        # Setting up Application Events
        self.startUpEvent=PyCadEvent()
        self.beforeOpenDocumentEvent=PyCadEvent()
        self.afterOpenDocumentEvent=PyCadEvent()
        self.beforeCloseDocumentEvent=PyCadEvent()
        self.afterCloseDocumentEvent=PyCadEvent()
        self.activeteDocumentEvent=PyCadEvent()
        # manage Document inizialization
        self.__Docuemnts={}
        if args.has_key('open'):
            self.openDocument(args['open'])
        else:
            self.__ActiveDocument=None
        # Fire the Application inizialization
        self.startUpEvent(self)
            
    @property
    def getRecentFiles(self):    
        """
            read from application settings the recent files
        """
        objSettings=self.getApplicationSetting()
        nFiles=objSettings.getVariable("MAX_RECENT_FILE")
        if nFiles:
            files=objSettings.getVariable("RECENT_FILE_ARRAY")
            if files:
                return files
            else:
                objSettings.setVariable("RECENT_FILE_ARRAY",[] )
                self.updateApplicationSetting(objSettings)
        else:
            objSettings.setVariable("MAX_RECENT_FILE",MAX_RECENT_FILE )
            objSettings.setVariable("RECENT_FILE_ARRAY",[] )
            self.updateApplicationSetting(objSettings)
        return []
    
    def addRecentFiles(self, name):
        """
            add recent file into the application
        """
        objSettings=self.getApplicationSetting()
        nFiles=objSettings.getVariable("MAX_RECENT_FILE")
        if not nFiles:
            objSettings.setVariable("MAX_RECENT_FILE",MAX_RECENT_FILE )
        
        files=objSettings.getVariable("RECENT_FILE_ARRAY")
        if not files:
            files=[]
        while(len(files)>nFiles-1):
            files.pop(0)
        files.append(name)
        objSettings.setVariable("RECENT_FILE_ARRAY", files)
        self.updateApplicationSetting(objSettings)
        
    def setActiveDocument(self, document):    
        """
            Set the document to active
        """
        if document:
            if self.__Docuemnts.has_key(document.dbPath):
                self.__ActiveDocument=self.__Docuemnts[document.dbPath]
            else:
                raise EntityMissing("Unable to set active the document %s"%str(document.dbPath))
        else:
            self.__ActiveDocument=document
        self.activeteDocumentEvent(self, self.__ActiveDocument)   

    def getCommand(self,commandType):
        """
            Get a command of commandType
        """
        if not self.__ActiveDocument:
            raise EntityMissing("Miss Active document in the application")
        if self.__applicationCommand.has_key(commandType):
            cmd=self.__applicationCommand[commandType]
            cmdIstance=cmd(self.__ActiveDocument) 
            return cmdIstance
        else:
            raise PyCadWrongCommand("") 

    def getCommandList(self):
        """
            get the list of all the command
        """
        return self.__applicationCommand.keys()
    
    def newDocument(self, fileName=None):
        """
            Create a new document empty document in the application
        """
        newDoc=Document(fileName)
        fileName=newDoc.dbPath
        self.__Docuemnts[fileName]=newDoc
        self.afterOpenDocumentEvent(self, self.__Docuemnts[fileName])   #   Fire the open document event
        self.setActiveDocument(self.__Docuemnts[fileName])              #   Set Active the document
        self.addRecentFiles(fileName)
        return self.__Docuemnts[fileName]
        
    def openDocument(self, fileName):
        """
            open a saved document 
        """
        self.beforeOpenDocumentEvent(self, fileName)
        if not self.__Docuemnts.has_key(fileName):
            self.__Docuemnts[fileName]=Document(fileName)
            self.addRecentFiles(fileName)
        self.afterOpenDocumentEvent(self, self.__Docuemnts[fileName])   #   Fire the open document event
        self.setActiveDocument(self.__Docuemnts[fileName])              #   Set Active the document
        return self.__Docuemnts[fileName]
    
    def saveAs(self, newFileName):
        """
            seve the current document to the new position
        """
        if self.__ActiveDocument:
            oldFileName=self.__ActiveDocument.getName()
            self.closeDocument(oldFileName)
            shutil.copy2(oldFileName,newFileName)
            return self.openDocument(newFileName)
        raise EntityMissing, "No document open in the application unable to perform the saveAs comand"
    
    def closeDocument(self, fileName):
        """
            close the document
        """
        self.beforeCloseDocumentEvent(self, fileName)
        if self.__Docuemnts.has_key(fileName):
            del(self.__Docuemnts[fileName])
            for keyDoc in self.__Docuemnts:
                self.setActiveDocument(self.__Docuemnts[keyDoc])
                break
            else:
                self.setActiveDocument(None)
        else:
            raise IOError, "Unable to remove the file %s"%str(fileName)
        self.afterCloseDocumentEvent(self)
    
    def getActiveDocument(self):
        """
            get The active Document
        """
        return self.__ActiveDocument
        
    def getDocuments(self):
        """
            get the Docuemnts Collection
        """    
        return self.__Docuemnts

    #
    # manage application style
    #
    def getApplicationStyleList(self):
        """
            Get the application styles
        """
        return self.kernel.getDBStyles()
    
    def getApplicationStyle(self, id=None, name=None):
        """
            retrive a style from the application
        """
        return self.kernel.getStyle(id, name)

    def setApplicationStyle(self, style):
        """
            add style to the application
        """
        self.kernel.saveEntity(style)
    
    def deleteApplicationStyle(self, styleID):
        """
            delete the application style
        """
        self.kernel.deleteEntity(styleID)

    #
    # Manage the application settings
    #
    def getApplicationSetting(self):
        """
            return the setting object from the application
        """
        return self.kernel.getDbSettingsObject()
    
    def updateApplicationSetting(self, settingObj):
        """
            update the application settingObj
        """
        #apObj=self.kernel.getDbSettingsObject()
        #apObj.setConstructionElement(settingObj)
        self.kernel.saveEntity(settingObj)  

if __name__=='__main__':
    import application_test  as test
    app= Application()
    doc=app.newDocument()
    #doc.importExternalFormat('C:\Users\mboscolo\Desktop\jettrainer.dxf')
    #segments=doc.getEntityFromType("SEGMENT")
    #print len(segments)
    #test.TestSympy()
    test.TestIntersection()
 
    
    
