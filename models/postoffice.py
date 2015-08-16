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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from models import Base

'''
    PostOffice
    -id             (int) (primary key)
    -name           (string(50))
    
    ---------------------------
    
    PostNumber
    -id             (int) (primary key)
    -post_office_id (int) 
    (-post_office   (PostOffice))
    -number         (string(10))
    
'''

class PostOffice(Base):
    __tablename__ = 'postoffices' 
    #maaritellaan taulukon olioiden asetukset
    id = Column(Integer, Sequence('postoffices_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False) 
    
    __table_args__ = {'extend_existing': True}
    
    def __init__(self, name):
        self.name = name
        
class PostNumber(Base):
    __tablename__="postnumbers"
    id = Column(Integer, Sequence('postnumber_id_seq'), primary_key=True)
    
    post_office_id = Column(Integer, ForeignKey('postoffices.id'), nullable=False)
    post_office = relationship('PostOffice')
    
    number = Column(String(10), nullable=False)
    
    __table_args__ = {'extend_existing': True}
    
    def __init__(self, post_office_id, number):
        self.post_office_id = post_office_id
        self.number = number
        
        