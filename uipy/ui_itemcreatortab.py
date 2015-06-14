# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uipy/ui_itemcreatortab.ui'
#
# Created: Sun Jun 14 12:32:21 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ItemCreatorTab(object):
    def setupUi(self, ItemCreatorTab):
        ItemCreatorTab.setObjectName(_fromUtf8("ItemCreatorTab"))
        ItemCreatorTab.resize(814, 519)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(ItemCreatorTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.searchlayout = QtGui.QVBoxLayout()
        self.searchlayout.setObjectName(_fromUtf8("searchlayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newItemButton = QtGui.QPushButton(ItemCreatorTab)
        self.newItemButton.setObjectName(_fromUtf8("newItemButton"))
        self.horizontalLayout.addWidget(self.newItemButton)
        self.deleteItemButton = QtGui.QPushButton(ItemCreatorTab)
        self.deleteItemButton.setObjectName(_fromUtf8("deleteItemButton"))
        self.horizontalLayout.addWidget(self.deleteItemButton)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.openItemButton = QtGui.QPushButton(ItemCreatorTab)
        self.openItemButton.setObjectName(_fromUtf8("openItemButton"))
        self.horizontalLayout.addWidget(self.openItemButton)
        self.searchlayout.addLayout(self.horizontalLayout)
        self.listView = QtGui.QListView(ItemCreatorTab)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.searchlayout.addWidget(self.listView)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.searchlayout.addItem(spacerItem1)
        self.horizontalLayout_2.addLayout(self.searchlayout)
        self.itemdialoglayout = QtGui.QVBoxLayout()
        self.itemdialoglayout.setObjectName(_fromUtf8("itemdialoglayout"))
        self.horizontalLayout_2.addLayout(self.itemdialoglayout)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.retranslateUi(ItemCreatorTab)
        QtCore.QMetaObject.connectSlotsByName(ItemCreatorTab)

    def retranslateUi(self, ItemCreatorTab):
        ItemCreatorTab.setWindowTitle(_translate("ItemCreatorTab", "Form", None))
        self.newItemButton.setText(_translate("ItemCreatorTab", "Uusi tuote", None))
        self.deleteItemButton.setText(_translate("ItemCreatorTab", "Poista pysyvästi", None))
        self.openItemButton.setText(_translate("ItemCreatorTab", "Avaa", None))

