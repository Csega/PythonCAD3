

# This is only needed for Python v2 but is harmless for Python v3.
import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui
from Interface.pycadapp import PyCadApp


class LayerDock(QtGui.QDockWidget):
    '''
    A dockable window containing a layer list object.
    The layer list contains all visible layers.
    '''
    
    def __init__(self, parent):
        '''
        Creates an edit line in which commands or expressions are evaluated.
        Evaluation of expressions is done by the FunctionHandler object.
        '''
        super(LayerDock, self).__init__('Layers', parent)
        # only dock at the bottom or top
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.__layer_ctrl = QtGui.QTreeWidget(self, itemDoubleClicked=self._itemActivated, itemActivated=self._itemActivated, itemSelectionChanged=self._itemSelectionChanged)
        self.setWidget(self.__layer_ctrl)
    
    
    def ShowAllLayers(self):
        '''
        Show all layers from the kernel in the control
        '''
        # application object from the kernel
        appl = getApplication()
        if appl:
            doc = appl.getActiveDocument()
            if doc:
                layer_tree = doc.LayerTree
                if layer_tree:
                    self._populateLayerCtrl(self.__layer_ctrl.invisibleRootItem(), layer_tree)
        return


    def _populateLayerCtrl(self, item, layers):
        '''
        Show layers from the kernel in the layer list/tree/ctrl
        '''
        if layers:
            for layer in layers:
                parent, children = layers[layer]
                # add parent to the tree
                
                
                # add child layers to the tree
                self._populateLayerCtrl(item, children)        
        return


    def _itemActivated(self, item):
        '''
        Make the selected layer in the list the active layer
        '''
        
        return
    
    
    def _itemSelectionChanged(self, item):
        '''
        The user selects an layer from the list
        '''
        
        return
    
    
    def addLayer(self, layer):
        '''
        Add a new layer to the drawing
        '''
        
        return
    
    
