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
    This class handles that tabs are opened correctly and are not closed if other needs it.
    Also sets focus to tabs and opens them
'''

import re
from models import SqlHandler
from models.translationtables import g_tab_name_dict

class TabManager(object):
    def __init__(self, tabwidget=None):
        self.tabwidget = tabwidget
        
        self.session = SqlHandler.newSession()
        self.previoustab = None

        self.new_text = 'Uusi '
        self.translate = g_tab_name_dict
        self.tabslist = {}
        
        self.returnList = {}
    
    def createCOnnections(self):
        self.tabwidget.tabCloseRequested.connect(self.askToCloseTab)
    
    def change(self):
        self.tabwidget.setCurrentIndex(self.tabwidget.currentIndex()+1)
    
    def initialize(self, tabwidget):
        self.tabwidget = tabwidget
        self.tabwidget.setTabsClosable(True)
        self.tabwidget.setMovable(True)
        self.createCOnnections()
    




    def openTab(self, tabCreator, newItem=None, returnTab=None):
        tabType = tabCreator.__name__
        newTab = None
        key = "UNDEFINED"
        text = "UNDEFINED"


        from models.translationtables import g_unique_tabs, g_tab_name_dict

        if tabType in g_unique_tabs:
            #check if tab is one of unique tabs
            if not tabType in self.tabslist:
                newTab = tabCreator(parent=self.tabwidget, item=newItem)
                key = tabType
                text = g_tab_name_dict[tabType]
            else:
                self.setCurrentTab(self.tabslist[tabType])
                return
        else:
            if newItem != None and newItem.__class__.__name__ != "dict":
                #check if item has allready tab
                if not tabType + str(newItem.id) in self.tabslist:
                    newTab = tabCreator(parent=self.tabwidget, item=newItem)
                    if tabType is "BillTab":
                        text = self.findNextNewText(tabCreator)
                        if newTab.item == None:
                            key = 'new' + tabType + self.findNextNewIndex('new'+tabType)
                        else:
                            key = tabType + str(newTab.item.id)
                    elif tabType is "VisitTab":
                        text = self.findNextNewText(tabCreator)
                        key = tabType + str(newItem.id)
                    elif tabType in ["OwnerTab","AnimalTab"]:
                        text = newItem.name
                        key = tabType + str(newItem.id)
                    else:
                        print("DEBUG: ERROR: TabManager->openTab() Wrong Tab Type: " + str(tabType))
                        return

                else:
                    #item has allready tab so we just set it as curent tab and return
                    self.setCurrentTab(self.tabslist[tabType + str(newItem.id)])
                    return
            else:
                #Make new tab without item or item is dictionary
                newTab = tabCreator(parent=self.tabwidget, item=newItem)

                index = self.findNextNewIndex('new'+tabType)
                text = self.new_text + self.translate[tabType] + index
                key = 'new' + tabType + index



        self.tabwidget.addTab(newTab, text)
        self.tabslist[key] = newTab
        self.returnList[newTab] = returnTab
        self.setCurrentTab(newTab)


    
    def askToCloseTab(self,index):
        tab = self.tabwidget.widget(index)
        if tab.canCloseTab():
            self.closeTab(tab=tab)

    '''
        item is Animal, Owner or Visit 
        tabName is real text in tab, so it is need to be translated
    '''
    def closeTab(self, tab=None, item=None):

        if not not item:
            print("DEBUG: closeTab: not not item is true")
            #save and close is called when there is item
            tabType = tab.__class__.__name__

            if not not tab.getItem():
                key = tabType + str(tab.getItem().id)
            else:
                key = 'new' + tabType + self.getNameNumber(tab)

            #give item to returnList tab
            if not not self.returnList[tab]:
                self.returnList[tab].addAskedItem(item)
                self.returnList[tab] = None

        elif not not tab:
            print("DEBUG: closeTab: tab.__name__ is ",tab.__class__.__name__)

            from models.translationtables import g_unique_tabs
            tabType = tab.__class__.__name__

            if(tabType in g_unique_tabs):
                key = tabType
            elif tabType is "VisitTab":
                #check if tab has item

                print("DEBUG: closeTab(), tab=",tab,"its item:", tab.getItem())

                if not not tab.getItem():
                    key = tabType + str(tab.getItem().id)
                else:
                    key = 'new' + tabType + self.getNameNumber(tab)

            elif(tabType in ["AnimalTab","OwnerTab"]):
                #visit tab will end visit so it just closes current session
                tabItem = tab.getItem()

                #check if tab has item
                if not not tabItem:
                    key = tabType + str(tabItem.id)

                    #is some one wants this tabItem then give it
                    returnTab = self.returnList[tab]
                    if not not returnTab:
                        self.returnList[tab].addAskedItem(tabItem)
                        self.returnList[tab] = None
                else:
                    key = 'new' + tabType + self.getNameNumber(tab)

            elif(tabType is "BillTab"):
                #get bill item for checking if bill is saved
                item = tab.getItem()
                if not not item:
                    key = tabType + str(item.id)
                else:
                    key = 'new' + tabType + str(tab.visit.id)
            else:
                #error this should not be seen in any time
                print("FATAL ERROR: Tabmanager->closeTab() unknown tab type of ",tabType)
                return


        else:
            print("DEBUG: TabManager closeTab,empty closetab call")
            return

        #remove tab and set next tab
        try:
            self.removeTab(self.tabslist[key])
        except:
            print("Tablist is : ", self.tabslist)
            print("Error key is: ", key)
            return

        #clean tabs from dictionarys
        del self.tabslist[key]
        del self.returnList[tab]


    '''
        This funcktion is called when new item is saved and it is not closed.
        So it has item that is in data base so we start to protect it so
        that it can not be opened twice.
    '''
    def newToSaved(self, tab):
        print("DEBUG: Tabmanager.newToSaved() tab:",tab)
        if not not tab:
            tabType = tab.__class__.__name__
            tabItem = tab.getItem()
            digit = self.getNameNumber(tab)

            key = ''
            if tabType is 'BillTab' and ('new' + tabType + str(tab.visit.id) in self.tabslist):
                key = 'new' + tabType + str(tab.visit.id)
            elif 'new' + tabType + digit in self.tabslist:
                key = 'new' + tabType + digit
            else:
                print("FATAL ERROR: TabManager.newToSaved(). Can not find the tab: ",tab)
                return

            #update tab with new name
            del self.tabslist[key]
            self.tabslist[tabType + str(tabItem.id)] = tab

            #check if item has tab in returnList
            if self.returnList[tab] != None:
                self.returnList[tab].addAskedItem(tabItem)
                self.returnList[tab] = None

            #update Tab text
            if tabItem.getType() == 'Visit':
                self.tabwidget.setTabText(self.tabwidget.indexOf(tab), self.findNextNewText(tab))
            else:
                self.tabwidget.setTabText(self.tabwidget.indexOf(tab), tabItem.name)

        else:
            print('FATAL ERROR: Tabmanager->newToSaved: Tab can not be None!')

        

    

    '''--------------HELPER FUNCTIONS-------------------'''
    
    def setCurrentTab(self, newTab):
        self.previoustab = self.tabwidget.currentWidget()
        self.tabwidget.setCurrentIndex(self.tabwidget.indexOf(newTab))
                                       
    def removeTab(self, tab):
        if not tab.isUnique() and self.returnList[tab] != None and self.returnList[tab] in self.returnList:
            self.setCurrentTab(self.returnList[tab])
        self.tabwidget.removeTab(self.tabwidget.indexOf(tab))
        tab.close()
        tab.setParent(None)
        del tab
        if self.previoustab in self.tabslist.values():
            self.tabwidget.setCurrentIndex(self.tabwidget.indexOf(self.previoustab))
    

    def findNextNewText(self, tab):
        #get transtalion table
        from models.translationtables import g_tab_name_dict
        try:
            text = g_tab_name_dict[tab.__class__.__name__]
        except:
            text = g_tab_name_dict[tab.__name__]

        names = []
        #get all table names
        for index in range(0,self.tabwidget.count()):
            names.append(self.tabwidget.tabText(index))
        index = 2

        #find next free text
        if not text in names:
            return text
        else:
            while text + ' ' + str(index) in names:
                index += 1
            return text + ' '  + str(index)

    '''
        return '' if none object found whit this itemName
        return 2,3,4... until free number is found
    ''' 
    def findNextNewIndex(self, itemName):
        index = 2
        if not (itemName in self.tabslist):
            return ''
        else:
            while itemName + str(index) in self.tabslist:
                index += 1
            return str(index)

    #this function will return number as string or empty string if there is no number in tab text
    def getNameNumber(self, tab):

        name = self.tabwidget.tabText(self.tabwidget.indexOf(tab))

        #select only digits
        temp = re.sub('[^0-9]', ' ', name.lower()).split()
        if len(temp) < 1:
            return ''
        else:
            return str(temp[len(temp)-1])
