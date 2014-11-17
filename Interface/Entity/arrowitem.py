 #QLinearGradient myGradient;
 #QPen myPen;
 #QPolygonF myPolygon;

 #QPainterPath myPath;
 #myPath.addPolygon(myPolygon);

 #QPainter painter(this);
 #painter.setBrush(myGradient);
 #painter.setPen(myPen);
 #painter.drawPath(myPath);

import math
from PyQt4 import QtCore, QtGui

class ArrowItem(QtGui.QGraphicsItem):
    
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
        
    def boundingRect(self):
        """
            overloading of the qt bounding rectangle
        """
        return QtCore.QRectF(-1,-250 ,80,50)
   
    def paint(self, painter,option,widget):
        """
            overloading of the paint method
        """
        painter.setPen(QtGui.QPen(QtGui.QColor(79, 106, 25)))
        painter.setBrush(QtGui.QColor(122, 163, 39))
        painter.drawPath(self.definePath())
