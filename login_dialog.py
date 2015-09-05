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
from PyQt4.QtGui import QMainWindow
from uipy.ui_login import Ui_LoginDialog
from models import SqlHandler


class LoginDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_LoginDialog()
        self.ui.setupUi(self)
        self.session = SqlHandler.newSession()
        self.configureConnections();
        self.setVets()

    def configureConnections(self):
        pass
    
    def openVetApp(self):
        vet_app = MainWindow()
        Tabmanager.openTab(tabCreator=MainMenuTab)
        vet_app.showMaximized()
    
    
    def checkPassword(self):
        vet = self.getSelectedVet()
        if vet != None:
            return vet.checkPassword(self.ui.passwordLineEdit.test())
        else:
            return False #should not be calleb but anycase False
    
    def getSelectedVet(self):
        return self.ui.vetComboBox.itemData(self.ui.vetComboBox.currentIndex())
    
    def setVets(self):
        self.ui.vetComboBox.clear()
        
        for vet_temp in SqlHandler.searchVet(self.session):
            self.ui.vetComboBox.addItem(vet_temp.name, vet_temp)


def main():
    
    #you can change databasename at models.__init__
    #status = False
    #if SqlHandler.usesLite():
    status = True #os.path.exists(getDBName())
    
    app = QtGui.QApplication(sys.argv)

    try:
        if not SqlHandler.initialize():
            print(g_error_msg_dict['database_init'])
            return
        init(status)
        vet_app = MainWindow()
        Tabmanager.openTab(tabCreator=MainMenuTab)
        vet_app.showMaximized()
    except:
        box = QMessageBox()
        box.setText('Error: can not connect to server! ')
        box.show()
    
    sys.exit(app.exec_())