'''
Created on 2.4.2013

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
from PyQt4.QtGui import QWidget, QTreeWidgetItem, QPushButton, QIcon, QMessageBox, QDialog, QSpinBox
from PyQt4.QtCore import QSize, QMetaObject

from mainwindowtabs import Tabmanager
from mainwindowtabs.searchlineedit import SearchLineEdit
from models import SqlHandler
from uipy.ui_listwidget import Ui_GenericTreeWidget
from datetime import datetime

class ButtonType():
    add = 'Lisää'
    remove = 'Poista'
    open = 'Avaa'
    check = 'Tehty'
    up = True
    down = False

class GenericTreeWidget(QWidget):
    def __init__(self, session, parent, updateFunctio=None):
        QWidget.__init__(self, parent=parent)
        self.ui = Ui_GenericTreeWidget()
        self.ui.setupUi(self)
        self.configure()
        self.iconplace = -1

        self.session = session
        
        self.updateFunctio = updateFunctio
        self.removecheck = False
        self.permanentRemove = False
        self.typecheck = False
        self.params = None
        self.tabcreator = None
        self.item = None
        self.ownDialog = None
        self.dialogitem = None
        self.searchlineedit = None
        self.searchLineFunction = None
    
    def configure(self):
        self.ui.treeWidget.setRootIsDecorated(False)
    
    def setTitle(self, title, hidden=False):
        if hidden:
            self.ui.textlabel.hide()
        else:
            self.ui.textlabel.setText(title)
        
    def setHeader(self,headertexts, iconplace=-1, iconsize=QSize(50,50), hidecolumns=[]):
        if iconplace >=0:
            self.ui.treeWidget.setIconSize(iconsize)
            self.iconplace = iconplace
            headertexts.insert(self.iconplace,'')
        
        self.ui.treeWidget.setHeaderItem(QTreeWidgetItem(headertexts))
        
        for column in hidecolumns:
            self.ui.treeWidget.hideColumn(column)
    
    def setRemoveCheck(self, text='Haluatko varmasti poistaa valitun?', status=True):
        self.removecheck = status
        self.removetext = text

    def setButtons(self, buttons, place=ButtonType.up):
        if place == ButtonType.up:
            for button in buttons:
                self.ui.topLayout.insertWidget(self.ui.topLayout.count(), self.cereateButton(button))
        else:
            for button in buttons:
                self.ui.bottomLayout.incertWidget(self.ui.bottomLayout.count(), self.cereateButton(button))
    
    def cereateButton(self, button):
        if button == ButtonType.add:
            self.addButton = QPushButton(button,parent=self)
            self.addButton.clicked.connect(self.addItem)
            return self.addButton
        elif button == ButtonType.remove:
            self.removeButton = QPushButton(button,parent=self)
            self.removeButton.clicked.connect(self.removeSelectedItem)
            return self.removeButton
        elif button == ButtonType.open:
            self.openButton = QPushButton(button, parent=self)
            self.openButton.clicked.connect(self.openItem)
            return self.openButton
        elif button == ButtonType.check:
            self.checkButton = QPushButton(button, parent=self)
            self.checkButton.clicked.connect(self.checkItem)
            return self.checkButton
        else:
            print('Error, not valid button type')
            return None
    
    def addItem(self):
        item = self.getItem()
        if item != None:
            self.addItemToTree(item)
     
    def getIcon(self, picture_path):#TODO Check
        if len(picture_path) > 3:
            return QIcon(picture_path)
        else:
            return QIcon('uni.jpg') #TODO: set Default image

    def setItems(self, itemList):
        self.ui.treeWidget.clear()
        for item in itemList:
            self.addItemToTree(item)
    

    #this function will return first selected item
    #So only one item is returned
    def getSelectedItem(self):
        if len(self.ui.treeWidget.selectedItems()) > 0:
            return self.ui.treeWidget.selectedItems()[0].data(0,0)
        else:
            return None

    def getItemsFromList(self):
        index=0
        itemList = []
        while self.ui.treeWidget.topLevelItem(index):
            item = self.ui.treeWidget.topLevelItem(index).data(0,0)
            itemList.append(item)
            index += 1
        return itemList
       
    def update(self):
        if self.updateFunctio != None and self.params != None:
            if len(self.params) == 0:
                self.setItems(self.updateFunctio(self.session))
            elif len(self.params) == 1:
                self.setItems(self.updateFunctio(self.session, self.params[0]))
            elif len(self.params) == 2:
                self.setItems(self.updateFunctio(self.session, self.params[0], self.params[1]))
            elif len(self.params) == 3:
                self.setItems(self.updateFunctio(self.session, self.params[0], self.params[1], self.params[2]))
            elif len(self.params) == 4:
                self.setItems(self.updateFunctio(self.session, self.params[0], self.params[1], self.params[2], self.params[3]))
        else:
            print('GenericTreeWidget.update(): self.updateFunction was None!')
    
    def addAskedItem(self, item):
        if item != None:
            self.addItemToTree(SqlHandler.makeCopy(self.session, item))
            
    def addAskedItemNoCopy(self, item):
        if item != None:
            self.session.add(item)
            self.addItemToTree(item)
    
    '''-----------OVERLOAD ABLE---------------'''
    def addItemToTree(self, item):
        if item == None:
            return
        if self.itemInList(item) >= 0:
            self.ui.treeWidget.takeTopLevelItem(self.itemInList(item))
        treeItem = self.makeTreeItem(item)
        self.ui.treeWidget.addTopLevelItem(treeItem)
        self.ui.treeWidget.setCurrentItem(treeItem)
    
    def makeTreeItem(self,item):#Overload if needed
        textString = item.stringList()
        #add '' to icon place
        treeItem = None
        if self.iconplace >= 0:
            textString.insert(self.iconplace, '')
            print('makeTreeItem() textString', textString)
            treeItem = QTreeWidgetItem(self.ui.treeWidget,textString)
            treeItem.setIcon(self.iconplace,self.getIcon(item.picurePath()))
        else:
            print('makeTreeItem() textString', textString)
            treeItem = QTreeWidgetItem(self.ui.treeWidget,textString)
        
        treeItem.setData(0,0,item)
        return treeItem
    
    def itemInList(self, item):#Overload if needed
        index = 0
        while self.ui.treeWidget.topLevelItem(index):
            treeItem= self.ui.treeWidget.topLevelItem(index)
            if treeItem.data(0,0) != None and treeItem.data(0,0).id == item.id:
                return index
            index += 1
        return -1

    def canRemoveItem(self):#Overload if needed
        if self.removecheck:
            result = QMessageBox.question(self,'Viesti',self.removetext, QMessageBox.Ok, QMessageBox.Cancel)
            if result == QMessageBox.Ok:
                return True
            else:
                return False
        else:
            return True
    '''-------------- OVERLOAD ------------'''   
    def setParameters(self, params):
        self.params = params
    
    def setPermanentRemove(self, status=True):
        self.permanentRemove = status    

    def setInputMethod(self,dialog=None, item=None,tabcreator=None, autoAdd=False, function=None, searchEnabled=True):
        if dialog != None:
            self.ownDialog = dialog
            if item != None:
                self.dialogitem = item
        else:
            self.tabcreator = tabcreator
            if searchEnabled:
                self.searchLineFunction = function
                self.searchlineedit = SearchLineEdit(tabcreator=self.tabcreator, session=self.session, parent=self, function=self.searchLineFunction)
                if autoAdd:
                    self.searchlineedit.ui.editor.returnPressed.connect(self.addItem)
                self.ui.topLayout.insertWidget(2, self.searchlineedit)   
    
    def openItem(self): #TODO: Make this more generic
        tree_item = self.ui.treeWidget.currentItem()
        if tree_item != None:
            item = tree_item.data(0,0)
            if hasattr(self.tabcreator, "getType"):
                    Tabmanager.openTab(tabCreator=self.tabcreator, newItem=item, returnTab=self)
            else:
                if self.ownDialog != None:
                    if self.dialogitem != None:
                        temp = self.ownDialog(parent=self, item=self.dialogitem)
                    else:
                        temp = self.ownDialog(parent=self)
                    temp.show()
   
    def getItem(self):
        if self.searchlineedit == None:
            if self.ownDialog != None:
                if self.dialogitem != None:
                    temp = self.ownDialog(parent=self, item=self.dialogitem)
                else:
                    temp = self.ownDialog(parent=self)
                temp.show()
            return None
        else:
            return self.searchlineedit.getCurrentItem()
    
    def removeSelectedItem(self):
        if self.canRemoveItem():
            removedItem = self.ui.treeWidget.takeTopLevelItem(self.ui.treeWidget.indexOfTopLevelItem(self.ui.treeWidget.currentItem()))
            if removedItem != None:
                item = removedItem.data(0,0)
                if self.permanentRemove and item != None and item.id != None:
                    self.session.delete(item)
    
    def clearTreeWidget(self):
        self.ui.treeWidget.clear()              
                    
class VisitAnimalTreeWidget(GenericTreeWidget):
    def __init__(self, session, parent):
        GenericTreeWidget.__init__(self, session, parent)
        self.setTitle('Eläimet')
        self.setHeader(headertexts=['id', 'Nimi', 'Virallinen nimi', 'Laji', 'Rotu'], iconplace=1, hidecolumns=[0])
        self.setButtons([ButtonType.remove,ButtonType.open])
        from mainwindowtabs.animaltab import AnimalTab
        self.setInputMethod(tabcreator=AnimalTab, autoAdd=True, function=SqlHandler.searchAnimal)
    
    def removeSelectedItem(self):
        if self.canRemoveItem():
            removedItem = self.ui.treeWidget.takeTopLevelItem(self.ui.treeWidget.indexOfTopLevelItem(self.ui.treeWidget.currentItem()))
            if removedItem != None:
                item = removedItem.data(0,0)
                if item in self.session:
                    self.session.delete(item)

    def openItem(self):
        tree_item = self.ui.treeWidget.currentItem()
        if tree_item != None:
            if hasattr(self.tabcreator, "getType"):
                item = tree_item.data(0,0)
                Tabmanager.openTab(tabCreator=self.tabcreator, newItem=item.animal)
            else:
                creator = self.tabcreator(parent=self)
                creator.show()
                
 
    def makeTreeItem(self,item):#Overload if needed
        if item.getType() != 'VisitAnimal':
            item = SqlHandler.VisitAnimal(item)
        
        textString = item.stringList()
        textString.insert(self.iconplace, '')
        treeItem = QTreeWidgetItem(self.ui.treeWidget, textString)
        treeItem.setIcon(self.iconplace,self.getIcon(item.animal.picurePath()))
        treeItem.setData(0,0,item)

        return treeItem
 
    def itemInList(self, item):
        index = 0
        while self.ui.treeWidget.topLevelItem(index):
            treeItem = self.ui.treeWidget.topLevelItem(index)
            if (treeItem.data(0,0) != None and treeItem.data(0,0).animal.id == 
                (item.id if item.getType() != 'VisitAnimal' else item.animal.id)):
                return index
            index += 1
        return -1
 
class OperationTreeWidget(GenericTreeWidget):
    def __init__(self, session, parent):
        GenericTreeWidget.__init__(self, session, parent)
        self.setTitle("Eläimelle tehdyt operaatiot")
        self.setButtons([ButtonType.add,ButtonType.remove])
        self.setHeader(headertexts=['id', 'Operaatiotyyppi', 'Nimi', 'Hinta'], hidecolumns=[0])
        from mainwindowtabs.operationbasecreator import OperationBaseCreator
        self.setInputMethod(tabcreator=OperationBaseCreator, autoAdd=True, function=SqlHandler.searchOperationBase)
        
    def removeSelectedItem(self):
        if self.canRemoveItem():
            removedItem = self.ui.treeWidget.takeTopLevelItem(self.ui.treeWidget.indexOfTopLevelItem(self.ui.treeWidget.currentItem()))
            if removedItem != None:
                item = removedItem.data(0,0)
                if item in self.session:
                    self.session.delete(item)

    def makeTreeItem(self,item):
        if 'Base' in item.getType():
            if item.hasList():
                item = type(item).ObjectCreator(type(item))(item.price, item.description, base=item, items=item.items)
            else:
                item = type(item).ObjectCreator(type(item))(item.price, item.description, base=item)
            self.session.add(item)

        treeItem = QTreeWidgetItem(self.ui.treeWidget, item.stringList())
        treeItem.setData(0,0,item)

        return treeItem
 
    def addItemToTree(self, item):
        
        print("OperationTreeWidget: item type is ", type(item))
        
        if item != None:
            self.ui.treeWidget.addTopLevelItem(self.makeTreeItem(item))

#TODO: Add method to increase decrease item count of items

class ItemTreeWidget(GenericTreeWidget):
    def __init__(self, session, parent, creator):
        GenericTreeWidget.__init__(self, session, parent)
        self.creator = creator
        self.setTitle('Tuotteet')
        self.setButtons([ButtonType.add,ButtonType.open,ButtonType.remove])
        self.setHeader(headertexts=['id', 'Nimi', 'Tyyppi', 'Hinta', 'Määrä'], hidecolumns=[0])
        
        from mainwindowtabs.itemcreatordialog import ItemCreatorDialog
        self.setInputMethod(tabcreator=ItemCreatorDialog, autoAdd=True, function=SqlHandler.searchItem)
        
        
        self.countSpinBox = QSpinBox(parent=self)
        self.countSpinBox.setRange(1, 99999999)
        self.countSpinBox.setValue(1)
        
        if self.ui.topLayout.count() > 0 or self.ui.bottomLayout.count() == 0:
            self.ui.topLayout.insertWidget(self.ui.topLayout.count(), self.countSpinBox)
        else:
            self.ui.bottomLayout.incertWidget(self.ui.bottomLayout.count(), self.countSpinBox)
        
        self.setUpTreewidget()
        self.countSpinBox.valueChanged['int'].connect(self.updateItemCount)
           
        self.ui.treeWidget.currentItemChanged.connect(self.handleChange)
    
    def setUpTreewidget(self):
        if self.ui.treeWidget.currentItem() != None:
            #set item count to countSpinBox
            self.countSpinBox.setValue(self.ui.treeWidget.currentItem().data(0,0).count)
    
    def updateItemCount(self,count):
        current = self.ui.treeWidget.currentItem()
        if current.data(0,0).count != count:
            current.data(0,0).count = count
            current.setText(3, str(current.data(0,0).item.price*count))
            current.setText(4, str(count))
        
    
    def handleChange(self, current, previous):
        if current != None:
            self.countSpinBox.setValue(self.ui.treeWidget.currentItem().data(0,0).count)
    
    '''
        This function is called when:
        1. searchLineEdit returns new item (Item)
        2. list of items is loaded from Surgery or SurgeryBase object
        3. just wanted to increase count of current item.
        
        item is type of Item/SurgeryItem/SurgetyBaseItem
    
    '''
    def addItemToTree(self, item):
        if item != None:
            if item.getType() == self.creator.getType():
                #Now we are loading data from Surgery or Surgery base object
                #So we make new tree objects and add counts to them
                treeItem = self.makeTreeItem(item)
                self.ui.treeWidget.addTopLevelItem(treeItem)
                self.ui.treeWidget.setCurrentItem(treeItem)
            else:
                item_index = self.itemInList(item)
                if item_index < 1:
                    #Item isnt found from list so we make new
                    treeItem = self.makeTreeItem(item)
                    self.ui.treeWidget.addTopLevelItem(treeItem)
                    self.ui.treeWidget.setCurrentItem(treeItem)
                else:
                    #item is in list and it is just returned from Itemcreator and data is needed to be edited
                    #or it it is tryed to add by searchline edit
                    removedItem = self.ui.treeWidget.takeTopLevelItem(item_index) #take line from list
                    
                    item_data = item.stringList() #get item new string list
                    
                    #update data, only item data not
                    for i in range(1,len(item_data)):
                        removedItem.setText(i,item_data[i]) #set updated text to line
                    
                    self.ui.treeWidget.addTopLevelItem(removedItem) #add line back to list
                    self.ui.treeWidget.setCurrentItem(removedItem) #set it current item
    
    def getItemsFromList(self):
        itemList = []
        for i in range(0, self.ui.treeWidget.topLevelItemCount()):
            itemList.append(self.ui.treeWidget.topLevelItem(i).data(0,0))
        return itemList        
    
    def removeSelectedItem(self):
        temp = self.ui.treeWidget.currentItem()
        if temp != None:
            removedItem = self.ui.treeWidget.takeTopLevelItem(self.ui.treeWidget.indexOfTopLevelItem(temp))
            if removedItem != None:
                item = removedItem.data(0,0)
                if item in self.session:
                    self.session.delete(item)

    def openItem(self):#TODO:check what happpens with empty list
        tree_item = self.ui.treeWidget.currentItem()
        if tree_item != None:
            creator = self.tabcreator(parent=self, item=tree_item.data(0,0).item)
            creator.show()
                
    '''
        item is Item(any of them) or SurgeryItem/SurgeryBaseItem
    '''
    def makeTreeItem(self,item):
        if item.getType() != self.creator.getType():
            item = self.creator(item) #make new item
            
        textString = item.stringList() #has all info
        treeItem = QTreeWidgetItem(self.ui.treeWidget, textString)
        treeItem.setData(0,0,item)

        return treeItem
 
    def itemInList(self, item):
        if item.getType() == self.creator.getType(): #get item from SurgeryBaseItem/SurgeryItem
            item = item.item
        
        for i in range(0, self.ui.treeWidget.topLevelItemCount()):
            temp_item = self.ui.treeWidget.topLevelItem(i).data(0,0)
            if temp_item.item.id == item.id:
                return i
        
        #item not found
        return -1



from uipy.ui_recipiemeicineDialog import Ui_RecipieMedicineDialog

class RecipieMedicineDialog(QDialog):
    def __init__(self, parent=None, item=None):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_RecipieMedicineDialog()
        self.ui.setupUi(self)
        self.item = item
        self.dialogitem = None
        self.session = SqlHandler.newSession()
        self.configure()
        self.createConnections()
        self.setBasicInfo()
    
    def configure(self):
        from mainwindowtabs.itemcreatordialog import ItemCreatorDialog
        self.searchItemEdit = SearchLineEdit(tabcreator=ItemCreatorDialog,session=self.session, parent=self, function=SqlHandler.searchItem)
        self.ui.verticalLayout.insertWidget(0,self.searchItemEdit)
    
    def createConnections(self):
        self.ui.closeButton.clicked.connect(self.closeDialog)
        self.ui.saveButton.clicked.connect(self.saveDialog)
    
    def saveDialog(self):
        if self.searchItemEdit.getCurrentItem() != None:
            if self.item == None:
                self.item = SqlHandler.RecipieMedicine(self.searchItemEdit.getCurrentItem(), self.ui.spinBox.value())
                self.session.add(self.item)
            else:
                self.item.update(self.getData())
            
            self.session.commit()
            self.parent().addAskedItem(self.item)
            self.closeDialog()
    
    def getData(self):
        data = []
        data.append(self.searchItemEdit.getCurrentItem())
        data.append(self.ui.spinBox.value())
        return data
                
    def closeDialog(self):
        self.session.close()
        self.setParent(None)
        self.close()
    
    def setBasicInfo(self):
        if self.item != None:
            self.ui.spinBox.setValue(self.item.count)
    

from uipy.ui_phonerecipiedialog import Ui_PhoneRecipieDialog

class PhoneRecipieDialog(QDialog):
    def __init__(self, parent=None, item=None, animal=None):
        QDialog.__init__(self, parent=parent)
        self.ui = Ui_PhoneRecipieDialog()
        self.ui.setupUi(self)
        self.session = SqlHandler.newSession()
        self.item = item
        self.animal = None
        if animal != None:
            self.animal = SqlHandler.makeCopy(self.session, animal)
        
        self.configure()
        self.createConnections()
        self.setBasicInfo()
        
    def configure(self):
        from mainwindowtabs.animaltab import AnimalTab
        self.animalsearch = SearchLineEdit(tabcreator=AnimalTab, session=self.session, parent=self, function=SqlHandler.searchAnimal)
        self.ui.searchLineEditLayout.addWidget(self.animalsearch)
        
        self.recipieMedicineTreeWidget = GenericTreeWidget(session=self.session, parent=self)
        self.recipieMedicineTreeWidget.setTitle('Reseptituotteet')
        self.recipieMedicineTreeWidget.setHeader(headertexts=['id', 'Nimi', 'Määrä'], hidecolumns=[0])
        self.recipieMedicineTreeWidget.setButtons([ButtonType.add, ButtonType.open, ButtonType.remove])
        self.recipieMedicineTreeWidget.setInputMethod(dialog=RecipieMedicineDialog, autoAdd=True)
        
        self.ui.verticalLayout.insertWidget(2, self.recipieMedicineTreeWidget)

    def setBasicInfo(self):
        if self.item != None:
            self.animalsearch.setCurrentItem(self.item.animal)
            self.animalsearch.setDisabled(True)
            self.ui.madeTimeEdit.setDate(self.item.made_time)
            if self.item.call_time != None:
                self.ui.dateTimeEdit.setDate(self.item.call_time)
            self.recipieMedicineTreeWidget.setItems(self.item.recipiemedicines)
        else:
            if self.animal != None:
                self.animalsearch.setCurrentItem(self.animal)
                self.animalsearch.setDisabled(True)
            self.ui.madeTimeEdit.setDateTime(datetime.now())

    def createConnections(self):
        self.ui.canselButton.clicked.connect(self.closeDialog)
        self.ui.saveButton.clicked.connect(self.saveDialog)
        self.ui.nowButton.clicked.connect(self.setRingTime)
    
    def setRingTime(self):
        self.ui.dateTimeEdit.setDateTime(datetime.now())
    
    def saveDialog(self):
        if self.animalsearch.getCurrentItem() != None:
            if self.item != None:
                self.item.update()
                self.parent().update()
                self.closeDialog()
            else:
                self.item = SqlHandler.PhoneRecipie(self.animalsearch.getCurrentItem(), self.recipieMedicineTreeWidget.getItemsFromList())
                self.item.update(self.getData())
                SqlHandler.addItem(self.session, self.item)
                self.parent().update()
                self.closeDialog()
    
    def getData(self):
        data = []
        data.append(self.animalsearch.getCurrentItem())
        data.append(self.ui.madeTimeEdit.dateTime().toPyDateTime())
        data.append(self.ui.dateTimeEdit.datetime().toPyDateTime() if self.ui.dateTimeEdit.dateTime() != datetime(2000,1,1) else None)
        data.append(self.recipieMedicineTreeWidget.getItemsFromList())
        return data
    
    def closeDialog(self):
        self.session.close()
        self.setParent(None)
        self.close()

class PhoneRecipieTreeWidget(GenericTreeWidget):
    def __init__(self, session, parent, findAll=False):
        GenericTreeWidget.__init__(self, session, parent) 
        self.setTitle('Puhelinreseptit')
        self.setHeader(headertexts=['id', 'Nimi', 'Määrä', 'Aika', 'Soitettu'], hidecolumns=[0])
        self.setButtons([ButtonType.add, ButtonType.open, ButtonType.remove])
        
        if findAll:
            self.updateFunctio = SqlHandler.searchPhoneRecipies
        else:
            self.updateFunctio = SqlHandler.searchAnimalPhoneRecipies 
        self.ownDialog = PhoneRecipieDialog
        self.tabcreator = PhoneRecipieDialog
        
        self.permanentRemove = True
        
    def getItem(self):
        if self.ownDialog != None:
            if self.dialogitem != None:
                temp = self.ownDialog(parent=self, animal=self.dialogitem)
            else:
                temp = self.ownDialog(parent=self)
            temp.show()

    def openItem(self): #TODO: Make this more generic
        tree_item = self.ui.treeWidget.currentItem()
        if tree_item != None:
            item = tree_item.data(0,0)
            temp = self.ownDialog(parent=self, item=item ,animal=self.dialogitem)
            temp.show()
    
    def removeSelectedItem(self):
        if self.canRemoveItem():
            removedItem = self.ui.treeWidget.takeTopLevelItem(self.ui.treeWidget.indexOfTopLevelItem(self.ui.treeWidget.currentItem()))
            if removedItem != None:
                print(removedItem.data(0,0))
                self.session.delete(removedItem.data(0,0))
    