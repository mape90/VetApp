# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_search.ui'
#
# Created: Thu Aug 29 13:39:40 2013
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_SearchTab(object):
    def setupUi(self, SearchTab):
        SearchTab.setObjectName(_fromUtf8("SearchTab"))
        SearchTab.resize(632, 463)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(SearchTab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(SearchTab)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.mainSearchLineLayout = QtGui.QHBoxLayout()
        self.mainSearchLineLayout.setObjectName(_fromUtf8("mainSearchLineLayout"))
        self.searchButton = QtGui.QPushButton(SearchTab)
        self.searchButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.searchButton.setObjectName(_fromUtf8("searchButton"))
        self.mainSearchLineLayout.addWidget(self.searchButton)
        self.openButton = QtGui.QPushButton(SearchTab)
        self.openButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.openButton.setObjectName(_fromUtf8("openButton"))
        self.mainSearchLineLayout.addWidget(self.openButton)
        self.verticalLayout.addLayout(self.mainSearchLineLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(SearchTab)
        self.label_2.setMinimumSize(QtCore.QSize(80, 0))
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.typeComboBox = QtGui.QComboBox(SearchTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeComboBox.sizePolicy().hasHeightForWidth())
        self.typeComboBox.setSizePolicy(sizePolicy)
        self.typeComboBox.setObjectName(_fromUtf8("typeComboBox"))
        self.horizontalLayout.addWidget(self.typeComboBox)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.stackedWidget = QtGui.QStackedWidget(SearchTab)
        self.stackedWidget.setObjectName(_fromUtf8("stackedWidget"))
        self.emptyPage = QtGui.QWidget()
        self.emptyPage.setObjectName(_fromUtf8("emptyPage"))
        self.stackedWidget.addWidget(self.emptyPage)
        self.AnimalPage = QtGui.QWidget()
        self.AnimalPage.setObjectName(_fromUtf8("AnimalPage"))
        self.animalLayout = QtGui.QHBoxLayout(self.AnimalPage)
        self.animalLayout.setObjectName(_fromUtf8("animalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_7 = QtGui.QLabel(self.AnimalPage)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_7)
        self.specieBox = QtGui.QComboBox(self.AnimalPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.specieBox.sizePolicy().hasHeightForWidth())
        self.specieBox.setSizePolicy(sizePolicy)
        self.specieBox.setObjectName(_fromUtf8("specieBox"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.specieBox)
        self.label_8 = QtGui.QLabel(self.AnimalPage)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_8)
        self.label_3 = QtGui.QLabel(self.AnimalPage)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.colorBox = QtGui.QComboBox(self.AnimalPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorBox.sizePolicy().hasHeightForWidth())
        self.colorBox.setSizePolicy(sizePolicy)
        self.colorBox.setObjectName(_fromUtf8("colorBox"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.colorBox)
        self.label_4 = QtGui.QLabel(self.AnimalPage)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_4)
        self.sexBox = QtGui.QComboBox(self.AnimalPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sexBox.sizePolicy().hasHeightForWidth())
        self.sexBox.setSizePolicy(sizePolicy)
        self.sexBox.setObjectName(_fromUtf8("sexBox"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.sexBox)
        self.label_5 = QtGui.QLabel(self.AnimalPage)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.LabelRole, self.label_5)
        self.label_6 = QtGui.QLabel(self.AnimalPage)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.LabelRole, self.label_6)
        self.dateEdit = QtGui.QDateEdit(self.AnimalPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit.sizePolicy().hasHeightForWidth())
        self.dateEdit.setSizePolicy(sizePolicy)
        self.dateEdit.setObjectName(_fromUtf8("dateEdit"))
        self.formLayout.setWidget(6, QtGui.QFormLayout.FieldRole, self.dateEdit)
        self.dateEdit_2 = QtGui.QDateEdit(self.AnimalPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dateEdit_2.sizePolicy().hasHeightForWidth())
        self.dateEdit_2.setSizePolicy(sizePolicy)
        self.dateEdit_2.setObjectName(_fromUtf8("dateEdit_2"))
        self.formLayout.setWidget(7, QtGui.QFormLayout.FieldRole, self.dateEdit_2)
        self.raceBox = QtGui.QComboBox(self.AnimalPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.raceBox.sizePolicy().hasHeightForWidth())
        self.raceBox.setSizePolicy(sizePolicy)
        self.raceBox.setObjectName(_fromUtf8("raceBox"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.raceBox)
        self.label_18 = QtGui.QLabel(self.AnimalPage)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_18)
        self.animalLayout.addLayout(self.formLayout)
        self.stackedWidget.addWidget(self.AnimalPage)
        self.VisitPage = QtGui.QWidget()
        self.VisitPage.setObjectName(_fromUtf8("VisitPage"))
        self.visitLayout = QtGui.QVBoxLayout(self.VisitPage)
        self.visitLayout.setObjectName(_fromUtf8("visitLayout"))
        self.VisitInnerLayout = QtGui.QFormLayout()
        self.VisitInnerLayout.setObjectName(_fromUtf8("VisitInnerLayout"))
        self.label_9 = QtGui.QLabel(self.VisitPage)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.VisitInnerLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_9)
        self.label_10 = QtGui.QLabel(self.VisitPage)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.VisitInnerLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_10)
        self.label_11 = QtGui.QLabel(self.VisitPage)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.VisitInnerLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_11)
        self.label_12 = QtGui.QLabel(self.VisitPage)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.VisitInnerLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_12)
        self.label_13 = QtGui.QLabel(self.VisitPage)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.VisitInnerLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.label_13)
        self.visitVetBox = QtGui.QComboBox(self.VisitPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.visitVetBox.sizePolicy().hasHeightForWidth())
        self.visitVetBox.setSizePolicy(sizePolicy)
        self.visitVetBox.setObjectName(_fromUtf8("visitVetBox"))
        self.VisitInnerLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.visitVetBox)
        self.visitStartEdit = QtGui.QDateEdit(self.VisitPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.visitStartEdit.sizePolicy().hasHeightForWidth())
        self.visitStartEdit.setSizePolicy(sizePolicy)
        self.visitStartEdit.setObjectName(_fromUtf8("visitStartEdit"))
        self.VisitInnerLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.visitStartEdit)
        self.VisitEndEdit = QtGui.QDateEdit(self.VisitPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VisitEndEdit.sizePolicy().hasHeightForWidth())
        self.VisitEndEdit.setSizePolicy(sizePolicy)
        self.VisitEndEdit.setObjectName(_fromUtf8("VisitEndEdit"))
        self.VisitInnerLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.VisitEndEdit)
        self.label_19 = QtGui.QLabel(self.VisitPage)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.VisitInnerLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_19)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.VisitInnerLayout.setItem(6, QtGui.QFormLayout.FieldRole, spacerItem)
        self.visitLayout.addLayout(self.VisitInnerLayout)
        self.stackedWidget.addWidget(self.VisitPage)
        self.BillPage = QtGui.QWidget()
        self.BillPage.setObjectName(_fromUtf8("BillPage"))
        self.billLayout = QtGui.QVBoxLayout(self.BillPage)
        self.billLayout.setObjectName(_fromUtf8("billLayout"))
        self.BillInnerLayout = QtGui.QFormLayout()
        self.BillInnerLayout.setObjectName(_fromUtf8("BillInnerLayout"))
        self.label_14 = QtGui.QLabel(self.BillPage)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.BillInnerLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_14)
        self.label_15 = QtGui.QLabel(self.BillPage)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.BillInnerLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_15)
        self.label_16 = QtGui.QLabel(self.BillPage)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.BillInnerLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_16)
        self.label_17 = QtGui.QLabel(self.BillPage)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.BillInnerLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.label_17)
        self.billEndEdit = QtGui.QDateEdit(self.BillPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.billEndEdit.sizePolicy().hasHeightForWidth())
        self.billEndEdit.setSizePolicy(sizePolicy)
        self.billEndEdit.setObjectName(_fromUtf8("billEndEdit"))
        self.BillInnerLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.billEndEdit)
        self.billStartEdit = QtGui.QDateEdit(self.BillPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.billStartEdit.sizePolicy().hasHeightForWidth())
        self.billStartEdit.setSizePolicy(sizePolicy)
        self.billStartEdit.setObjectName(_fromUtf8("billStartEdit"))
        self.BillInnerLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.billStartEdit)
        self.billVetBox = QtGui.QComboBox(self.BillPage)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.billVetBox.sizePolicy().hasHeightForWidth())
        self.billVetBox.setSizePolicy(sizePolicy)
        self.billVetBox.setObjectName(_fromUtf8("billVetBox"))
        self.BillInnerLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.billVetBox)
        self.label_20 = QtGui.QLabel(self.BillPage)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.BillInnerLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_20)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.BillInnerLayout.setItem(5, QtGui.QFormLayout.LabelRole, spacerItem1)
        self.billLayout.addLayout(self.BillInnerLayout)
        self.stackedWidget.addWidget(self.BillPage)
        self.verticalLayout.addWidget(self.stackedWidget)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)

        self.retranslateUi(SearchTab)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(SearchTab)

    def retranslateUi(self, SearchTab):
        SearchTab.setWindowTitle(QtGui.QApplication.translate("SearchTab", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("SearchTab", "Haku", None, QtGui.QApplication.UnicodeUTF8))
        self.searchButton.setText(QtGui.QApplication.translate("SearchTab", "Hae", None, QtGui.QApplication.UnicodeUTF8))
        self.openButton.setText(QtGui.QApplication.translate("SearchTab", "Avaa", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("SearchTab", "Tyyppi", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("SearchTab", "Laji", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("SearchTab", "Rotu", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("SearchTab", "Väri", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("SearchTab", "Sukupuoli", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("SearchTab", "Alkaen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("SearchTab", "Päättyen", None, QtGui.QApplication.UnicodeUTF8))
        self.dateEdit.setDisplayFormat(QtGui.QApplication.translate("SearchTab", "dd.MM.yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.dateEdit_2.setDisplayFormat(QtGui.QApplication.translate("SearchTab", "dd.MM.yyyy", None, QtGui.QApplication.UnicodeUTF8))
        self.label_18.setText(QtGui.QApplication.translate("SearchTab", "Syntymäaika:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("SearchTab", "Omistaja", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("SearchTab", "Eläin", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setText(QtGui.QApplication.translate("SearchTab", "Eläinlääkäri", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setText(QtGui.QApplication.translate("SearchTab", "Alkaen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_13.setText(QtGui.QApplication.translate("SearchTab", "Päättyen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_19.setText(QtGui.QApplication.translate("SearchTab", "Ajankohta:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("SearchTab", "Omistaja", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("SearchTab", "Eläinlääkäri", None, QtGui.QApplication.UnicodeUTF8))
        self.label_16.setText(QtGui.QApplication.translate("SearchTab", "Alkaen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_17.setText(QtGui.QApplication.translate("SearchTab", "Päättyen", None, QtGui.QApplication.UnicodeUTF8))
        self.label_20.setText(QtGui.QApplication.translate("SearchTab", "Ajankohta", None, QtGui.QApplication.UnicodeUTF8))

