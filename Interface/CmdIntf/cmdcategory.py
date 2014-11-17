#
# Copyright (c) 2002, 2003, 2004, 2005, 2006, 2007 Art Haas
# Copyright (c) 2009, 2010 Matteo Boscolo, Gertwin Groen
#
# This file is part of PythonCAD.
#
# PythonCAD is free software; you can redistribute it and/or modify
# it under the termscl_bo of the GNU General Public License as published by
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


class CmdCategory(object):
    '''
    Defines all possible categories for the user input interface
    A category represents a menu or a tool-bar.
    '''
    
    def __init__(self, main_window):
        '''
        Create category attributes from a string.
        Adding a category is adding it to the string categories.
        '''
        # list with menus
        self.__menus = {}
        # list with tool-bars
        self.__toolbars = {}
        # categories defines all possible categories
        self.__categories = 'File Edit Draw Modify View Snap Tools Windows Help'
        # create attributes from the categories string
        for number, category in enumerate(self.__categories.split()):
            # create menu
            menu_name = '&' + category
            menu = main_window.menuBar().addMenu(menu_name)
            self.__menus[number] = menu
            # create tool-bar
            toolbar = main_window.addToolBar(category)
            toolbar.setObjectName(category)  #this is needed for remember toolbar position in cadwindow.writesettings(savestate)
            self.__toolbars[number] = toolbar
            # set attribute for category
            setattr(self, category, number)
        return
    
    
    def getMenu(self, number):
        '''
        Gets an menu from the list.
        The number is the enumerated number from the categories string
        '''
        if self.__menus.has_key(number):
            return self.__menus[number]
        return None

    @property
    def getToolbarList(self):
        return self.__toolbars
        
    def getToolbar(self, number):
        '''
        Gets an tool-bar from the list.
        The number is the enumerated number from the categories string
        '''
        if self.__toolbars.has_key(number):
            return self.__toolbars[number]
        return None
    
    
    
