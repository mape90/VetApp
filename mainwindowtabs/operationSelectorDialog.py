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
from PyQt4.QtGui import QWidget, QPushButton, QComboBox, QMessageBox, QLabel, QHBoxLayout, QVBoxLayout
from mainwindowtabs.searchlineedit import SearchLineEdit
#from models.operation import OperationBase, VaccinationBase, SurgeryBase, MedicationBase
#from models.operation import LamenessBase, XrayBase, UltrasonicBase, EndoscopyBase, DentalexaminationBase
from models import SqlHandler

class OperationSelectorDialog(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self,parent)
        self.resize(280, 150)#Todo: find good values
        
        self.serachlineedit = SearchLineEdit(parent=self, function=None)
        self.setWindowTitle('Operaatiopohja haku')
        
        self.makeComboBox()
        self.makeButtons()
        self.makeLayout()
    
    def makeComboBox(self):
        self.combobox = QComboBox(parent=self)
        self.combobox.addItem('Lääkintä', SqlHandler.searchAnimal)#MedicationBase
        self.combobox.addItem('Rokotus', SqlHandler.searchAnimal)#VaccinationBase
        self.combobox.addItem('Leikkaus', SqlHandler.searchAnimal)#SurgeryBase
        self.combobox.addItem('Ultraäänitutkimus', SqlHandler.searchAnimal)#UltrasonicBase
        self.combobox.addItem('Endoskopointi', SqlHandler.searchAnimal)#EndoscopyBase
        self.combobox.addItem('Ontumatutkimus', SqlHandler.searchAnimal)#LamenessBase
        self.combobox.addItem('Röntkentutkimus', SqlHandler.searchAnimal)#XrayBase
        self.combobox.addItem('Hammastutkimus', SqlHandler.searchAnimal)#DentalexaminationBase
        self.combobox.addItem('Laboratoriotutkimus', SqlHandler.searchAnimal)#OperationBase
        self.combobox.addItem('muu', SqlHandler.searchAnimal)#OperationBase
        
        self.combobox.currentIndexChanged['int'].connect(self.changeSearchLineEditFunction)
        self.combobox.setCurrentIndex(0)
    
    def makeButtons(self):
        self.cancelButton = QPushButton(parent=self, text='Hylkää')
        self.cancelButton.clicked.connect(self.close)
        
        self.okButton = QPushButton(parent=self, text='Valitse')
        self.okButton.clicked.connect(self.okPressed)
    
    
    def makeLayout(self):
        print('makeLayout')
        buttonslayout = QHBoxLayout()
        buttonslayout.addStretch()
        buttonslayout.addWidget(self.cancelButton)
        buttonslayout.addWidget(self.okButton)

        searchLayout = QHBoxLayout()
        searchLayout.addWidget(QLabel(text='Etsi', parent=self))
        searchLayout.addWidget(self.serachlineedit)
        
        selectorlayout = QVBoxLayout()
        selectorlayout.addLayout(searchLayout)
        selectorlayout.addWidget(QLabel(text='Operaation tyyppi', parent=self))
        selectorlayout.addWidget(self.combobox)
        selectorlayout.addStretch()
        
        ownmainlayout = QVBoxLayout()
        ownmainlayout.addLayout(selectorlayout)
        ownmainlayout.addLayout(buttonslayout)
        self.setLayout(ownmainlayout)
        

    def changeSearchLineEditFunction(self, index):
        self.serachlineedit.function = self.combobox.itemData(index)
    
    def okPressed(self):
        item = self.serachlineedit.getCurrentItem()
        if item != None:
            self.parent().addAskedItem(item)
            self.close()
        else:
            box = QMessageBox()
            box.setText('Valitse operaatio')
            box.exec()
        
        
        
        