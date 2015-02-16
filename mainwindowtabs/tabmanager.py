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
    
    def createConnections(self):
        self.tabwidget.tabCloseRequested.connect(self.askToCloseTab)
    
    def change(self):
        self.tabwidget.setCurrentIndex(self.tabwidget.currentIndex()+1)
    
    def initialize(self, tabwidget):
        self.tabwidget = tabwidget
        self.tabwidget.setTabsClosable(True)
        self.tabwidget.setMovable(True)
        self.createConnections()
    

    def openTab(self, tabCreator, newItem=None, returnTab=None):
        
        print("DEBUG: TabManager->openTab(): tabCreator, newItem, returnTab:",(tabCreator, newItem, returnTab))
        
        tabType = tabCreator.__name__
        newTab = None
        key = "UNDEFINED"
        text = "UNDEFINED"


        from models.translationtables import g_unique_tabs, g_tab_name_dict
        
        #check if tab is one of unique tabs
        if tabType in g_unique_tabs:
            #check if it is in tablist
            if not tabType in self.tabslist:
                #if not then make it
                newTab = tabCreator(parent=self.tabwidget, item=newItem)
                key = tabType
                text = g_tab_name_dict[tabType]
            else:
                #set tab as current tab and return
                self.setCurrentTab(self.tabslist[tabType])
                return
        else:
            #not uniqueTab
            #check if we need to make 'new'-tab 
            #if item is None, or if item is dict (<Owner>,<Animal>)
            if newItem == None or newItem.__class__.__name__ == "dict":
                #make new tab
                newTab = tabCreator(parent=self.tabwidget, item=newItem) #tabCreator handles item what ever type it is

                index = self.findNextNewIndex('new'+tabType)            #make index '' or 1,2,3...
                newTab.setNumber(index)

                text = self.new_text + self.translate[tabType] + " " + index  #make text for gui
                key = 'new' + tabType + index                           #make key for dictionary
            elif tabType == "BillTab" and newItem.__class__.__name__ == 'Visit':
                # newBillTab<Visit.id>
                key = 'new' + tabType + str(newItem.id)
                
                #check if key is in tablist
                if key in self.tabslist:
                    self.setCurrentTab(self.tabslist[key])
                    return
                
                #make new tab
                newTab = tabCreator(parent=self.tabwidget, item=newItem) #tabCreator handles item what ever type it is
                
                index = str(newItem.id)
                newTab.setNumber(index)
                
                #handle new bill special case so that only one bill for one visit is possible to exsist
                text = self.new_text + self.translate[tabType] + " " + index  #make text for gui
            else:
                #so we have item that is in database so we just open it
                #check if it is open allready
                # <tabType><DB-id>
                key = tabType + str(newItem.id)
                
                if not key in self.tabslist:
                    #make tab
                    newTab = tabCreator(parent=self.tabwidget, item=newItem)
                    
                    #only Owner and animal tabs have special naming
                    if tabType in ["OwnerTab","AnimalTab"]:
                        text = newItem.name #owner or animal name
                    else:
                        text = self.translate[tabType] + " " + str(newItem.id) #Translated name of tabtype with DB-id

                else:
                    #item has allready tab so we just set it as curent tab and return
                    self.setCurrentTab(self.tabslist[key])
                    return

        print("DEBUG: TabManager->openTab(): key, text, returnTab:",(key, text, returnTab))

        self.tabwidget.addTab(newTab, text)
        self.tabslist[key] = newTab
        self.returnList[newTab] = returnTab
        self.setCurrentTab(newTab)

    
    def askToCloseTab(self,index):
        tab = self.tabwidget.widget(index)
        if tab.canCloseTab():
            self.closeTab(tab=tab)


    '''
        This function will close tabs and it wont check if there is changes or if
        items in it have been saved it should be done before calling this function
    
        tab cab be any tab type
    '''
    def closeTab(self, tab=None):
        print("DEBUG: closeTab: tab = ", tab)
        
        tabType = tab.__class__.__name__
        
        from models.translationtables import g_unique_tabs, g_tab_name_dict
        
        if tabType in g_unique_tabs:
            key = tabType
        else:
            #check if tab is saved
            if not tab.getItem() == None:
                #tab has saved item so we can get id from it
                item_id = str(tab.getItem().id)
                
                key = tabType + item_id

                #if saveAndClose is called then we have item but name is still
                #starting with new-word because it have not been updated
                if not key in self.tabslist:
                    key = 'new' + tabType + tab.getNumber()
                
            else:
                #so tab do not have saved item so it is new
                key = 'new' + tabType + tab.getNumber()
        

        #get tab object from list
        if key in self.tabslist:

            #give item for return tab
            if self.returnList[tab] != None:
                self.returnList[tab].addAskedItem(tab.getItem())

            #remove tab and update current tab to correct one
            #previous or returnTab
            self.removeTab(tab)

            #remove items from dictionarys
            del self.returnList[tab]
            del self.tabslist[key]
        else:
            #tab not found so print error message
            print("ERROR: closeTab: key:" , key , " not in tablist:", self.tabslist)


    '''
        This funcktion is called when new item is saved and it is not closed.
        So it has item that is in data base so we start to protect it so
        that it can not be opened twice.
    '''
    def newToSaved(self, tab):
        #check that our input is valid
        if tab == None:
            print('FATAL ERROR: tabmanager->newToSaved() tab is None!')
            return
        if tab.getItem() == None:
            print('FATAL ERROR: tabmanager->newToSaved() Item in tab is None! tab is: ', tab)
            return
        
        tabType = tab.__class__.__name__

        #make old and new keys
        key = 'new' + tabType + tab.getNumber()

        #make new key for tab
        new_key = tabType + str(tab.getItem().id)

        #update tab to match its new key
        if not key in self.tabslist:
            print("FATAL ERROR: tabmanager->newToSaved(), invalid key:",key,
                  "key is in tablist, but is should be unique")
            return

        #change tab key
        del self.tabslist[key]
        self.tabslist[new_key] = tab
        
        #give TabItem to returnTab if it exist
        if self.returnList[tab] != None:
            self.returnList[tab].addAskedItem(tabItem)
            self.returnList[tab] = None
        
       
        #update Tab text
        if tabType in ["OwnerTab","AnimalTab"]:
            text = newItem.name #owner or animal name
        else:
            text = self.translate[tabType] + " " + str(tab.getItem().id)
        
        self.tabwidget.setTabText(self.tabwidget.indexOf(tab),text)



    '''--------------HELPER FUNCTIONS-------------------'''
    
    def setCurrentTab(self, newTab):
        self.previoustab = self.tabwidget.currentWidget()
        self.tabwidget.setCurrentIndex(self.tabwidget.indexOf(newTab))
     
     
    '''
        This functio remove permanently selected tab
        and sets next one correctly if needed
    '''
    def removeTab(self, tab):
        if self.returnList[tab] != None and self.returnList[tab] in self.returnList:
            self.setCurrentTab(self.returnList[tab])
        
        #remove tab from tabwidget
        self.tabwidget.removeTab(self.tabwidget.indexOf(tab))
        
        #permanent delete tab
        tab.close()
        tab.setParent(None)
        del tab
        
        #check if previoustab is in tablist and set it current tab
        #now current and previous are same tab
        if self.previoustab in self.tabslist.values():
            self.tabwidget.setCurrentIndex(self.tabwidget.indexOf(self.previoustab))
    

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

