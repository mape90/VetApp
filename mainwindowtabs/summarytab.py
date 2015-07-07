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
from uipy.ui_summary import Ui_SummaryTab
from uipy.ui_searchlineedit import Ui_SearchLineEdit

from mainwindowtabs.searchlineedit import SearchLineEdit
from mainwindowtabs.addNewDialog import AddNewSummary

from PyQt4.QtGui import QMessageBox

from configfile import logDEBUG, logERROR

from models import SqlHandler


class SummaryTab(GenericTab):
    def __init__(self, parent=None,item=None):
        GenericTab.__init__(self, parent=parent, item=None)
        self.ui = Ui_SummaryTab()
        self.ui.setupUi(self)
        self.returnItem = False
        self.visitanimal = None

        if type(item) is dict:
            if 'owner' in item:
                self.ui.ownerNameLabel.setText(item['owner'].name)
            else:
                logERROR(self, "SummaryTab.init: owner not found from dict")
            if 'visitanimal' in item:
                self.visitanimal = item['visitanimal']
                self.ui.animalNameLabel.setText(item['visitanimal'].animal.name)
            else:
                logERROR(self, "SummaryTab.init: owner not found from dict")
            if 'text' in item:
                self.addText(item['text'])
            else:
                logERROR(self, "SummaryTab.init: text not found from dict")
        else:
            logDEBUG(self, "SummaryTab.init: item is not dict it is: "+ item)
        
        self.session = SqlHandler.newSession()
        
        self.itemSearchEdit = SearchLineEdit(tabcreator=AddNewSummary, 
                                             session=self.session, 
                                             parent=self, 
                                             function=SqlHandler.searchSummary)
        
        self.configure()
        self.configureConnctions()

    def getItem(self):
        if self.returnItem:
            return self.ui.plainTextEdit.toPlainText()
        else:
            return None

    def getDataFromVisitanimal(self):
        if(self.visitanimal):
            d = self.visitanimal.getMedicineDict()
            for key in d.keys():
                self.addText(key +':\n')
                self.addText(d[key] +'\n')


    def saveChanges(self):
        self.returnItem = True;
        self.closeTab()

    def configureConnctions(self):
        self.ui.getInfoFromVisitButton.clicked.connect(self.getDataFromVisitanimal)
        self.ui.canselButton.clicked.connect(self.closeTab)
        self.ui.closeButton.clicked.connect(self.saveChanges)
        self.ui.addSearchButton.clicked.connect(self.addFromSearch)
    
    def addFromSearch(self):
        self.addText(self.itemSearchEdit.getCurrentItem().text)

    def configure(self):
        self.ui.searchLayout.insertWidget(0,self.itemSearchEdit)
    
    def addText(self, text):
        self.ui.plainTextEdit.appendPlainText(text)
    
    def addAskedItem(self, item):
        try:
            self.ui.plainTextEdit.appendPlainText(item)
        except:
            logERROR(self, "Added item was not string it was : " + str(type(item)))
