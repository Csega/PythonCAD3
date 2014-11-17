#!/usr/bin/env python
#
# This is only needed for Python v2 but is harmless for Python v3.
#
import sip
sip.setapi('QString', 2)
#
from PyQt5 import QtCore, QtGui
#
import sys
import os
import sqlite3 as sqlite
#
# this is needed for me to use unpickle objects
#
sys.path.append(os.path.join(os.getcwd(), 'Generic'))
genericPath=sys.path[len(sys.path)-1]
sys.path.append(os.path.join(genericPath,  'Kernel'))
sys.path.append(os.path.join(genericPath, 'Interface'))
#
from Interface.cadwindow import CadWindowMdi
#
def getPythonCAD():
    app = QtGui.QApplication(sys.argv)
    
    #splashscreen
    splashPath=os.path.join(os.getcwd(), 'icons', 'splashScreen1.png')
    splash_pix = QtGui.QPixmap(splashPath)
    splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.setMask(splash_pix.mask())
    splash.show()
    
    w=CadWindowMdi()
    w.show()
    
    #end splashscreen
    splash.finish(w)

    return w, app
#
if __name__ == '__main__':
    w,app=getPythonCAD()
    sys.exit(app.exec_())
