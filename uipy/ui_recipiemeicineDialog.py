# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_recipiemeicineDialog.ui'
#
# Created: Sun Apr 21 16:21:54 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RecipieMedicineDialog(object):
    def setupUi(self, RecipieMedicineDialog):
        RecipieMedicineDialog.setObjectName(_fromUtf8("RecipieMedicineDialog"))
        RecipieMedicineDialog.resize(243, 117)
        self.verticalLayout = QtGui.QVBoxLayout(RecipieMedicineDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.spinBox = QtGui.QSpinBox(RecipieMedicineDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox.sizePolicy().hasHeightForWidth())
        self.spinBox.setSizePolicy(sizePolicy)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.verticalLayout.addWidget(self.spinBox)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.closeButton = QtGui.QPushButton(RecipieMedicineDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.saveButton = QtGui.QPushButton(RecipieMedicineDialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(RecipieMedicineDialog)
        QtCore.QMetaObject.connectSlotsByName(RecipieMedicineDialog)

    def retranslateUi(self, RecipieMedicineDialog):
        RecipieMedicineDialog.setWindowTitle(QtGui.QApplication.translate("RecipieMedicineDialog", "Reseptilääke", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("RecipieMedicineDialog", "Sulje", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("RecipieMedicineDialog", "Tallenna", None, QtGui.QApplication.UnicodeUTF8))

