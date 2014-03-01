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
    VisitTab(GenericTab)
    Variables:
    -ui        (Gui objects)
    -session   (sql session)
    -item      (Visit)
    
    Functions:
    Own functions:
    -None     <- createConnections()
    
    Functions From parent:
    -string   <- getType()
    -item     <- getItem() i.e. Animal, Owner, visit
    -bool     <- askUserIfCanClose()
    -bool     <- canCloseTab()
    -None     <- closeTab()
    -None     <- saveAndCloseTab()
    -None     <- saveTab()
    -bool     <- isUnique()
    
    Overloaded
    -list     <- getData()
    -None     <- addAskedItem()
    -item     <- makeItem()
    -bool     <- saveAble
    -bool     <- hasChanged
    -string   <- getMessageBoxText
'''

from mainwindowtabs.generictab import GenericTab
from uipy.ui_visit import Ui_Visit
from models import SqlHandler
from mainwindowtabs import Tabmanager

import datetime


from mainwindowtabs.searchlineedit import SearchLineEdit
from mainwindowtabs.generictreewidget import GenericTreeWidget, ButtonType, VisitAnimalTreeWidget, OperationTreeWidget, ItemTreeWidget

class VisitTab(GenericTab):
    def __init__(self, parent=None, item=None):
        GenericTab.__init__(self, parent=parent, item=item)
        self.ui = Ui_Visit()
        self.ui.setupUi(self)
        self.ui.stackedWidget.setCurrentIndex(0) #TODO:remove if needed
        
        self.currentVisitAnimal = None
        self.currentOperation = None
        
        self.configure()
           
        self.createConnections()
        self.setBasicInfo()
    
    def setBasicInfo(self):
        self.disableAnimalTree(True)
        if self.item != None:
            self.ownerserachline.setCurrentItem(self.item.owner)
            if self.item.start_time != None:
                self.ui.startTimeEdit.setDateTime(self.item.start_time)
            if self.item.end_time:
                self.ui.endTimeEdit.setDateTime(self.item.end_time)
            self.setVet(self.item.vet)
            self.animalTreeWidget.setItems(self.item.visitanimals)
            self.disableAnimalTree(False)
        else:
            self.ui.startTimeEdit.setDateTime(datetime.datetime.now())
            self.setVet()
    
    def setVet(self, vet=None):
        self.ui.vetComboBox.clear()
        
        for vet_temp in SqlHandler.searchVet(self.session):
            self.ui.vetComboBox.addItem(vet_temp.name, vet_temp)
        
        if vet != None:
            for index in range(0, self.ui.vetComboBox.count()):
                if self.ui.vetComboBox.itemData(index).id == vet.id:
                    self.ui.vetComboBox.setCurrentIndex(index)
                    return
        else:
            pass #TODO: Select current vet! ConfigServer
        
    def configure(self):
        self.operationTreeWidget = OperationTreeWidget(parent=self, session=self.session)
        
        self.ui.operationMainLayout.insertWidget(0, self.operationTreeWidget)
        self.ui.operationMainLayout.setStretch(0,1)
        self.ui.operationMainLayout.setStretch(1,2)
        
        
        self.animalTreeWidget = VisitAnimalTreeWidget(parent=self, session=self.session)
       
        self.ui.animalSelectorLayout.addWidget(self.animalTreeWidget)
        
        from models.operation import SurgeryItem
        self.itemTreeWidget = ItemTreeWidget(parent=self, session=self.session, creator=SurgeryItem)
        self.ui.itemTreeWidgetLayout.addWidget(self.itemTreeWidget)
        
        from mainwindowtabs.ownertab import OwnerTab
        self.ownerserachline = SearchLineEdit(tabcreator=OwnerTab, session=self.session ,parent=self, function=SqlHandler.searchOwner)
        self.ui.ownerLayout.addWidget(self.ownerserachline)
        
    def createConnections(self):
        self.ownerserachline.ui.editor.returnPressed.connect(self.ownerSet)
        self.animalTreeWidget.ui.treeWidget.currentItemChanged.connect(self.animalChanged)
        
        self.operationTreeWidget.ui.treeWidget.currentItemChanged.connect(self.operationChanged)
        
        self.ui.saveandcloseButton.clicked.connect(self.saveAndCloseTab)
        self.ui.saveButton.clicked.connect(self.saveTab)
        self.ui.billButton.clicked.connect(self.openBill)
        self.ui.closeButton.clicked.connect(self.closeTab)

        
    def operationChanged(self,current, previous):
        if current != None:
            '''Enable operation related if those arent enabled'''
            if not self.ui.operationNameLabel.isEnabled():
                self.disableOperationRelated(False)
            '''Only if real change have happened then update'''
            if current != previous:
                if self.currentOperation != None:
                    self.updateCurerentOperation()
                    if previous != None:
                        previous.setText(3, str(self.currentOperation.stringList()[3]))
                self.currentOperation = current.data(0,0)
                self.setOperationData(current.data(0,0))
        else:
            '''If current is None then treeWidget is empty and all data will be removed'''
            print('Current was None-----------------------')
            if self.ui.operationNameLabel.isEnabled():
                self.clearOperationRelated()
                self.disableOperationRelated(True)
                self.currentOperation = None
        
    def clearOperationRelated(self):
        self.closeOperation()
    
    def closeOperation(self):
        print("visitTab closeOperation, ")
        self.ui.operationNameLabel.setText('Nimi')
        self.ui.retailPriceLabel.setText('0.00')
        self.itemTreeWidget.clearTreeWidget()
        self.ui.priceSpinBox.setValue(0)
        self.ui.descriptionTextEdit.setPlainText('')
        self.ui.stackedWidget.setCurrentIndex(0)
        
        
    def updateCurerentOperation(self):
        if self.currentOperation != None:
            data = []
            data.append(self.ui.priceSpinBox.value())
            data.append(self.ui.descriptionTextEdit.toPlainText())
            if self.currentOperation.hasList():
                data.append(self.itemTreeWidget.getItemsFromList())
            self.currentOperation.update(data)

    def setOperationData(self, operation=None):
        self.ui.operationNameLabel.setText(operation.base.name)
        self.ui.retailPriceLabel.setText(str(operation.base.price))
        self.ui.priceSpinBox.setValue(operation.price)
        self.ui.descriptionTextEdit.setPlainText(operation.description)
        
        if self.currentOperation.hasList():
            self.ui.stackedWidget.setCurrentIndex(2)
            self.itemTreeWidget.setItems(self.currentOperation.items)
        elif self.currentOperation.base.hasItem():
            self.ui.stackedWidget.setCurrentIndex(1)
            self.ui.nameLabel.setText(self.currentOperation.base.item.name if self.currentOperation.base.item != None else '')
            self.ui.typeLabel.setText(self.currentOperation.base.item.typeName() if self.currentOperation.base.item != None else '')
            self.ui.itemPriceLabel.setText(str(self.currentOperation.base.item.price) if self.currentOperation.base.item != None else '')
        else:
            self.ui.stackedWidget.setCurrentIndex(0)

    
    def openBill(self):
        if self.saveAble():
            self.saveTab()
            from mainwindowtabs.billTab import BillTab
            #TODO: add check if there is already bill so open it
            bill = SqlHandler.getBill(self.session, self.item)
            if bill != None:
                Tabmanager.openTab(tabCreator=BillTab, newItem=bill)
            else:
                Tabmanager.openTab(tabCreator=BillTab, newItem=self.item)
        else:
            self.errorMessage('Omistajaa ei ole asetettu!')
        
    def animalChanged(self,current, previous):
        print('VisitTab: animalChanged: current', current)
        print('VisitTab: animalChanged: previous', previous)
        if current != None:
            '''Enable animal related if those arent enabled'''
            if not self.operationTreeWidget.isEnabled():
                self.disableAnimalRelated(False)
            '''Only if real change have happened then update'''
            if current != previous:
                if previous != None:
                    self.updateCurrentVisitAnimal()
                self.currentVisitAnimal = current.data(0,0)
                self.setVisitAnimalData(current.data(0,0))
        else:
            '''If current is None then treeWidget is empty and all data will be removed'''
            if self.operationTreeWidget.isEnabled():
                self.clearAnimalRelated()
                self.disableAnimalRelated(True)
                self.currentVisitAnimal = None
  
    '''Clears text areas and operation tree'''
    def clearAnimalRelated(self):
        self.ui.animalNameLabel.setText('Ei valittua eläintä')
        self.ui.amanuensisTextEdit.setPlainText('')
        self.ui.statusTextEdit.setPlainText('')
        self.ui.diagnosisTextEdit.setPlainText('')
        self.ui.treatmentTextEdit.setPlainText('')
        self.operationTreeWidget.clearTreeWidget()
    
    '''Saves current data to self.currentVisitAnimal'''
    def updateCurrentVisitAnimal(self):
        print('VisitTab: updateCurrentVisitAnimal')
        if self.currentVisitAnimal != None:
            self.currentVisitAnimal.update(self.getVisitAnimalData())

    def getVisitAnimalData(self):
        print('VisitTab: getVisitAnimalData')
        data = []    
        data.append(self.ui.amanuensisTextEdit.toPlainText())
        data.append(self.ui.statusTextEdit.toPlainText())
        data.append(self.ui.diagnosisTextEdit.toPlainText())
        data.append(self.ui.treatmentTextEdit.toPlainText())
        self.updateCurerentOperation()
        data.append(self.operationTreeWidget.getItemsFromList())
        #self.clearOperationRelated()
        self.disableOperationRelated(True)
        return data
    
    def setVisitAnimalData(self,visitanimal):
        self.ui.animalNameLabel.setText(visitanimal.animal.name)
        self.ui.amanuensisTextEdit.setPlainText(visitanimal.anamnesis)
        self.ui.statusTextEdit.setPlainText(visitanimal.status)
        self.ui.diagnosisTextEdit.setPlainText(visitanimal.diagnosis)
        self.ui.treatmentTextEdit.setPlainText(visitanimal.treatment)
        self.operationTreeWidget.setItems(visitanimal.operations)
    
    def ownerSet(self):
        if self.item == None:
            self.item = self.makeItem()
            self.session.add(self.item)
            self.disableAnimalTree(False)
            
    def disableAnimalTree(self, state):
        self.animalTreeWidget.setDisabled(state)
        if state:
            self.disableAnimalRelated(state)
    
    def disableAnimalRelated(self, state):
        self.ui.amamnesisLabel.setDisabled(state)
        self.ui.amanuensisTextEdit.setDisabled(state)
        self.ui.statusLabel.setDisabled(state)
        self.ui.statusTextEdit.setDisabled(state)
        self.ui.diagnosisLabel.setDisabled(state)
        self.ui.diagnosisTextEdit.setDisabled(state)
        self.ui.threatmentLabel.setDisabled(state)
        self.ui.treatmentTextEdit.setDisabled(state)
        self.operationTreeWidget.setDisabled(state)
        if state:
            self.disableOperationRelated(state)
    
    def disableOperationRelated(self, state):
        self.ui.operationNameLabel.setDisabled(state)
        self.ui.priceLabel.setDisabled(state)
        self.ui.priceSpinBox.setDisabled(state)
        self.ui.retailPriceLabel.setDisabled(state)
        self.ui.retailPriceLabel_2.setDisabled(state)
        self.ui.descriptionLabel.setDisabled(state)
        self.ui.descriptionTextEdit.setDisabled(state)
        self.ui.stackedWidget.setDisabled(state)
            
    '''-------------OVERLOADED FUNCTIONS-----------------'''
    def getType(self=None):
        return 'Visit'
    
    def getName(self=None):
        return 'Käynti'
    
   
    def getData(self):
        data = []
        data.append(self.qdateToPy(self.ui.startTimeEdit.dateTime()))#start_time
        data.append(self.ownerserachline.getCurrentItem())#owner
        data.append(self.ui.vetComboBox.itemData(self.ui.vetComboBox.currentIndex()))#vet
        data.append(self.qdateToPy(self.ui.endTimeEdit.dateTime()) if self.item != None and self.item.end_time != None else datetime.datetime.now())#end_time
        self.updateCurrentVisitAnimal()
        data.append(self.animalTreeWidget.getItemsFromList())#visitAnimals
        print(data)
        return data

    def makeItem(self):
        data = self.getData()
        self.item = SqlHandler.Visit(data[0], data[1], data[2])        
        return self.item

    def saveAble(self): 
        if self.ownerserachline.getCurrentItem() != None:
            return True
        else:
            return False

    ''' If owner is not set then ignore all else changed is True'''
    def hasChanged(self):
        if self.ownerserachline.getCurrentItem() != None:
            return True
        else:
            return False
     
    def getMessageBoxText(self):
        return 'Haluatko tallentaa käyntiin tehdyt muutokset?'
    