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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Date
from sqlalchemy.orm import relationship

from models import Base
from models.vet import Vet
import datetime

class Note(Base):
    #Asetetaan taulukon nimi
    __tablename__ = 'notes'
        
    #maaritellaan taulukon olioiden asetukset
    id = Column(Integer, Sequence('notes_id_seq'), primary_key=True)
    
    vet_id = Column(Integer, ForeignKey('vets.id'))
    vet = relationship('Vet')

    made = Column(Date, nullable=False)
    title = Column(String(255),nullable=False)
    text = Column(String(1000),nullable=False)
        
    def __init__(self, vet_id, title, text):
        self.vet_id = vet_id
        self.made = datetime.datetime.now()
        self.title = title
        self.text = text
    
    
