#coding: utf-8
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

import sys

from PyQt4 import QtGui
import datetime

from models import SqlHandler, databasename
#from models.animal import Animal, Sex, Race, Color
#from models.specie import Specie
#from models.postoffice import PostOffice, PostNumber
#from models.owner import Owner

from mainwindowtabs import Tabmanager

from mainwindowtabs.mainmenutab import MainMenuTab
from mainwindowtabs.searchtab import SearchTab
from mainwindowtabs.visittab import VisitTab
from mainwindowtabs.animaltab import AnimalTab
from mainwindowtabs.ownertab import OwnerTab
from mainwindowtabs.vettab import VetTab

from mainwindowtabs.generictreewidget import GenericTreeWidget, ButtonType
from mainwindowtabs.addNewDialog import AddNewDialog, AddNewWeight
from mainwindowtabs.searchlineedit import SearchLineEdit
from mainwindowtabs.operationbasecreator import OperationBaseCreator
from mainwindowtabs.itemcreatordialog import ItemCreatorDialog
from mainWindow import MainWindow

from mainwindowtabs.printFileCreator import PrintFileCreator

from mainwindowtabs.operationSelectorDialog import OperationSelectorDialog

import os.path

def main():
    
    #you can change databasename at models.__init__
    status = os.path.exists(databasename)
    
    SqlHandler.initialize()

    if not status:
        session = SqlHandler.newSession()
        SqlHandler.addItems(session,[SqlHandler.ALV(alv=24,alv_class=1),    #Normal items
                                     SqlHandler.ALV(alv=10,alv_class=2),    #Medicines
                                     SqlHandler.ALV(alv=14,alv_class=3)])   #Feed
                   
        #create species
        koira = SqlHandler.Specie('Koira')
        kissa = SqlHandler.Specie('Kissa')
        hevonen = SqlHandler.Specie('Hevonen')
        #add species
        SqlHandler.addItems(session, [koira, kissa, hevonen])
    
        item_list = []
        try:
            f = open("koirarodut.txt", "r", encoding="utf-8")
            for race_name in f.readlines():
                item_list.append(SqlHandler.Race(race_name.strip(),koira.id)) 
            f.close()
        except IOError:
            print("Error 1")
            pass
        try:
            f = open("kissarodut.txt", "r", encoding="utf-8")
            for race_name in f.readlines():
                item_list.append(SqlHandler.Race(race_name.strip(),kissa.id)) 
            f.close()
        except IOError:
            print("Error 2")
            pass
        
        SqlHandler.addItems(session,item_list)
        
        #generate vet TODO: make startup popup window
        hamina = SqlHandler.PostOffice('Hamina')
        SqlHandler.addItem(session,hamina)
        pnum = SqlHandler.PostNumber(hamina.id,'49420')
        SqlHandler.addItem(session, pnum)
        vet = SqlHandler.Vet("Sini","Vuoksenkuja 9A", hamina, pnum, 'y_number', 'vet_number','bank_name', 'IBAN', 'SWIF', ['','',''],[])
        SqlHandler.addItem(session,vet)


    
    
    app = QtGui.QApplication(sys.argv)
    vet_app = MainWindow()
    Tabmanager.openTab(tabCreator=MainMenuTab)

    vet_app.showMaximized()
    
    sys.exit(app.exec_())
    
    
main()
