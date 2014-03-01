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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Interval, Boolean, Table, Date
from sqlalchemy.orm import relationship

#from sqlalchemy.ext.declarative import declarative_base

#from models import Base
from models.item import *

import datetime


##----------------------------------------------##
#
#            OperationBase classes
#
##----------------------------------------------##

class OperationBase(Base):
    __tablename__='operationbases'
    id = Column(Integer, Sequence('operationbases_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Integer, nullable=False)
    type = Column(String(50))
    description = Column(String(1000))
    __mapper_args__ = {'polymorphic_identity':'operationbases','polymorphic_on':type}
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description
        
    def getName(self=None):
        return 'Operaatio'
    
    def getType(self):
        return 'OperationBase'
    
    def stringList(self):
        return [str(self.id), self.name, self.getName(), str(self.price)]
    
    def ObjectCreator(self=None):
        return Basic
    
    def hasList(self=None):
        return False
    
    def hasItem(self):
        return False
    
    def hasMedicine(self):
        return False
    
    def update(self, data):
        self.name = data[0]
        self.price = data[1]
        self.description = data[2]
   
class VaccinationBase(OperationBase):
    __tablename__='vaccinationbases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    duration = Column(Interval)
    need_resit = Column(Boolean)
    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item")
    __mapper_args__ = {'polymorphic_identity':'vaccinationbases',}
    def __init__(self,name, price, description, duration, need_resit, item):
        super().__init__(name, price, description)
        self.duration = duration
        self.need_resit = need_resit
        self.item= item
   
    def hasItem(self):
        return True
    
    def stringList(self):
        return [str(self.id), self.name, self.getName(), str(self.price+self.item.price) if self.item != None else str(self.price)]
   
    def getName(self=None):
        return 'Rokotus'
    
    def ObjectCreator(self=None):
        return Vaccination
    
    def update(self, data):
        OperationBase.update(self, data)
        self.duration = data[3]
        self.need_resit = data[4]
        self.item = data[5]
   

class SurgeryBaseItem(Base):
    __tablename__='surgerybaseitems'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    surgerybase_id = Column(Integer, ForeignKey('surgerybases.id'))
    item = relationship("Item")
    count = Column(Integer)
    def __init__(self,item,count=1):
        self.item = item
        self.count = count
        
    def getType(self=None):
        return 'SurgeryBaseItem'
    
    def stringList(self):
        string_list = self.item.stringList()
        string_list[3] = str(float(string_list[3])*self.count)
        string_list.append(str(self.count))
        return string_list
    

class SurgeryBase(OperationBase):
    __tablename__='surgerybases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    items = relationship("SurgeryBaseItem")
    __mapper_args__ = {'polymorphic_identity':'surgerybases',}
    def __init__(self,name, price, description, items=[]):
        super().__init__(name, price, description)
        self.items = items
    
    def getName(self=None):
        return 'Leikkaus'
    
    def ObjectCreator(self=None):
        return Surgery
    
    def hasList(self=None):
        return True
    
    def stringList(self):
        price = 0.0
        for i in self.items:
            price += float(i.item.price) * i.count
        price += self.price
        return [str(self.id), self.name, self.getName(), str(price)]

    def update(self, data):
        OperationBase.update(self, data)
        self.items = data[3]

class MedicationBase(OperationBase):
    __tablename__='medicationbases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship('Medicine')
    __mapper_args__ = {'polymorphic_identity':'medicationbases',}
    def __init__(self, name, price, description, item):
        super().__init__(name, price, description)
        self.item = item
    
    def getName(self=None):
        return 'Lääkitys'
    
    def ObjectCreator(self=None):
        return Medication
    
    def hasItem(self):
        return True
       
    def stringList(self):
        return [str(self.id), self.name, self.getName(), str(self.price+self.item.price) if self.item != None else str(self.price)]

    def update(self, data):
        OperationBase.update(self, data)
        self.item = data[3]
       
class LabBase(OperationBase):
    __tablename__='labbases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    def __init__(self, name, price, description):
        super().__init__(name, price, description)
    
    def getName(self=None):
        return 'Laboratoriotutkimus'

    def ObjectCreator(self=None):
        return Lab
'''

'''
class LamenessBase(OperationBase):
    __tablename__='lamenessbases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'lamenessbases',}
    def __init__(self, name, price, description):
        super().__init__(name, price, description)
        
    def getName(self=None):
        return 'Ontumatutkimus'

    def ObjectCreator(self=None):
        return Lameness
'''

'''
class XrayBase(OperationBase):
    __tablename__='xraybasess'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'xraybase',}
    def __init__(self, name, price, description):
        super().__init__(name, price, description)
    
    def getName(self=None):
        return 'Röntkentutkimus'
    
    def ObjectCreator(self=None):
        return Xray

'''
    
'''
class UltrasonicBase(OperationBase):
    __tablename__='ultrasonicbases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'ultrasonicbases',}
    def __init__(self, name, price, description):
        super().__init__(name, price, description)
    
    def getName(self=None):
        return 'Ultraäänitutkimus'
    
    def ObjectCreator(self=None):
        return Ultrasonic

'''
    
'''
class EndoscopyBase(OperationBase):
    __tablename__='endoscopybases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'endoscopybases',}
    def __init__(self, name, price, description):
        super().__init__(name, price, description)

    def getName(self=None):
        return 'Endoskooppitutkimus'
    
    def ObjectCreator(self=None):
        return Endoscopy
    
'''
    
'''
class DentalexaminationBase(OperationBase):
    __tablename__='dentalexaminationbases'
    id = Column(Integer, ForeignKey('operationbases.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'dentalexaminationbases',}
    def __init__(self, name, price, description):
        super().__init__(name, price, description)
    
    def getName(self=None):
        return 'Hammashoito'

    def ObjectCreator(self=None):
        return Dentalexamination
#----------------------------------------------
#
#                Operations
#
#----------------------------------------------

'''
    These classes are for visit to handle and save operations thet have been done.
'''
class Operation(Base):
    __tablename__='operations'
    id = Column(Integer, Sequence('operations_id_seq'), primary_key=True)
    visitanimal_id = Column(Integer, ForeignKey('visitanimals.id'))
    price = Column(Integer)
    count = Column(Integer)
    description = Column(String(500))
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_identity':'operations','polymorphic_on':type}
    def __init__(self, price, description, base=None, count=1):
        self.price = price
        self.description = description
        
        if isinstance(count, int):
            self.count = count
        else:
            self.count = 1
    
    def update(self, data):
        self.price = data[0]
        self.description = data[1]
        if(len(data)>2):
            self.base = data[2]
        if(len(data)>3):
            self.count = data[3]
        
    def getType(self):
        return 'Operation'
    
    def hasList(self=None):
        return False
    
    def stringList(self):
        return [str(self.id), self.base.getName(), self.base.name, str(self.price)]
#TODO: check that medicines is valid table name and you can call id for it

class Basic(Operation):
    __tablename__='basics'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("OperationBase")
    __mapper_args__ = {'polymorphic_identity':'basics',}
    def __init__(self,price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base



'''

'''   
class Vaccination(Operation):
    __tablename__='vaccinations'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("VaccinationBase")
    __mapper_args__ = {'polymorphic_identity':'vaccinations',}
    def __init__(self,price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def stringList(self):
        return [str(self.id), self.base.getName(), self.base.name, str(self.price+self.base.item.price) if self.base.item != None else str(self.price)]


'''

'''
class SurgeryItem(Base):
    __tablename__='surgeryitems'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    surgery_id = Column(Integer, ForeignKey('surgerys.id'))
    item = relationship("Item")
    count = Column(Integer)
    def __init__(self,item,count=1):
        self.item = item
        self.count = count
        
    def getType(self=None):
        return 'SurgeryItem'
    
    def stringList(self):
        string_list = self.item.stringList()
        string_list[3] = str(float(string_list[3]) * self.count)
        string_list.append(str(self.count))
        return string_list

class Surgery(Operation):
    __tablename__='surgerys'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("SurgeryBase")
    items = relationship("SurgeryItem")
    __mapper_args__ = {'polymorphic_identity':'surgery',}
    def __init__(self,price, description, base, items):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base
        self.items = []
        
        for item in items:
            if item.getType() == SurgeryItem.getType():
                self.items.append(item)
            else:
                self.items.append(SurgeryItem(item=item.item,count=item.count))
                
    
    def update(self, data):
        super(Surgery,self).update(data)#TODO check
        self.items = data[3]
        
    def hasList(self=None):
        return True

    def stringList(self):
        price = 0.0
        for i in self.items:
            price += float(i.item.price) * i.count
        price += self.price
        return [str(self.id), self.base.name, self.base.getName(), str(price)]
'''

'''
           
class Lab(Operation):
    __tablename__='labs'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("LabBase")
    path = Column(String(255))
    __mapper_args__ = {'polymorphic_identity':'lab',}
    def __init__(self,price, description, base, path=''):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base
        self.path = path
        
    def update(self, data):
        super(Lab,self).update(data)
        self.path = data[3]

'''

'''
class Medication(Operation):
    __tablename__='medications'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("MedicationBase")
    __mapper_args__ = {'polymorphic_identity':'medications',}
    def __init__(self, price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def stringList(self):
        return [str(self.id), self.base.getName(), self.base.name, str(self.price+self.base.item.price) if self.base.item != None else str(self.price)]
'''

'''
class Lameness(Operation):
    __tablename__='lameness'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship(LamenessBase)
    #pictures = relationship("Picture")
    __mapper_args__ = {'polymorphic_identity':'lameness',}
    def __init__(self, price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def update(self, data):
        super(Lameness,self).update(data)
        #self.pictures = data[3]
'''

'''
class Xray(Operation):
    __tablename__='xrays'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("XrayBase")
    #pictures = relationship("Picture")
    __mapper_args__ = {'polymorphic_identity':'xray',}
    def __init__(self, price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def update(self, data):
        super(Xray,self).update(data)
        #self.pictures = data[3]

'''
    
'''
class Ultrasonic(Operation):
    __tablename__='ultrasonics'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("UltrasonicBase")
    #pictures = relationship("Picture")
    __mapper_args__ = {'polymorphic_identity':'ultrasonic',}
    def __init__(self, price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def update(self, data):
        super(Ultrasonic,self).update(data)
        #self.pictures = data[3]

'''
    
'''
class Endoscopy(Operation):
    __tablename__='endoscopys'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("EndoscopyBase")
    #pictures = relationship("Picture")
    __mapper_args__ = {'polymorphic_identity':'endoscopy',}
    def __init__(self, price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def update(self, data):
        super(Endoscopy,self).update(data)
        #self.pictures = data[3]

'''
    
'''
class Dentalexamination(Operation):
    __tablename__='dentalexaminations'
    id = Column(Integer, ForeignKey('operations.id'), primary_key=True)
    base_id  = Column(Integer, ForeignKey('operationbases.id'))
    base = relationship("DentalexaminationBase")
    #pictures = relationship("Picture")
    __mapper_args__ = {'polymorphic_identity':'dentalexamination',}
    def __init__(self, price, description, base):
        super().__init__(price, description)
        self.base_id = base.id
        self.base = base

    def update(self, data):
        super(Dentalexamination,self).update(data)
        #self.pictures = data[3]



class RecipieMedicine(Base):
    __tablename__='recipiemedicines'
    id = Column(Integer, Sequence('recipiemedicines_id_seq'), primary_key=True)
    medicine_id = Column(Integer, ForeignKey('items.id'))
    medicine = relationship("Item")
    count = Column(Integer)
    
    def __init__(self, medicine, count=1):
        self.medicine = medicine
        self.medicine_id = medicine.id
        self.count = count
    
    def update(self, data):
        self.medicine = data[0]
        self.medicine_id = data[0].id
        self.count = data[1]

    def stringList(self):
        return [str(self.id), self.medicine.name, str(self.count)]

recipie_medicine_table = Table('recipie_medicines', Base.metadata,
                               Column('recipiemedicines_id', Integer,ForeignKey('recipiemedicines.id')),
                               Column('phonerecipie_id', Integer, ForeignKey('phonerecipies.id')))

class PhoneRecipie(Base):
    __tablename__='phonerecipies'
    id = Column(Integer, Sequence('phonerecipies_id_seq'), primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    animal = relationship("Animal")
    made_time = Column(Date)
    call_time = Column(Date)
    
    recipiemedicines = relationship("RecipieMedicine", secondary = recipie_medicine_table)
    def __init__(self, animal,recipiemedicines=[]):
        self.animal = animal
        self.animal_id = animal.id
        self.made_time = datetime.datetime.now()
        self.recipiemedicines = recipiemedicines
        
    def update(self, data):
        self.animal = data[0]
        self.made_time = data[1]
        self.call_time = data[2]
        self.recipiemedicines = data[3]
        
    def stringList(self):
        temp = [str(self.id),str(self.made_time), str(self.call_time) if self.call_time != None else '']
        temp2 = ''
        for item in self.recipiemedicines:
            temp2 += item.medicine.name + ' x ' + str(item.count) + ' '
        temp2 = temp2.strip()
        temp.append(temp2)
        return temp
