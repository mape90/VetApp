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
from PyQt4.QtGui import QMainWindow, qApp, QDialog, QMessageBox, QApplication

from uipy.ui_login import Ui_LoginDialog
from models import SqlHandler
from mainwindowtabs import Tabmanager
from mainWindow import MainWindow

from mainwindowtabs.mainmenutab import MainMenuTab
from mainwindowtabs.vettab import VetTab
from models.translationtables import g_login_error_messages

class WidgetVetTab(QDialog, VetTab):
    def __init__(self, parent=None, closeFunction=None):
        VetTab.__init__(self, parent=parent)
        self.ui.saveButton.hide()
        self.closeFunction = closeFunction
    
    def closeTab(self):
        self.closeFunction(self.item) #should be vet
        self.close()

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.session = SqlHandler.newSession()
        self.configureConnections();
        self.setVets()

    def setVets(self, vet=None): #TODO: select last used vet
        self.ui.vetComboBox.clear()
        
        for vet_temp in SqlHandler.searchVet(self.session):
            self.ui.vetComboBox.addItem(vet_temp.name, vet_temp)
            if vet != None and vet.name == vet_temp.name:
                tmp_index = self.ui.vetComboBox.findText(vet_temp.name)
                if tmp_index >= 0:
                    self.ui.vetComboBox.setCurrentIndex(tmp_index)
            

    def configureConnections(self):
        self.ui.loginButton.clicked.connect(self.tryToOpenVetApp)
        self.ui.newVetButton.clicked.connect(self.openVetTab)

    def openVetTab(self):
        vettab = WidgetVetTab(self, self.setVets)
        vettab.show()
    
    def tryToOpenVetApp(self):
        res = self.checkPassword()
        res = True
        if res == True: #ok
            self.accept()
        elif res == False: #password wont match
            QMessageBox.warning(self, 'Error', g_login_error_messages["wrong_password"])
        else: #other error
            QMessageBox.warning(self, 'Error', g_login_error_messages["other_error"])
    
    
    def checkPassword(self):
        vet = self.getSelectedVet()
        if vet != None:
            return vet.checkPassword(self.ui.passwordLineEdit.test())
        else:
            return None #should not be calleb but anycase False
    
    def getSelectedVet(self):
        return self.ui.vetComboBox.itemData(self.ui.vetComboBox.currentIndex())
