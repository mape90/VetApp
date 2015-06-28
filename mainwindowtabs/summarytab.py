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
from uipy.ui_summary import Ui_summaryTab
from uipy.ui_searchlineedit import Ui_SearchLineEdit

from mainwindowtabs.searchlineedit import SearchLineEdit
from mainwindowtabs.addNewDialog import AddNewSummary

from PyQt4.QtGui import QMessageBox

from configfile import logDEBUG, logERROR

from models import SqlHandler


class SummaryTab(GenericTab):
    def __init__(self, parent=None,visit=None):
        GenericTab.__init__(self, parent=parent, item=None)
        self.ui = Ui_summaryTab()
        self.ui.setupUi(self)
        self.visit = visit
        
        self.session = SqlHandler.newSession()
        
        self.itemSearchEdit = SearchLineEdit(tabcreator=AddNewSummary, 
                                             session=self.session, 
                                             parent=self, 
                                             function=SqlHandler.searchSummary)
        
        self.configure()
        self.configureConnctions()
    
    def getDataFromVisit(self):
        if self.visit:
            #TODO
            self.ui.plainTextEdit.appendPlainText("")
        else:
            logERROR("Summary do not hava visit, as it should have")

    def configureConnctions(self):
        self.ui.getInfoFromVisitButton.clicked.connect(self.getDataFromVisit)
    
    def configure(self):
        self.ui.searchLayout.insertWidget(0,self.itemSearchEdit)
    
    def addText(self, text):
        self.ui.plainTextEdit.appendPlainText(text)
    
    def addAskedItem(self, item):
        logDEBUG("Some one called SummaryTab with addAskedItem, item ", item)

class    