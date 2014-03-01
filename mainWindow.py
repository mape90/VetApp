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
from PyQt4.QtGui import QMainWindow, qApp

from mainwindowtabs import Tabmanager
from mainwindowtabs.mainmenutab import MainMenuTab
from uipy.ui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        #määritetään pääikkunan layoutti
        QMainWindow.__init__(self, parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.configureMainWindow()
        self.createConnections()
        
        Tabmanager.initialize(self.ui.tabWidget)


    def configureMainWindow(self):
        self.setWindowTitle('VetApp 0.1 (Alfa)')
        
    
    '''
        This function makes all neened connection to handle
    '''
    def createConnections(self):
        self.ui.actionMainMenu.triggered.connect(self.openMainMenu)
        self.ui.actionClose.triggered.connect(qApp.quit)
        
    def openMainMenu(self):
        Tabmanager.openTab(tabCreator=MainMenuTab)
