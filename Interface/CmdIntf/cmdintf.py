import os
import sys

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui

from Interface.CmdIntf.cmdcategory  import CmdCategory
from Interface.CmdIntf.cmdaction    import CmdAction
from Interface.CmdIntf.cmdlinedock  import CmdLineDock


class CmdIntf(object):
    '''
    Future implementation:
        Dynamic read menu, toolbars and panels from a cui/xml definition file.
    Current implementation:
        Create static menu, toolbars and palettes.
    '''
    
    def __init__(self, parent):
        # parent is the main_window object
        self.__main_window = parent
        # command line window
        self.__edit_ctrl = CmdLineDock('Command', self.__main_window)
        # dictionary with file action objects
        self.__actions = {}
        # categories in which commands are stored
        self.__category = CmdCategory(self.__main_window) 
        # icons search path
        self.__icon_dir = os.path.join(os.getcwd(), 'icons')
        #add custom event
        return
        
    #-------- properties -----------#
    @property
    def commandLine(self):
        """
            Get the command line dock window
        """
        return self.__edit_ctrl
   
    @property
    def FunctionHandler(self):
        """
            Get the function handler object
        """
        return self.__edit_ctrl.FunctionHandler
    @property 
    def Category(self):
        """
            Get the category enumerator object
        """
        return self.__category   
        
    #-------- properties -----------#
    @QtCore.pyqtSlot(str)
    def _actionHandler(self, expression):
        '''
        Callback function for all QAction objects.
        1) Look up command in the dictionary.
        2) Execute command by calling the FunctionHandler.Evaluate member.
        '''
        # evaluate command
        if len(expression) > 0:
            # command is found, evaluate it
            self.__edit_ctrl.FunctionHandler.evaluate(expression)
        return
    
    def _getIcon(self, cmd):
        '''
        Create an QIcon object based on the command name.
        The name of the icon is ':/images/' + cmd + '.png'.
        If the cmd = 'Open', the name of the icon is ':/images/Open.png'.
        '''
        icon_name = cmd + '.png'
        icon_path = os.path.join(self.__icon_dir, icon_name)
        # check if icon exist
        if os.path.exists(icon_path):
            icon = QtGui.QIcon(icon_path)
            return icon
        # icon not found, don't use an icon, return None
        return None
        
    
    def registerCommand(self, category_enum, cmd, text=None, callback=None):
        '''
        Register a command with it's call-back in the command table.
        Commands are executed by a call to the evaluate function.
        params:
            category_enum: enumerated attribute value of CmdCategory
            cmd: command name
            text: menu entry text 
            callback: call-back function
        '''
        # get the menu for this category
        menu = self.__category.getMenu(category_enum)
        # get the tool-bar for this category
        toolbar = self.__category.getToolbar(category_enum)
        # Check for the special separator name: '-'
        # A separator is not a command, it defines an separator in the menu and tool-bar.
        if cmd == '-':
            # add a separator to the menu
            if not menu is None:
                menu.addSeparator()
#            # add a separator to the tool-bar
#            if not toolbar is None:
#                toolbar.addSeparator()
        elif cmd=='>':
            #add subMenu
            pass
        else:
            # register the command with the function handler
            self.__edit_ctrl.FunctionHandler.registerCommand(cmd, callback)
            # get an icon for command, needed for tool-bar
            icon = self._getIcon(cmd)
            # create action object for this command
            action = CmdAction(cmd, icon, text, self.__main_window, self.__edit_ctrl.FunctionHandler)
            #action.callback = self._actionHandler
            # add it to the action table for fast lookup
            self.__actions[cmd] = action
            # add action to menu
            if not menu is None:
                menu.addAction(action)
            # add action to tool-bar only if an icon if found
            if (not toolbar is None) and (not icon is None):
                toolbar.addAction(action)
        return


    def evaluate(self, expression):
        '''
        Looks up the expression from the command table.
        If a command is found, it's callback function is called.
        If it is not a command the expression is evaluated.
        Return: command exit, the evaluated expression or "*error*"
        '''    
        self.__edit_ctrl.FunctionHandler.evaluate(expression)
        return
        
    def evaluateInnerCommand(self, kernelCommand, selectedItems):
        '''
            evaluate a kernel command
        '''
        self.__edit_ctrl.FunctionHandler.evaluateInnerCommand(kernelCommand, selectedItems)
     
    def evaluateMouseImput(self,view,event):
        '''
            get imput from viewport
        '''
        self.__edit_ctrl.FunctionHandler.evaluateMouseImput(event)
        
    def resetCommand(self):
        """
            reset the active command 
        """
        self.__edit_ctrl.FunctionHandler.resetCommand()

    def hideAction(self, name):
        """
            hide the name action
        """
        if self.__actions.has_key(name):
            self.__actions[name].hide()
    
    def showAction(self, name):
        """
            show the name action
        """
        if self.__actions.has_key(name):
            self.__actions[name].show()
    
    def setVisible(self, name, value):
        """
            set the action name to visible value
        """
        if self.__actions.has_key(name):
            if value:
                self.__actions[name].show()
            else:
                self.__actions[name].hide()
                
    def updateText(self, name, text):
        """
            update the label text
        """
        if self.__actions.has_key(name):
            self.__actions[name].setText(text)


    
    
