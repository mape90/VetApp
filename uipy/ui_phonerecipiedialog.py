# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_phonerecipiedialog.ui'
#
# Created: Sun Apr 21 13:37:49 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_PhoneRecipieDialog(object):
    def setupUi(self, PhoneRecipieDialog):
        PhoneRecipieDialog.setObjectName(_fromUtf8("PhoneRecipieDialog"))
        PhoneRecipieDialog.resize(361, 214)
        self.verticalLayout = QtGui.QVBoxLayout(PhoneRecipieDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.searchLineEditLayout = QtGui.QHBoxLayout()
        self.searchLineEditLayout.setObjectName(_fromUtf8("searchLineEditLayout"))
        self.label = QtGui.QLabel(PhoneRecipieDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.searchLineEditLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.searchLineEditLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.madetextLabel = QtGui.QLabel(PhoneRecipieDialog)
        self.madetextLabel.setMaximumSize(QtCore.QSize(80, 16777215))
        self.madetextLabel.setObjectName(_fromUtf8("madetextLabel"))
        self.horizontalLayout.addWidget(self.madetextLabel)
        self.madeTimeEdit = QtGui.QDateTimeEdit(PhoneRecipieDialog)
        self.madeTimeEdit.setCalendarPopup(True)
        self.madeTimeEdit.setObjectName(_fromUtf8("madeTimeEdit"))
        self.horizontalLayout.addWidget(self.madeTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(PhoneRecipieDialog)
        self.label_3.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.dateTimeEdit = QtGui.QDateTimeEdit(PhoneRecipieDialog)
        self.dateTimeEdit.setCalendarPopup(True)
        self.dateTimeEdit.setObjectName(_fromUtf8("dateTimeEdit"))
        self.horizontalLayout_2.addWidget(self.dateTimeEdit)
        self.nowButton = QtGui.QPushButton(PhoneRecipieDialog)
        self.nowButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.nowButton.setObjectName(_fromUtf8("nowButton"))
        self.horizontalLayout_2.addWidget(self.nowButton)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.canselButton = QtGui.QPushButton(PhoneRecipieDialog)
        self.canselButton.setObjectName(_fromUtf8("canselButton"))
        self.horizontalLayout_3.addWidget(self.canselButton)
        self.saveButton = QtGui.QPushButton(PhoneRecipieDialog)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_3.addWidget(self.saveButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(PhoneRecipieDialog)
        QtCore.QMetaObject.connectSlotsByName(PhoneRecipieDialog)

    def retranslateUi(self, PhoneRecipieDialog):
        PhoneRecipieDialog.setWindowTitle(QtGui.QApplication.translate("PhoneRecipieDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PhoneRecipieDialog", "Eläin", None, QtGui.QApplication.UnicodeUTF8))
        self.madetextLabel.setText(QtGui.QApplication.translate("PhoneRecipieDialog", "Tehty", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PhoneRecipieDialog", "Soitettu", None, QtGui.QApplication.UnicodeUTF8))
        self.nowButton.setToolTip(QtGui.QApplication.translate("PhoneRecipieDialog", "Asettaa soitto ajan tähän hetkeen", None, QtGui.QApplication.UnicodeUTF8))
        self.nowButton.setText(QtGui.QApplication.translate("PhoneRecipieDialog", "Nyt", None, QtGui.QApplication.UnicodeUTF8))
        self.canselButton.setText(QtGui.QApplication.translate("PhoneRecipieDialog", "Hylkää", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("PhoneRecipieDialog", "Tallenna", None, QtGui.QApplication.UnicodeUTF8))

