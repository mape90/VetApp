# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_popup.ui'
#
# Created: Sat Mar 16 20:44:05 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(318, 128)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newItemlabel = QtGui.QLabel(Dialog)
        self.newItemlabel.setMinimumSize(QtCore.QSize(100, 0))
        self.newItemlabel.setMaximumSize(QtCore.QSize(120, 16777215))
        self.newItemlabel.setObjectName(_fromUtf8("newItemlabel"))
        self.horizontalLayout.addWidget(self.newItemlabel)
        self.lineEdit = QtGui.QLineEdit(Dialog)
        self.lineEdit.setMinimumSize(QtCore.QSize(200, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(200, 16777215))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboboxLabel = QtGui.QLabel(Dialog)
        self.comboboxLabel.setMinimumSize(QtCore.QSize(100, 0))
        self.comboboxLabel.setMaximumSize(QtCore.QSize(100, 16777215))
        self.comboboxLabel.setObjectName(_fromUtf8("comboboxLabel"))
        self.horizontalLayout_2.addWidget(self.comboboxLabel)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setMinimumSize(QtCore.QSize(200, 0))
        self.comboBox.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.horizontalLayout_2.addWidget(self.comboBox)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.cancelButton = QtGui.QPushButton(Dialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_3.addWidget(self.cancelButton)
        spacerItem4 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.saveButton = QtGui.QPushButton(Dialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.newItemlabel.setText(QtGui.QApplication.translate("Dialog", "Uusi Rotu", None, QtGui.QApplication.UnicodeUTF8))
        self.comboboxLabel.setText(QtGui.QApplication.translate("Dialog", "Laji", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Dialog", "Hylkää", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("Dialog", "Tallenna", None, QtGui.QApplication.UnicodeUTF8))

