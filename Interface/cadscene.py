#
# Copyright (c) 2010 Matteo Boscolo, Gertwin Groen
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
# This module the graphics scene class
#
#

import math

from PyQt4 import QtCore, QtGui

from Generic.application import Application

from Interface.pycadapp             import PyCadApp
from Interface.Entity.base          import BaseEntity
from Interface.Entity.segment       import Segment
from Interface.Entity.arc           import Arc
from Interface.Entity.text          import Text
from Interface.Entity.ellipse       import Ellipse
from Interface.Entity.arrowitem     import ArrowItem
from Interface.Entity.actionhandler import PositionHandler
from Interface.cadinitsetting       import *
from Interface.dinamicentryobject   import DinamicEntryLine
from Interface.Preview.base         import BaseQtPreviewItem

from Kernel.pycadevent              import PyCadEvent
from Kernel.GeoEntity.point         import Point
from Kernel.exception               import *


class CadScene(QtGui.QGraphicsScene):
    def __init__(self, document, parent=None):
        super(CadScene, self).__init__(parent)
        # drawing limits
        self.setSceneRect(-10000, -10000, 20000, 20000)
        # scene custom event
#        self.pyCadScenePressEvent=PyCadEvent()   <<<<this seems unuseful
        self.updatePreview=PyCadEvent()
        self.zoomWindows=PyCadEvent()
        self.fireCommandlineFocus=PyCadEvent()
        self.fireKeyShortcut=PyCadEvent()
        self.fireKeyEvent=PyCadEvent()
        self.fireWarning=PyCadEvent()
        self.fireCoords=PyCadEvent()
        #fire Pan and Zoom events to the view
        self.firePan=PyCadEvent()
        self.fireZoomFit=PyCadEvent()
        self.__document=document
        self.__oldClickPoint=None
        self.needPreview=False
        self.forceDirection=None
        self.__lastPickedEntity=None
        self.isInPan=False
        self.forceSnap=None
        self._cmdZoomWindow=None
        self.showHandler=False
        self.posHandler=None
        #
        # new command implementation
        #
        self.__activeKernelCommand=None
        self.activeICommand=None
        #
        self.__grapWithd=20.0
        #
        # Input implemetation by carlo
        #
        self.fromPoint=None #frompoint is assigned in icommand.getClickedPoint() and deleted by applycommand and cancelcommand, is needed for statusbar coordinates dx,dy
        self.mouseOnSceneX=0.0
        self.mouseOnSceneY=0.0
        self.selectionAddMode=False
        
        # scene aspect
        r, g, b=BACKGROUND_COLOR #defined in cadinitsetting
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(r, g, b), QtCore.Qt.SolidPattern))
        
    @property
    def activeKernelCommand(self):
        """
            return the active command
        """
        return self.__activeKernelCommand
    @activeKernelCommand.setter
    def activeKernelCommand(self, value):
        self.__activeKernelCommand=value
    
    def setActiveSnap(self, value):
        if self.activeICommand!=None:
            self.activeICommand.activeSnap=value

    def _qtInputPopUpReturnPressed(self):
        self.forceDirection="F"+self.qtInputPopUp.text
        
# ###############################################MOUSE EVENTS
# ##########################################################

    def mouseMoveEvent(self, event):
        scenePos=event.scenePos()
        self.mouseOnSceneX=scenePos.x()
        self.mouseOnSceneY=scenePos.y()*-1.0
        #
        #This event manages middle mouse button PAN
        #
        if self.isInPan:
            self.firePan(None, event.scenePos())
        #
        #This event manages the status bar coordinates display (relative or absolute depending on self.fromPoint)
        #
        else:
            if self.fromPoint==None:
                self.fireCoords(scenePos.x(), (scenePos.y()*-1.0), "abs")
            else:
                x=scenePos.x()-self.fromPoint.getx()
                y=scenePos.y()*-1.0-self.fromPoint.gety()
                self.fireCoords(x, y, "rel")
        #
        #This seems needed to preview commands
        #
            if self.activeICommand:
                #scenePos=event.scenePos()
                distance=None
                point=Point(scenePos.x(), scenePos.y()*-1.0)
                qtItem=[self.itemAt(scenePos)]
                if self.__oldClickPoint:
                    distance=self.getDistance(event)
                self.activeICommand.updateMauseEvent(point, distance, qtItem)

#            self.updatePreview(self,point, distance)
        #
#        path=QtGui.QPainterPath()
#        path.addRect(scenePos.x()-self.__grapWithd/2, scenePos.y()+self.__grapWithd/2, self.__grapWithd, self.__grapWithd)
#        self.setSelectionArea(path)
        #
        super(CadScene, self).mouseMoveEvent(event)
        return 
    
    def mousePressEvent(self, event):
        if event.button()==QtCore.Qt.MidButton:
            self.isInPan=True
            self.firePan(True, event.scenePos())
        if not self.isInPan:
            qtItem=self.itemAt(event.scenePos())
            p= QtCore.QPointF(event.scenePos().x(),event.scenePos().y())
            if qtItem:
                qtItem.setSelected(True)
                self.updateSelected()
            #else:
            #    print "No item selected"
            #re fire the event
        super(CadScene, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button()==QtCore.Qt.MidButton:
            self.isInPan=False
            self.firePan(False, None)
        if not self.isInPan:
            self.updateSelected()
            qtItems=[item for item in self.selectedItems() if isinstance(item, BaseEntity)]
            if self.activeICommand:
                if event.button()==QtCore.Qt.RightButton:
                    try:
                        self.activeICommand.applyCommand()
                    except PyCadWrongImputData:
                        self.fireWarning("Wrong input value")
                    super(CadScene, self).mouseReleaseEvent(event)
                    return
                    
                if event.button()==QtCore.Qt.LeftButton:
                    point=None
                    if self.showHandler:
                        if self.posHandler==None:
                            self.posHandler=PositionHandler(event.scenePos())
                            self.addItem(self.posHandler)
                            return
                        else:
                            self.posHandler.show()
                            return
                    if point==None:
                        point=Point(event.scenePos().x(), event.scenePos().y()*-1.0)
                    # fire the mouse to the ICommand class
                    self.activeICommand.addMauseEvent(point=point,
                                                    entity=qtItems,
                                                    force=self.forceDirection)
            else:
                self.hideHandler()
                
        if self._cmdZoomWindow:
            self.zoomWindows(self.selectionArea().boundingRect())
            self._cmdZoomWindow=None
            self.clearSelection() #clear the selection after the window zoom, why? because zoom windows select entities_>that's bad
            
        super(CadScene, self).mouseReleaseEvent(event)
        return
        
    def hanhlerDoubleClick(self):  
        """
            event add from the handler 
        """
        point=Point(self.posHandler.scenePos.x(), self.posHandler.scenePos.y()*-1.0)
        self.activeICommand.addMauseEvent(point=point, 
                                            distance=posHandler.distance,
                                            angle=posHandler.angle)
        self.hideHandler()
        
    def hideHandler(self):
        """
            this function is used to hide the handler 
        """
        if self.posHandler!=None:
            self.posHandler.hide()
            
    def mouseDoubleClickEvent(self, event):
        if event.button()==QtCore.Qt.MidButton:
            self.fireZoomFit()
        else:
            pass
    
    def cancelCommand(self):
        """
            cancel the active command
        """
        self.clearSelection()
        self.updateSelected()
        #self.forceDirection=None
        self.__activeKernelCommand=None
        self.activeICommand=None
        self.showHandler=False
        self.fromPoint=None
        
# ################################################# KEY EVENTS
# ##########################################################  

    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Return:
            if self.activeICommand!=None:
                self.activeICommand.applyCommand()
        elif event.key()==QtCore.Qt.Key_Escape:
            self.cancelCommand()
        elif event.key()==QtCore.Qt.Key_Space:
            self.fireCommandlineFocus(self, event)
        elif event.key()==QtCore.Qt.Key_Shift:
            self.selectionAddMode=True
            print self.selectionAddMode
#        elif event.key()==QtCore.Qt.Key_F8:  <<<<this must maybe be implemented in cadwindow
#            if self.forceDirection is None:
#                self.forceDirection=True
#            else:
#                self.forceDirection=None
#            print self.forceDirection
#            self.forceDirection='H'        <<<<<<<H and V are substituted by ortho mode, for future implementations it could be nice if shift pressed locks the direction of the mouse pointer
#        elif event.key()==QtCore.Qt.Key_V:  <<<Ortho mode should be rewritten allowing to enter step angles and snap direction
#            self.forceDirection='V'
        elif event.key()==QtCore.Qt.Key_Q: #Maybe we could use TAB
            self.showHandler=True
        else:
            if self.activeICommand!=None:
                self.fireCommandlineFocus(self, event)
                self.fireKeyEvent(event)
            elif event.key() in KEY_MAP:
                    #exec(KEY_MAP[event.key()])
                    self.fireKeyShortcut(KEY_MAP[event.key()])
        super(CadScene, self).keyPressEvent(event)
    
    def keyReleaseEvent(self, event):
        if event.key()==QtCore.Qt.Key_Shift:
#            if self.activeICommand!=None:
#                if self.activeKernelCommand.activeException()==ExcMultiEntity:
            self.selectionAddMode=False
            print self.selectionAddMode
        else:
            pass
            
    def textInput(self, value):
        """
            someone give some test imput at the scene
        """
        if self.activeICommand!=None:
            #self.forceDirection=None # reset force direction for the imput value
            self.updateSelected()
            self.activeICommand.addTextEvent(value)
        return
            
    def updateSelected(self):
        """
            update all the selected items
        """
        for item in self.selectedItems():
            item.updateSelected()

    def clearPreview(self):
        """
            remove the preview items from the scene
        """
        entitys=[item for item in self.items() if isinstance(item, BaseQtPreviewItem)]
        for ent in entitys:
            self.removeItem(ent)
        self.__oldClickPoint=None
   
    def initDocumentEvents(self):
        """
            Initialize the document events.
        """
        if not self.__document is None:
            self.__document.showEntEvent        += self.eventShow
            self.__document.updateShowEntEvent  += self.eventUpdate
            self.__document.deleteEntityEvent   += self.eventDelete
            self.__document.massiveDeleteEvent  += self.eventMassiveDelete
            self.__document.undoRedoEvent       += self.eventUndoRedo

    def populateScene(self, document):
        """
            Traverse all entities in the document and add these to the scene.
        """
        entities = self.__document.getEntityFromType(SCENE_SUPPORTED_TYPE)
        for entity in entities:
            self.addGraficalObject(entity)
 
    def addGraficalObject(self, entity):                
        """
            Add the single object
        """
        newQtEnt=None
        entityType=entity.getEntityType()
        if entityType in SCENE_SUPPORTED_TYPE:
            newQtEnt=SCANE_OBJECT_TYPE[entityType](entity)
            self.addGraficalItem(newQtEnt)
    
    def addGraficalItem(self, qtItem):
        """
            add item to the scene 
        """
        if qtItem:
            self.addItem(qtItem)
    
    def eventUndoRedo(self, document, entity):
        """
            Manage the undo redo event
        """
        self.clear()
        self.populateScene(document)


    def eventShow(self, document, entity):        
        """
            Manage the show entity event
        """
        self.addGraficalObject(entity)
    
    
    def eventUpdate(self, document, entity):    
        """
            Manage the Update entity event  
        """
        self.updateItemsFromID([entity])
    

    def eventDelete(self, document, entity):    
        """
            Manage the Delete entity event
        """
        #import time 
        #startTime=time.clock()
        self.deleteEntity([entity])
        #endTime=time.clock()-startTime
        #print "eventDelete in %s"%str(endTime)
        
    def eventMassiveDelete(self, document,  entitys):
        """
            Massive delete of all entity event
        """
        #import time 
        #startTime=time.clock()
        self.deleteEntity(entitys)
        #endTime=time.clock()-startTime
        #print "eventDelete in %s"%str(endTime)    
    
    def deleteEntity(self, entitys):
        """
            delete the entity from the scene
        """
        dicItems=dict([( item.ID, item)for item in self.items() if isinstance(item, BaseEntity)])
        for ent in entitys:
            self.removeItem(dicItems[ent.getId()])

    def getEntFromId(self, id):
        """
            get the grafical entity from an id
        """
        dicItems=dict([( item.ID, item)for item in self.items() if isinstance(item, BaseEntity) and item.ID==id])
        if len(dicItems)>0:
            return dicItems[0][1]
        return None
        
    def updateItemsFromID(self,entitys):
        """
            Update the scene from the Entity []
        """
        dicItems=self.getAllBaseEntity()
        for ent in entitys:
            if ent.getId() in dicItems:
                self.removeItem(dicItems[ent.getId()])
                self.addGraficalObject(ent)
    
    def getAllBaseEntity(self):
        """
            get all the base entity from the scene
        """
        return dict([( item.ID, item)for item in self.items() if isinstance(item, BaseEntity)])
    
    def updateItemsFromID_2(self,entities):
        """
            update the scene from the Entity []
        """
        ids=[ent.getId() for ent in entities]
        items=[item for item in self.items() if item.ID in ids]
        for item in items:
                self.removeItem(item)
        for ent in entities:
                self.addGraficalObject(ent)
