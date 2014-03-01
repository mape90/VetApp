# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainmenu.ui'
#
# Created: Wed Apr 24 09:16:23 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        MainMenu.setObjectName(_fromUtf8("MainMenu"))
        MainMenu.resize(1114, 714)
        self.verticalLayout_2 = QtGui.QVBoxLayout(MainMenu)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.new_visit_button = QtGui.QPushButton(MainMenu)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.new_visit_button.sizePolicy().hasHeightForWidth())
        self.new_visit_button.setSizePolicy(sizePolicy)
        self.new_visit_button.setMinimumSize(QtCore.QSize(100, 50))
        self.new_visit_button.setObjectName(_fromUtf8("new_visit_button"))
        self.verticalLayout.addWidget(self.new_visit_button)
        self.owner_button = QtGui.QPushButton(MainMenu)
        self.owner_button.setMinimumSize(QtCore.QSize(0, 50))
        self.owner_button.setObjectName(_fromUtf8("owner_button"))
        self.verticalLayout.addWidget(self.owner_button)
        self.animal_button = QtGui.QPushButton(MainMenu)
        self.animal_button.setMinimumSize(QtCore.QSize(0, 50))
        self.animal_button.setObjectName(_fromUtf8("animal_button"))
        self.verticalLayout.addWidget(self.animal_button)
        self.search_button = QtGui.QPushButton(MainMenu)
        self.search_button.setMinimumSize(QtCore.QSize(0, 50))
        self.search_button.setObjectName(_fromUtf8("search_button"))
        self.verticalLayout.addWidget(self.search_button)
        self.vetbutton = QtGui.QPushButton(MainMenu)
        self.vetbutton.setMinimumSize(QtCore.QSize(0, 50))
        self.vetbutton.setObjectName(_fromUtf8("vetbutton"))
        self.verticalLayout.addWidget(self.vetbutton)
        self.drugButton = QtGui.QPushButton(MainMenu)
        self.drugButton.setEnabled(False)
        self.drugButton.setMinimumSize(QtCore.QSize(0, 50))
        self.drugButton.setObjectName(_fromUtf8("drugButton"))
        self.verticalLayout.addWidget(self.drugButton)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.grindLayout = QtGui.QGridLayout()
        self.grindLayout.setObjectName(_fromUtf8("grindLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.grindLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.grindLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        MainMenu.setWindowTitle(QtGui.QApplication.translate("MainMenu", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.new_visit_button.setText(QtGui.QApplication.translate("MainMenu", "Uusi käynti", None, QtGui.QApplication.UnicodeUTF8))
        self.owner_button.setText(QtGui.QApplication.translate("MainMenu", "Uusi Omistaja", None, QtGui.QApplication.UnicodeUTF8))
        self.animal_button.setText(QtGui.QApplication.translate("MainMenu", "Uusi Eläin", None, QtGui.QApplication.UnicodeUTF8))
        self.search_button.setText(QtGui.QApplication.translate("MainMenu", "Haku", None, QtGui.QApplication.UnicodeUTF8))
        self.vetbutton.setText(QtGui.QApplication.translate("MainMenu", "Eläinlääkäri", None, QtGui.QApplication.UnicodeUTF8))
        self.drugButton.setText(QtGui.QApplication.translate("MainMenu", "Huumeseuranta", None, QtGui.QApplication.UnicodeUTF8))

