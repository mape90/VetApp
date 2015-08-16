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
from models.translationtables import g_payment_time_dict, g_item_alv_dict
from configfile import getBillPath


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

        self.setDefaultClinicPrice()
     
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
                    self.ui.clinicPriceSpinBox.setValue(self.item.clinic_payment * ((100+SqlHandler.getALV(1))/100.))
                else:
                    self.ui.clinic_radio_button.setChecked(False)
                    self.ui.KmSpinBox.setValue(self.item.km)

                    self.ui.visitPriceSpinBox.setValue(self.item.clinic_payment * ((100+SqlHandler.getALV(1))/100.))
                    self.ui.KmPriceSpinBox.setValue(self.item.km_payment * ((100+SqlHandler.getALV(1))/100.))

                self.ui.operationSpinBox.setValue(self.item.operations_payment * ((100+SqlHandler.getALV(1))/100.))
                self.ui.accessoriesSpinBox.setValue(self.item.accessories_payment * ((100+SqlHandler.getALV(1))/100.))
                self.ui.labSpinBox.setValue(self.item.lab_payment * ((100+SqlHandler.getALV(1))/100.))
                self.ui.medicineSpinBox.setValue(self.item.medicines_payment * ((100+SqlHandler.getALV(2))/100.))
                self.ui.dietSpinBox.setValue(self.item.diet_payment * ((100+SqlHandler.getALV(3))/100.))
                self.ui.paidSpinBox.setValue(self.item.paid_value) #this has all alvs so it cant be out of them

                self.ui.otherInfoTextEdit.setPlainText(self.item.other_info)
                self.ui.paymentComboBox.setCurrentIndex(self.ui.paymentComboBox.findData(self.item.payment_method))
                self.ui.paidDateEdit.setDate(self.item.paid_time)
                self.ui.DueDateEdit.setDate(self.item.due_date)
                self.ui.precentSlider.setValue(self.item.extra_percent)
                self.ui.indexNumberLabel.setText(str(self.item.index_number)) 
                
            else:
                self.ui.ownerLabel.setText(self.item.owner.name)
                self.setDefaultClinicPrice()
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
        self.ui.clinicPriceSpinBox.setValue(SqlHandler.getGlobalVar(key="clinicpayment") * (100+SqlHandler.getALV(1))/100.)
    


        

        
    def setPrices(self, visit):
        price_dict = visit.getPriceDict()

        self.ui.operationSpinBox.setValue(price_dict["operation_price"] * (100+SqlHandler.getALV(1))/100.)
        self.ui.accessoriesSpinBox.setValue(price_dict["accesories_price"] * (100+SqlHandler.getALV(1))/100.)
        self.ui.labSpinBox.setValue( price_dict["lab_price"] * (100+SqlHandler.getALV(1))/100.)
        self.ui.medicineSpinBox.setValue(price_dict["medicine_price"] * (100+SqlHandler.getALV(2))/100.)
        self.ui.dietSpinBox.setValue(price_dict["diet_price"] * (100+SqlHandler.getALV(3))/100.)

    def dueDateChanged(self,value):
        self.ui.DueDateEdit.setDate(datetime.datetime.now()+self.ui.DueDateTimeComboBox.itemData(self.ui.DueDateTimeComboBox.currentIndex()))
    
    def fullPricePaid(self):
        self.ui.paidSpinBox.setValue(float(self.ui.endPriceLabel.text()))
        self.ui.paidDateEdit.setDate(QDate.currentDate())
        self.ui.DueDateEdit.setDate(QDate.currentDate())
    
    def setDueDates(self):
        self.ui.DueDateTimeComboBox.clear()
        data = g_payment_time_dict
        for key in data:
            self.ui.DueDateTimeComboBox.addItem(key,data[key])
        
        self.ui.DueDateTimeComboBox.setCurrentIndex(2)
    
    def setPaymnetMethods(self):
        self.ui.paymentComboBox.clear()
        for method in self.payment_methods:
            self.ui.paymentComboBox.addItem(method, method)
       
    def clinicVisitPageChange(self, status):
        self.ui.stackedWidget.setCurrentIndex(0 if status else 1)
        self.updateEndPrice(0) #zero is just because connections need to give parameter
    
    def updateKmData(self):
        pass
        '''#km = self.ui.KmSpinBox.value()

        #self.ui.visitPriceSpinBox.setValue(SqlHandler.getGlobalVar(key="clinicpayment") if km > 0.0 else 0)
        #self.ui.KmPriceSpinBox.setValue(km*SqlHandler.getGlobalVar(key="km_price"))'''

        
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
        
        return (price_ALV1*(100 + self.ui.precentSlider.value())/100.0) / ((100+SqlHandler.getALV(1))/100.)
        
    def getALV2Price(self):
        return self.ui.medicineSpinBox.value() / ((100+SqlHandler.getALV(2))/100.)
        
    def getALV3Price(self):
        return self.ui.dietSpinBox.value() / ((100+SqlHandler.getALV(3))/100.)
      
    def getTotal(self):
        return self.getALV1Price()*((100+SqlHandler.getALV(1))/100.) + self.getALV2Price()*((100+SqlHandler.getALV(2))/100.) + self.getALV3Price()*((100+SqlHandler.getALV(3))/100.)
      
    
    def roundEndPrice1(self):
        self.roundEndPrice(1.0)
    
    def roundEndPrice05(self):
        self.roundEndPrice(0.5)
    
    def roundEndPrice005(self):
        self.roundEndPrice(0.05)
    
    def roundEndPrice(self, precision):
        total = round(self.getTotal(), 3) #convert i.e 1.000000000001 to 1.000

        print("rounding: total: " , total)

        from math import ceil
        rounded = ceil(total/precision) * precision
        previous_value = self.ui.operationSpinBox.value()
        self.ui.operationSpinBox.setValue(previous_value + rounded - total)
        
        print("value after round should be: ", previous_value + rounded - total)
        print("it is: ", self.ui.operationSpinBox.value())
        
          
    def updateEndPrice(self):
        price_ALV1 = self.getALV1Price() * (100+SqlHandler.getALV(1))/100.
        price_ALV2 = self.getALV2Price() * (100+SqlHandler.getALV(2))/100.
        price_ALV3 = self.getALV3Price() * (100+SqlHandler.getALV(3))/100.
        
        self.ui.price_ALV1_total_label.setText('%.2f' % price_ALV1)
        self.ui.ALV1_total.setText('%.2f' % (price_ALV1-self.getALV1Price()))
        
        self.ui.price_ALV2_total_label.setText('%.2f' % price_ALV2)
        self.ui.ALV2_total.setText('%.2f' % (price_ALV2-self.getALV2Price()))
        
        self.ui.price_ALV3_total_label.setText('%.2f' % price_ALV3)
        self.ui.ALV3_total.setText('%.2f' % (price_ALV3-self.getALV3Price()))
        
        self.ui.endPriceLabel.setText('%.2f' % (price_ALV1 + price_ALV2 + price_ALV3))
      
    
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
        
        printer.setOutputFileName(getBillPath() + str(datetime.datetime.now())[0:-7] + '_' + str(self.item.id) + '.pdf')
        
        printpreview = QPrintDialog(printer, self)
        printpreview.exec()
        
        document.print(printer)
     
    def getData(self):
        print("DEBUG: getData")
        data = {}
        data['visit'] = self.visit
        if self.ui.clinic_radio_button.isChecked():
            data['clinic_payment'] = self.ui.clinicPriceSpinBox.value() / ((100+SqlHandler.getALV(1))/100.)
            data['km'] = 0.0
            data['km_payment'] = 0.0
        else:
            data['clinic_payment'] = self.ui.visitPriceSpinBox.value() / ((100+SqlHandler.getALV(1))/100.)
            data['km'] = self.ui.KmSpinBox.value()
            data['km_payment'] = self.ui.KmPriceSpinBox.value() / ((100+SqlHandler.getALV(1))/100.)

        data['operations_payment'] = self.ui.operationSpinBox.value() / ((100+SqlHandler.getALV(1))/100.)
        data['lab_payment'] = self.ui.labSpinBox.value() / ((100+SqlHandler.getALV(1))/100.)
        data['accessories_payment'] = self.ui.accessoriesSpinBox.value() / ((100+SqlHandler.getALV(1))/100.)
        data['extra_percent'] = self.ui.precentSlider.value()
        data['medicines_payment'] = self.ui.medicineSpinBox.value() / ((100+SqlHandler.getALV(2))/100.)
        data['diet_payment'] = self.ui.dietSpinBox.value() / ((100+SqlHandler.getALV(3))/100.)
        data['payment_method'] = (self.ui.paymentComboBox.itemData(self.ui.paymentComboBox.currentIndex()))
        data['due_date'] = self.qdateToPy(self.ui.DueDateEdit.date())
        data['paid_time'] = self.qdateToPy(self.ui.paidDateEdit.date())
        data['paid_value'] = self.ui.paidSpinBox.value()
        data['index_number'] = self.ui.indexNumberLabel.text()
        data['other_info'] = self.ui.otherInfoTextEdit.toPlainText()
        data['satus'] = 0 #status TODO: implement if needed
        
        print('operations_payment ',data['operations_payment'])
        
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