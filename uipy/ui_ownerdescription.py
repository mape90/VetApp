# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ownerdescription.ui'
#
# Created: Tue Apr 16 17:28:34 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_OwnerDescriptionDialog(object):
    def setupUi(self, OwnerDescriptionDialog):
        OwnerDescriptionDialog.setObjectName(_fromUtf8("OwnerDescriptionDialog"))
        OwnerDescriptionDialog.resize(264, 182)
        self.verticalLayout = QtGui.QVBoxLayout(OwnerDescriptionDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(OwnerDescriptionDialog)
        self.label.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.specieComboBox = QtGui.QComboBox(OwnerDescriptionDialog)
        self.specieComboBox.setObjectName(_fromUtf8("specieComboBox"))
        self.horizontalLayout.addWidget(self.specieComboBox)
        self.newbutton = QtGui.QPushButton(OwnerDescriptionDialog)
        self.newbutton.setMaximumSize(QtCore.QSize(25, 25))
        self.newbutton.setObjectName(_fromUtf8("newbutton"))
        self.horizontalLayout.addWidget(self.newbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label_2 = QtGui.QLabel(OwnerDescriptionDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.plainTextEdit = QtGui.QPlainTextEdit(OwnerDescriptionDialog)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.canselButton = QtGui.QPushButton(OwnerDescriptionDialog)
        self.canselButton.setObjectName(_fromUtf8("canselButton"))
        self.horizontalLayout_2.addWidget(self.canselButton)
        self.saveButton = QtGui.QPushButton(OwnerDescriptionDialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(OwnerDescriptionDialog)
        QtCore.QMetaObject.connectSlotsByName(OwnerDescriptionDialog)

    def retranslateUi(self, OwnerDescriptionDialog):
        OwnerDescriptionDialog.setWindowTitle(QtGui.QApplication.translate("OwnerDescriptionDialog", "Omistajan ohje", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("OwnerDescriptionDialog", "Laji", None, QtGui.QApplication.UnicodeUTF8))
        self.newbutton.setText(QtGui.QApplication.translate("OwnerDescriptionDialog", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("OwnerDescriptionDialog", "Teksti", None, QtGui.QApplication.UnicodeUTF8))
        self.canselButton.setText(QtGui.QApplication.translate("OwnerDescriptionDialog", "Hylkää", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("OwnerDescriptionDialog", "Tallenna", None, QtGui.QApplication.UnicodeUTF8))

