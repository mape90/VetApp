# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uipy/ui_summary.ui'
#
# Created: Sat Jun 27 22:52:57 2015
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

class Ui_SummaryTab(object):
    def setupUi(self, SummaryTab):
        SummaryTab.setObjectName(_fromUtf8("SummaryTab"))
        SummaryTab.resize(715, 499)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SummaryTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label = QtGui.QLabel(SummaryTab)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.getInfoFromVisitButton = QtGui.QPushButton(SummaryTab)
        self.getInfoFromVisitButton.setObjectName(_fromUtf8("getInfoFromVisitButton"))
        self.horizontalLayout_3.addWidget(self.getInfoFromVisitButton)
        self.searchLayout = QtGui.QHBoxLayout()
        self.searchLayout.setObjectName(_fromUtf8("searchLayout"))
        self.horizontalLayout_3.addLayout(self.searchLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(SummaryTab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(False)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.ownerNameLabel = QtGui.QLabel(SummaryTab)
        self.ownerNameLabel.setObjectName(_fromUtf8("ownerNameLabel"))
        self.horizontalLayout_2.addWidget(self.ownerNameLabel)
        self.label_4 = QtGui.QLabel(SummaryTab)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        self.animalNameLabel = QtGui.QLabel(SummaryTab)
        self.animalNameLabel.setObjectName(_fromUtf8("animalNameLabel"))
        self.horizontalLayout_2.addWidget(self.animalNameLabel)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.plainTextEdit = QtGui.QPlainTextEdit(SummaryTab)
        self.plainTextEdit.setObjectName(_fromUtf8("plainTextEdit"))
        self.verticalLayout_2.addWidget(self.plainTextEdit)

        self.retranslateUi(SummaryTab)
        QtCore.QMetaObject.connectSlotsByName(SummaryTab)

    def retranslateUi(self, SummaryTab):
        SummaryTab.setWindowTitle(_translate("SummaryTab", "Form", None))
        self.label.setText(_translate("SummaryTab", "Yhteenveto/Hoito-ohje", None))
        self.getInfoFromVisitButton.setText(_translate("SummaryTab", "Hae lääketiedot käynnistä", None))
        self.label_2.setText(_translate("SummaryTab", "Omistaja:", None))
        self.ownerNameLabel.setText(_translate("SummaryTab", "owner_name", None))
        self.label_4.setText(_translate("SummaryTab", "Eläin", None))
        self.animalNameLabel.setText(_translate("SummaryTab", "animal_name", None))

