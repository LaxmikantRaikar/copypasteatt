from qgis.PyQt.QtCore import Qt, QTimer, QUrl
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMenu, QApplication
from qgis.core import *
import os
from qgis.utils import iface





class CopyPasteAtt:

    
    
    
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.toolbar = self.iface.addToolBar('Copy Paste Attribute Toolbar')
        
        self.toolbar.setObjectName('CopyPasteAttToolbar')
        

    def initGui(self):

        icon = QIcon(os.path.dirname(__file__) + "/images/copy.png")
        self.copyAction = QAction(icon, "Copy Feature Attribute", self.iface.mainWindow())
        #self.iface.registerMainWindowAction(self.copyAction, "right")
        self.copyAction.setObjectName('copytool')
        self.copyAction.triggered.connect(self.copy)
       # self.copyAction.setCheckable(True)
        self.toolbar.addAction(self.copyAction)
        self.iface.addPluginToMenu("Copy Paste Attribute Toolbar", self.copyAction)
        

        

        icon = QIcon(os.path.dirname(__file__) + "/images/paste.png")
        self.pasteAction = QAction(icon, "Paste Feature Attribute", self.iface.mainWindow())
        #self.iface.registerMainWindowAction(self.pasteAction, "left")
        self.pasteAction.setObjectName('pastetool')
        self.pasteAction.triggered.connect(self.paste)
        #self.pasteAction.setCheckable(True)
        self.toolbar.addAction(self.pasteAction)
        self.iface.addPluginToMenu("Copy Paste Attribute Toolbar", self.pasteAction)
        self.pasteAction.setEnabled(False)


     


    def unload(self):

        self.iface.removePluginMenu('Copy Paste Attribute Toolbar', self.copyAction)
        self.iface.removePluginMenu('Copy Paste Attribute Toolbar', self.pasteAction)

        # Remove Toolbar Icons
        self.iface.removeToolBarIcon(self.copyAction)
        self.iface.removeToolBarIcon(self.pasteAction)
        
        
        #self.iface.unregisterMainWindowAction(self.copyAction)
        #self.iface.unregisterMainWindowAction(self.pasteAction)
        
        del self.toolbar


    
        
    def copy(self):
        self.field_list = dict()
        layer = iface.activeLayer()
        field_names = layer.fields().names()
        selection = layer.selectedFeatures()
        
        self.pasteAction.setEnabled(True)
        
        
        count = layer.selectedFeatureCount()
        
        if count == 1:
            for feature in selection: 
                for f in field_names:
                    if str(f) not in self.field_list:
                        self.field_list[str(f)] = str(feature[f])
            self.iface.messageBar().pushMessage("Copied attributes succesfully")
        
            
        else:
            self.iface.messageBar().pushMessage("Select only one feature")
  



    def paste(self):
        paste_dect = self.field_list
        paste_layer = iface.activeLayer()
        paste_field = paste_layer.fields().names()
        paste_sel = paste_layer.selectedFeatures()
        
        count = paste_layer.selectedFeatureCount()

        
        if count != 0:
        
            if paste_layer.isEditable():
            
                for paste_feature in paste_sel: 
                    for f in paste_field:
                        if str(f) in paste_dect: 
                            my_key = str(f)
                            my_value = str(paste_dect.get(my_key))
                            #print(my_key+"::"+ my_value)
                            paste_feature.setAttribute(paste_feature.fieldNameIndex(my_key), my_value)
                    paste_layer.updateFeature(paste_feature)
                    
                self.iface.messageBar().pushMessage("Pasted attributes succesfully")
                self.field_list = dict()
                #self.pasteAction.setEnabled(Flase)
                
                
            else:
                self.iface.messageBar().pushMessage("layer is not editable")
            
        else:
            self.iface.messageBar().pushMessage("Select atleast one feature")
        
    
  
