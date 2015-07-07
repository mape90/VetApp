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
from sqlalchemy import Column, Integer, String, Sequence, Interval, ForeignKey, Table, Float, DateTime
from sqlalchemy.orm import relationship, backref

from models import Base
from models.specie import Specie


from models.translationtables import g_item_alv_dict
from models.translationtables import g_item_name_dict

class ALV(Base):
    __tablename__ = 'alvs'
    id = Column(Integer, Sequence('alvs_id_seq'), primary_key=True)
    alv = Column(Integer)
    alv_class = Column(Integer, unique=True)
    
    def __init__(self,alv, alv_class):
        self.alv = alv
        self.alv_class = alv_class
        
    def update(self, data):
        self.alv = data[0]
        self.alv_class = data[1]
    


class ItemStrings():
    item = 'Item'
    medicine = 'Medicine'
    drug = 'Drug'
    vaccine = 'Vaccine'
    feed = 'Feed'

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence('items_id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(1000))
    stock_price = Column(Integer)
    price = Column(Integer)
    barcode = Column(String(100))
    item_type = Column(String(50))

    count_type = Column(String(10))

    customer_descriptions = relationship("ItemDescription", backref='item', cascade="all, delete, delete-orphan")
    __mapper_args__ = {'polymorphic_identity':'item','polymorphic_on':item_type}
    def __init__(self, name, description, stock_price, price, barcode=''):
        self.name = name
        self.description = description
        self.stock_price = stock_price
        self.price = price
        self.barcode = barcode
        self.customer_descriptions=[]
        self.count_type = 'kpl'
 
    def update(self, data):      
        for key, item in data.items():
            try:
                setattr(self, key, item)
            except:
                print("DEBUG ERROR Item->update(): wrong variable name: " + str(key))
    
    def stringList(self):
        return [str(self.id), self.name, self.typeName(), ('%.2f' % self.price)]
    
    def hasDuration(self=None):
        return False
    
    def getType(self=None):
        return ItemStrings.item
    
    def typeName(self=None):
        return g_item_name_dict[ItemStrings.item]
    
    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(g_item_alv_dict[ItemStrings.item])




'''
    Item class for medicines
'''
class Medicine(Item):
    __tablename__='medicines'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    duration = Column(Interval)
    __mapper_args__ = {'polymorphic_identity':'medicine',}
    def __init__(self, name, description, stock_price, price, barcode='', duration=None):
        super().__init__(name, description, stock_price, price, barcode)
        self.duration = duration

    def hasDuration(self=None):
        return True
    
    def getType(self=None):
        return ItemStrings.medicine

    def typeName(self=None):

        return g_item_name_dict[ItemStrings.medicine]

    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(g_item_alv_dict[ItemStrings.medicine])


class DrugUsage(Base):
    __tablename__='drugusages'
    id = Column(Integer, primary_key=True)
    drug_id = Column(Integer, ForeignKey('medicines.id'))
    drug = relationship("Drug") #will this work or shuld it be Medicine?
    amount = Column(Float)
    time = Column(DateTime)
    
    def __init__(self,drug, amount, time):
        self.drug = drug
        self.drug_id = drug.id
        self.amount = amount
        self.time = time
        

class Drug(Medicine):
    __tablename__='drugs'
    id = Column(Integer, ForeignKey('medicines.id'), primary_key=True)
    duration = Column(Interval)  
    
    opening_time = Column(DateTime)
    end_time = Column(DateTime)
    batch_nunber = Column(String(255))
    
    __mapper_args__ = {'polymorphic_identity':'drug',}
    def __init__(self, name, description, stock_price, price, opening_time,batch_nunber,end_time=None, barcode='', duration=None):
        super().__init__(name, description, stock_price, price, barcode, duration)
        self.opening_time = opening_time
        self.end_time = end_time
        self.batch_nunber = batch_nunber
        
        
    def getType(self=None):
        return ItemStrings.drug
    
    def typeName(self=None):
        return g_item_name_dict[ItemStrings.drug]

    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(g_item_alv_dict[ItemStrings.drug])

'''
    Item class for feed.
    
    This class currently dosent add anything
'''
    
'''
    Item class for vaccines
'''
class Vaccine(Medicine):
    __tablename__='vaccines'
    id = Column(Integer, ForeignKey('medicines.id'), primary_key=True)
    duration = Column(Interval)
    __mapper_args__ = {'polymorphic_identity':'vaccine',}
    def __init__(self, name, description, stock_price, price, barcode='', duration=None):
        super().__init__(name, description, stock_price, price, barcode, duration)
    
    def getType(self=None):
        return ItemStrings.vaccine
    
    def typeName(self=None):
        return g_item_name_dict[ItemStrings.vaccine]

    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(g_item_alv_dict[ItemStrings.vaccine])
    

class Feed(Item):
    __tablename__='feeds'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'feed',}
    def __init__(self, name, description, stock_price, price, barcode=''):
        super().__init__(name, description, stock_price, price, barcode)

    def getType(self=None):
        return ItemStrings.feed

    def typeName(self=None):
        return g_item_name_dict[ItemStrings.feed]

    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(g_item_alv_dict[ItemStrings.feed])


'''
    This class is because for different species needs different 
    threatment quides.
    -specie (specie_id)
    -text
'''
class ItemDescription(Base):
    __tablename__ = 'itemdescriptions'
    id = Column(Integer, Sequence('itemdescriptions_id_seq'), primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    specie_id = Column(Integer, ForeignKey('species.id'))
    specie = relationship("Specie")
    text = Column(String(1000))
    def __init__(self, specie, text):
        self.specie = specie
        self.text = text

    def update(self, data):
        for key, item in data.items():
            try:
                setattr(self,key,item)
            except:
                print("DEBUG ERROR ItemDescription->update(): wrong variable name: " + str(key))

    def stringList(self):
        return [str(self.id), self.specie.name, self.text]
