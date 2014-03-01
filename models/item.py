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
from sqlalchemy import Column, Integer, String, Sequence, Interval, ForeignKey, Table
from sqlalchemy.orm import relationship, backref

from models import Base
from models.specie import Specie


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
    



class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, Sequence('items_id_seq'), primary_key=True)
    name = Column(String(50))
    description = Column(String(1000))
    stock_price = Column(Integer)
    price = Column(Integer)
    barcode = Column(String(100))
    item_type = Column(String(50))
    customer_descriptions = relationship("ItemDescription", backref='item', cascade="all, delete, delete-orphan")
    __mapper_args__ = {'polymorphic_identity':'item','polymorphic_on':item_type}
    def __init__(self, name, description, stock_price, price, barcode=''):
        self.name = name
        self.description = description
        self.stock_price = stock_price
        self.price = price
        self.barcode = barcode
        self.customer_descriptions=[]
 
    def update(self, itemlist):
        self.name = itemlist[0]
        self.price = itemlist[1]
        self.stock_price = itemlist[2]
        self.barcode = itemlist[3]
        self.description = itemlist[4]
        self.customer_descriptions = itemlist[5]
    
    def stringList(self):
        return [str(self.id), self.name, self.typeName(), str(self.price)]
    
    def hasDuration(self=None):
        return False
    
    def getType(self=None):
        return 'Item'
    
    def typeName(self=None):
        return 'Tuote'
    
    def getALVClass(self=None):
        return 1
    
    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(1)




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

    def update(self, itemlist):
        Item.update(self,itemlist[:6])
        self.duration = itemlist[6]

    def hasDuration(self=None):
        return True
    
    def getType(self=None):
        return 'Medicine'

    def typeName(self=None):
        return 'Lääke'
    
    def getALVClass(self=None):
        return 2
    
    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(2)
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
        return 'Vaccine'
    
    def typeName(self=None):
        return 'Rokote'
    

class Feed(Item):
    __tablename__='feeds'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'feed',}
    def __init__(self, name, description, stock_price, price, barcode=''):
        super().__init__(name, description, stock_price, price, barcode)

    def getType(self=None):
        return 'Feed'

    def typeName(self=None):
        return 'Rehu'
    
    def getALVClass(self=None):
        return 3
    
    def getALV(self=None):
        from models import SqlHandler
        return SqlHandler.getALV(3)
'''
    Item class for anthelmintics
    
    This class currently dosent add anything
'''
'''class Anthelmintic(Item):
    __tablename__='anthelmintics'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'anthelmintic',}
    def __init__(self, name, description, stock_price, price, barcode='', image_path=''):
        super().__init__(name, description, stock_price, price, barcode, image_path)
'''

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
        self.specie_id = specie.id
        self.text = text
        
    def stringList(self):
        return [str(self.id), self.specie.name, self.text]
