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

from configfile import logDEBUG, logERROR

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
    
    def __init__(self, data):
        self.update(data)

   
    def update(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    def calcPricesFromVisit(self):
        return self.visit.getPriceDict()

    
    def getExtraPartFromPrice(self):
        return (self.operations_payment*((self.extra_percent)/100.0))
   
    def getALVMul(self, alv_type):
        if(alv_type):
            from models import SqlHandler
            return (1.0 + SqlHandler.getALV(alv_type) / 100.0)
        else:
            return 1.0
    
    def getRawPrice(self, alv_type):
        if(alv_type == 1):
            return ((self.km_payment + self.clinic_payment + self.operations_payment*((100+self.extra_percent)/100.0) +
                     self.lab_payment + self.accessories_payment))
        elif(alv_type == 2):
            return self.medicines_payment
        elif(alv_type == 3):
            return self.diet_payment
        elif(alv_type == 0):
            return 0
        else:
            logError("getRawPrice, incorrect alv_type: ", alv_type)
    
    def getALVXPrice(self, alv_type):
        return self.getRawPrice(alv_type) * self.getALVMul(alv_type)

    def getALVDiff(self, alv_type):
        return self.getALVXPrice(alv_type) - self.getRawPrice(alv_type)
    
    
    #def getALV(self, alv_type):
        #return self.getALVXPrice(alv_type)
      
    def getTotalPrice(self):
        total = 0.0
        for i in range(0,4):
            tmp = self.getALVXPrice(i)
            logDEBUG("tmp", tmp )
            total += tmp
        
        logDEBUG("Total price: ", total)
        return total
                
    def getTotalALV(self):
        total = 0.0
        for i in range(1,4):
            total += self.getALVDiff(i)
        return total
        
    def getType(self):
        return 'Bill'
    
    def getName(self):
        return 'Lasku'
    
    