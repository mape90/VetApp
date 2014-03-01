# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_listwidget.ui'
#
# Created: Fri Apr  5 10:20:33 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GenericTreeWidget(object):
    def setupUi(self, GenericTreeWidget):
        GenericTreeWidget.setObjectName(_fromUtf8("GenericTreeWidget"))
        GenericTreeWidget.resize(463, 376)
        self.verticalLayout = QtGui.QVBoxLayout(GenericTreeWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.topLayout = QtGui.QHBoxLayout()
        self.topLayout.setObjectName(_fromUtf8("topLayout"))
        self.textlabel = QtGui.QLabel(GenericTreeWidget)
        self.textlabel.setObjectName(_fromUtf8("textlabel"))
        self.topLayout.addWidget(self.textlabel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.topLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.topLayout)
        self.treeWidget = QtGui.QTreeWidget(GenericTreeWidget)
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, _fromUtf8("1"))
        self.verticalLayout.addWidget(self.treeWidget)
        self.bottomLayout = QtGui.QHBoxLayout()
        self.bottomLayout.setObjectName(_fromUtf8("bottomLayout"))
        self.verticalLayout.addLayout(self.bottomLayout)

        self.retranslateUi(GenericTreeWidget)
        QtCore.QMetaObject.connectSlotsByName(GenericTreeWidget)

    def retranslateUi(self, GenericTreeWidget):
        GenericTreeWidget.setWindowTitle(QtGui.QApplication.translate("GenericTreeWidget", "GenericTreeWidget", None, QtGui.QApplication.UnicodeUTF8))
        self.textlabel.setText(QtGui.QApplication.translate("GenericTreeWidget", "Teksti", None, QtGui.QApplication.UnicodeUTF8))

