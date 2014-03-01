#!/usr/bin/python
# -*- coding: utf-8
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
'''
Created on Apr 21, 2013

@author: mp
'''

from sqlalchemy import Column, Integer, String, Date, Sequence, ForeignKey
from sqlalchemy.orm import relationship

import datetime
#import Base from init file
from models import Base

class Bill(Base):
    __tablename__ = 'bills'
    id = Column(Integer, Sequence('bills_id_seq'), primary_key=True)
    
    visit_id = Column(Integer, ForeignKey('visits.id'), nullable=False)
    visit = relationship('Visit')
    
    #ALV1
    clinic_payment = Column(Integer) 
    operations_payment = Column(Integer)
    lab_payment = Column(Integer)
    accessories_payment = Column(Integer)    
    extra_percent = Column(Integer)
    
    #ALV2
    medicines_payment = Column(Integer)
    
    #ALV3
    diet_payment = Column(Integer)
    
    km = Column(Integer)
    km_payment = Column(Integer)
    
    payment_method = Column(String)
    due_date = Column(Date)
    paid_time  = Column(Date)
    paid_value = Column(Integer)
   
    index_number = Column(Integer)
   
    other_info = Column(String(1000))
    status = Column(Integer)
    
    def __init__(self, visit, clinic_payment, km, km_payment, operations_payment, lab_payment, accessories_payment, extra_percent,
                 medicines_payment, diet_payment, payment_method, due_date, paid_time, paid_value,index_number, other_info,satus = 0):
        self.visit = visit
        self.visit_id = visit.id
        self.clinic_payment = clinic_payment
        self.km = km
        self.km_payment = km_payment
        self.operations_payment = operations_payment
        self.lab_payment = lab_payment
        self.accessories_payment = accessories_payment
        self.extra_percent = extra_percent
        self.medicines_payment = medicines_payment
        self.diet_payment = diet_payment
        self.payment_method = payment_method
        self.due_date = due_date
        self.paid_time = paid_time
        self.paid_value = paid_value
        self.other_info = other_info
        self.index_number = index_number
        self.satus = satus 

   
    def update(self, data):
        self.visit = data[0]
        self.clinic_payment = data[1]
        self.km = data[2]
        self.km_payment = data[3]
        self.operations_payment = data[4]
        self.lab_payment = data[5]
        self.accessories_payment = data[6]
        self.extra_percent = data[7]
        self.medicines_payment = data[8]
        self.diet_payment = data[9]
        self.payment_method = data[10]
        self.due_date = data[11]
        self.paid_time = data[12]
        self.paid_value = data[13]
        self.index_number = data[14]
        self.other_info = data[15]
        self.satus = data[16] 

    def calcPricesFromVisit(self):
        temp_operation_price = 0.0
        temp_accesories_price = 0.0
        temp_lab_price = 0.0
        temp_medicine_price = 0.0
        temp_diet_price = 0.0
        
        for visit_animal in self.visit.visitanimals:
            for operation in visit_animal.operations:
                from models.operation import Lab
                if isinstance(operation, Lab):
                    temp_lab_price += operation.price
                else:
                    temp_operation_price += operation.price
                if operation.hasList():
                    for item in operation.items:
                        if 1 == item.item.getALVClass():
                            temp_accesories_price += item.item.price * item.count
                        elif 2 == item.item.getALVClass(): 
                            temp_medicine_price += item.item.price * item.count
                        elif 3 == item.item.getALVClass():
                            temp_diet_price += item.item.price * item.count
                        else:
                            pass#self.errorMessage('ERROR: BillTab.setPrices(): ALV is not valid!')    
                if operation.base.hasItem():
                    if operation.base.item != None:
                        if 1 == operation.base.item.getALVClass():
                            temp_accesories_price += operation.base.item.price
                        elif 2 == operation.base.item.getALVClass():
                            temp_medicine_price += operation.base.item.price
                        elif 3 == operation.base.item.getALVClass():
                            temp_diet_price += operation.base.item.price
                        else:
                            pass#self.errorMessage('ERROR: BillTab.setPrices(): ALV is not valid!')
                    else:
                        pass#self.errorMessage('ERROR: BillTab.setPrices(): operation.hasItem() is true but item is None!')
            return [temp_operation_price,temp_accesories_price, temp_lab_price, temp_medicine_price, temp_diet_price]
        

    def getALV0Price(self):
        return self.km_payment

    def getALV1Price(self):
        return ((self.clinic_payment+self.operations_payment+self.lab_payment
                +self.accessories_payment)*((100+self.extra_percent)/100.0))
    
    def getExtraPartFromPrice(self):
        return ((self.clinic_payment+self.operations_payment+self.lab_payment
                +self.accessories_payment)*((self.extra_percent)/100.0))
    
    def getALV2Price(self):
        return self.medicines_payment
    
    def getALV3Price(self):
        return self.diet_payment
    
    def getALVXPrice(self, alv_type):
        if(alv_type == 3):
            return self.getALV3Price()
        elif(alv_type == 2):
            return self.getALV2Price()
        else:
            return self.getALV1Price()
    
    def getTaxFreePrice(self):
        return self.getTotalPrice()-self.getTotalALV()
    
    def getALV(self, alv_type):
        from models import  SqlHandler
        return round(self.getALVXPrice(alv_type)*(1.0-1.0/(1.0+SqlHandler.getALV(alv_type)/100.0))*100.0)/100.0
      
    def getTotalPrice(self):
        return self.getALV0Price()+self.getALV1Price()+self.getALV2Price()+self.getALV3Price()
                
    def getTotalALV(self):
        return self.getALV(1) + self.getALV(2) + self.getALV(3)
        
    def getType(self):
        return 'Bill'
    
    def getName(self):
        return 'Lasku'
    
    