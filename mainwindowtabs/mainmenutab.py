#!/usr/bin/python
# -*- coding: utf-8

'''
    MainMenuTab(GenericTab)
    Variables:
    -ui        (GUI objects)
    -session   (sql session)
        
    Functions:
    -None     <- createConnections()
    -None     <- newVisit()            
    
    -bool     <- canCloseTab()
    -string   <- getType()
    -None     <- getItem()
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
from uipy.ui_mainmenu import Ui_MainMenu
from mainwindowtabs import Tabmanager
from mainwindowtabs.generictab import GenericTab

from mainwindowtabs.generictreewidget import GenericTreeWidget

#from models import SqlHandler

class MainMenuTab(GenericTab):
    def __init__(self, parent=None, item=None):
        GenericTab.__init__(self, parent=parent)
        self.ui = Ui_MainMenu()
        self.ui.setupUi(self)
        self.createConnections()
        self.configure()
        
    def createConnections(self):
        self.ui.new_visit_button.clicked.connect(self.newVisit)
        self.ui.search_button.clicked.connect(self.newSearch)
        self.ui.owner_button.clicked.connect(self.newOwner)
        self.ui.animal_button.clicked.connect(self.newAnimal)
        self.ui.vetbutton.clicked.connect(self.newVet)
        self.ui.itemcreator_button.clicked.connect(self.newItemCreator)
        self.ui.operationcreator_button.clicked.connect(self.newOperationCreator)
        
    def configure(self):
        self.ui.grindLayout

    def isUnique(self=None):
        return True
    #------------------Signals-----------------------
    def getType(self=None):
        return 'MainMenu'
    
    def newOperationCreator(self):
        from mainwindowtabs.operationbasecreatortab import OperationBaseCreatorTab
        Tabmanager.openTab(tabCreator=OperationBaseCreatorTab)
    
    def newItemCreator(self):
        from mainwindowtabs.itemcreatortab import ItemCreatorTab
        Tabmanager.openTab(tabCreator=ItemCreatorTab)
    
    def newVet(self):
        from mainwindowtabs.vettab import VetTab
        Tabmanager.openTab(tabCreator=VetTab)
        
    def newAnimal(self):
        from mainwindowtabs.animaltab import AnimalTab
        Tabmanager.openTab(tabCreator=AnimalTab)
    
    def newOwner(self):
        from mainwindowtabs.ownertab import OwnerTab
        Tabmanager.openTab(tabCreator=OwnerTab)
    
    def newVisit(self):
        from mainwindowtabs.visittab import VisitTab
        Tabmanager.openTab(tabCreator=VisitTab)
        
    def newSearch(self):
        from mainwindowtabs.searchtab import SearchTab
        Tabmanager.openTab(tabCreator=SearchTab)