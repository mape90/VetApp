'''
Created on Apr 9, 2013

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

from models.vet import Vet, CustomerText, ContactInfo, Phonenumber, Email
from models import SqlHandler
from mainwindowtabs.addNewDialog  import AddNewPostOffice, AddNewPostNumber

from uipy.ui_vettab import Ui_VetTab

class VetTab(GenericTab):
    def __init__(self, parent=None):
        GenericTab.__init__(self, parent=parent)
        self.ui = Ui_VetTab()
        self.ui.setupUi(self)
        
        self.configure()
        
        self.configureConnections()
        
        self.setVets()

        
    def configure(self):
        pass
        
    def configureConnections(self):
        self.ui.addPostOfficeButton.clicked.connect(self.openAddNewPostOffice)
        self.ui.addPostNumberButton.clicked.connect(self.openAddNewPostNumber)

        self.ui.postNumberComboBox.currentIndexChanged['int'].connect(self.updatePostOffice)
        self.ui.postOfficeComboBox.currentIndexChanged['int'].connect(self.updatePostNumber)
        self.ui.comboBox.currentIndexChanged['int'].connect(self.changeVet)
        
        self.ui.saveAndCloseButton.clicked.connect(self.saveAndCloseTab)
        self.ui.saveButton.clicked.connect(self.saveTab)
        self.ui.closeButton.clicked.connect(self.closeTab)
        

    def changeVet(self,index):
        vet = self.ui.comboBox.itemData(index)
        self.item = vet
        self.setBasicInfo(vet)

    def setVets(self):
        self.ui.comboBox.clear()
        self.ui.comboBox.addItem('Uusi', None)
        
        for vet_temp in SqlHandler.searchVet(self.session):
            self.ui.comboBox.addItem(vet_temp.name, vet_temp)

        if self.item != None:
            for index in range(0, self.ui.comboBox.count()):
                if self.ui.comboBox.itemData(index).id == self.item.id:
                    self.ui.comboBox.setCurrentIndex(index)
                    return
        self.ui.comboBox.setCurrentIndex(0)
    
    
    def update(self):
        self.setVets()
        
    def isUnique(self=None):#Can Overload
        return True    
    
    def getType(self=None):
        return 'VetTab'
    
    def setBasicInfo(self, item):
        if item != None:
            self.ui.nameEdit.setText(item.name)
            self.ui.addressEdit.setText(item.address)
            self.setPostOffice(item.post_office.name if item.post_office != None else '')
            self.setPostNumber(item.postnumber.number if item.postnumber != None else '')
            self.ui.y_numberEdit.setText(item.y_number)
            self.ui.vetNumberEdit.setText(item.vet_number)
            self.ui.bankEdit.setText(item.bank_name)
            self.ui.IbanEdit.setText(item.IBAN)
            for text in item.customertexts:
                if text.language == 'Finnish':
                    self.ui.finnishPextEdit.setPlainText(text.text)
                elif text.language == 'English':
                    self.ui.englishTextEdit_3.setPlainText(text.text)
                elif text.language == 'Swedish':
                    self.ui.swedenTextEdit.setPlainText(text.text)
                else:
                    self.errorMessage('Error while loading vet data: Wrong language in customer text!')
                    
        else:
            self.ui.nameEdit.setText('')
            self.ui.addressEdit.setText('')
            self.setPostOffice()
            self.setPostNumber()
            self.ui.y_numberEdit.setText('')
            self.ui.vetNumberEdit.setText('')
            self.ui.bankEdit.setText('')
            self.ui.IbanEdit.setText('')
    
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

    
    def getData(self):
        data = []
        data.append(self.ui.nameEdit.text())
        data.append(self.ui.addressEdit.text())
        data.append(self.ui.postOfficeComboBox.itemData(self.ui.postOfficeComboBox.currentIndex()))
        data.append(self.ui.postNumberComboBox.itemData(self.ui.postNumberComboBox.currentIndex()))
        data.append(self.ui.y_numberEdit.text())
        data.append(self.ui.vetNumberEdit.text())
        data.append(self.ui.bankEdit.text())
        data.append(self.ui.IbanEdit.text())
        data.append("") #TODO implement SWIF
        data.append([self.ui.finnishPextEdit.toPlainText(),
                     self.ui.englishTextEdit_3.toPlainText(),
                     self.ui.swedenTextEdit.toPlainText()])#DO NOT CHANGE THESE ORDER
        data.append([])#TODO: add here contact info
        print("VetTab getData, data len" + str(len(data)))
        return data
    
    def addAskedItem(self, item):#Overload
        pass
    
    def makeItem(self): #Overload
        data = self.getData()
        self.item = Vet(data[0], data[1], data[2], data[3], data[4], 
                        data[5], data[6], data[7], data[8], data[9])
        return self.item
    
    def saveAble(self): #Overload
        if len(self.ui.nameEdit.text()) > 0:
            return True
        else:
            return False
    
    def hasChanged(self): #Overload
        #TODO: implement
        return True
    
    def getMessageBoxText(self): #Overload
        return 'Haluatko tallentaa eläinlääkärin tietoihin tehdyt muutokset?'
    