'''
Created on May 12, 2010

@author: gertwin
'''

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt5 import QtCore, QtGui, QtWidgets



class CmdAction(QtWidgets.QAction):
    '''
    Derived action class to hold a command name.
    The FunctionHandler class handles signals emitted by this class.
    '''
    
    def __init__(self, command, icon, text, parent, function_handler):
        '''
        Parameters:
            command: name of the command.
            function_handler: reference to the function_handler object. 
        '''
        if not icon is None:
            super(CmdAction, self).__init__(icon, text, parent, triggered=self._actionHandler)
        else:
            super(CmdAction, self).__init__(text, parent, triggered=self._actionHandler)
        # command name
        self.__command = command
        # function handler
        self.__function_handler = function_handler
        # visible 
        self.__visible = True
        return
    
    def show(self):
        """
            show the command 
        """
        self.setEnabled(True)
        
    def hide(self):
        """
            hide the command
        """
        self.setEnabled(False)
        
    @property   
    def command(self):
        """
            get the command name
        """
        return self.__command
    
    def _actionHandler(self):
        '''
        All actions are handled by the function handler.
        From the function handler the command call-back is called.
        '''
        self.__function_handler.evaluate(self.__command)
        return
        
        
