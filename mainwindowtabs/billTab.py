#!/usr/bin/python
# -*- coding: utf-8

'''
Created on Apr 22, 2013

@author: mp
'''
'''
    This file is part of VetApp.

    VetApp is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    VetApp is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with VetApp.  If not, see <http://www.gnu.org/licenses/>.
'''


from mainwindowtabs.generictab import GenericTab
from mainwindowtabs.printFileCreator import PrintFileCreator
from uipy.ui_bill import Ui_BillTab
from models import SqlHandler

from mainwindowtabs import Tabmanager

import datetime
from math import ceil

from PyQt4.QtGui import QTextDocument, QPrinter, QPrintPreviewDialog, QPrintDialog
from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import QDate

class BillTab(GenericTab):
    def __init__(self, parent=None,item=None):
        GenericTab.__init__(self, parent=parent, item=item)
        self.ui = Ui_BillTab()
        self.ui.setupUi(self)
        
        self.print_format_path = "print_formating.html"
        self.payment_methods = ['Käteinen','Pankkikortti','Luottokortti','Pankkisiirto','Muu']
        self.index_number_start = 0
        
        self.creator = PrintFileCreator(path=self.print_format_path)
        self.configure()
        self.configureConnection()
        self.setBasicInfo()
        
        if self.item.getType() == 'Visit':
            self.visit = self.item
            self.item = None
            self.ui.indexNumberLabel.setText(str(self.calcIndexNumber()))
        else:
            self.visit = self.item.visit
     
    def configure(self):  
        pass
       
    def configureConnection(self):
        self.ui.printButton.clicked.connect(self.printBill)
        
        self.ui.savePushButton.clicked.connect(self.saveTab)
        
        self.ui.DueDateTimeComboBox.currentIndexChanged.connect(self.dueDateChanged)
        
        self.ui.precentSlider.valueChanged.connect(self.changePercent)
        self.ui.precentSlider.valueChanged.connect(self.updateEndPrice)
        
        self.ui.clinic_radio_button.toggled.connect(self.clinicVisitPageChange)
        self.ui.setDefaultclinicPriceButton.clicked.connect(self.setDefaultClinicPrice)
        
        self.ui.KmSpinBox.valueChanged['double'].connect(self.updateKmData)

        self.ui.clinicPriceSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.KmPriceSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.visitPriceSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.operationSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.accessoriesSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.labSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.medicineSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        self.ui.dietSpinBox.valueChanged['double'].connect(self.updateEndPrice)
        
        self.ui.nowButton.clicked.connect(self.setToday)
        self.ui.all_pushButton.clicked.connect(self.fullPricePaid)
        
        self.ui.roundButton1.clicked.connect(self.roundEndPrice1)
        self.ui.roundButton05.clicked.connect(self.roundEndPrice05)
        self.ui.roundButton005.clicked.connect(self.roundEndPrice005)
        
        self.ui.toVisitButton.clicked.connect(self.openVisit)
        
        self.ui.updateFromVisitButton.clicked.connect(self.getDataFromVisit)

    
    def getDataFromVisit(self):
        self.setPrices(self.visit)
    
    def setBasicInfo(self):
        self.setPaymnetMethods()
        self.setDueDates()
        self.setAlv1Names()
        self.setAlv2Names()
        self.setAlv3Names()
        
        if self.item != None:
            if self.item.getType() != 'Visit':
                self.ui.ownerLabel.setText(self.item.visit.owner.name)   
                if self.item.km < 0.001 and self.item.km_payment < 0.001:
                    self.ui.clinic_radio_button.setChecked(True)
                    self.ui.clinicPriceSpinBox.setValue(self.item.clinic_payment)
                else:
                    self.ui.clinic_radio_button.setChecked(False)
                    self.ui.KmSpinBox.setValue(self.item.km)
                    self.ui.visitPriceSpinBox.setValue(self.item.clinic_payment)
                    self.ui.KmPriceSpinBox.setValue(self.item.km_payment)
                self.ui.operationSpinBox.setValue(self.item.operations_payment)
                self.ui.accessoriesSpinBox.setValue(self.item.accessories_payment)
                self.ui.labSpinBox.setValue(self.item.lab_payment)
                self.ui.medicineSpinBox.setValue(self.item.medicines_payment)
                self.ui.dietSpinBox.setValue(self.item.diet_payment)
                self.ui.otherInfoTextEdit.setPlainText(self.item.other_info)
                self.ui.paymentComboBox.setCurrentIndex(self.ui.paymentComboBox.findData(self.item.payment_method))
                self.ui.paidSpinBox.setValue(self.item.paid_value)
                self.ui.paidDateEdit.setDate(self.item.paid_time)
                self.ui.DueDateEdit.setDate(self.item.due_date)
                self.ui.precentSlider.setValue(self.item.extra_percent)
                self.ui.indexNumberLabel.setText(str(self.item.index_number)) 
                
            else:
                self.ui.ownerLabel.setText(self.item.owner.name)
                self.ui.clinicPriceSpinBox.setValue(28.06) #TODO: take default clinicPrice from configServer
                self.setPrices(self.item) #item is visit
            
        else:
            self.errorMessage("ERROR: BillTab: setBasicInfo: item is None")
    
    def openVisit(self):
        from mainwindowtabs.visittab import VisitTab
        Tabmanager.openTab(VisitTab, self.visit)
    
    def calcIndexNumber(self):
        base_number = self.visit.id+self.index_number_start+100  #TODO: take start point from configServer
        data = [int(i) for i in reversed(str(base_number))]
        cn = [7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1, 7, 3, 1]
        total = 0
        for i in range(0,len(data)):
            total += data[i]*cn[i]
        
        check_sum = int(ceil(total/10.0))*10 - total
        return base_number*10 + check_sum
    
    def setDefaultClinicPrice(self):
        self.ui.clinicPriceSpinBox.setValue(28.06)  #TODO: take default clinicPrice from configServer
    
        
    def updatePriceList(self, operation, old_prices):
        _type = operation.getType()
        
        prices = {}
        prices["operation_price"] = 0.0
        prices["accesories_price"] = 0.0
        prices["lab_price"] = 0.0
        prices["medicine_price"] = 0.0
        prices["diet_price"] = 0.0
        
        if _type is 'Basic':
            prices["operation_price"] += operation.price
        elif _type is 'Vaccination':
            prices["operation_price"] += operation.price
            if operation.base.item != None:
                prices["medicine_price"] += operation.base.item.price
            else:
                self.errorMessage('ERROR: BillTab.setPrices(): operation.hasItem() is true but item is None!')
        elif _type is 'Surgery':
            for item in operation.items:
                from models.translationtables import g_item_alv_dict
                if g_item_alv_dict[item.item.__class__.__name__] == 1:
                    prices["accesories_price"] += item.item.price * item.count
                elif g_item_alv_dict[item.item.__class__.__name__] == 2:
                    prices["medicine_price"] += item.item.price * item.count
                elif g_item_alv_dict[item.item.__class__.__name__] == 3:
                    prices["diet_price"] += item.item.price * item.count
                else:
                    self.errorMessage('ERROR: BillTab.setPrices(): ALV is not valid!') 
        elif _type is 'Lab':
            price_dict["lab_price"] += operation.price
        elif _type is 'Medication':
            if operation.price > 0.001:
                prices["medicine_price"] += operation.price
            else:
                prices["medicine_price"] += operation.base.item.price
        elif _type is 'Lameness':
            prices["operation_price"] += operation.price
        elif _type is 'Xray':
            prices["operation_price"] += operation.price
        elif _type is 'Ultrasonic':
            prices["operation_price"] += operation.price
        elif _type is 'Endoscopy':
            prices["operation_price"] += operation.price
        elif _type is 'Dentalexamination':
            prices["operation_price"] += operation.price
        else:
            print("DEBUG: ERROR: cant solve operation type, type is ", _type)

        for key in prices:
            old_prices[key] += prices[key]*operation.count
        return old_prices
        
    def setPrices(self, visit):
        price_dict = {}
        price_dict["operation_price"] = 0.0
        price_dict["accesories_price"] = 0.0
        price_dict["lab_price"] = 0.0
        price_dict["medicine_price"] = 0.0
        price_dict["diet_price"] = 0.0
        
        for visit_animal in visit.visitanimals:
            for operation in visit_animal.operations:
                price_dict = self.updatePriceList(operation, price_dict)

        self.ui.operationSpinBox.setValue(price_dict["operation_price"])
        self.ui.accessoriesSpinBox.setValue(price_dict["accesories_price"])
        self.ui.labSpinBox.setValue( price_dict["lab_price"])
        self.ui.medicineSpinBox.setValue(price_dict["medicine_price"])
        self.ui.dietSpinBox.setValue(price_dict["diet_price"])

    def dueDateChanged(self,value):
        self.ui.DueDateEdit.setDate(datetime.datetime.now()+self.ui.DueDateTimeComboBox.itemData(self.ui.DueDateTimeComboBox.currentIndex()))
    
    def fullPricePaid(self):
        self.ui.paidSpinBox.setValue(float(self.ui.endPriceLabel.text()))
        self.ui.paidDateEdit.setDate(QDate.currentDate())
        self.ui.DueDateEdit.setDate(QDate.currentDate())
    
    def setDueDates(self):
        self.ui.DueDateTimeComboBox.clear()
        data = dict([('Heti',datetime.timedelta(days=0)),('1 vk',datetime.timedelta(days=7)),('2 vk',datetime.timedelta(days=14))])
        for key in data:
            self.ui.DueDateTimeComboBox.addItem(key,data[key])
        
        self.ui.DueDateTimeComboBox.setCurrentIndex(2)
    
    def setPaymnetMethods(self):
        self.ui.paymentComboBox.clear()
        for method in self.payment_methods:
            self.ui.paymentComboBox.addItem(method, method)
       
    def clinicVisitPageChange(self, status):
        self.ui.stackedWidget.setCurrentIndex(0 if status else 1)
        self.updateEndPrice(0)
    
    def updateKmData(self):
        km = self.ui.KmSpinBox.value()
        #TODO: add these hardcoded values to configure server (msg from UpdateKmData)
        self.ui.visitPriceSpinBox.setValue(26.93 if km > 0.0 else 0)
        self.ui.KmPriceSpinBox.setValue(km*0.48)

        
    def setToday(self):
        self.ui.paidDateEdit.setDate(datetime.datetime.today().date())
    
    def changePercent(self, value):
        self.ui.extraPercentLabel.setText(str(value))
    
       
    
        
    def getALV1Price(self):
        price_ALV1 = 0.0
        if not self.ui.clinic_radio_button.isChecked():
            price_ALV1 += self.ui.KmPriceSpinBox.value()
            price_ALV1 += self.ui.visitPriceSpinBox.value()
        else:
            price_ALV1 += self.ui.clinicPriceSpinBox.value()
        
        price_ALV1 += self.ui.operationSpinBox.value()
        price_ALV1 += self.ui.accessoriesSpinBox.value()
        price_ALV1 += self.ui.labSpinBox.value()
        
        return price_ALV1*(100 + self.ui.precentSlider.value())/100.0
        
    def getALV2Price(self):
        return self.ui.medicineSpinBox.value()
        
    def getALV3Price(self):
        return self.ui.dietSpinBox.value()
      
    def getTotal(self):
        return self.getALV1Price() + self.getALV2Price() + self.getALV3Price()
      
    
    def roundEndPrice1(self):
        self.roundEndPrice(1.0)
    
    def roundEndPrice05(self):
        self.roundEndPrice(0.5)
    
    def roundEndPrice005(self):
        self.roundEndPrice(0.05)
    
    def roundEndPrice(self, precision):
        total = self.getTotal()
        from math import ceil
        rounded = ceil(total/precision) * precision
        previous_value = self.ui.operationSpinBox.value()
        self.ui.operationSpinBox.setValue(previous_value + rounded - total)
          
    def updateEndPrice(self, value):
        price_ALV1 = self.getALV1Price()
        price_ALV2 = self.getALV2Price()
        price_ALV3 = self.getALV3Price()
        
        ALV1 = SqlHandler.getALV(1)
        ALV2 = SqlHandler.getALV(2)
        ALV3 = SqlHandler.getALV(3)
        
        self.ui.price_ALV1_total_label.setText('%.2f' % price_ALV1)
        self.ui.ALV1_total.setText('%.2f' % (price_ALV1 * (ALV1/(100.0+ALV1))))
        
        self.ui.price_ALV2_total_label.setText('%.2f' % price_ALV2)
        self.ui.ALV2_total.setText('%.2f' % (price_ALV2 * (ALV2/(100.0+ALV2))))
        
        self.ui.price_ALV3_total_label.setText('%.2f' % price_ALV3)
        self.ui.ALV3_total.setText('%.2f' % (price_ALV3 * (ALV3/(100.0+ALV3))))
        
        self.ui.endPriceLabel.setText('%.2f' % self.getTotal())
      
    
    def setAlv1Names(self):
        alv = str(SqlHandler.getALV(1))
        self.ui.ALV1_1.setText(alv + '%')
        self.ui.ALV1_2.setText(alv + '%')
        self.ui.ALV1_3.setText(alv + '%')
        self.ui.ALV1_4.setText(alv + '%')
        #self.ui.ALV1_5.setText(alv + '%')
        self.ui.ALV1_6.setText(alv + '%')
        self.ui.ALV1_7.setText(alv + '%')

    def setAlv2Names(self):
        alv2 = str(SqlHandler.getALV(2))
        self.ui.ALV2_1.setText(alv2 + '%')
        self.ui.ALV2_2.setText(alv2 + '%')
    
    def setAlv3Names(self):
        alv3 = str(SqlHandler.getALV(3))
        self.ui.ALV3_1.setText(alv3 + '%')
        self.ui.ALV3_2.setText(alv3 + '%')
        
    def printBill(self):
        self.saveTab() #save before printing so that changes will be added to print
        
        html = self.creator.makePrintfile(self.item)
        document = QWebView()
        document.setHtml(html)

        printer = QPrinter()
        
        printpreview = QPrintDialog(printer, self)
        printpreview.exec()
        
        document.print(printer)
     
    def getData(self):
        data = []
        data.append(self.visit)
        if self.ui.clinic_radio_button.isChecked():
            data.append(self.ui.clinicPriceSpinBox.value())
            data.append(0.0) #km
            data.append(0.0) #km_paymnet
        else:
            data.append(self.ui.visitPriceSpinBox.value())
            data.append(self.ui.KmSpinBox.value())
            data.append(self.ui.KmPriceSpinBox.value())
        
        data.append(self.ui.operationSpinBox.value())
        data.append(self.ui.labSpinBox.value())
        data.append(self.ui.accessoriesSpinBox.value())
        data.append(self.ui.precentSlider.value())
        data.append(self.ui.medicineSpinBox.value())
        data.append(self.ui.dietSpinBox.value())
        data.append(self.ui.paymentComboBox.itemData(self.ui.paymentComboBox.currentIndex()))
        data.append(self.qdateToPy(self.ui.DueDateEdit.date()))
        data.append(self.qdateToPy(self.ui.paidDateEdit.date()))
        data.append(self.ui.paidSpinBox.value())
        data.append(self.ui.indexNumberLabel.text())
        data.append(self.ui.otherInfoTextEdit.toPlainText())
        data.append(0)#status
        return data
    
    def makeItem(self):
        return SqlHandler.Bill(self.getData())
    
    def saveAble(self):
        return True
    
    def hasChanged(self):
        if self.item == None:
            if self.ui.clinic_radio_button.isChecked():
                #if self.ui.clinicPriceSpinBox.value() != ConfigServer.getClinicPrice():
                #    return True
                pass
            else:
                if self.ui.visitPriceSpinBox.value() > 0 or self.ui.KmSpinBox.value() > 0 or self.ui.KmPriceSpinBox.value() > 0:
                    return True
            
            if 99.999 > self.ui.precentSlider.value() > 100.001:
                return True
    
            if self.ui.otherInfoTextEdit.toPlainText () != '':
                return True
            return False
            
        else:
            if( self.ui.clinicPriceSpinBox.value() != self.item.clinic_payment or
            self.ui.KmSpinBox.value() != self.item.km or
            self.ui.KmPriceSpinBox.value() != self.item.km_payment or
            self.ui.operationSpinBox.value() != self.item.operations_payment or
            self.ui.labSpinBox.value() != self.item.lab_payment or
            self.ui.accessoriesSpinBox.value() != self.item.accessories_payment or
            self.ui.precentSlider.value() != self.item.extra_percent or
            self.ui.medicineSpinBox.value() != self.item.medicines_payment or
            self.ui.dietSpinBox.value() != self.item.diet_payment or
            self.ui.paymentComboBox.itemData(self.ui.paymentComboBox.currentIndex()) != self.item.payment_method or
            self.ui.DueDateEdit.date() != self.item.due_date or
            self.ui.paidDateEdit.date() != self.item.paid_time or
            self.ui.paidSpinBox.value() != self.item.paid_value or
            self.ui.otherInfoTextEdit.toPlainText () != self.item.other_info):
                return True
            else:
                return False
            
        
    def getType(self=None):
        return 'Bill'
    
    def getName(self=None):
        return 'Lasku'