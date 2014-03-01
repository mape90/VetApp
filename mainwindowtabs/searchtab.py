#!/usr/bin/python
# -*- coding: utf-8
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
'''
    SearchTab(GenericTab)
    Variables:
    -ui        (GUI objects)
    -session   (sql session)
    
    Functions:
    -None     <- createConnections()
    
    -bool     <- canCloseTab()
    -string   <- getType()
    -None     <- getItem()
'''
from PyQt4 import QtGui
from mainwindowtabs.generictab import GenericTab
from mainwindowtabs.searchlineedit import SearchLineEdit
from uipy.ui_searchtab import Ui_SearchTab
from models import SqlHandler
from mainwindowtabs import Tabmanager
from mainwindowtabs.itemcreatordialog import ItemCreatorDialog
import datetime

class SearchTab(GenericTab):
    def __init__(self, parent=None):
        GenericTab.__init__(self, parent=parent)
        self.ui = Ui_SearchTab()
        self.ui.setupUi(self)
        self.configure()
        self.configureConnections()
        self.setBasicInfo()
        
        
    def configure(self):
        self.billSearchLine = SearchLineEdit(tabcreator=None, session=self.session, parent=self, function=SqlHandler.searchOwner)
        self.ui.BillInnerLayout.setWidget(0,QtGui.QFormLayout.FieldRole, self.billSearchLine)
        
        self.visitOwnerSearchLineEdit = SearchLineEdit(tabcreator=None, session=self.session, parent=self, function=SqlHandler.searchOwner)
        self.ui.VisitInnerLayout.setWidget(0,QtGui.QFormLayout.FieldRole, self.visitOwnerSearchLineEdit)
        
        self.visitAnimalSearchLineEdit = SearchLineEdit(tabcreator=None, session=self.session, parent=self, function=SqlHandler.searchAnimal)
        self.ui.VisitInnerLayout.setWidget(1,QtGui.QFormLayout.FieldRole, self.visitAnimalSearchLineEdit)
        
        self.mainSearchLineEdit = SearchLineEdit(tabcreator=None, session=self.session, parent=self)
        self.ui.mainSearchLineLayout.insertWidget(0,self.mainSearchLineEdit)
    
    def configureConnections(self):
        self.ui.typeComboBox.currentIndexChanged['int'].connect(self.searchItemChanged)
        
        self.ui.specieBox.currentIndexChanged['int'].connect(self.updateSpecieRelated)
        
        self.mainSearchLineEdit.ui.editor.textEdited.connect(self.changeSearchFunction)
        self.ui.openButton.clicked.connect(self.openItem)
        
        self.ui.searchButton.clicked.connect(self.searchNow)
        
    
    def searchNow(self):
        pass
    
    def openItem(self):
        creator = self.ui.typeComboBox.itemData(self.ui.typeComboBox.currentIndex())
        currentItem = self.mainSearchLineEdit.getCurrentItem()
        if currentItem != None:
            if hasattr(creator, "getType"):
                Tabmanager.openTab(tabCreator=creator, newItem=currentItem)
            else:
                ItemCreatorDialog(parent=self, item=self.mainSearchLineEdit.getCurrentItem()).show()
    
    def searchItemChanged(self, index):
        creator = self.ui.typeComboBox.itemData(index)
        typeName = creator.getType()
        if typeName == 'Animal':
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.AnimalPage))
        elif typeName == 'Visit':
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.VisitPage))
        elif typeName == 'Bill':
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.BillPage))
        else:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.emptyPage))

   
    
    def changeSearchFunction(self):
        creator = self.ui.typeComboBox.itemData(self.ui.typeComboBox.currentIndex())
        typeName = creator.getType()
        self.mainSearchLineEdit.params = None
        if typeName == 'Animal':
            self.mainSearchLineEdit.function = self.getAnimalFunction()
        elif typeName == 'Owner':
            self.mainSearchLineEdit.function = SqlHandler.searchOwner
        elif typeName == 'Visit':
            self.mainSearchLineEdit.function = self.getVisitFunction()
        elif typeName == 'Bill':
            self.mainSearchLineEdit.function = self.getBillFunction()
        elif typeName == 'Item':
            self.mainSearchLineEdit.function = SqlHandler.searchRealItem
        elif typeName == 'Medicine':
            self.mainSearchLineEdit.function = SqlHandler.searchMedicine
        elif typeName == 'Vaccine':
            self.mainSearchLineEdit.function = SqlHandler.searchVaccine
        elif typeName == 'Feed':
            self.mainSearchLineEdit.function = SqlHandler.searchFeed
        else:
            print('SearchTab: SearchItemChanged: typeName is not specified')
    
    def getAnimalFunction(self):
        params_list = []
        params_list.append(self.specie())
        params_list.append(self.ui.raceBox.itemData(self.ui.raceBox.currentIndex()))
        params_list.append(self.ui.colorBox.itemData(self.ui.colorBox.currentIndex()))
        params_list.append(self.ui.sexBox.itemData(self.ui.sexBox.currentIndex()))
        params_list.append(self.ui.visitStartEdit.date().toPyDate())
        params_list.append(self.ui.VisitEndEdit.date().toPyDate())
        self.mainSearchLineEdit.params = params_list
        return SqlHandler.searchLineSearchAnimal
    
    def getBillFunction(self):
        params_list = []
        params_list.append(self.billSearchLine.getCurrentItem())
        params_list.append(self.ui.billVetBox.itemData(self.ui.billVetBox.currentIndex()))
        params_list.append(self.ui.billStartEdit.date().toPyDate())
        params_list.append(self.ui.billEndEdit.date().toPyDate())
        
        self.mainSearchLineEdit.params = params_list
        return SqlHandler.searchLineSearchBill
    
    def getVisitFunction(self):
        params_list = []
        params_list.append(self.visitOwnerSearchLineEdit.getCurrentItem())
        params_list.append(self.visitAnimalSearchLineEdit.getCurrentItem())
        params_list.append(self.ui.visitVetBox.itemData(self.ui.visitVetBox.currentIndex()).id if self.ui.visitVetBox.itemData(self.ui.visitVetBox.currentIndex()) != None else None)
        params_list.append(self.ui.visitStartEdit.date().toPyDate())
        params_list.append(self.ui.VisitEndEdit.date().toPyDate())
        
        self.mainSearchLineEdit.params = params_list
        return SqlHandler.searchLineSearchVisit
        
    
    def setBasicInfo(self):
        self.ui.VisitEndEdit.setDate(datetime.datetime.today())
        self.ui.billEndEdit.setDate(datetime.datetime.today())
        self.ui.dateEdit_2.setDate(datetime.datetime.today())
        self.setSex()
        self.setSpecie()
        self.setTypes()
        self.setVet()
    
    def setTypes(self):
        from mainwindowtabs.animaltab import AnimalTab
        from mainwindowtabs.visittab import VisitTab
        from mainwindowtabs.ownertab import OwnerTab
        from mainwindowtabs.billTab import BillTab
        data = [AnimalTab, OwnerTab, VisitTab, BillTab]
        for item in data:
            self.ui.typeComboBox.addItem(item.getName(), item)
        
        data = SqlHandler.getItemCreators()
        for item in data:
            self.ui.typeComboBox.addItem(item.typeName(), item)
    
    def updateSpecieRelated(self, index):
        self.ui.raceBox.clear()
        self.ui.colorBox.clear()
        specie = self.ui.specieBox.itemData(index)
        
        #check that specie is valid
        if not not specie:
            self.setRace()
            self.setColor()
    
    def setVet(self):
        self.ui.billVetBox.clear()
        self.ui.visitVetBox.clear()
        self.ui.visitVetBox.addItem('',None)
        self.ui.billVetBox.addItem('',None)
        for vet_temp in SqlHandler.searchVet(self.session):
            self.ui.visitVetBox.addItem(vet_temp.name, vet_temp)
            self.ui.billVetBox.addItem(vet_temp.name, vet_temp)
    
    def specie(self):
        return self.ui.specieBox.itemData(self.ui.specieBox.currentIndex())
    
    def setSpecie(self):   
        self.ui.specieBox.clear()
        self.ui.specieBox.addItem('', None)
        for specie in SqlHandler.searchSpecie(self.session):
            self.ui.specieBox.addItem(specie.name, specie)

    
    def setSex(self):
        self.ui.sexBox.clear()
        self.ui.sexBox.addItem('', None)
        for sex in SqlHandler.searchSex(self.session):
            self.ui.sexBox.addItem(sex.name, sex)
    
    def setColor(self):
        self.ui.colorBox.clear()
        self.ui.colorBox.addItem('', None)
        specie = self.specie()
        if specie != None:
            for color in SqlHandler.searchColor(self.session, specie.id):
                self.ui.colorBox.addItem(color.name, color)
    
    def setRace(self, newName=''):
        self.ui.raceBox.clear()
        self.ui.raceBox.addItem('', None)
        specie = self.specie()
        if specie != None:
            for race in SqlHandler.searchRace(self.session, specie.id):
                self.ui.raceBox.addItem(race.name, race)  

    def isUnique(self=None):
        return True    
    
    def createConnections(self):
        pass
    
    def getType(self=None):
        return 'Search'
    #------------------Signals-----------------------


        