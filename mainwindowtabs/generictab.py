#!/usr/bin/python
# -*- coding: utf-8
'''
Created on 31.3.2013

@author: Markus Peltola
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
'''
    GenericTab(QWidget)
    Variables:
    -session   (sql session)
    -item
    
    Functions:
    -string   <- getType()
    -item     <- getItem() i.e. Animal, Owner, visit
    -bool     <- askUserIfCanClose()
    -bool     <- canCloseTab()
    -None     <- closeTab()
    -None     <- saveAndCloseTab()
    -None     <- saveTab()
    
    Overload Able
    -bool     <- isUnique()
    
    Need to bee overloaded
    -list     <- getData()
    -None     <- addAskedItem()
    -item     <- makeItem()
    -bool     <- saveAble
    -bool     <- hasChanged
    -string   <- getMessageBoxText
    
'''


from PyQt4.QtGui import QWidget, QMessageBox
from PyQt4.QtCore import QDate
from models import SqlHandler

from mainwindowtabs import Tabmanager

import datetime

class GenericTab(QWidget):
    def __init__(self, parent=None, item=None):
        QWidget.__init__(self, parent)
        self.session = SqlHandler.newSession()
        
        self.item = SqlHandler.makeCopy(self.session, item) if item != None else None

        
    def getItem(self): 
        return self.item
    
    def askUserIfCanClose(self):
        print('GenericTab FUNCTIO: askUserIfCanClose')
        reply = QMessageBox.question(self,'Viesti',self.getMessageBoxText(), QMessageBox.Save, QMessageBox.Cancel, QMessageBox.Discard)
        if reply == QMessageBox.Save:
            print('Saving changes')
            self.saveTab()
            return True
        elif reply == QMessageBox.Discard:
            return True
        else:
            return False
    
    def canCloseTab(self):
        print('GenericTab  FUNCTIO: CanCloseTab')
        if self.hasChanged():
            if self.saveAble():
                return self.askUserIfCanClose()
            else:
                return True
        else:
            return True
    
    ''' For close button and external close '''
    def closeTab(self): #SLOT
        print('GenericTab FUNCTIO: closeTab')
        if self.canCloseTab():
            Tabmanager.closeTab(tab=self)
    
    def errorMessage(self, message):
        print('GenericTab FUNCTION: errorMessage')
        box = QMessageBox()
        box.setText(message)
        box.exec()
    
    def saveAndCloseTab(self):
        print('GenericTab FUNCTIO: saveAndCloseTab')
        if self.saveAble():
            if self.item == None:
                self.item = self.makeItem()
                print(self.item)
                SqlHandler.addItem(self.session, self.item)
            else:
                print('saveAndCloseTab: Is tab changed?')
                if self.hasChanged():
                    print('Yes')
                    self.item.update(self.getData())
                    SqlHandler.commitSession(self.session)
                else:
                    print('No')        
        else:
            self.errorMessage('Can not save item! Because it is not valid')
            return #wont close tab
        Tabmanager.closeTab(item=self.item)
    
    def saveTab(self):
        print('GenericTab FUNCTIO: SaveTab')
        if self.saveAble():
            #print("GenericTab->saveTab(), self.item == " + str(self.item))
            #print(str(Tabmanager.session))
            #print("GenericTab->saveTab(), item in session == " + str(self.item in self.session))
            if self.item == None:
                self.item = self.makeItem()
                SqlHandler.addItem(self.session, self.item)
                self.update()
                Tabmanager.newToSaved(self)
            else:
                self.item.update(self.getData())
                SqlHandler.commitSession(self.session)
        else:
            self.errorMessage('Can not save item! Because it is not valid')

    
    def qdateToPy(self, date):
        if type(date) is QDate:
            return date.toPyDate()
        else:
            return date.toPyDateTime()

    '''---------------CAN OVERLOAD THESE-----------------'''
    
    def isUnique(self=None):#Can Overload
        return False
    
    '''-----------------OVERLOAD THESE-------------------'''
    
    def getType(self=None):
        return 'Generic'
    
    def getData(self):
        return []
    
    def addAskedItem(self, item):#Overload
        pass
    
    def makeItem(self): #Overload
        return None
            
    def saveAble(self): #Overload
        return True
    
    def hasChanged(self): #Overload
        return False
    
    def getMessageBoxText(self): #Overload
        return 'Haluatko tallentaa tabiin tehdyt muutokset?'
    
    def update(self):
        pass
    
    