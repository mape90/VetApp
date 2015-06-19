#!/usr/bin/python
# -*- coding: utf-8

'''
Created on 14, 6, 2015

@author: mp
'''
'''
    This file is part of VetApp.

    VetApp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    VetApp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with VetApp.  If not, see <http://www.gnu.org/licenses/>.
'''

from mainwindowtabs.generictab import GenericTab
from uipy.ui_itemcreatortab import Ui_ItemCreatorTab
from uipy.ui_searchlineedit import Ui_SearchLineEdit

from mainwindowtabs.operationbasecreator import OperationBaseCreator
from mainwindowtabs.searchlineedit import SearchLineEdit

from PyQt4.QtGui import QMessageBox

from configfile import logDEBUG, logERROR

from models import SqlHandler


class OperationBaseCreatorTab(GenericTab):
    def __init__(self, parent=None,item=None):
        GenericTab.__init__(self, parent=parent, item=item)
        self.ui = Ui_ItemCreatorTab()
        self.ui.setupUi(self)
        
        self.session = SqlHandler.newSession()
        
        self.itemSearchEdit = SearchLineEdit(tabcreator=OperationBaseCreator, 
                                             session=self.session, 
                                             parent=self, 
                                             function=SqlHandler.searchOperationBase)
        
        self.configure()
        self.configureConnctions()
        self.modifyTab()
      
    def modifyTab(self):
        pass
    
    def openItem(self, item=None):
        self.itemCreator = OperationBaseCreator(parent=self, item=item)
        #self.ui.itemdialoglayout.addWidget(self.itemCreator)
        self.itemCreator.show()
    
    def openItemFromSearch(self):
        item = self.itemSearchEdit.getCurrentItem()
        if item :
            self.openItem(item)
        else:
            logDEBUG(self,"openItemFromSearch:  item is None");
    
    def itemCanBeDeleted(self, item):
        return True
    
    def deleteItemFromSearch(self):
        item = self.itemSearchEdit.getCurrentItem()
        if item and self.askUser():
            if self.itemCanBeDeleted(item):
                SqlHandler.removeItem(self.session, item)
            else:
                pass #error

    def refresh(self):
        SqlHandler.commitSession(self.session)
    
    def askUser(self):
        reply = QMessageBox.question(self,'Huomio!','Haluatko varmasti poistaa operaation pysyvästi?', QMessageBox.Ok, QMessageBox.Cancel)
        if reply == QMessageBox.Ok:
            return True
        else:
            return False
    
    def openItemNew(self):
        self.openItem(item = None)
    
    def configureConnctions(self):
        self.ui.newItemButton.clicked.connect(self.openItemNew)
        self.ui.openItemButton.clicked.connect(self.openItemFromSearch)
        self.ui.deleteItemButton.clicked.connect(self.deleteItemFromSearch)
    
    def configure(self):
        self.ui.newItemButton.setText("Uusi operaatio");
        self.ui.searchlayout.insertWidget(0,self.itemSearchEdit)
        #self.ui.itemdialoglayout.addWidget(self.itemCreator)
       
    # item is returned so we should refresh session
    def addAskedItem(self, item):
        self.refresh()
    