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
# This module provide class to manage geometrical CustomVector operation
#
import math

from PyQt4 import QtCore, QtGui

from Kernel.pycadevent              import PyCadEvent

class CustomVector(object):
    """
        Provide a full 2d CustomVector operation and definition
    """
    def __init__(self,p1,p2):
        """
            Default Constructor
        """
        x=p1.x()
        y=p1.y()
        x1=p2.x()
        y1=p2.y()
        self.X=x1-x
        self.Y=y1-y
    @property    
    def absAng(self):
        """
            return the angle from the cartesian reference
        """
        _y=self.Y
        ang=math.atan2(float(_y),float(self.X))
        if _y<0:
            ang=ang+2*math.pi
        return ang
    @property
    def qtPoint(self):
        """
            get the qtPoint 
        """
        return QtCore.QPointF(self.X, self.Y)
    def mag(self):
        """
            Get the versor
        """
        _a=self.absAng
        self.X=math.cos(_a)
        self.Y=math.sin(_a)
        
    def mult(self,scalar):
        """
            Multiplae the CustomVector for a scalar value
        """
        self.X=scalar*self.norm*math.cos(self.absAng)
        self.Y=scalar*self.norm*math.sin(self.absAng)    
    @property    
    def norm(self):
        """
          Get The Norm Of the CustomVector
        """
        return math.sqrt(pow(self.X,2)+pow(self.Y,2))
        
class PositionHandler(QtGui.QGraphicsItem):
    """
        this class provide a custom object for easily moving entity into
        PythonCAD
    """
    def __init__(self, position=None ):
        super(PositionHandler, self).__init__()
        self.setAcceptsHoverEvents(True)
        self.circle=CirclePosition(self, QtCore.QPointF(5,5))
        self.circle.setAcceptsHoverEvents(False)
        self.circle.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, False)
        self.circle.setAcceptDrops(False)
        self.circle.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        self.ActionHandler=ActionHandler(self, QtCore.QPointF(0,0))
        self.ActionHandler.fireApply+=self._fireApply
        self.customAction=PyCadEvent()
        self.confirmEvent=PyCadEvent()
        self.fireApply=PyCadEvent()
        if position!=None:
            self.setPos(position)
        self.position=position
        
    def _fireApply(self):
        print "Apply"
        self.fireApply()
        
    def handlerUpdated(self, angle, position):
        """
            re fire the event to the upper class
        """
        self.customAction(item, angle, position, self.distance)
       
        
    def updateSelected(self):
        pass
        
    def boundingRect(self):
        """
            method overloaded
        """
        return self.shape().boundingRect()
    
    def definePath(self):
        """
        method overloaded
        """
        p1=QtCore.QPointF(self.circle.pos().x()-5.0,self.circle.pos().y()-5.0)
        p2=QtCore.QPointF(self.ActionHandler.pos().x(),self.ActionHandler.pos().y())
        rect=QtCore.QRectF(p1,p2)
        rectPath=QtGui.QPainterPath()
        rectPath.addRect(rect)
        return rectPath
        
    def shape(self):            
        """
            overloading of the shape method 
        """
        return self.definePath()
    
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        #painter.setBrush(QtCore.Qt.cyan);
        #painter.setPen(QtCore.Qt.darkCyan);
        #painter.drawPath(self.definePath())
        pass
        
    @property
    def distance(self):  
        """
            get the distance of the trasformation
        """  
        distance=self.deltaPos
        dis=math.sqrt(pow(distance.x()-5.0, 2)+pow(distance.y()-5.0, 2))
        return dis
        
    @property
    def angle(self):
        """
            get the angle of the trasformation
        """
        return self.ActionHandler.rotation()
    @property
    def scenePos(self):
        """
            get the scene position
        """
        scenePos=self.ActionHandler.scenePos()
        return QtCore.QPointF(scenePos.x()-5,scenePos.y()-5)
    @property
    def deltaPos(self):
        """
            get the position from the starting point
        """
        return self.circle.scenePos()-self.ActionHandler.scenePos()
        
class ActionHandler(QtGui.QGraphicsItem):
    def __init__(self,parent=None, position=None ):
        super(ActionHandler, self).__init__(parent)
        # supported event 
        self.customAction=PyCadEvent()
        self.fireApply=PyCadEvent()
        # Center point 
        p0=QtCore.QPointF(5,5)
        self.circle=CirclePosition(self, p0)
        self.circle.customAction+=self.positionChanged
        self.circle.fireApply+=self._fireApply
        # Angle hendler
        self.arcAngle=ArcAngle(self, p0)
        self.arcAngle.customAction+=self.positionChanged
        self.arcAngle.fireApply+=self._fireApply
        p1=QtCore.QPointF(10,0)
        # Horizontal Arrow
        self.hArrow=ArrowItem(self,p1)
        p2=QtCore.QPointF(0,-10)
        self.hArrow.customAction+=self.positionChanged
        self.arcAngle.fireApply+=self._fireApply
        # Vertical Arrow
        self.vArrow=ArrowItem(self,p2, 90, QtGui.QPen(QtGui.QColor(79, 106, 25)))
        self.vArrow.customAction+=self.positionChanged
        self.arcAngle.fireApply+=self._fireApply
        # QGraphicsItem settings
        if position!=None:
            self.setPos(position)
        self.position=position
        self.setAcceptsHoverEvents(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        
    def _fireApply(self):   
        print "ActionHandler apply" 
        self.fireApply()
        
    def positionChanged(self):
        """
            notifies that some changed are made in position 
        """
        self.customAction(self.rotation(), self.scenePos())       
        
    def boundingRect(self):
        return QtCore.QRectF()
        
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        self.parentItem().paint(painter,option,widget)
    
        
class ArcAngle(QtGui.QGraphicsItem):
    def __init__(self,parent=None , position=None ):
        super(ArcAngle, self).__init__(parent)
        self.setAcceptsHoverEvents(True)                        #Fire over events
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)
        if position!=None:
            self.setPos(position)
        self.position=position
        self.customAction=PyCadEvent()
        self.fireApply=PyCadEvent()
    def updateSelected(self):
        pass    
    def definePath(self):
        rectangle=QtCore.QRectF(-47.5,40, 105, -110)
        arrowPath=QtGui.QPainterPath()
        arrowPath.moveTo(5, -15)
        arrowPath.arcTo(rectangle, 0, -90)
        return arrowPath
    
    def shape(self):            
        """
            overloading of the shape method 
        """
        return self.definePath()
        
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        return self.shape().boundingRect()
   
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        painter.setPen(QtGui.QPen(QtGui.QColor(79, 106, 25)))
        painter.setBrush(QtGui.QColor(0,0,128))
        painter.drawPath(self.definePath())
    
    def mousePressEvent(self, event):
        self.update()
        r=self.parentItem().rotation()
        r1=abs(math.degrees(CustomVector(self.parentItem().scenePos(),event.scenePos()).absAng))
        if r>=0 and r<=90:
            if r1>=270 and r1<=360:
                r=abs(360+r)
        self.delta=abs(r-r1)
        super(ArcAngle, self).mousePressEvent(event)
   
    def mouseMoveEvent(self, event):
        v=CustomVector(self.parentItem().scenePos(),event.scenePos())
        ang=abs(math.degrees(v.absAng))+self.delta
        self.setRotation(ang)
        super(ArcAngle, self).mouseMoveEvent(event)    
    
    def setRotation(self, angle):
        """
            set the rotation angle
        """
        self.parentItem().setRotation(angle%360)
        self.customAction()
        
    def contextMenuEvent(self, event) :
        self.menu=ContextMenu(self._keyPress, self._apply)
        self.menu.exec_(event.screenPos())
        del(self.menu)
        
    def _keyPress(self, keyEvent):
        """
            keyPressEvent
        """
        if keyEvent.key()==16777220: # Return Pressed
            text=self.menu.qle.text()
            r=self.parentItem().rotation()
            self.setRotation(float(text)+r)
            return
        QtGui.QLineEdit.keyPressEvent(self.menu.qle, keyEvent)   
        
    def _apply(self, event):
        self.fireApply()
            
        
class ContextMenu(QtGui.QMenu):
    def __init__(self, keyPressFunction=None, confermationFunction=None):
        super(ContextMenu, self).__init__()
        #set action QLineEdit
        if keyPressFunction!= None:
            self.qle=QtGui.QLineEdit()
            self.qle.keyPressEvent=keyPressFunction
            wac=QtGui.QWidgetAction(self)
            wac.setDefaultWidget(self.qle)
            dummyAction=self.addAction(wac)
        #set apply action 
        if confermationFunction!=None:
            self.label=QtGui.QLabel()
            self.label.setText("Apply")
            self.label.mouseReleaseEvent=confermationFunction
            wac1=QtGui.QWidgetAction(self)
            wac1.setDefaultWidget(self.label)
            dummyAction=self.addAction(wac1);
        
class CirclePosition(QtGui.QGraphicsItem):
    def __init__(self,parent=None , position=None ):
        super(CirclePosition, self).__init__(parent)
        self.setAcceptsHoverEvents(True)                        #Fire over events
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, False)
        if position!=None:
            self.setPos(position)
        self.customAction=PyCadEvent()
        self.fireApply=PyCadEvent()
    def updateSelected(self):
        pass    
    def definePath(self):
        ellipse=QtCore.QRectF(-10.0, -10.0, 10.0, 10.0)
        arrowPath=QtGui.QPainterPath()
        arrowPath.addEllipse(ellipse)
        return arrowPath
    
    def shape(self):            
        """
            overloading of the shape method 
        """
        return self.definePath()
        
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        return self.shape().boundingRect()
   
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        painter.setPen(QtGui.QPen(QtGui.QColor(79, 106, 25)))
        painter.setBrush(QtGui.QColor(0,0,128))
        painter.drawPath(self.definePath())
        
    def mousePressEvent(self, event):
        self.update()
        self.delta=event.pos()
        super(CirclePosition, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(CirclePosition, self).mouseReleaseEvent(event)
    
    def mouseMoveEvent(self, event):
        x=event.pos().x()-self.delta.x()+self.parentItem().pos().x()
        y=event.pos().y()-self.delta.y()+self.parentItem().pos().y()
        if self.parentItem()!= None:         
            p=QtCore.QPointF(x, y)
            self.parentItem().setPos(p)
        else:
            self.setPos(QtCore.QPointF(x, y))
            super(mouseMoveEvent, self).mouseMoveEvent(event)
        self.customAction() 
    
    def contextMenuEvent(self, event):
        self.menu=ContextMenu(self._keyPress, self._apply)
        self.menu.exec_(event.screenPos())
        del(self.menu)
        
    def _keyPress(self, keyEvent):
        """
            keyPressEvent
        """
        if keyEvent.key()==16777220: # Return Pressed
            text=self.menu.qle.text()
            x, y=text.split(',')
            p=QtCore.QPointF(float(x), float(y))
            self.parentItem().setPos(p)
            return
        QtGui.QLineEdit.keyPressEvent(self.menu.qle, keyEvent)   
        
    def _apply(self, event):
        self.fireApply()
        
class ArrowItem(QtGui.QGraphicsItem):
    def __init__(self,parent=None, position=None, rotation=None , arrowColor=None):
        super(ArrowItem, self).__init__(parent)
        self.setAcceptsHoverEvents(True)                        #Fire over events
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setAcceptDrops(True)
        self.arrowColor=QtGui.QPen(QtGui.QColor(79, 106, 25))
        self._angle=0
        if arrowColor!=None:
            self.arrowColor=arrowColor
        if position!=None:
            self.setPos(position)
        if rotation!=None:
            self.rotate(-rotation)
            self._angle=rotation
        self.delta=0
        self.customAction=PyCadEvent()
        self.fireApply=PyCadEvent()
        
    def updateSelected(self):
        pass
    def definePath(self):
        poligonArrow=QtGui.QPolygonF()
        poligonArrow.append(QtCore.QPointF(0.0, 5.0))
        poligonArrow.append(QtCore.QPointF(60.0, 5.0))
        poligonArrow.append(QtCore.QPointF(60.0, 10.0))
        poligonArrow.append(QtCore.QPointF(80.0, 0.0))
        poligonArrow.append(QtCore.QPointF(60.0, -10.0))        
        poligonArrow.append(QtCore.QPointF(60.0, -5.0))
        poligonArrow.append(QtCore.QPointF(0.0, -5.0))
        poligonArrow.append(QtCore.QPointF(0.0, 5.0))
        arrowPath=QtGui.QPainterPath()
        arrowPath.addPolygon(poligonArrow)
        return arrowPath
    
    def shape(self):            
        """
            overloading of the shape method 
        """
        return self.definePath()
        
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        return self.shape().boundingRect()
   
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        painter.setPen(self.arrowColor)
        painter.setBrush(QtGui.QColor(255,0,0))
        painter.drawPath(self.definePath())
        
    def mousePressEvent(self, event):
        self.update()
        self.delta=event.pos()
        super(ArrowItem, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(ArrowItem, self).mouseReleaseEvent(event)
        
    def mouseMoveEvent(self, event):
        if self.parentItem()!= None:
            distance=event.pos().x()-self.delta.x()
            self.setDistance(distance)
        else:
            super(ArrowItem, self).mouseMoveEvent(event)
    
    def setDistance(self, distance):
        ang=math.radians((self.parentItem().rotation()%360)-self._angle)
        x=distance*math.cos(ang)+self.parentItem().pos().x()
        y=distance*math.sin(ang)+self.parentItem().pos().y()
        self.parentItem().setPos(QtCore.QPointF(x, y))
        self.customAction()
        
    def contextMenuEvent(self, event):
        self.menu=ContextMenu(self._keyPress, self._apply)
        self.menu.exec_(event.screenPos())
        del(self.menu)
        
    def _keyPress(self, keyEvent):
        """
            keyPressEvent
        """
        if keyEvent.key()==16777220: # Return Pressed
            text=self.menu.qle.text()
            self.setDistance(float(text))
            return
        QtGui.QLineEdit.keyPressEvent(self.menu.qle, keyEvent)   
        
    def _apply(self, event):
        print "ArrowItem apply"
        self.fireApply()

