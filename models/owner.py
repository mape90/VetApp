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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Table
from sqlalchemy.orm import relationship

from models import Base
from models.postoffice import PostOffice, PostNumber

from models.animal import *

#Change this to work with multiple import
own_table = Table('own', Base.metadata,
    Column('animal_id', Integer, ForeignKey('animals.id')),
    Column('owner_id', Integer, ForeignKey('owners.id'))
)

'''
    Class Owner
    -id             Integer
    -name           String(100)
    -address        String(100)
    -post_office_id Integer
    -post_office    Link(PostOffice)
    -postnumber     String(50)
    -email          String(100)
    -other_info     String(500)
    -flags          Integer
'''
class Owner(Base):
    __tablename__ = "owners"
    id = Column(Integer, Sequence('owners_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    
    animals = relationship("Animal", secondary = own_table, backref="Owner")
    
    address = Column(String(100))
    post_office_id = Column(Integer, ForeignKey('postoffices.id'))
    post_office = relationship("PostOffice")
    postnumber_id = Column(Integer, ForeignKey('postnumbers.id'))
    postnumber = relationship("PostNumber")
    
    phonenumber = Column(String(100))
    email = Column(String(100))
    other_info = Column(String(500))
    flags = Column(Integer)
    
    __table_args__ = {'extend_existing': True}
    def __init__(self, name, address, post_office_id, postnumber_id, email, phonenumber, other_info, flags=0, animals=[]):
        self.name = name
        self.address = address
        self.post_office_id = post_office_id
        self.postnumber_id = postnumber_id
        self.email = email
        self.phonenumber = phonenumber
        self.other_info = other_info
        self.flags = flags
        self.animals = animals
    
    def getType(self):
        return 'Owner'
    
    def stringList(self):
        return [str(self.id), self.name]
    
    def update(self, items):
        self.name = items[0]
        self.address = items[1]
        self.post_office_id = items[2]
        self.postnumber_id = items[3]
        self.email = items[4]
        self.phonenumber = items[5]
        self.other_info = items[6]
        self.flags = items[7]
        self.animals = items[8]
        
        