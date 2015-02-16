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
        
        self.number = ''

    def setNumber(self, number):
        self.number = number
   
    def getNumber(self):
        return self.number
   
    def getItem(self): 
        return self.item
    
    def askUserIfCanClose(self):
        print('GenericTab FUNCTIO: askUserIfCanClose')
        reply = QMessageBox.question(self,'Viesti',self.getMessageBoxText(), QMessageBox.Save, QMessageBox.Cancel, QMessageBox.Discard)
        if reply == QMessageBox.Save:
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
    
    #Functio makes popup to show error message
    def errorMessage(self, message):
        box = QMessageBox()
        box.setText(message)
        box.exec()
    
    def saveAndCloseTab(self):
        print('GenericTab FUNCTIO: saveAndCloseTab')
        tmp_item = None
        if self.saveAble():
            if self.item == None:
                self.item = self.makeItem()
                SqlHandler.addItem(self.session, self.item)
            else:
                if self.hasChanged():
                    #update item if it has changes
                    self.item.update(self.getData())
                    SqlHandler.commitSession(self.session)
                else:
                    pass #print('No')
            Tabmanager.closeTab(tab=self)
        else:
            from models.translationtables import g_save_error_message
            self.errorMessage(g_save_error_message)       
    


    def saveTab(self):
        print('GenericTab FUNCTIO: SaveTab')
        #check if tab is valid
        if self.saveAble():
            #check if there is items
            if self.item == None:
                #here self.item can be set because newToSaved will handle it
                self.item = self.makeItem()
                SqlHandler.addItem(self.session, self.item)
                self.update()
                Tabmanager.newToSaved(self)
            else:
                self.item.update(self.getData())
                SqlHandler.commitSession(self.session)
        else:
            from models.translationtables import g_save_error_message
            self.errorMessage(g_save_error_message)      

    
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
    
    #do not add made item to selt.item in overloaded function
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
    