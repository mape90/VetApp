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
    
    def genAnimalInfo(self, visitanimal):
        tmp = '<div class="animalinfo"><p style="font-size:70%;"> <b style="font-size:110%;">'
        tmp +=  visitanimal.animal.name + '</b>'
        if len(visitanimal.animal.official_name) > 0:
            tmp += '(' + visitanimal.animal.official_name + ')'
        tmp += '</br> Syntynyt: ' + self.datetimeToStr(visitanimal.animal.birthday) +' <br>'
        tmp += 'Rotu: ' + visitanimal.animal.race.name +' <br> '
        tmp += 'Sukupuoli: ' +visitanimal.animal.sex.name +' </p></div>'
        return tmp

    def genAnimalInfos(self, visitanimals): #TODO: will work only for 1-3 animals FIX this
        tmp = ''
        for visitanimal in visitanimals:
            tmp += self.genAnimalInfo(visitanimal)
        return tmp

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
        #self.change("alv_number", bill.visit.vet.alv_number)#alv_number
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
        
        
        self.html = self.html.replace("animal_info_area", self.genAnimalInfos(bill.visit.visitanimals))
        
        self.html = self.html.replace('visitanimal_summarys',self.summaryToHTML(bill.visit.visitanimals))
        
        operation_rows = ""
        operation_row_count = 0
        
        if(bill.clinic_payment > 0):
            if(bill.km == 0):
                operation_rows += self.genTableRowPrue("Klinikkamaksu", 1, "", bill.clinic_payment,  SqlHandler.getALV(1))
            else:
                operation_rows += self.genTableRowPrue("Käyntimaksu", 1, "", bill.clinic_payment,  SqlHandler.getALV(1))
            operation_row_count +=1
                
        if(bill.km_payment > 0):
            operation_rows += self.genTableRowPrue("Kilometrikorvaus " + str(bill.km) + "km", 1, "", bill.clinic_payment,  SqlHandler.getALV(1))
            operation_row_count +=1
              
        
        for va in bill.visit.visitanimals:
            if(len(bill.visit.visitanimals) > 1):
                (rows, count) = self.genAnimalTableRow(va.animal.name)
                operation_rows += rows
                operation_row_count += count

            for oper in va.operations:
                (rows, count) = self.genTableRow(oper)
                operation_rows += rows
                operation_row_count += count

            for item in va.items:
                (rows, count) = self.genItemTableRow(item)
                operation_rows += rows
                operation_row_count += count


        price_dict = bill.calcPricesFromVisit()
        
                
        if(not self.floatEqual(price_dict["operation_price"], bill.operations_payment)):
            print("DEBUG: PrintFileCreator: ", price_dict["operation_price"] ," ", bill.operations_payment)
            operation_rows += self.genTableRowPrue("Operaatioiden hintamuutos", 1, "", -price_dict["operation_price"] + bill.operations_payment,  SqlHandler.getALV(1))
            operation_row_count +=1
            
        if(not self.floatEqual(price_dict["accesories_price"], bill.accessories_payment)):
            operation_rows += self.genTableRowPrue("Tarvikkeiden hintamuutos", 1, "", -price_dict["accesories_price"] + bill.accessories_payment,  SqlHandler.getALV(1))
            operation_row_count +=1
        
        if(not self.floatEqual(price_dict["lab_price"], bill.lab_payment)):
            operation_rows += self.genTableRowPrue("Laboratorio hintamuutos", 1, "", -price_dict["lab_price"] + bill.lab_payment,  SqlHandler.getALV(1))
            operation_row_count +=1

        if(not self.floatEqual(price_dict["medicine_price"], bill.medicines_payment)):
            print("DEBUG: PrintFileCreator: ", price_dict["medicine_price"] ," ", bill.medicines_payment)
            operation_rows += self.genTableRowPrue("Lääkkeiden hintamuutos", 1, "", -price_dict["medicine_price"] + bill.medicines_payment,  SqlHandler.getALV(2))
            operation_row_count +=1
            
        if(not self.floatEqual(price_dict["diet_price"], bill.diet_payment)):
            operation_rows += self.genTableRowPrue("Rehujen hintamuutos", 1, "", -price_dict["diet_price"] + bill.diet_payment,  SqlHandler.getALV(3))
            operation_row_count +=1
            
            
        if(not self.floatEqual(0,bill.extra_percent) ):
            operation_rows += self.genTableRowPrue("Muu korotus (" + str(bill.extra_percent) + "%)", 1, "", bill.getExtraPartFromPrice(),  SqlHandler.getALV(1))
            operation_row_count +=1
        
        
        for i in range(0,self.table_row_count-operation_row_count):
            operation_rows += self.genEmptyTableRow()
        
        self.change("operations_lists", operation_rows, False)
        
        self.change("price_total", self.toStr(bill.getTotalPrice()))
        self.change("need_to_pay", self.toStr(bill.getTotalPrice()-bill.paid_value))
        self.change("alv_total", self.toStr(bill.getTotalALV()))
        
        self.change("vet_phonenumber", "") #TODO implement
        self.change("vet_email_address", "") #TODO implement
        
        self.change("other_info", bill.other_info)
        
        return self.html
    
    def floatEqual(self, a,b, dif=0.01):
        return abs(a-b) < dif
    
    
    def summaryToHTML(self, visitanimals):
        tmp = '</br></br></br></br></br>'
        tmp += '<h1>Yhteenveto ja hoitoohjeet</h1>'
        for visitanimal in visitanimals:
            tmp += '</br><p>'
            if len(visitanimals) > 1:
                tmp += '<b>' + visitanimal.animal.name + '</b> </br>'
            tmp += visitanimal.treatment + '</p>'
        return tmp
        
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
    
    def genAnimalTableRow(self, name):
        return '''<tr>
                    <td style="text-align:left">''' + name + '''</td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:center"> </td>
                    <td style="text-align:right">  </td>
                    <td style="align:right;"> <br> </td>
            </tr>'''

    
    def incALV(self, value, alv_p):
        return value*(100+alv_p)/100.0
    
    def genTableRowPrue(self, name, count, type_, price, alv):
        alv_p = alv
        inc_alv_price = self.incALV(price, alv_p)
        temp = '''<tr> 
                <td style="text-align:left">''' + name + '''</td>
                <td style="text-align:center">''' + self.toStr(count) + '''</td>
                <td style="text-align:center">''' + type_ + '''</td>
                <td style="text-align:center">''' + self.toStr(inc_alv_price) + '''</td>
                <td style="text-align:center">''' + self.toStr(alv_p) + '''</td>
                <td style="text-align:right">''' + self.toStr(inc_alv_price-price)+ '''</td>
                <td style="align:right;">''' + self.toStr(inc_alv_price * count) + '''</td>
            </tr>'''
        return temp
    
    def toStr(self,val):
        return ('%.2f' % val)
    
    def genItemTableRow(self,item):
        return (self.genTableRowPrue(name = item.item.name,
                               count = item.count,
                               type_ = item.item.count_type,
                               price = item.item.price,
                               alv  = item.item.getALV()) ,1)


    def genTableRow(self, operation):
        counter = 0
        tmp_rows = ''
        tmp_rows += self.genTableRowPrue(name = operation.base.name,
                                        count = operation.count,
                                        type_ = "kpl",
                                        price = operation.price,
                                        alv = SqlHandler.getALV(1))
        counter += 1
        if(hasattr(operation.base, 'item')):
            print("operation.base.item: ", operation.base.item)
            tmp_rows += self.genTableRowPrue(name = ('- ' + operation.base.item.name),
                                             count = operation.count,
                                             type_ = operation.base.item.count_type,
                                             price = operation.base.item.price,
                                             alv = operation.base.item.getALV())
            counter += 1
        if(hasattr(operation, 'items')):
            print("items listing strt")
            for surgeryitem in operation.items:
                total_count = operation.count*surgeryitem.count
                
                tmp_rows += self.genTableRowPrue(name = ('- ' + surgeryitem.item.name),
                                                count = total_count,
                                                type_ = surgeryitem.item.count_type,
                                                price = surgeryitem.item.price,
                                                alv = surgeryitem.item.getALV())
                counter += 1
        
        return (tmp_rows, counter)


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
 
        