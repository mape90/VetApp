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

class TabManager(object):
    def __init__(self, tabwidget=None):
        self.tabwidget = tabwidget
        
        self.session = SqlHandler.newSession()
        self.previoustab = None

        self.new_text = 'Uusi '
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
            if newItem != None and newItem.__class__.__name__ == "dict":
                #check if item has allready tab
                if not tabType + str(newItem.id) in self.tabslist:
                    newTab = tabCreator(parent=self.tabwidget, item=newItem)
                    if tabType is "BillTab":
                        text = self.billText()
                        if newTab.item == None:
                            key = 'new' + tabType
                        else:
                            key = tabType + str(newTab.item.id)
                    elif tabType is "VisitTab":
                        text = self.visitText()
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
                #Make new tab without item
                newTab = tabCreator(parent=self.tabwidget, item=newItem)

                index = self.findNextNewIndex('new'+tabType)
                text = self.new_text + self.translate[tabType] + index
                key = 'new' + tabType + index



        self.tabwidget.addTab(newTab, text)
        self.tabslist[key] = newTab
        self.returnList[newTab] = returnTab
        self.setCurrentTab(newTab)

        #//---------------------------------------

        #else:
            #if newItem != None:
                #newTab = tabCreator(parent=self.tabwidget, item=newItem)

                #if tabType is "BillTab":
                    #text = self.billText()
                    #if newTab.item == None:
                        #text = 'new' + tabType
                    #else:
                        #text = tabType
                #elif tabType is "VisitTab":
                    #if newItem.__class__.__name__ is "dict":
                        #pass
                    #else:
                        #pass
                #elif tabType is "OwnerTab":

                #elif tabType is "AnimalTab":

                #else:
                    ##check if there is tab opened for that object
                    ##dont make new tab if there is allready tab open
                    #if not tabType + str(newItem.id) in self.tabslist:


                ##add tab to to tabwidget (item, text_str)

                #temp_tab_name = tabType+ str(newItem.id)

                #temp_tab = self.tabslist[name]


                #self.tabwidget.addTab(newTab, text)
                #self.setCurrentTab(temp_tab)
                #self.returnList[newTab] = returnTab


        #else:
            #if newItem != None:
                #if(newItem.__class__.__name__ != 'dict'):
                    #if not tabType + str(newItem.id) in self.tabslist:

                        #newTab = tabCreator(parent=self.tabwidget, item=newItem)

                        #if tabCreator.getType() == 'Bill':
                            #self.tabwidget.addTab(newTab, self.billText())
                            #if newTab.item == None:
                                #tabType = 'new' + tabType
                        #elif newItem.getType() == 'Visit':
                            #self.tabwidget.addTab(newTab, self.visitText())
                        #else:
                            #self.tabwidget.addTab(newTab, newItem.name)

                        #self.tabslist[tabType + str(newItem.id)] = newTab

                        #self.returnList[newTab] = returnTab
                    #else:
                        #print("DEBUG: Tabmanager: tab allready is open!")

                #else:
                    #newTab = tabCreator(parent=self.tabwidget, item=newItem)
                    #self.tabwidget.addTab(newTab, self.new_text + self.translate[tabType] + self.findNextNewIndex('new'+tabType))
                    #self.tabslist['new' + tabType + self.findNextNewIndex('new'+tabType)] = newTab
                    #self.setCurrentTab(newTab)

                    #self.returnList[newTab] = returnTab

            #else:

    
    def askToCloseTab(self,index):
        tab = self.tabwidget.widget(index)
        if tab.canCloseTab():
            self.closeTab(tab=tab)

    '''
        item is Animal, Owner or Visit 
        tabName is real text in tab, so it is need to be translated
    '''
    def closeTab(self, tabType=None, item=None, tab=None):
        #print('Tabmanager is closing Tab')
        #print('tabType:', tabType)
        #print('item:', item)
        #print('tab:', tab)
        digit=-1
        if tab != None:
            tabType = tab.getType()
            item = tab.getItem()
            digit = self.getNameNumber(tab)
        
        if tabType == 'Bill':
            if item != None: #check if tab is saved
                if tabType + str(item.id) in self.tabslist:
                    self.removeTab(self.tabslist[tabType + str(item.id)])
                    del self.tabslist[tabType + str(item.id)]
                    del self.returnList[tab]
            else:#tab is not saved
                if 'new' + tabType + str(tab.visit.id) in self.tabslist:
                    self.removeTab(self.tabslist['new' + tabType + str(tab.visit.id)])
                    del self.tabslist['new' + tabType + str(tab.visit.id)]
                    del self.returnList[tab]
            return   
                
        
        if tabType == 'VetTab':
            self.removeTab(self.tabslist[tabType])
            del self.tabslist[tabType]
            return
        
        if item != None:
            if item.getType() == 'Vet':
                self.removeTab(self.tabslist['VetTab'])
                del self.tabslist['VetTab']
                return
            if item.getType() + str(item.id) in self.tabslist:
                if self.returnList[self.tabslist[item.getType() + str(item.id)]] != None:
                    self.returnList[self.tabslist[item.getType() + str(item.id)]].addAskedItem(item)
                self.removeTab(self.tabslist[item.getType() + str(item.id)])
                del self.tabslist[item.getType() + str(item.id)]
                return
        
        if tabType in self.tabslist:
            self.removeTab(self.tabslist[tabType])
            del self.tabslist[tabType]
            return
        
        if tabType != None:
            newName = 'new' + tabType + (str(digit) if digit > 0 else '')
        else:
            newName = 'new' + item.getType() + (str(digit) if digit > 0 else '')
        #print('closeTab newName: ', newName)
        if newName in self.tabslist:
            self.removeTab(self.tabslist[newName])
            if self.returnList[self.tabslist[newName]] != None:
                if item != None:
                    self.returnList[self.tabslist[newName]].addAskedItem(item)
            del self.returnList[self.tabslist[newName]]
            del self.tabslist[newName]
        else:
            print('Could not create tab as input is: tabType=%, item=%, digit=%, tab=%',
                  (tabType, item, digit, tab))
    '''
        This funcktion is called when new item is saved and it is not closed.
        So it has item that is in data base so we start to protect it so
        that it can not be opened twice.
        
        TODO: Also it updates tabs that are related to this
    '''
    def newToSaved(self, tab):
        if tab == None:
            print('newToSaved: Tab can not be NoneType! Aborting!')
            return
        
        tabType = tab.getType()
        tabItem = tab.getItem()
        digit = self.getNameNumber(tab)
        
        if tabType == 'Bill':
            del self.tabslist['new' + tabType + str(tab.visit.id)]
            self.tabslist[tabType + str(tabItem.id)] = tab
            return
        
        #remove old key from list and add same tab with new key
        if 'new' + tabType + (str(digit) if digit > 0 else '') in self.tabslist:
            del self.tabslist['new' + tabType + (str(digit) if digit > 0 else '')]
            self.tabslist[tabType + str(tabItem.id)] = tab
        else:
            return
        
        #give TabItem to returnTab if it exist
        if self.returnList[tab] != None:
            self.returnList[tab].addAskedItem(tabItem)
            self.returnList[tab] = None
        
        #update Tab text
        if tabItem.getType == 'Visit':
            self.tabwidget.setTabText(self.tabwidget.indexOf(tab),self.visitText())
        else:
            self.tabwidget.setTabText(self.tabwidget.indexOf(tab),tabItem.name)
    

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
    
    def visitText(self):
        names = []
        for index in range(0,self.tabwidget.count()):
            names.append(self.tabwidget.tabText(index))
        index = 2
        if not 'Käynti' in names:
            return 'Käynti'
        else:
            while 'Käynti ' + str(index) in names:
                index += 1
            return 'Käynti ' + str(index)

    def billText(self):
        names = []
        for index in range(0,self.tabwidget.count()):
            names.append(self.tabwidget.tabText(index))
        index = 2
        if not 'Lasku' in names:
            return 'Lasku'
        else:
            while 'Lasku ' + str(index) in names:
                index += 1
            return 'Lasku ' + str(index)

    '''
        return '' if none object found whit this itemName
        return 2,3,4... until free number is found
    ''' 
    def findNextNewIndex(self, itemName):
        index = 2
        if not itemName in self.tabslist:
            return ''
        else:
            while itemName + str(index) in self.tabslist:
                index += 1
            return str(index)

    def getNameNumber(self, tab):
        print('getNameNumber input:',tab)
        name = self.tabwidget.tabText(self.tabwidget.indexOf(tab))
        temp = re.sub('[^0-9]', ' ', name.lower()).split()
        if len(temp) < 1:
            return -1
        else:
            return int(temp[len(temp)-1])
