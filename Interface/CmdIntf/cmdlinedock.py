
# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt5 import QtCore, QtGui, QtWidgets
from Interface.CmdIntf.functionhandler import FunctionHandler
from Kernel.pycadevent import PyCadEvent

class CmdLineDock(QtWidgets.QDockWidget):
    '''
        A dockable window containing a edit line object.
        The edit line is used to enter commands or expressions.
    '''
    def __init__(self, title, parent):
        '''
            Creates an edit line in which commands or expressions are evaluated.
            Evaluation of expressions is done by the FunctionHandler object.
        '''
        super(CmdLineDock, self).__init__(title, parent)
        self.setMinimumHeight(100)
        self._remainder = []
        self._remainderIndex = 0
        # only dock at the bottom or top
        self.setAllowedAreas(QtCore.Qt.BottomDockWidgetArea | QtCore.Qt.TopDockWidgetArea)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dockWidgetContents.sizePolicy().hasHeightForWidth())
        self.dockWidgetContents.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        
        self.textEditOutput=PyCadTextView(self.dockWidgetContents)
        
        self.verticalLayout_2.addWidget(self.textEditOutput)
        self.__edit_ctrl = QtGui.QLineEdit(self, returnPressed=self._returnPressed)
        self.__edit_ctrl.keyPressEvent = self._keyPress
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEditOutput.sizePolicy().hasHeightForWidth())
        self.__edit_ctrl.setSizePolicy(sizePolicy)
        self.verticalLayout_2.addWidget(self.__edit_ctrl)
        self.setWidget(self.dockWidgetContents)
        self.__function_handler = FunctionHandler(self.__edit_ctrl,self.textEditOutput )
        #QtCore.QObject.connect(self.__edit_ctrl, QtCore.SIGNAL("returnPressed()"), self.textEditOutput.centerCursor)
        #
        self.evaluatePressed = PyCadEvent()
        
        self.setObjectName("CmdLineDock") #this is needed for remember toolbar position in cadwindow.writesettings(savestate)
        
    #-------- properties -----------#
    @property
    def FunctionHandler(self):
        """
            Get the function handle object
        """
        return self.__function_handler
    
    #-------- functions -----------#
    
    def _returnPressed(self):
        '''
        Text entered on the command line is accepted by the user by pressing the return button
        '''
        expression = self.__edit_ctrl.text()
        self._remainder.append(expression)
        self._remainderIndex = len(self._remainder)
        self.evaluate(expression)
        
    
    def _keyPress(self, keyEvent):
        """
            keyPressEvent
        """
        if keyEvent == QtGui.QKeySequence.MoveToNextLine:
            if self._remainderIndex < len(self._remainder) - 1:
                self._remainderIndex += 1
                self.__edit_ctrl.clear()
                self.__edit_ctrl.setText(self._remainder[self._remainderIndex])
            
        elif keyEvent == QtGui.QKeySequence.MoveToPreviousLine:
            if self._remainderIndex > 0:
                self._remainderIndex -= 1
                self.__edit_ctrl.clear()
                self.__edit_ctrl.setText(self._remainder[self._remainderIndex])
        else:
            QtGui.QLineEdit.keyPressEvent(self.__edit_ctrl, keyEvent)
            

    def evaluate(self, expression):
        '''
        Let the function handler evaluate the expression.
        * Commamds are executed.
        * Expressions are evaluated, the result is placed in the command line edit field.
        '''
        # evaluate the expression
        result = self.__function_handler.evaluate(expression)
        self.evaluatePressed(expression) # fire event 
        return result
    
    def setFocus(self, scene, event):
        """
            set the focus into the text imput
        """
        self.__edit_ctrl.clear()
        self.__edit_ctrl.setFocus()
    
    def printMsg(self, msg):
        """
            Print message in to the message windows
        """
        self.textEditOutput.printMsg(msg)
        
class PyCadTextView(QtWidgets.QTextEdit):
    """
        this class represent the text view that pyCad use for rendering the output
    """
    def __init__(self, parent):
        super(PyCadTextView, self).__init__(parent)
        self.setObjectName("textEditOutput") 
        self.setReadOnly(True) 
        self.ensureCursorVisible()
        
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu(event.pos());
        clearAction = QtGui.QAction("Clear", self, triggered=self.clear)
        menu.addAction(clearAction);
        menu.exec_(event.globalPos())
        del(menu)

    def printMsg(self, msg):
        """
            print a message withouth formatting in the last row
        """
        self.append(str(msg))
        self.scrollToBottom()

    def scrollToBottom(self):    
        """
            scroll the qttext to the end
        """
        sb = self.verticalScrollBar()
        sb.setValue(sb.maximum())
        