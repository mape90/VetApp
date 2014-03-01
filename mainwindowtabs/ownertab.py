#!/usr/bin/python
# -*- coding: utf-8

'''
NOT VALID
    OwnerTab(GenericTab)
    Variables:
    -ui        (GUI objects)
    -session   (sql session)
    -item     (Owner)
    
    FUNCTIONS:
    -None     <- setBasicInfo()
    -None     <- createConnections()
    
    -bool     <- canCloseTab()
    -bool     <- isUnique()
    -string   <- getType()
    -None     <- getItem()
    -string   <- postOfficeName()
    
    SLOTS:
    -None     <- updatePostNumber()
    -None     <- updatePostOffice()
    -None     <- openAddNewPostOffice()
    -None     <- openAddNewPostNumber()
    
    HELPER FUNCTIONS
    -string   <- animalText(animal)
    
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

from PyQt4.QtGui import QPushButton
from uipy.ui_ownertab import Ui_OwnerTab
from mainwindowtabs.addNewDialog  import AddNewPostOffice, AddNewPostNumber
from mainwindowtabs.generictab import GenericTab
from models import SqlHandler
from models.owner import Owner
from mainwindowtabs import Tabmanager



from mainwindowtabs.generictreewidget import GenericTreeWidget, ButtonType


class OwnerTab(GenericTab):
    def __init__(self, parent=None, item=None):
        GenericTab.__init__(self, parent=parent, item=item)
        self.ui = Ui_OwnerTab()
        self.ui.setupUi(self)
        self.configure()
        self.createConnections()
        self.setBasicInfo()
        self.setSpecialInfo()
    
    def configure(self):
        self.animalTreeWidget = GenericTreeWidget(session=self.session, parent=self)
        self.animalTreeWidget.setTitle('Eläimet')
        self.animalTreeWidget.setHeader(headertexts=['id', 'Nimi', 'Virallinen nimi', 'Laji', 'Rotu'], iconplace=1, hidecolumns=[0])
        self.animalTreeWidget.setButtons([ButtonType.add,ButtonType.open])
        
        from mainwindowtabs.animaltab import AnimalTab
        self.animalTreeWidget.setInputMethod(tabcreator=AnimalTab, autoAdd=True, function=SqlHandler.searchAnimal)
        self.animalTreeWidget.setMaximumWidth(500)
        self.ui.animalvisitLayout.addWidget(self.animalTreeWidget)
    
        self.visitTreeWidget = GenericTreeWidget(session=self.session, parent=self)
        self.visitTreeWidget.setTitle('Viimeisimmät käynnit')
        self.visitTreeWidget.setHeader(headertexts=['id', 'Aika'],hidecolumns=[0])
        self.visitTreeWidget.setButtons([ButtonType.open])
        button = QPushButton(parent=self.visitTreeWidget, text='Uusi käynti')
        button.clicked.connect(self.openNewVisit)
        self.visitTreeWidget.ui.topLayout.insertWidget(2, button)
        
        self.visitTreeWidget.setMaximumWidth(500)
        self.ui.animalvisitLayout.addWidget(self.visitTreeWidget)
    
    def openNewVisit(self):
        from mainwindowtabs.visittab import VisitTab
        Tabmanager.openTab(tabCreator=VisitTab, returnTab=self)
        
    def createConnections(self):
        self.ui.addPostOfficeButton.clicked.connect(self.openAddNewPostOffice)
        self.ui.addPostNumberButton.clicked.connect(self.openAddNewPostNumber)
        self.ui.postNumberComboBox.currentIndexChanged['int'].connect(self.updatePostOffice) 
        self.ui.postOfficeComboBox.currentIndexChanged['int'].connect(self.updatePostNumber)
        
        self.ui.saveButton.clicked.connect(self.saveTab)
        self.ui.saveAndExitButton.clicked.connect(self.saveAndCloseTab)
        self.ui.canselButton.clicked.connect(self.closeTab)
  
    
    def setSpecialInfo(self):
        if self.item != None:
            self.animalTreeWidget.setItems(self.item.animals)
  
    def setBasicInfo(self):
        if self.item != None:
            self.ui.nameEdit.setText(self.item.name)
            self.ui.addressEdit.setText(self.item.address)
            self.ui.phonenumberEdit.setText(self.item.phonenumber)
            self.ui.emailEdit.setText(self.item.email)
            self.ui.otherInfoEdit.setPlainText(self.item.other_info)
                        
            self.setPostOffice(newName=self.item.post_office.name if self.item.post_office != None else '')
            self.ui.postNumberComboBox.setCurrentIndex(self.ui.postNumberComboBox.findText(self.item.postnumber.number if self.item.postnumber != None else ''))
            
        else:
            self.setPostOffice()
            self.setPostNumber()
    
    def postOfficeName(self):
        postoffice = self.ui.postOfficeComboBox.itemData(self.ui.postOfficeComboBox.currentIndex())
        if not not postoffice:
            return postoffice.name
        else:
            return ''
    
    def postOffice(self):
        return self.ui.postOfficeComboBox.itemData(self.ui.postOfficeComboBox.currentIndex())
    
    def postNumber(self):
        return self.ui.postNumberComboBox.itemData(self.ui.postNumberComboBox.currentIndex())

    
    '''-----------OWN SLOTS------------------'''   
   
    def openAddNewPostOffice(self):
        dialog = AddNewPostOffice(parent=self)
        dialog.show()
        
    def openAddNewPostNumber(self):
        dialog = AddNewPostNumber(parent=self)
        dialog.show()
     
    def updatePostNumber(self, index):
        postoffice = self.postOffice()
        if postoffice == None:
            self.setPostNumber()
        elif self.postNumber() != None and self.postNumber().post_office_id == postoffice.id:
            self.ui.postOfficeComboBox.setCurrentIndex(self.ui.postOfficeComboBox.findText(postoffice.name))    
        else:
            self.setPostNumber()

    def updatePostOffice(self, index):
        postNumber = self.ui.postNumberComboBox.itemData(index)
        if postNumber != None and self.postOffice() == None:
            self.ui.postOfficeComboBox.setCurrentIndex(self.ui.postOfficeComboBox.findText(postNumber.post_office.name))
            self.setPostNumber(postNumber.number)
          
    def setPostOffice(self, newName=''):
        self.ui.postOfficeComboBox.clear()
        self.ui.postOfficeComboBox.addItem('', None)
        
        for postOffice in SqlHandler.searchPostOffice(self.session):
            
            self.ui.postOfficeComboBox.addItem(postOffice.name, postOffice)
        
        if newName != None and len(newName) > 0:
            self.ui.postOfficeComboBox.setCurrentIndex(self.ui.postOfficeComboBox.findText(newName))
     
    def setPostNumber(self, newName=''):
        self.ui.postNumberComboBox.clear()
        self.ui.postNumberComboBox.addItem('', None)
        
        for postNumber in SqlHandler.searchPostNumber(self.session, postOffice=self.postOffice()):
            self.ui.postNumberComboBox.addItem(postNumber.number, postNumber)
        
        if newName != None and len(newName) > 0:
            self.ui.postNumberComboBox.setCurrentIndex(self.ui.postNumberComboBox.findText(newName))
    
    '''-----------OVERLOADED FUNCTIONS-----------'''
    def getType(self=None):
        return 'Owner'   
    
    def getName(self=None):
        return 'Omistaja' 

    def getData(self):
        data = []
        data.append(self.ui.nameEdit.text())
        data.append(self.ui.addressEdit.text())
        
        postOffice = self.ui.postOfficeComboBox.itemData(self.ui.postOfficeComboBox.currentIndex())
        postNumber = self.ui.postNumberComboBox.itemData(self.ui.postNumberComboBox.currentIndex())
        
        data.append(postOffice.id if postOffice != None else None)
        data.append(postNumber.id if postNumber != None else None)
        
        data.append(self.ui.emailEdit.text())
        data.append(self.ui.phonenumberEdit.text())
        data.append(self.ui.otherInfoEdit.toPlainText())
        data.append(0) #TODO implement Flags
        data.append(self.animalTreeWidget.getItemsFromList())
        return data
    
    def addAskedItem(self, item): #TODO: Implement
        print('AddAskedItem-------------------------------TODO implement')
    
    def makeItem(self):
        data = self.getData()
        return Owner(data[0], data[1], data[2], data[3], 
                     data[4], data[5], data[6], data[7], data[8])
    
    def saveAble(self):
        #print('Owner FUNCTION saveAble')
        return len(self.ui.nameEdit.text()) > 0
    
    def hasChanged(self):
        #print('--------hasChanged---------')
        if self.item != None:
            post_office = self.ui.postOfficeComboBox.itemData(self.ui.postOfficeComboBox.currentIndex())
            post_number = self.ui.postNumberComboBox.itemData(self.ui.postNumberComboBox.currentIndex())
            if self.ui.nameEdit.text() != self.item.name:
                return True
            elif self.ui.addressEdit.text() != self.item.address:
                return True
            elif (post_office.id if post_office != None else None) != self.item.post_office_id:
                return True
            elif (post_number.id if post_number != None else None) != self.item.postnumber_id:
                return True
            elif self.ui.emailEdit.text() != self.item.email:
                return True
            elif self.ui.phonenumberEdit.text() != self.item.phonenumber:
                return True
            elif self.ui.otherInfoEdit.toPlainText() != self.item.other_info:
                return True
            else:
                return False
        else:
            #print('self.item == None')
            if (self.ui.nameEdit.text() != ''or 
            self.ui.addressEdit.text() != '' or
            self.ui.postOfficeComboBox.itemData(self.ui.postOfficeComboBox.currentIndex()) != None or
            self.ui.postNumberComboBox.itemData(self.ui.postNumberComboBox.currentIndex()) != None or
            self.ui.emailEdit.text() != '' or
            self.ui.phonenumberEdit.text() != '' or
            self.ui.otherInfoEdit.toPlainText() != ''):
            #TODO implement Flags
                return True
            else:
                return False
    
    def getMessageBoxText(self):
        return 'Haluatko tallentaa omistajaan tehdyt muutokset?'
    
    
    