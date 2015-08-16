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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Date, Table, Text
from sqlalchemy.orm import relationship

from models import Base
#import datetime

'''
    Appointment
    -id            Integer
    -start_time    Date
    -end_time      Date
    -amanuensis    String(1000)
    -owner_id      Integer
    
    -owner
    -animals       appointmant_animals_table
    
'''

appointment_animals_table = Table('appointment_animals', Base.metadata,
    Column('animal_id', Integer, ForeignKey('animals.id')),
    Column('appointment_id', Integer, ForeignKey('appointments.id'))
)

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, Sequence('appointments_id_seq'), primary_key=True)
    start_time = Column(Date, nullable=False)
    end_time = Column(Date, nullable=False) 
    amanuensis = Column(Text)
    
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    owner = relationship('Owner')
    
    animals = relationship("Animal", secondary = appointment_animals_table)

    def __init__(self, owner_id, start_time, end_time, amanuensis):
        self.owner_id = owner_id
        self.start_time = start_time
        self.end_time = end_time
        self.amanuensis = amanuensis
        
    
    def length(self):
        return self.end_time - self.start_time 