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

#TODO update this class to use SqlHandler


from PyQt4.QtGui import QLineEdit, QFrame, QTreeWidgetItem, QTreeWidget, QWidget
from PyQt4.QtCore import Qt, QObject, QTimer, QPoint, QEvent, QMetaObject
from uipy.ui_searchlineedit import Ui_SearchLineEdit

from mainwindowtabs import Tabmanager
from models import SqlHandler

class QueryTypes:
    OwnerSortByName = 0
    PostOfficeSortByName = 1
'''
  This widget works like google autoSuggest
  
  It's layout is made by Qt creator
  
  It has objects:
    -popup (QtreeWidget)
    -editor (QlineEdit)
    -newButton (QPushButton) Not currently used 
'''
class SearchLineEdit(QWidget):
    def __init__(self, tabcreator, session, parent=None, function=None, interval=400):
        QWidget.__init__(self, parent)
        self.ui = Ui_SearchLineEdit()
        self.ui.setupUi(self)
        
        self.tabcreator = tabcreator
        self.function = function
        self.params = None
        
        self.textplacetoeditor = 1
        #if you change this you have to change id place in string list got from items
        self.itemplace = 0         
       
        self.currentItem = None
        self.item = None
        self.interval = interval
        self.session = session
        self.configure()

    def configure(self): 
        #configure popup
        self.ui.popup.setWindowFlags(Qt.Popup)
        self.ui.popup.setFocusPolicy(Qt.NoFocus)
        self.ui.popup.setFocusProxy(self.parent())
        self.ui.popup.setMouseTracking(True)
        
        #in hiden column is hidden real item and id
        self.ui.popup.hideColumn(self.itemplace)

        #more popup configurations
        self.ui.popup.setUniformRowHeights(True)
        self.ui.popup.setRootIsDecorated(False)
        self.ui.popup.setEditTriggers(QTreeWidget.NoEditTriggers)
        self.ui.popup.setSelectionBehavior(QTreeWidget.SelectRows)
        self.ui.popup.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.ui.popup.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.popup.header().hide()
        self.ui.popup.installEventFilter(self)

        #setup timer for delay
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)        
        self.timer.setInterval(self.interval)
        
        #Create connectons
        self.ui.popup.itemClicked.connect(self.doneCompletion)
        self.timer.timeout.connect(self.autoSuggest)
        self.ui.editor.textEdited.connect(self.timer.start)
        #self.ui.editor.returnPressed.connect(self.moveNext)
        
        #button not used so we hide it
        if self.tabcreator != None:
            self.ui.newButton.setText('+')
            self.ui.newButton.clicked.connect(self.createNewItem)
        else:
            self.ui.newButton.hide()
    
    def setAnimalForDialog(self, animal):
        self.animal = animal
    
    def addAskedItem(self, item):
        print("DEBUG: SearchLineEdit.addAskedItem() item: ", item)
        if item != None:
            self.setCurrentItem(SqlHandler.makeCopy(self.session, item))
    
    def createNewItem(self):
        if hasattr(self.tabcreator, "getType"):
            Tabmanager.openTab(tabCreator=self.tabcreator, returnTab=self)
        else:
            creator = self.tabcreator(parent=self)
            creator.show()
    '''
      filter for events
      
    '''
    def eventFilter(self, source ,event):
        if not source == self.ui.popup: #TODO check that this dont cause problem
            return False
     
        if event.type() == QEvent.MouseButtonPress:
            self.ui.popup.hide()
            self.ui.editor.setFocus()
            return True

        if event.type() == QEvent.KeyPress:
            consumed = False
            if event.key() in {Qt.Key_Enter, Qt.Key_Return}:
                self.doneCompletion()
                consumed = True
            elif event.key() == Qt.Key_Escape:
                self.ui.editor.setFocus()
                self.ui.popup.hide()
                consumed = True
            elif event.key() in {Qt.Key_Up, Qt.Key_Down, Qt.Key_Home, Qt.Key_End, Qt.Key_PageUp, Qt.Key_PageDown}:
                pass
            else:
                self.ui.editor.setFocus()
                self.ui.editor.event(event)
                self.ui.popup.hide()
            return consumed
        return False
        
    
    '''
        Signal to update result view
    '''
    def autoSuggest(self):
        self.ui.popup.setUpdatesEnabled(False)
        self.ui.popup.clear()
        stringList = None
        
        print(self.params)
        print(self.function)
        
        if self.params != None:
            items_list = self.function(session=self.session, question=self.ui.editor.text(), params=self.params)
        else:
            items_list = self.function(session=self.session, question=self.ui.editor.text())
        
        for item in items_list:#TODO test that this works
            TreeWidgetItem = QTreeWidgetItem(self.ui.popup)
            stringList = item.stringList()
            if self.ui.popup.columnCount () < len(stringList):
                self.ui.popup.setColumnCount(len(stringList))
        
            for index in range(0,len(stringList)):
                TreeWidgetItem.setText(index, stringList[index])
            TreeWidgetItem.setData(self.itemplace, 0, item)
        
        self.ui.popup.setCurrentItem(self.ui.popup.topLevelItem(0))
        
        if stringList != None:
            for index in range(0,len(stringList)):
                self.ui.popup.resizeColumnToContents(index)
        
        self.ui.popup.adjustSize()
        self.ui.popup.setUpdatesEnabled(True)

        self.ui.popup.resize(self.ui.editor.width() if self.ui.editor.width() > 300 else 300, self.ui.popup.sizeHintForRow(0) * 10)
        
        self.ui.popup.move(self.ui.editor.mapToGlobal(QPoint(0, self.ui.editor.height())))
        self.ui.popup.setFocus()
        self.ui.popup.show()
        
    '''
        End searching
    '''
    def doneCompletion(self):
        self.timer.stop()
        self.ui.popup.hide()
        self.ui.editor.setFocus()
        item = self.ui.popup.currentItem()
        if item != None:
            self.currentItem = self.ui.popup.currentItem().data(0,0)
            self.ui.editor.setText(item.text(self.textplacetoeditor))
            QMetaObject.invokeMethod(self.ui.editor, "returnPressed");

    def getCurrentItem(self):
        if self.currentItem != None and self.currentItem.stringList()[self.textplacetoeditor] == self.ui.editor.text():
            return self.currentItem
        else:
            return None
    
    def setCurrentItem(self, item):
        print('setCurrentItem: ',item)
        self.currentItem = item
        self.ui.editor.setText(item.stringList()[self.textplacetoeditor])
        QMetaObject.invokeMethod(self.ui.editor, "returnPressed")
    