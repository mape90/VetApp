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
    GNU General Public License for more details.how 

    You should have received a copy of the GNU General Public License
    along with VetApp.  If not, see <http://www.gnu.org/licenses/>.
'''

from models import SqlHandler
import datetime
from sqlalchemy import Date
from PyQt4.QtGui import QMessageBox


class PrintFileCreator(object):
    def __init__(self, path):
        self.path = path
        self.html = ""
        self.table_row_count = 25
    
    def errorMessage(self, message):
        box = QMessageBox()
        box.setText(message)
        box.exec()
    
    def makePrintfile(self, bill, language='Finnish'):#TODO:add bill needed info
        
        self.html = ""
        try:
            f = open(self.path, 'r', encoding="utf-8")
        except  IOError:
            self.errorMessage("Can not open file named: " + self.path)
            return ""
        
        for i in f.readlines():
            self.html += i

        
        self.change("vet_name", bill.visit.vet.name)
        self.change("vet_number", str(bill.visit.vet.vet_number))
        self.change("vet_address", bill.visit.vet.address)
        if(not bill.visit.vet.postnumber == None):
            self.change("vet_postnumber", bill.visit.vet.postnumber.number)
        else:
            self.change("vet_postnumber","")
            
        if(not bill.visit.vet.post_office == None):
            self.change("vet_postaddress", bill.visit.vet.post_office.name)
        else:
            self.change("vet_postaddress","")
        self.change("alv_number", bill.visit.vet.alv_number)#alv_number
        self.change("owner_name", bill.visit.owner.name)
        self.change("owner_address", bill.visit.owner.address)
        if(not bill.visit.owner.post_office == None):
            self.change("owner_postaddress", bill.visit.owner.post_office.name)
        else:
            self.change("owner_postaddress","");
            
        if(not bill.visit.owner.postnumber == None):
            self.change("owner_postnumber", bill.visit.owner.postnumber.number)
        else:
            self.change("owner_postnumber","")
        self.change("bill_number", bill.id) #TODO change id to some other
        self.change("bill_date", self.getDateNow()) #TODO change or add to Bill
        self.change("due_date", bill.due_date)
        self.change("penalty_interest", 8.00) #TODO change
        self.change("index_number", bill.index_number)
        self.change("payment_condition", "14 pv") #todo change
        self.change("bank_name", bill.visit.vet.bank_name)
        self.change("account_number", bill.visit.vet.IBAN)
        self.change("swif_bic", bill.visit.vet.SWIF)
        self.change("payment_method", bill.payment_method)
        
        
        
        operation_rows = ""
        operation_row_count = 0
        
        if(bill.clinic_payment > 0):
            if(bill.km == 0):
                operation_rows += self.genTableRowPrue("Klinikkamaksu", 1, "", bill.clinic_payment, 1)
            else:
                operation_rows += self.genTableRowPrue("Käyntimaksu", 1, "", bill.clinic_payment, 1)
            operation_row_count +=1
                
        if(bill.km_payment > 0):
            operation_rows += self.genTableRowPrue("Kilometrikorvaus " + str(bill.km) + "km", 1, "", bill.clinic_payment, 0)
            operation_row_count +=1
              
        
        for va in bill.visit.visitanimals:
            for oper in va.operations:
                operation_rows += self.genTableRow(oper)
                operation_row_count += 1
                if(oper.hasList()):
                    for item in oper.items:
                        operation_rows += self.genItemTableRow(item)
                        operation_row_count += 1
                elif(oper.base.hasItem()):
                    operation_rows += self.genTableRowPrue(oper.base.item.name, 1, "kpl", oper.base.item.price, oper.base.item.getALVClass()) 
                    operation_row_count += 1
                else:
                    pass
        
        #[operation_price, accesories_price, lab_price, medicine_price, diet_price]
        list_visit_prices = bill.calcPricesFromVisit()
        if(not list_visit_prices[0] == bill.operations_payment):
            operation_rows += self.genTableRowPrue("Operaatioiden hintamuutos", 1, "", -list_visit_prices[0] + bill.operations_payment, 1)
            operation_row_count +=1
        if(not list_visit_prices[1] == bill.accessories_payment):
            operation_rows += self.genTableRowPrue("Tarvikkeiden hintamuutos", 1, "", -list_visit_prices[1] + bill.accessories_payment, 1)
            operation_row_count +=1
        if(not list_visit_prices[2] == bill.lab_payment):
            operation_rows += self.genTableRowPrue("Laboratorio hintamuutos", 1, "", -list_visit_prices[2] + bill.lab_payment, 2)
            operation_row_count +=1
        if(not list_visit_prices[3] == bill.medicines_payment):
            operation_rows += self.genTableRowPrue("Lääkkeiden hintamuutos", 1, "", -list_visit_prices[3] + bill.medicines_payment, 2)
            operation_row_count +=1
        if(not list_visit_prices[4] == bill.diet_payment):
            operation_rows += self.genTableRowPrue("Rehujen hintamuutos", 1, "", -list_visit_prices[4] + bill.diet_payment, 3)
            operation_row_count +=1
            
        if(not 0 == bill.extra_percent):
            operation_rows += self.genTableRowPrue("Muu korotus (" + str(bill.extra_percent) + "%)", 1, "", bill.getExtraPartFromPrice(), 1)
            operation_row_count +=1
        
        
        for i in range(0,self.table_row_count-operation_row_count):
            operation_rows += self.genEmptyTableRow()
        
        self.change("operations_lists", operation_rows, False)
        
        self.change("price_total", str(bill.getTotalPrice()))
        self.change("need_to_pay", str(bill.getTotalPrice()-bill.paid_value))
        self.change("alv_total", str(bill.getTotalALV()))
        
        self.change("vet_phonenumber", "") #TODO implement
        self.change("vet_email_address", "") #TODO implement
        
        self.change("other_info", bill.other_info)
        
        return self.html
        
    def genEmptyTableRow(self):
        return '''<tr>
                    <td style="text-align:left"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:right">  </td>
                    <td style="align:right;"> <br> </td>
            </tr>'''
    
    
    def genTableRowPrue(self, name, count, type_, price, alv):
        temp = '''<tr>
                <td style="text-align:left"> operation_name </td>
                <td style="text-align:center"> count </td>
                <td style="text-align:center"> value </td>
                <td style="text-align:center"> a_price </td>
                <td style="text-align:center"> alv_p </td>
                <td style="text-align:right"> alv </td>
                <td style="align:right;"> t_price </td>
            </tr>'''
        temp = temp.replace("operation_name", name)
        temp = temp.replace("count", str(count))
        temp = temp.replace("value", type_) #TODO change this to more generic form
        temp = temp.replace("a_price", str(price))
        temp = temp.replace("alv_p", str(SqlHandler.getALV(alv)))
        temp = temp.replace("alv", str(round(count*price*(1.0-1.0/(1.0+SqlHandler.getALV(alv)/100.0))*100.0)/100.0))
        temp = temp.replace("t_price", str(count*price))
        return temp
    
    def genItemTableRow(self,surgeryItem):
        return self.genTableRowPrue(name = surgeryItem.item.name, 
                               count = surgeryItem.count,
                               type_ ="kpl",
                               price = surgeryItem.item.price,
                               alv  = surgeryItem.item.getALVClass())

    
    def genTableRow(self, operation, alv = 1):
        return self.genTableRowPrue(name = operation.base.name,
                                    count = operation.count,
                                    type_ = "kpl",
                                    price = operation.price,
                                    alv = alv)


    def change(self, old, new, parse=True):
        if(isinstance(new, str)):
            if(self.stirngIsntEmpty(new)):
                if(parse):
                    self.html = self.html.replace(old, self.parse(new))
                else:
                    self.html = self.html.replace(old, new)
            else:
                self.html = self.html.replace(old, '&nbsp;')
        elif(isinstance(new, (Date, datetime.datetime, datetime.date))):
            self.html = self.html.replace(old, self.datetimeToStr(new))
        elif(isinstance(new, (int, float))):
            self.html = self.html.replace(old, str(new))
        else:
            self.html = self.html.replace(old, self.parse(str(type(new))))
     
    #check if new is empty or wont contain any real character       
    def stirngIsntEmpty(self, new):
        if(not new.strip() is ""):
            return True;
        else:
            return False;
    
    #parse < > & marks off string so that those wont mess up html file
    def parse(self, new):
        new = new.replace("<","&lt;")
        new = new.replace(">","&gt;")
        new = new.replace("&","&amp;")
        return new
     
    def datetimeToStr(self, date):
        d = str(date.day)
        m = str(date.month)
        y = str(date.year)
        return d + "." + m + "." + y 
        
    def getDateNow(self):
        d = str(datetime.datetime.today().date().day)
        m = str(datetime.datetime.today().date().month)
        y = str(datetime.datetime.today().date().year)
        return d + "." + m + "." + y 
 
        