#!/usr/bin/env python3
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

# If this script is run directly, ensure the local Kernel directory is in path
if __name__ == "__main__":
    sys.path.append(os.path.join(os.getcwd(), "Kernel"))

# Imports
from pycadevent import PyCadEvent
from exception import *  # Assuming EntityMissing, etc. are defined here
from document import Document
from Command import APPLICATION_COMMAND


class Application(object):
    """
    This class provides the real PythonCAD API interface.
    """

    def __init__(self, **args):
        # Determine user directory for config
        userDirectory = os.getenv("USERPROFILE") or os.getenv("HOME")
        pyUserDir = os.path.join(userDirectory, "PythonCAD")
        if not os.path.exists(pyUserDir):
            os.makedirs(pyUserDir)

        baseDbName = os.path.join(pyUserDir, "PythonCAD_Local.pdr")

        self.kernel = Document(baseDbName)
        # Use a valid constant (ensure APPLICATION_COMMAND is defined in Command module)
        self.__applicationCommand = APPLICATION_COMMAND

        # Setting up Application Events
        self.startUpEvent = PyCadEvent()
        self.beforeOpenDocumentEvent = PyCadEvent()
        self.afterOpenDocumentEvent = PyCadEvent()
        self.beforeCloseDocumentEvent = PyCadEvent()
        self.afterCloseDocumentEvent = PyCadEvent()
        self.activeDocumentEvent = PyCadEvent()  # Renamed from 'activete' for spelling

        # Manage Document initialization (Fixed typo: __Docuemnts -> __documents)
        self.__documents = {}

        if "open" in args:
            self.openDocument(args["open"])
        else:
            self.__activeDocument = None

        # Fire the Application initialization event
        self.startUpEvent(self)

    @property
    def getRecentFiles(self):
        """Read from application settings the recent files."""
        objSettings = self.getApplicationSetting()

        # Sanitization: Handle case where MAX_RECENT_FILE isn't set yet
        nFiles = objSettings.getVariable("MAX_RECENT_FILE")

        if nFiles is None:
            # Default value (ensure constant is defined or use literal)
            DEFAULT_MAX = 10
            objSettings.setVariable("MAX_RECENT_FILE", DEFAULT_MAX)
            nFiles = DEFAULT_MAX

        files = objSettings.getVariable("RECENT_FILE_ARRAY")

        if not files:
            files = []
            objSettings.setVariable("RECENT_FILE_ARRAY", files)
            self.updateApplicationSetting(objSettings)

        return files

    def addRecentFiles(self, name):
        """Add recent file into the application."""
        objSettings = self.getApplicationSetting()

        nFiles = objSettings.getVariable("MAX_RECENT_FILE")
        if not nFiles:
            # Default fallback
            DEFAULT_MAX = 10
            objSettings.setVariable("MAX_RECENT_FILE", DEFAULT_MAX)
            nFiles = DEFAULT_MAX

        files = objSettings.getVariable("RECENT_FILE_ARRAY")
        if not files:
            files = []

        # Keep list size manageable
        while len(files) > nFiles - 1:
            files.pop(0)

        if name not in files:
            files.append(name)

        objSettings.setVariable("RECENT_FILE_ARRAY", files)
        self.updateApplicationSetting(objSettings)

    def setActiveDocument(self, document):
        """Set the document to active."""
        if document:
            # Python 3 fix: 'in' operator instead of has_key()
            if document.dbPath in self.__documents:
                self.__activeDocument = self.__documents[document.dbPath]
            else:
                raise EntityMissing(
                    f"Unable to set active the document {document.dbPath}"
                )
        else:
            self.__activeDocument = document

        # Event fired with updated spelling of method name if applicable, or original
        self.activeDocumentEvent(self, self.__activeDocument)

    def getCommand(self, commandType):
        """Get a command of commandType."""
        if not self.__activeDocument:
            raise EntityMissing("Missing an active document in the application")

        # Python 3 fix: 'in' operator instead of has_key()
        if commandType in self.__applicationCommand:
            cmd = self.__applicationCommand[commandType]
            # Instantiate command with active doc
            cmdInstance = cmd(self.__activeDocument)
            return cmdInstance
        else:
            raise PyCadWrongCommand(f"Wrong PythonCAD command: {commandType}")

    def getCommandList(self):
        """Get the list of all commands."""
        return self.__applicationCommand.keys()

    def newDocument(self, fileName=None):
        """Create a new document empty document in the application."""
        newDoc = Document(fileName)
        fileName = newDoc.dbPath

        # Using modern variable name
        self.__documents[fileName] = newDoc

        # Fire events
        self.afterOpenDocumentEvent(self, self.__documents[fileName])
        self.setActiveDocument(self.__documents[fileName])
        self.addRecentFiles(fileName)

        return self.__documents[fileName]

    def openDocument(self, fileName):
        """Open a saved document."""
        self.beforeOpenDocumentEvent(self, fileName)

        # Python 3 fix: 'in' operator check
        if not fileName in self.__documents:
            self.__documents[fileName] = Document(fileName)
            self.addRecentFiles(fileName)

        self.afterOpenDocumentEvent(self, self.__documents[fileName])
        self.setActiveDocument(self.__documents[fileName])
        return self.__documents[fileName]

    def saveAs(self, newFileName):
        """Save the current document to a new position."""
        if self.__activeDocument:
            oldFileName = self.__activeDocument.getName()

            # Bug Fix: Move copy before close to prevent data loss on error
            try:
                shutil.copy2(oldFileName, newFileName)
            except IOError as e:
                raise IOError(f"Failed to save file: {e}")

            self.closeDocument(oldFileName)
            return self.openDocument(newFileName)

        raise EntityMissing(
            "No document open in the application unable to perform the saveAs command"
        )

    def closeDocument(self, fileName):
        """Close the document."""
        self.beforeCloseDocumentEvent(self, fileName)

        # Bug Fix: 'key' method doesn't exist on dicts. Fixed logic to check existence.
        if fileName in self.__documents:
            del self.__documents[fileName]

            # Find next active document (first one in dict iteration order)
            # Logic preserved from original: if empty, set to None
            new_active_set = False
            for docPath in self.__documents:
                self.setActiveDocument(self.__documents[docPath])
                new_active_set = True
                break

            if not new_active_set:
                self.setActiveDocument(None)
        else:
            raise IOError(f"Unable to remove the file {fileName}")

        self.afterCloseDocumentEvent(self)

    def getActiveDocument(self):
        """Get The active Document."""
        return self.__activeDocument

    def getDocuments(self):
        """Get the Documents Collection."""
        return self.__documents

    # Manage application style

    def getApplicationStyleList(self):
        """Get the application styles."""
        return self.kernel.getDBStyles()

    def getApplicationStyle(self, id=None, name=None):
        """Retrieve a style from the application."""
        return self.kernel.getStyle(id, name)

    def setApplicationStyle(self, style):
        """Add style to the application."""
        self.kernel.saveEntity(style)

    def deleteApplicationStyle(self, styleID):
        """Delete the application style."""
        self.kernel.deleteEntity(styleID)

    # Manage the application settings

    def getApplicationSetting(self):
        """Return the setting object from the application."""
        return self.kernel.getDbSettingsObject()

    def updateApplicationSetting(self, settingObj):
        """Update the application settingObj."""
        # Updated logic to save directly via kernel API as per original intent
        self.kernel.saveEntity(settingObj)


if __name__ == "__main__":
    import application_test as test

    app = Application()
    doc = app.newDocument()

    # Uncomment to test (ensure file exists at path)
    # doc.importExternalFormat(r'C:\Users\mboscolo\Desktop\jettrainer.dxf')

    print("PythonCAD App Initialized")
