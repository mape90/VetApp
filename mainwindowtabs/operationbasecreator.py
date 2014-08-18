#!/usr/bin/python
# -*- coding: utf-8
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
from PyQt4.QtGui import QDialog, QMessageBox
from models import SqlHandler
from uipy.ui_operationcreator import Ui_OperationCreator
from mainwindowtabs.generictreewidget import GenericTreeWidget, ButtonType, ItemTreeWidget
from mainwindowtabs.searchlineedit import SearchLineEdit
from mainwindowtabs.itemcreatordialog import ItemCreatorDialog
import inspect
from datetime import timedelta

class OperationBaseCreator(QDialog):
    def __init__(self, parent=None, item=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_OperationCreator()
        self.ui.setupUi(self)
        self.session = SqlHandler.newSession()
        if item != None:
            self.item = SqlHandler.makeCopy(self.session, self.item)
        else:
            self.item = None


        from models.operation import SurgeryBaseItem
        self.itemTreeWidget =  ItemTreeWidget(session = self.session, parent=self, creator=SurgeryBaseItem)
        self.itemTreeWidget.setTitle("Leikkauksen tavarat")
        self.ui.itemPageLayout.addWidget(self.itemTreeWidget)
        
        self.itemSearchEdit = SearchLineEdit(tabcreator=ItemCreatorDialog, session=self.session, 
                                             parent=self, function=SqlHandler.searchItem)
        
        self.ui.searchLineEditLayout.insertWidget(0,self.itemSearchEdit)
        self.configureConnections()
        self.setBasicInfo()
    
    def configureConnections(self):
        self.ui.typeComboBox.currentIndexChanged['int'].connect(self.setSpecialInfo)
        self.ui.closeButton.clicked.connect(self.closeCreator)
        self.ui.saveButton.clicked.connect(self.saveCreator)
        self.ui.resitCheckBox.stateChanged.connect(self.showHideResistRelative)
        self.ui.getFromMedicineButton.clicked.connect(self.getMedicineDuration)
        self.ui.editmedicine.clicked.connect(self.openCurrentMedicine)
    
    def openCurrentMedicine(self):
        current_item = self.itemSearchEdit.getCurrentItem()
        if current_item != None:
            creator = ItemCreatorDialog(parent=self.itemSearchEdit,item=current_item)
            creator.show()
        else:
            self.errorMessage('Lääkettä ei ole valittu!')
        
    def getMedicineDuration(self):
        current_item = self.itemSearchEdit.getCurrentItem()
        if current_item != None:
            if current_item.getType() == 'Vaccine':
                self.ui.durationspinBox.setValue(current_item.duration.days if current_item.duration != None else 0)
            else:
                self.errorMessage('Valittu tuote ei ole lääke!')

        else:
            self.errorMessage('Lääkettä ei ole valittu!')
        
    def showHideResistRelative(self, state):
        self.ui.label_6.setEnabled(True if state>0 else False)
        self.ui.durationspinBox.setEnabled(True if state>0 else False)
        self.ui.label_8.setEnabled(True if state>0 else False)
        self.ui.getFromMedicineButton.setEnabled(True if state>0 else False)
    
    def closeCreator(self):
        self.session.close()
        self.setParent(None)
        self.close()
    
    def saveCreator(self):
        if len(self.ui.nameEdit.text()) > 0:
            self.updateItem()
            if not self.item is self.session:
                self.session.add(self.item)
            self.session.commit()
            self.parent().addAskedItem(self.item)
            self.closeCreator()
        else:
            self.errorMessage('Operaatiopohjaa ei voida tallentaa sillä sen nimeä ei ole asetettu.')
                
            
    def updateItem(self):
        functio = self.ui.typeComboBox.itemData(self.ui.typeComboBox.currentIndex())
        args = inspect.getargspec(functio.__init__).args
        name = self.ui.nameEdit.text()
        price = self.ui.priceSpinBox.value()
        description = self.ui.descriptionTextEdit.toPlainText()
        duration = timedelta(self.ui.durationspinBox.value())
        need_resit = self.ui.resitCheckBox.isChecked()
        item = self.itemSearchEdit.getCurrentItem()
        if self.item == None:
            if 'need_resit' in args:
                self.item = functio(name, price, description, duration, need_resit, item)
            elif 'item' in args:
                self.item = functio(name, price, description, item)
            elif 'items' in args:
                self.item = functio(name, price, description, self.itemTreeWidget.getItemsFromList())
            else:
                self.item = functio(name, price, description)
        else:
            if 'need_resit' in args:
                self.item.update([name, price, description, duration, need_resit, item])
            elif 'item' in args:
                self.item.update([name, price, description, item])
            elif 'items' in args:
                self.item([name, price, description, self.itemTreeWidget.getItemsFromList()])
            else:
                self.item.update([name, price, description])

    
    def setBasicInfo(self):
        self.setTypes()
        if self.item != None:
            self.ui.typeComboBox.setCurrentIndex(self.ui.typeComboBox.findText(self.item.getName()))
            self.ui.typeComboBox.setDisabled(True)
            #TODO: add items to their places
    
    def setTypes(self):
        from models.operation import OperationBase,VaccinationBase,SurgeryBase,MedicationBase,LabBase,LamenessBase,XrayBase,UltrasonicBase,EndoscopyBase,DentalexaminationBase
        for item in [OperationBase,VaccinationBase,SurgeryBase,MedicationBase,LabBase,LamenessBase,XrayBase,UltrasonicBase,EndoscopyBase,DentalexaminationBase]:
            self.ui.typeComboBox.addItem(item.getName(item), item)


    def setSpecialInfo(self, index):
        from models.operation import VaccinationBase, MedicationBase, SurgeryBase

        operationType = self.ui.typeComboBox.itemData(index).__name__ #get baseObject name
        if operationType is VaccinationBase.__name__:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.vaccinePage))
            self.ui.resitCheckBox.setDisabled(False)
            self.ui.durationspinBox.setDisabled(False)

        elif operationType is MedicationBase.__name__:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.vaccinePage))
            self.ui.resitCheckBox.setDisabled(True)
            self.ui.durationspinBox.setDisabled(True)
            
        elif operationType is SurgeryBase.__name__:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.itemPage))

        else:
            self.ui.stackedWidget.setCurrentIndex(self.ui.stackedWidget.indexOf(self.ui.emptyPage))
            
    def errorMessage(self,msg):
        box = QMessageBox()
        box.setText(msg)
        box.exec()         
        