#!/usr/bin/env python3
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

from models import SqlHandler
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

from PyQt4.QtGui import QProgressDialog

from configfile import genDBString, getDBName

import os.path

def init(status):
    if not status:
        session = SqlHandler.newSession()
        SqlHandler.addItems(session,[SqlHandler.ALV(alv=24,alv_class=1),    #Normal items
                                     SqlHandler.ALV(alv=10,alv_class=2),    #Medicines
                                     SqlHandler.ALV(alv=14,alv_class=3)])   #Feed

        SqlHandler.addItems(session, [SqlHandler.GlobalVar(key="clinicpayment", value="20.00"),
                                      SqlHandler.GlobalVar(key="km_price", value="0.48")])

        #create species
        koira = SqlHandler.Specie('Koira')
        kissa = SqlHandler.Specie('Kissa')
        hevonen = SqlHandler.Specie('Hevonen')
        #add species
        SqlHandler.addItems(session, [koira, kissa, hevonen])
    
        item_list = []
        dogs_file_name = "koirarodut.txt"
        cats_file_name = "kissarodut.txt"
        horse_file_name = "hevosrodut.txt"
        try:
            f = open(dogs_file_name, "r", encoding="utf-8")
            for race_name in f.readlines():
                item_list.append(SqlHandler.Race(race_name.strip(),koira.id)) 
            f.close()
        except IOError:
            print("Can not find file named: " + dogs_file_name)
            pass
        try:
            f = open(cats_file_name, "r", encoding="utf-8")
            for race_name in f.readlines():
                item_list.append(SqlHandler.Race(race_name.strip(),kissa.id)) 
            f.close()
        except IOError:
            print("Can not find file named: "+ cats_file_name)
            pass
        try:
            f = open(horse_file_name, "r", encoding="utf-8")
            for race_name in f.readlines():
                item_list.append(SqlHandler.Race(race_name.strip(),hevonen.id)) 
            f.close()
        except IOError:
            print("Can not find file named: "+ cats_file_name)
            pass
        
        SqlHandler.addItems(session,item_list)
        
        try:
            f = open('postinumerot.txt', "r", encoding="utf-8")
            raw_p_data  = f.readlines()
            
            offices = []
            offices_dict = {}
            for line in raw_p_data:
                if len(line) > 1:
                    office = SqlHandler.PostOffice(line.split(' ')[0])
                    offices.append(office)
                    offices_dict[line.split(' ')[0]] = office;
            
            SqlHandler.addItems(session,offices)
            
            numbers = []
            for line in raw_p_data:
                if len(line) > 1:
                    for item in line.split(' ')[1].strip().split(','):
                        numbers.append(SqlHandler.PostNumber(offices_dict[line.split(' ')[0]].id, int(item)))
            
            SqlHandler.addItems(session,numbers)
            f.close()
        except IOError:
            print("Can not find file named: "+ cats_file_name)
            pass
        
        
        
def main():
    
    #you can change databasename at models.__init__
    #status = False
    #if SqlHandler.usesLite():
    status = False #os.path.exists(getDBName())
    
    app = QtGui.QApplication(sys.argv)

    box = QProgressDialog()
    box.setMinimum(0);
    box.setMaximum(0);
    box.setLabelText('Ladataan...')
    box.show()
    
    
    if not SqlHandler.initialize():
        print(g_error_msg_dict['database_init'])
        return
    
    init(status)
    
    vet_app = MainWindow()
    Tabmanager.openTab(tabCreator=MainMenuTab)
    
    box.reset()
    vet_app.showMaximized()
    
    
    sys.exit(app.exec_())
    
    
    
main()
