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

from PyQt4.QtGui import QDialog, QDoubleSpinBox,QSizePolicy
from PyQt4.QtCore import Qt
from uipy.ui_popup import Ui_Dialog

from models import SqlHandler

'''
    AddNewDialog (Not Used)
    AddNewSex
    AddNewSpecie
    AddNewRace
    AddNewColor
    
    AddNewPostOffice
    AddNewPostNumber
    
'''
    
class AddNewDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.session = SqlHandler.newSession()
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        
        #save button
        self.ui.saveButton.clicked.connect(self.saveCheck)
        #enter
        self.ui.lineEdit.returnPressed.connect(self.saveCheck)
        self.ui.cancelButton.clicked.connect(self.closeDialog)
    
    def hideComboBox(self):
        self.ui.comboBox.hide()
        self.ui.comboboxLabel.hide()
    
    def setText(self, title, label):
        self.setWindowTitle(title)
        self.ui.newItemlabel.setText(label)
    
    def setSpecie(self):
        for specie in SqlHandler.searchSpecie(self.session):
            self.ui.comboBox.addItem(specie.name, specie)
        
        current = self.ui.comboBox.findText(self.parent().specieName())
        if current > 0:
            self.ui.comboBox.setCurrentIndex(current)
  
    def saveCheck(self):
        if len(self.ui.lineEdit.text()) > 0:
            self.saveNewItem()
        
    def saveNewItem(self):
        pass
    
    def closeDialog(self):
        self.session.close()
        self.setParent(None)
        self.close()

class AddNewWeight(AddNewDialog):
    def __init__(self, parent, item):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi punnitus', 'Uusi punnitus')
        self.ui.lineEdit.hide()
        self.item = item
        self.priceSelector = QDoubleSpinBox(parent=self)
        self.priceSelector.setMaximum(999999)
        self.priceSelector.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        self.ui.horizontalLayout.addWidget(self.priceSelector)
        self.hideComboBox()
    
    def saveCheck(self):
        if self.priceSelector.value() > 0:
            self.saveNewItem()
        
    def saveNewItem(self):
        item = SqlHandler.WeightControl(animal_id = self.item.id, weight=self.priceSelector.value())
        SqlHandler.addItem(self.session, item)
        print('WeightControl saveNweItem, ', item)
        self.parent().addAskedItem(item)
        self.closeDialog()
                
class AddNewSex(AddNewDialog):
    def __init__(self, parent=None):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi sukupuoli', 'Uusi sukupuoli')
        self.hideComboBox()
        
    def saveNewItem(self):
        SqlHandler.addItem(self.session, SqlHandler.Sex(self.ui.lineEdit.text()))
        #Will always be updated
        self.parent().setSex(self.ui.lineEdit.text())
        self.closeDialog()

class AddNewSpecie(AddNewDialog):
    def __init__(self, parent=None):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi laji', 'Uusi laji')
        self.hideComboBox()
        
    def saveNewItem(self):
        SqlHandler.addItem(self.session, SqlHandler.Specie(self.ui.lineEdit.text()))       
        #Will always be updated
        self.parent().setSpecie(self.ui.lineEdit.text())
        self.closeDialog()

class AddNewRace(AddNewDialog):
    def __init__(self, parent=None):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi rotu', 'Uusi Rotu')
        self.setSpecie()
    
    def saveNewItem(self):
        specie = self.ui.comboBox.itemData(self.ui.comboBox.currentIndex())
        if specie != None:
            SqlHandler.addItem(self.session, SqlHandler.Race(self.ui.lineEdit.text(), specie.id))
            if self.parent().specieName() == specie.name:
                self.parent().setRace(self.ui.lineEdit.text())
        self.closeDialog()
    
class AddNewColor(AddNewDialog):
    def __init__(self, parent=None):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi Väri', 'Uusi väri')
        self.setSpecie()
        
    def saveNewItem(self):
        specie = self.ui.comboBox.itemData(self.ui.comboBox.currentIndex())
        if specie != None:
            SqlHandler.addItem(self.session, SqlHandler.Color(self.ui.lineEdit.text(), specie.id))
            if self.parent().specieName() == specie.name:
                self.parent().setColor(self.ui.lineEdit.text())
        self.closeDialog()

'''
    Functions needed from parent
    -setPostOffice()
    -setPostNumber()
    -postOfficeName()
'''
class AddNewPostOffice(AddNewDialog):
    def __init__(self, parent=None):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi postitoimipaikka', 'Postitoimipaikka')
        self.hideComboBox()

    def saveNewItem(self):
        SqlHandler.addItem(self.session, SqlHandler.PostOffice(self.ui.lineEdit.text()))
        #Will always be updated
        self.parent().setPostOffice(self.ui.lineEdit.text())
        self.closeDialog()
          
class AddNewPostNumber(AddNewDialog):
    def __init__(self, parent=None):
        AddNewDialog.__init__(self, parent)
        self.setText('Lisää uusi postinumero', 'Postinumero')
        self.setPostOffice()
    
    def saveNewItem(self):
        postoffice = self.ui.comboBox.itemData(self.ui.comboBox.currentIndex())
        if postoffice != None:
            SqlHandler.addItem(self.session, SqlHandler.PostNumber(postoffice.id,self.ui.lineEdit.text()))
            self.parent().setPostNumber(self.ui.lineEdit.text())
        self.closeDialog()
        
    def setPostOffice(self):
        for postoffice in SqlHandler.searchPostOffice(self.session):
            self.ui.comboBox.addItem(postoffice.name, postoffice)
        
        current = self.ui.comboBox.findText(self.parent().postOfficeName())
        if current > 0:
            self.ui.comboBox.setCurrentIndex(current)
                