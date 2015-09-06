# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uipy/ui_login.ui'
#
# Created: Sun Sep  6 11:20:04 2015
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

class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName(_fromUtf8("LoginDialog"))
        LoginDialog.resize(300, 134)
        self.verticalLayout_2 = QtGui.QVBoxLayout(LoginDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(LoginDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(80, 20))
        self.label.setMaximumSize(QtCore.QSize(80, 20))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.vetComboBox = QtGui.QComboBox(LoginDialog)
        self.vetComboBox.setMinimumSize(QtCore.QSize(0, 25))
        self.vetComboBox.setMaximumSize(QtCore.QSize(16777215, 25))
        self.vetComboBox.setObjectName(_fromUtf8("vetComboBox"))
        self.horizontalLayout.addWidget(self.vetComboBox)
        self.newVetButton = QtGui.QPushButton(LoginDialog)
        self.newVetButton.setMinimumSize(QtCore.QSize(50, 27))
        self.newVetButton.setMaximumSize(QtCore.QSize(50, 27))
        self.newVetButton.setObjectName(_fromUtf8("newVetButton"))
        self.horizontalLayout.addWidget(self.newVetButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_2 = QtGui.QLabel(LoginDialog)
        self.label_2.setMinimumSize(QtCore.QSize(80, 20))
        self.label_2.setMaximumSize(QtCore.QSize(80, 20))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.passwordLineEdit = QtGui.QLineEdit(LoginDialog)
        self.passwordLineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.passwordLineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.passwordLineEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwordLineEdit.setObjectName(_fromUtf8("passwordLineEdit"))
        self.horizontalLayout_2.addWidget(self.passwordLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.loginButton = QtGui.QPushButton(LoginDialog)
        self.loginButton.setObjectName(_fromUtf8("loginButton"))
        self.horizontalLayout_3.addWidget(self.loginButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Kirjaudu", None))
        self.label.setText(_translate("LoginDialog", "Eläinlääkäri", None))
        self.newVetButton.setText(_translate("LoginDialog", "Uusi", None))
        self.label_2.setText(_translate("LoginDialog", "Salasana", None))
        self.loginButton.setText(_translate("LoginDialog", "Kirjaudu", None))

