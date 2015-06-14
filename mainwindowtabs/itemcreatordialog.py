#!/usr/bin/python
# -*- coding: utf-8
'''
Created on Apr 16, 2013

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
from PyQt4.QtGui import QDialog,QMessageBox, QWidget
from mainwindowtabs.generictreewidget import GenericTreeWidget, ButtonType
from mainwindowtabs.addNewDialog import AddNewSpecie
from uipy.ui_itemcreator import Ui_ItemCreatorDialog
from uipy.ui_ownerdescription import Ui_OwnerDescriptionDialog

from models.translationtables import g_operationbase_to_item_translation_dict

from models import SqlHandler
import datetime

class OwnerDescriptionDialog(QDialog):
    def __init__(self, parent, item=None):
        QDialog.__init__(self,parent=parent)
        self.ui = Ui_OwnerDescriptionDialog()
        self.ui.setupUi(self)
        self.item = item
        self.session = SqlHandler.newSession()
        
        self.configureConnections()
        self.setBasicInfo()
    
    def configureConnections(self):
        self.ui.saveButton.clicked.connect(self.saveDialog)
        self.ui.canselButton.clicked.connect(self.closeDialog)
        self.ui.newbutton.clicked.connect(self.openSpecieDialog)
    
    def setBasicInfo(self):
        if self.item != None:
            self.setSpecie(self.item.specie.name)
            self.ui.plainTextEdit.setPlainText(self.item.text)
        else:
            self.setSpecie()
    
    def setSpecie(self, newName=''):   
        self.ui.specieComboBox.clear()
        self.ui.specieComboBox.addItem('', None)
        
        for specie in SqlHandler.searchSpecie(self.session):
            self.ui.specieComboBox.addItem(specie.name, specie)
        
        if len(newName):
            self.ui.specieComboBox.setCurrentIndex(self.ui.specieComboBox.findText(newName))
    
    def openSpecieDialog(self):
        dialog = AddNewSpecie(parent=self)
        dialog.show()

    def sendItem(self):
        self.parent().addAskedItemNoCopy(self.item)
        
    def closeDialog(self):
        SqlHandler.closeSession(self.session)
        self.setParent(None)
        self.close()
    
    def saveDialog(self):
        if self.saveAble():
            if self.item == None:
                specie = self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex())
                self.item = SqlHandler.ItemDescription(specie, self.ui.plainTextEdit.toPlainText())
            else:
                self.item.specie = self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex())
                self.item.text = self.ui.plainTextEdit.toPlainText()
            self.session.expunge_all()
            self.sendItem()
            self.closeDialog()
    
    def saveAble(self):
        return self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex()) != None


'''----------------------------------------------------------------
self.session.expunge()

----------------------------------------------------------------'''


        

class ItemCreatorDialog(QDialog):
    def __init__(self, parent, item=None):
        QDialog.__init__(self,parent=parent)
        self.ui = Ui_ItemCreatorDialog()
        self.ui.setupUi(self)
        self.session = SqlHandler.newSession()
        
        self.item = item
        if self.item != None:
            self.item = SqlHandler.makeCopy(self.session, self.item)
            self.session.add(self.item)
        
        self.configure()
        self.configureConnections()
        self.setBasicInfo()
        
        self.selectCorrectItem()

        
    def selectCorrectItem(self):
        #find operation creator and select it ui and typeComboBox that has operation list
        try:
            parent_typeComboBox = self.parent().parent().parent().parent().ui.typeComboBox
            operation = parent_typeComboBox.itemData(parent_typeComboBox.currentIndex())

            #set correct item selected
            if operation.__name__ in g_operationbase_to_item_translation_dict:
                self.ui.typeSelectComboBox.setCurrentIndex(self.ui.typeSelectComboBox.findText(
                    g_operationbase_to_item_translation_dict[operation.__name__]))
        except:
            print("ERROR: ItemCreatorDialog->selectCorrectItem(). error to find parent. something is changed in operationbase! FIX ME!")


    def configureConnections(self):
        self.ui.preSetDurationsComboBox.currentIndexChanged['int'].connect(self.updateDays)
        self.ui.typeSelectComboBox.currentIndexChanged['int'].connect(self.typeChanged)
        self.ui.canselButton.clicked.connect(self.closePressed)
        self.ui.saveButton.clicked.connect(self.savePressed)
    
    def configure(self):
        self.customerTreeWidget = GenericTreeWidget(session=self.session,parent=self)
        self.customerTreeWidget.setTitle('Ohjeet omistajalle')
        self.customerTreeWidget.setHeader(headertexts=['id', 'Laji', 'Teksti'],hidecolumns=[0])
        self.customerTreeWidget.setInputMethod(OwnerDescriptionDialog)
        self.customerTreeWidget.setButtons([ButtonType.remove, ButtonType.add])
        self.ui.verticalLayout.addWidget(self.customerTreeWidget)
        
    def setBasicInfo(self):
        self.setTypes()
        self.addPreSetDurations()
        if self.item != None:
            self.ui.typeSelectComboBox.setDisabled(True)
            self.ui.nameEdit.setText(self.item.name)
            self.ui.typeSelectComboBox.setCurrentIndex(self.ui.typeSelectComboBox.findText(self.item.typeName()))
            self.ui.priceSpinBox.setValue(self.item.price)
            self.ui.stockPriceSpinBox.setValue(self.item.stock_price)
            self.ui.BarCodeEdit.setText(self.item.barcode)
            self.ui.plainTextEdit.setPlainText(self.item.description)
            self.customerTreeWidget.setItems(self.item.customer_descriptions)
            if self.item.hasDuration():
                self.setDuration(self.item.duration)
    
    def updateDays(self, index):
        self.ui.daySpinEdit.setValue(self.ui.preSetDurationsComboBox.itemData(index))
    
    def addPreSetDurations(self):   
        values = [('kuukausi',30), ('1/2 vuosi',180), ('1 vuosi',365), 
                       ('2 vuotta',730), ('3 vuotta',1095), ('5 vuotta',1825)] #TODO: take hardcoded values and save then to configServer
        
        for item in values:
            self.ui.preSetDurationsComboBox.addItem(item[0],item[1])
        
        self.ui.preSetDurationsComboBox.setCurrentIndex(0)
    
    def setTypes(self):
        itemCreators = SqlHandler.getItemCreators()
        for item in itemCreators:
            self.ui.typeSelectComboBox.addItem(item.typeName(), item) 
    
    def typeChanged(self, index):
        print("ItemCreator: typeChenged: got item")
        print(self.ui.typeSelectComboBox.itemData(index))    
        
        self.ui.alvLabel.setText(str(self.ui.typeSelectComboBox.itemData(index).getALV()))
        if self.ui.typeSelectComboBox.itemData(index).hasDuration():
            self.ui.durationLabel.setDisabled(False)
            self.ui.preSetDurationsComboBox.setDisabled(False)
            self.ui.daySpinEdit.setDisabled(False)
            self.ui.label_9.setDisabled(False)
            self.ui.label_8.setDisabled(False)
        else:
            self.ui.durationLabel.setDisabled(True)
            self.ui.preSetDurationsComboBox.setDisabled(True)
            self.ui.daySpinEdit.setDisabled(True)
            self.ui.label_9.setDisabled(True)
            self.ui.label_8.setDisabled(True)
    
    def savePressed(self):
        if self.hasChangedAndSaveAble():
            self.saveDialog()
            if self.parent() != None:
                self.parent().addAskedItem(self.item)
            self.closeDialog()
        else:
            self.errorMessage()
    
    def saveDialog(self):
        if self.hasChangedAndSaveAble():
            self.updateItem()
            SqlHandler.addItem(self.session, self.item)
            
           
    def closePressed(self):
        if self.hasChangedAndSaveAble() and self.askuser():
            self.saveDialog()
        self.closeDialog()
    
    def closeDialog(self):
        SqlHandler.closeSession(self.session)
        self.setParent(None)
        self.close()

    '''returns new object or updated old one'''
    def updateItem(self):
        data = {}
        data["name"] = self.ui.nameEdit.text()
        data["price"] = self.ui.priceSpinBox.value()
        data["stock_price"] = self.ui.stockPriceSpinBox.value()
        data["barcode"] = self.ui.BarCodeEdit.text()
        data["description"] = self.ui.plainTextEdit.toPlainText()
        data["customer_descriptions"] = self.customerTreeWidget.getItemsFromList()

        itemCreator = self.ui.typeSelectComboBox.itemData(self.ui.typeSelectComboBox.currentIndex())
        
        if itemCreator.hasDuration():
            data["duration"] = self.getDuration()
        
        if self.item != None:
            self.item.update(data)
        else:
            if itemCreator.hasDuration():
                self.item = itemCreator(name=data["name"], price=data["price"], stock_price=data["stock_price"], barcode=data["barcode"], description=data["description"], duration=data["duration"])
            else:
                self.item = itemCreator(name=data["name"], price=data["price"], stock_price=data["stock_price"], barcode=data["barcode"], description=data["description"])
            self.item.customer_descriptions = data["customer_descriptions"]
       
    def askuser(self):
        reply = QMessageBox.question(self,'Viesti','Haluatko tallentaa muutokset?', QMessageBox.Save, QMessageBox.Discard)
        if reply == QMessageBox.Save:
            return True
        else:
            return False
    
    def hasChangedAndSaveAble(self):
        if len(self.ui.nameEdit.text()) > 0:
            return True
        else:
            return False
    
    def setDuration(self, duration):
        self.ui.daySpinEdit.setValue(duration.days)
    
    def getDuration(self):
        return datetime.timedelta(days=self.ui.daySpinEdit.value())
    
    def errorMessage(self):
        box = QMessageBox()
        box.setText('Tuotetta ei voida tallentaa sillä sen nimeä ei ole asetettu')
        box.exec()         
        