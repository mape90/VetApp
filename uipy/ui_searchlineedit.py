# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_searchlineedit.ui'
#
# Created: Thu Mar 14 21:48:28 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchLineEdit(object):
    def setupUi(self, SearchLineEdit):
        SearchLineEdit.setObjectName(_fromUtf8("SearchLineEdit"))
        SearchLineEdit.resize(596, 494)
        self.verticalLayout = QtGui.QVBoxLayout(SearchLineEdit)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.editor = QtGui.QLineEdit(SearchLineEdit)
        self.editor.setMinimumSize(QtCore.QSize(100, 20))
        self.editor.setMaximumSize(QtCore.QSize(16777215, 20))
        self.editor.setObjectName(_fromUtf8("editor"))
        self.horizontalLayout.addWidget(self.editor)
        self.newButton = QtGui.QPushButton(SearchLineEdit)
        self.newButton.setMinimumSize(QtCore.QSize(25, 25))
        self.newButton.setMaximumSize(QtCore.QSize(25, 25))
        self.newButton.setText(_fromUtf8(""))
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.horizontalLayout.addWidget(self.newButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.popup = QtGui.QTreeWidget(SearchLineEdit)
        self.popup.setObjectName(_fromUtf8("popup"))
        self.popup.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.popup)

        self.retranslateUi(SearchLineEdit)
        QtCore.QMetaObject.connectSlotsByName(SearchLineEdit)

    def retranslateUi(self, SearchLineEdit):
        SearchLineEdit.setWindowTitle(QtGui.QApplication.translate("SearchLineEdit", "Form", None, QtGui.QApplication.UnicodeUTF8))

