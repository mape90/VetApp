# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_visit.ui'
#
# Created: Thu Aug 29 19:13:07 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Visit(object):
    def setupUi(self, Visit):
        Visit.setObjectName(_fromUtf8("Visit"))
        Visit.resize(1047, 809)
        self.verticalLayout_9 = QtGui.QVBoxLayout(Visit)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ownerLayout = QtGui.QHBoxLayout()
        self.ownerLayout.setObjectName(_fromUtf8("ownerLayout"))
        self.owner = QtGui.QLabel(Visit)
        self.owner.setMinimumSize(QtCore.QSize(80, 0))
        self.owner.setObjectName(_fromUtf8("owner"))
        self.ownerLayout.addWidget(self.owner)
        self.verticalLayout.addLayout(self.ownerLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.startlabel = QtGui.QLabel(Visit)
        self.startlabel.setMinimumSize(QtCore.QSize(80, 0))
        self.startlabel.setMaximumSize(QtCore.QSize(80, 16777215))
        self.startlabel.setObjectName(_fromUtf8("startlabel"))
        self.horizontalLayout.addWidget(self.startlabel)
        self.startTimeEdit = QtGui.QDateTimeEdit(Visit)
        self.startTimeEdit.setObjectName(_fromUtf8("startTimeEdit"))
        self.horizontalLayout.addWidget(self.startTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.endlabel = QtGui.QLabel(Visit)
        self.endlabel.setMinimumSize(QtCore.QSize(80, 0))
        self.endlabel.setMaximumSize(QtCore.QSize(80, 16777215))
        self.endlabel.setObjectName(_fromUtf8("endlabel"))
        self.horizontalLayout_2.addWidget(self.endlabel)
        self.endTimeEdit = QtGui.QDateTimeEdit(Visit)
        self.endTimeEdit.setEnabled(True)
        self.endTimeEdit.setObjectName(_fromUtf8("endTimeEdit"))
        self.horizontalLayout_2.addWidget(self.endTimeEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(Visit)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.vetComboBox = QtGui.QComboBox(Visit)
        self.vetComboBox.setObjectName(_fromUtf8("vetComboBox"))
        self.horizontalLayout_3.addWidget(self.vetComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label_10 = QtGui.QLabel(Visit)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout.addWidget(self.label_10)
        self.animalNameLabel = QtGui.QLabel(Visit)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.animalNameLabel.setFont(font)
        self.animalNameLabel.setObjectName(_fromUtf8("animalNameLabel"))
        self.verticalLayout.addWidget(self.animalNameLabel)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.horizontalLayout_5.addLayout(self.verticalLayout)
        self.animalVisitInfoLayout = QtGui.QVBoxLayout()
        self.animalVisitInfoLayout.setObjectName(_fromUtf8("animalVisitInfoLayout"))
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.amamnesisLabel = QtGui.QLabel(Visit)
        self.amamnesisLabel.setObjectName(_fromUtf8("amamnesisLabel"))
        self.verticalLayout_8.addWidget(self.amamnesisLabel)
        self.amanuensisTextEdit = QtGui.QPlainTextEdit(Visit)
        self.amanuensisTextEdit.setObjectName(_fromUtf8("amanuensisTextEdit"))
        self.verticalLayout_8.addWidget(self.amanuensisTextEdit)
        self.animalVisitInfoLayout.addLayout(self.verticalLayout_8)
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.statusLabel = QtGui.QLabel(Visit)
        self.statusLabel.setObjectName(_fromUtf8("statusLabel"))
        self.verticalLayout_7.addWidget(self.statusLabel)
        self.statusTextEdit = QtGui.QPlainTextEdit(Visit)
        self.statusTextEdit.setObjectName(_fromUtf8("statusTextEdit"))
        self.verticalLayout_7.addWidget(self.statusTextEdit)
        self.animalVisitInfoLayout.addLayout(self.verticalLayout_7)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.diagnosisLabel = QtGui.QLabel(Visit)
        self.diagnosisLabel.setObjectName(_fromUtf8("diagnosisLabel"))
        self.verticalLayout_6.addWidget(self.diagnosisLabel)
        self.diagnosisTextEdit = QtGui.QPlainTextEdit(Visit)
        self.diagnosisTextEdit.setObjectName(_fromUtf8("diagnosisTextEdit"))
        self.verticalLayout_6.addWidget(self.diagnosisTextEdit)
        self.verticalLayout_10 = QtGui.QVBoxLayout()
        self.verticalLayout_10.setObjectName(_fromUtf8("verticalLayout_10"))
        self.threatmentLabel = QtGui.QLabel(Visit)
        self.threatmentLabel.setObjectName(_fromUtf8("threatmentLabel"))
        self.verticalLayout_10.addWidget(self.threatmentLabel)
        self.treatmentTextEdit = QtGui.QPlainTextEdit(Visit)
        self.treatmentTextEdit.setObjectName(_fromUtf8("treatmentTextEdit"))
        self.verticalLayout_10.addWidget(self.treatmentTextEdit)
        self.verticalLayout_6.addLayout(self.verticalLayout_10)
        self.animalVisitInfoLayout.addLayout(self.verticalLayout_6)
        self.horizontalLayout_5.addLayout(self.animalVisitInfoLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.animalSelectorLayout = QtGui.QHBoxLayout()
        self.animalSelectorLayout.setObjectName(_fromUtf8("animalSelectorLayout"))
        self.verticalLayout_2.addLayout(self.animalSelectorLayout)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.setStretch(1, 1)
        self.horizontalLayout_5.setStretch(2, 1)
        self.verticalLayout_9.addLayout(self.horizontalLayout_5)
        self.operationMainLayout = QtGui.QHBoxLayout()
        self.operationMainLayout.setObjectName(_fromUtf8("operationMainLayout"))
        self.operationLayout = QtGui.QHBoxLayout()
        self.operationLayout.setObjectName(_fromUtf8("operationLayout"))
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.operationNameLabel = QtGui.QLabel(Visit)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.operationNameLabel.setFont(font)
        self.operationNameLabel.setObjectName(_fromUtf8("operationNameLabel"))
        self.verticalLayout_5.addWidget(self.operationNameLabel)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.priceLabel = QtGui.QLabel(Visit)
        self.priceLabel.setMinimumSize(QtCore.QSize(80, 0))
        self.priceLabel.setObjectName(_fromUtf8("priceLabel"))
        self.horizontalLayout_6.addWidget(self.priceLabel)
        self.priceSpinBox = QtGui.QDoubleSpinBox(Visit)
        self.priceSpinBox.setMaximum(999999999.95)
        self.priceSpinBox.setSingleStep(0.05)
        self.priceSpinBox.setObjectName(_fromUtf8("priceSpinBox"))
        self.horizontalLayout_6.addWidget(self.priceSpinBox)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.retailPriceLabel_2 = QtGui.QLabel(Visit)
        self.retailPriceLabel_2.setMinimumSize(QtCore.QSize(83, 0))
        self.retailPriceLabel_2.setObjectName(_fromUtf8("retailPriceLabel_2"))
        self.horizontalLayout_7.addWidget(self.retailPriceLabel_2)
        self.retailPriceLabel = QtGui.QLabel(Visit)
        self.retailPriceLabel.setMinimumSize(QtCore.QSize(97, 0))
        self.retailPriceLabel.setFrameShape(QtGui.QFrame.Box)
        self.retailPriceLabel.setObjectName(_fromUtf8("retailPriceLabel"))
        self.horizontalLayout_7.addWidget(self.retailPriceLabel)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.descriptionLabel = QtGui.QLabel(Visit)
        self.descriptionLabel.setObjectName(_fromUtf8("descriptionLabel"))
        self.verticalLayout_4.addWidget(self.descriptionLabel)
        self.descriptionTextEdit = QtGui.QPlainTextEdit(Visit)
        self.descriptionTextEdit.setObjectName(_fromUtf8("descriptionTextEdit"))
        self.verticalLayout_4.addWidget(self.descriptionTextEdit)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem4)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.operationLayout.addLayout(self.verticalLayout_5)
        self.stackedWidget = QtGui.QStackedWidget(Visit)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.emptyPage = QtGui.QWidget()
        self.emptyPage.setObjectName(_fromUtf8("emptyPage"))
        self.stackedWidget.addWidget(self.emptyPage)
        self.ItemInfoPage = QtGui.QWidget()
        self.ItemInfoPage.setObjectName(_fromUtf8("ItemInfoPage"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.ItemInfoPage)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.ItemInfoPage)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.nameLabel = QtGui.QLabel(self.ItemInfoPage)
        self.nameLabel.setObjectName(_fromUtf8("nameLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.nameLabel)
        self.label_4 = QtGui.QLabel(self.ItemInfoPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_4)
        self.typeLabel = QtGui.QLabel(self.ItemInfoPage)
        self.typeLabel.setObjectName(_fromUtf8("typeLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.typeLabel)
        self.label_5 = QtGui.QLabel(self.ItemInfoPage)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_5)
        self.itemPriceLabel = QtGui.QLabel(self.ItemInfoPage)
        self.itemPriceLabel.setObjectName(_fromUtf8("itemPriceLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.itemPriceLabel)
        self.label_3 = QtGui.QLabel(self.ItemInfoPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_9.addLayout(self.formLayout)
        self.stackedWidget.addWidget(self.ItemInfoPage)
        self.treeWidgetPage = QtGui.QWidget()
        self.treeWidgetPage.setObjectName(_fromUtf8("treeWidgetPage"))
        self.itemTreeWidgetLayout = QtGui.QVBoxLayout(self.treeWidgetPage)
        self.itemTreeWidgetLayout.setObjectName(_fromUtf8("itemTreeWidgetLayout"))
        self.stackedWidget.addWidget(self.treeWidgetPage)
        self.operationLayout.addWidget(self.stackedWidget)
        self.operationLayout.setStretch(0, 1)
        self.operationLayout.setStretch(1, 2)
        self.operationMainLayout.addLayout(self.operationLayout)
        self.verticalLayout_9.addLayout(self.operationMainLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.billButton = QtGui.QPushButton(Visit)
        self.billButton.setObjectName(_fromUtf8("billButton"))
        self.horizontalLayout_4.addWidget(self.billButton)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem5)
        self.closeButton = QtGui.QPushButton(Visit)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_4.addWidget(self.closeButton)
        self.saveButton = QtGui.QPushButton(Visit)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.saveandcloseButton = QtGui.QPushButton(Visit)
        self.saveandcloseButton.setObjectName(_fromUtf8("saveandcloseButton"))
        self.horizontalLayout_4.addWidget(self.saveandcloseButton)
        self.verticalLayout_9.addLayout(self.horizontalLayout_4)
        self.verticalLayout_9.setStretch(0, 1)
        self.verticalLayout_9.setStretch(1, 2)

        self.retranslateUi(Visit)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(Visit)

    def retranslateUi(self, Visit):
        Visit.setWindowTitle(QtGui.QApplication.translate("Visit", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.owner.setText(QtGui.QApplication.translate("Visit", "Omistaja", None, QtGui.QApplication.UnicodeUTF8))
        self.startlabel.setText(QtGui.QApplication.translate("Visit", "Aloitus aika", None, QtGui.QApplication.UnicodeUTF8))
        self.endlabel.setText(QtGui.QApplication.translate("Visit", "Lopetus aika", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Visit", "Eläinlääkäri", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("Visit", "Valittu Eläin:", None, QtGui.QApplication.UnicodeUTF8))
        self.animalNameLabel.setText(QtGui.QApplication.translate("Visit", "Ei valittua eläintä", None, QtGui.QApplication.UnicodeUTF8))
        self.amamnesisLabel.setText(QtGui.QApplication.translate("Visit", "Anamneesi", None, QtGui.QApplication.UnicodeUTF8))
        self.statusLabel.setText(QtGui.QApplication.translate("Visit", "Status", None, QtGui.QApplication.UnicodeUTF8))
        self.diagnosisLabel.setText(QtGui.QApplication.translate("Visit", "Diagnoosi", None, QtGui.QApplication.UnicodeUTF8))
        self.threatmentLabel.setText(QtGui.QApplication.translate("Visit", "Hoito-ohje", None, QtGui.QApplication.UnicodeUTF8))
        self.operationNameLabel.setText(QtGui.QApplication.translate("Visit", "Nimi", None, QtGui.QApplication.UnicodeUTF8))
        self.priceLabel.setText(QtGui.QApplication.translate("Visit", "Hinta", None, QtGui.QApplication.UnicodeUTF8))
        self.priceSpinBox.setToolTip(QtGui.QApplication.translate("Visit", "Painamalla Ctrl:n pohjaan voit rullata lukuja nopeammin", None, QtGui.QApplication.UnicodeUTF8))
        self.retailPriceLabel_2.setText(QtGui.QApplication.translate("Visit", "Ohjehinta", None, QtGui.QApplication.UnicodeUTF8))
        self.retailPriceLabel.setText(QtGui.QApplication.translate("Visit", "0.00", None, QtGui.QApplication.UnicodeUTF8))
        self.descriptionLabel.setText(QtGui.QApplication.translate("Visit", "Kuvaus", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Visit", "Nimi", None, QtGui.QApplication.UnicodeUTF8))
        self.nameLabel.setText(QtGui.QApplication.translate("Visit", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Visit", "Tyyppi", None, QtGui.QApplication.UnicodeUTF8))
        self.typeLabel.setText(QtGui.QApplication.translate("Visit", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Visit", "Hinta", None, QtGui.QApplication.UnicodeUTF8))
        self.itemPriceLabel.setText(QtGui.QApplication.translate("Visit", "0.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Visit", "Tuotetiedot", None, QtGui.QApplication.UnicodeUTF8))
        self.billButton.setText(QtGui.QApplication.translate("Visit", "Lasku", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Visit", "Poistu", None, QtGui.QApplication.UnicodeUTF8))
        self.saveButton.setText(QtGui.QApplication.translate("Visit", "Tallenna", None, QtGui.QApplication.UnicodeUTF8))
        self.saveandcloseButton.setText(QtGui.QApplication.translate("Visit", "Tallenna ja poistu", None, QtGui.QApplication.UnicodeUTF8))

