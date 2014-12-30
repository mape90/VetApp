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
    TODO: check that close will rollback databases

    AnimalTab(GenericTab)
    Variables:
    -ui        (GUI objects)
    -session   (sql session)
    -item      (Animal)
    
    FUNCTIONS:
    -None     <- setBasicInfo()
    -None     <- createConnections()
    
    -None     <- getBasicInfo()
    
    -string   <- specieName()
    -specie   <- specie()
        
    -bool     <- canCloseTab()
    -string   <- getType()
    -None     <- getItem()
    -string   <- postOfficeName()
    
    SLOTS:
    -None     <- openRaceDialog()
    -None     <- openSpecieDialog()
    -None     <- openSexDialog()
    -None     <- openColorDialog()
    -None     <- setSpecie()
    -None     <- setSex()
    -None     <- setRace()
    -None     <- setColor()
    -None     <- updateSpecieRelated()
    
'''

from mainwindowtabs.generictab import GenericTab
from mainwindowtabs.generictreewidget import GenericTreeWidget, ButtonType, PhoneRecipieTreeWidget, PhoneRecipieDialog

from uipy.ui_animaltab import Ui_Animal
from mainwindowtabs.addNewDialog import AddNewWeight, AddNewRace, AddNewSex, AddNewSpecie, AddNewColor
from mainwindowtabs import Tabmanager
from models import SqlHandler
from models.animal import Animal
from datetime import datetime

from PyQt4.QtGui import QDialog, QHBoxLayout

class AnimalTab(GenericTab):
    def __init__(self, parent=None, item=None):
        GenericTab.__init__(self, parent=parent, item=item)
        self.ui = Ui_Animal()
        self.ui.setupUi(self)
        self.configure()
        self.createConnections()
        self.setBasicInfo()
        

    def configure(self):
        self.labTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=None)
        self.labTreeWidget.setTitle('Laboratorio tulokset')
        self.labTreeWidget.setHeader(headertexts=['id','Nimi', "Tyyppi"], iconplace=-1, iconsize=None, hidecolumns=[0])
        self.labTreeWidget.setButtons([ButtonType.open])
        self.ui.labLayout.addWidget(self.labTreeWidget)

        self.medicineTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=None)
        self.medicineTreeWidget.setTitle('Viimeisimmät lääkkeet')
        self.medicineTreeWidget.setHeader(headertexts=['id', 'Nimi', 'Annettu', 'Päättyy'], hidecolumns=[0])
        self.ui.medicineLayout.addWidget(self.medicineTreeWidget)        
        
        self.visitTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=None)
        self.visitTreeWidget.setTitle('Viimeisimmät käynnit')
        self.visitTreeWidget.setHeader(headertexts=['id','Aika'], hidecolumns=[0])
        self.visitTreeWidget.setButtons([ButtonType.open])
        self.ui.gridLayout.addWidget(self.visitTreeWidget,0,0)
        
        self.examinationTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=None)
        self.examinationTreeWidget.setTitle('Viimeisimmät toimenpiteet')
        self.examinationTreeWidget.setHeader(headertexts=['id', 'Nimi', 'Tehty', 'Tyyppi'], hidecolumns=[0])
        self.examinationTreeWidget.setButtons([ButtonType.open])
        self.ui.gridLayout.addWidget(self.examinationTreeWidget,0,1)
        
        self.vaccineTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=None)
        self.vaccineTreeWidget.setTitle('Viimeisimmät rokotukset')
        self.vaccineTreeWidget.setHeader(headertexts=['id', 'Nimi', 'Annettu', 'Päättyy'], hidecolumns=[0])
        self.ui.vaccineLayout.addWidget(self.vaccineTreeWidget)
        
        self.weightcontrolTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=SqlHandler.searchAnimalWeights)
        self.weightcontrolTreeWidget.setPermanentRemove()
        self.weightcontrolTreeWidget.setTitle('Painon seuranta')
        self.weightcontrolTreeWidget.setHeader(headertexts=['id', 'Aika', 'Paino'], hidecolumns=[0])
        self.weightcontrolTreeWidget.setButtons([ButtonType.add, ButtonType.remove])
        
        self.ui.weigthcontrolLayout.addWidget(self.weightcontrolTreeWidget)
        
        self.pictureTreeWidget = GenericTreeWidget(parent=self, session=self.session, updateFunctio=None)
        self.pictureTreeWidget.setTitle('Eläimen kuvat')
        self.pictureTreeWidget.setHeader(headertexts=['id','Selitys'], iconplace=1, hidecolumns=[0])
        self.pictureTreeWidget.setButtons([ButtonType.open])
        self.ui.pictureLayout.addWidget(self.pictureTreeWidget)
        
        self.phonerecipieTreeWidget = PhoneRecipieTreeWidget(parent=self, session=self.session)
        self.ui.phoneLayout.addWidget(self.phonerecipieTreeWidget)
   
    def initializeParameters(self):
        if self.item != None:
            self.labTreeWidget.setParameters([self.item])
            self.medicineTreeWidget.setParameters([self.item])
            self.visitTreeWidget.setParameters([self.item])
            self.examinationTreeWidget.setParameters([self.item])
            self.vaccineTreeWidget.setParameters([self.item])
            self.weightcontrolTreeWidget.setParameters([self.item])
            self.weightcontrolTreeWidget.dialogitem = self.item
            self.weightcontrolTreeWidget.setInputMethod(AddNewWeight)
            self.pictureTreeWidget.setParameters([self.item])
            self.phonerecipieTreeWidget.setParameters([self.item])
            self.phonerecipieTreeWidget.dialogitem = self.item
            self.phonerecipieTreeWidget.setInputMethod(PhoneRecipieDialog)
        else:
            print('ERROR: AnimalTab: initializeParameters: self.item was not set')
   
    def updateListItems(self):
        if self.item != None:
            self.weightcontrolTreeWidget.update()
            self.visitTreeWidget.update()
            self.examinationTreeWidget.update()
            self.medicineTreeWidget.update()
            self.labTreeWidget.update()
            self.phonerecipieTreeWidget.update()
            self.vaccineTreeWidget.update()
            self.pictureTreeWidget.update()
        
    '''
        setBasicInfo
        
        Description:
            Sets item basic infos to their lines.
            i.e item.name is set to nameLineEdit
        
        Input:
            self
        Output:
            None
    '''
    def setBasicInfo(self):
        #print('AnimalTab FUNCTIO: SetBasicInfo')
        if self.item != None:
            self.ui.nameLineEdit.setText(self.item.name)
            self.ui.officialNamelineEdit.setText(self.item.official_name)
            self.ui.birthdayEdit.setDate(self.item.birthday)
            self.ui.microLineEdit.setText(self.item.micro_num)
            self.ui.recNumlineEdit.setText(self.item.rec_num)
            self.ui.tattooLineEdit.setText(self.item.tattoo)
            self.ui.passportLineEdit.setText(self.item.passport)
            self.ui.insuranceEdit.setPlainText(self.item.insurance)
            self.ui.otherInfoTextEdit.setPlainText(self.item.other_info)
            
            if self.item.death_day != None:
                self.ui.deathcheckBox.setChecked(True)
                self.ui.dateEdit.setDate(self.item.death_day)
            if self.item.flags != None:
                self.ui.statusCheckBox.setChecked(True)
            
            #check that specie is set
            if self.item.specie_id != None and self.item.specie_id > 0:
                self.setSpecie(self.item.specie.name)
            
            if self.item.sex_id != None and self.item.sex_id > 0:
                self.setSex(self.item.sex.name)
            
            self.initializeParameters()
            self.updateListItems()
        else:
            self.setSpecie()
            self.setSex()

    def createConnections(self):
        self.ui.specieComboBox.currentIndexChanged['int'].connect(self.updateSpecieRelated)
        
        self.ui.newRaceButton.clicked.connect(self.openRaceDialog)
        self.ui.newSpecieButton.clicked.connect(self.openSpecieDialog)
        self.ui.newSexButton.clicked.connect(self.openSexDialog)
        self.ui.newColorButton.clicked.connect(self.openColorDialog)
        
        self.ui.saveButton.clicked.connect(self.saveAnimalTab)
        self.ui.saveAndExitButton.clicked.connect(self.saveAndCloseTab)
        self.ui.canselButton.clicked.connect(self.closeTab)
        self.ui.searchOwnersButton.clicked.connect(self.openOwners)
    
        self.ui.deathcheckBox.stateChanged.connect(self.changeDeathDateEdit)
    
    def saveAnimalTab(self):
        self.saveTab()
        self.weightcontrolTreeWidget.setParameters([self.item])
        self.weightcontrolTreeWidget.setInputMethod(AddNewWeight)
    
    def changeDeathDateEdit(self,state):
        self.ui.dateEdit.setDisabled(not state)
        if state:
            self.ui.dateEdit.setDate(datetime.today().date())
    
    def openOwners(self):
        if self.item != None:
            dialog = QDialog(self)
            owners = GenericTreeWidget(parent=dialog, session=self.session, updateFunctio=SqlHandler.searchAnimalOwners)
            owners.setTitle('Omistajat')
            owners.setButtons([ButtonType.open])
            owners.setHeader(headertexts=['id', 'Nimi'], hidecolumns=[0])
            owners.setParameters([self.item.id])
            from mainwindowtabs.ownertab import OwnerTab
            owners.setInputMethod(tabcreator=OwnerTab, searchEnabled=False)
            owners.openButton.clicked.connect(dialog.close)
            owners.update()
            layout = QHBoxLayout()
            layout.addWidget(owners)
            dialog.setLayout(layout)
            dialog.show()
    
    def specieName(self):
        specie = self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex())
        if specie != None:
            return specie.name
        else:
            return ''
        
    def specie(self):
        return self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex())
    

    '''----------OWN SLOTS----------------'''
    
    def openRaceDialog(self):
        dialog = AddNewRace(parent=self)
        dialog.show()
    
    def openSpecieDialog(self):
        dialog = AddNewSpecie(parent=self)
        dialog.show()
    
    def openSexDialog(self):
        dialog = AddNewSex( parent=self)
        dialog.show()
    
    def openColorDialog(self):
        dialog = AddNewColor( parent=self)
        dialog.show()
         
    def setSpecie(self, newName=''):   
        self.ui.specieComboBox.clear()
        self.ui.specieComboBox.addItem('', None)
        
        for specie in SqlHandler.searchSpecie(self.session):
            self.ui.specieComboBox.addItem(specie.name, specie)
        
        if len(newName):
            self.ui.specieComboBox.setCurrentIndex(self.ui.specieComboBox.findText(newName))
    
    def setSex(self, newName=''):
        self.ui.sexComboBox.clear()
        self.ui.sexComboBox.addItem('', None)
        
        for sex in SqlHandler.searchSex(self.session):
            self.ui.sexComboBox.addItem(sex.name, sex)
        
        if newName != '':
            self.ui.sexComboBox.setCurrentIndex(self.ui.sexComboBox.findText(newName))
    
    def setColor(self, newName=''):
        self.ui.colorComboBox.clear()
        self.ui.colorComboBox.addItem('', None)

        specie = self.specie()
        if specie != None:
            for color in SqlHandler.searchColor(self.session, specie.id):
                self.ui.colorComboBox.addItem(color.name, color)
            if len(newName):
                self.ui.colorComboBox.setCurrentIndex(self.ui.colorComboBox.findText(newName))
    
    def setRace(self, newName=''):
        self.ui.raceComboBox.clear()
        self.ui.raceComboBox.addItem('', None)
        
        specie = self.specie()
        if specie != None:
            for race in SqlHandler.searchRace(self.session, specie.id):
                self.ui.raceComboBox.addItem(race.name, race)
            if len(newName):
                self.ui.raceComboBox.setCurrentIndex(self.ui.raceComboBox.findText(newName))
        
    def updateSpecieRelated(self, index):
        self.ui.raceComboBox.clear()
        self.ui.colorComboBox.clear()
        specie = self.ui.specieComboBox.itemData(index)
        
        #check that specie is valid
        if not not specie:
            if self.item != None and self.item.specie != None and self.item.specie.name == specie.name:
                if self.item.race != None:
                    self.setRace(self.item.race.name)
                if self.item.color != None:
                    self.setColor(self.item.color.name)
            else:
                self.setRace()
                self.setColor()
      
    '''---------OWERLOADED FUNCTIONS-----------'''          

    def getData(self):
        #print('AnimalTab FUNCTIO: getData')
        data = []
        data.append(self.ui.nameLineEdit.text())
        data.append(self.ui.officialNamelineEdit.text())
        
        race = self.ui.raceComboBox.itemData(self.ui.raceComboBox.currentIndex())
        specie = self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex())
        sex = self.ui.sexComboBox.itemData(self.ui.sexComboBox.currentIndex())
        color = self.ui.colorComboBox.itemData(self.ui.colorComboBox.currentIndex())
        
        data.append(race.id if race != None else None)
        data.append(specie.id if specie != None else None)
        data.append(sex.id if sex != None else None)
        data.append(color.id if color != None else None)
        
        data.append(self.qdateToPy(self.ui.birthdayEdit.date()))
        data.append(self.ui.microLineEdit.text())
        data.append(self.ui.recNumlineEdit.text())
        data.append(self.ui.tattooLineEdit.text())
        data.append(self.ui.insuranceEdit.toPlainText())
        data.append(self.ui.passportLineEdit.text())
        data.append(self.ui.otherInfoTextEdit.toPlainText())
        
        if self.ui.deathcheckBox.isChecked():
            data.append(self.ui.dateEdit.date().toPyDate())
        else:
            data.append(None)
        
        if self.ui.statusCheckBox.isChecked():
            data.append(1)
        else:
            data.append(None)
        
        return data

    def hasChanged(self):
        #print('AnimalTab FUNCTIO: hasChanged')
        race = self.ui.raceComboBox.itemData(self.ui.raceComboBox.currentIndex())
        specie = self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex())
        sex = self.ui.sexComboBox.itemData(self.ui.sexComboBox.currentIndex())
        color = self.ui.colorComboBox.itemData(self.ui.colorComboBox.currentIndex())
        if self.item != None:
            return True
            if (self.ui.nameLineEdit.text() != self.item.name or
            self.uimakeItem.officialNamelineEdit.text() != self.item.official_name or
            (race.id if race != None else None) != self.item.race_id or
            (specie.id if specie != None else None) != self.item.specie_id or
            (sex.id if sex != None else None) != self.item.sex_id or
            (color.id if color != None else None) != self.item.color_id or
            self.ui.birthdayEdit.date() != self.item.birthday or
            self.ui.microLineEdit.text() != self.item.micro_num or
            self.ui.recNumlineEdit.text() != self.item.rec_num or
            self.ui.tattooLineEdit.text() != self.item.tattoo or
            self.ui.insuranceEdit.toPlainText() != self.item.insurance or
            self.ui.passportLineEdit.text() != self.item.passport or
            self.ui.otherInfoTextEdit.toPlainText() != self.item.other_info):
                return True
            elif ((self.ui.deathcheckBox.isChecked() and self.item.death_day == None) or
                  (not self.ui.deathcheckBox.isChecked() and self.item.death_day != None)):
                return True
            elif ((self.item.flags == None and self.ui.statusCheckBox.isChecked()) or
                  (self.item.flags != None and not self.ui.statusCheckBox.isChecked())):
                return True
            else:
                return False
        else:
            if (self.ui.nameLineEdit.text() != '' or
            self.ui.officialNamelineEdit.text() != '' or
            self.ui.raceComboBox.itemData(self.ui.raceComboBox.currentIndex()) != None or
            self.ui.specieComboBox.itemData(self.ui.specieComboBox.currentIndex()) != None or
            self.ui.sexComboBox.itemData(self.ui.sexComboBox.currentIndex()) != None or
            self.ui.colorComboBox.itemData(self.ui.colorComboBox.currentIndex()) != None or
            self.ui.birthdayEdit.date() != datetime(2000,1,1).date() or
            self.ui.microLineEdit.text() != '' or
            self.ui.recNumlineEdit.text() != '' or
            self.ui.tattooLineEdit.text() != '' or
            self.ui.insuranceEdit.toPlainText() != '' or
            self.ui.passportLineEdit.text() != '' or
            self.ui.otherInfoTextEdit.toPlainText() != ''):
                return True
            else:
                return False    

    def getType(self=None):
        return 'Animal'
    
    def getName(self=None):
        return 'Eläin'
    
    def getMessageBoxText(self):
        return 'Haluatko tallentaa eläimeen tehdyt muutokset?'
    
    def makeItem(self):
        data = self.getData()
        return Animal(data[0], data[1], data[2], data[3], data[4], 
                 data[5], data[6], data[7], data[8], data[9], 
                 data[10], data[11], data[12])
        
        #self.initializeParameters()
    
    def saveAble(self):
        return len(self.ui.nameLineEdit.text() + self.ui.officialNamelineEdit.text()) > 1
    
    def addAskedItem(self, item):#TODO: implement
        pass
