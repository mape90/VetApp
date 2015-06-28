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
from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship, backref

from models import Base

class SummaryText(Base):
    __tablename__ = 'summarytexts'
    id = Column(Integer, Sequence('summarytexts_id_seq'), primary_key=True)
    name = Column(Integer, unique=True)
    text = Column(String(5000))
    
    def __init__(self,name, text):
        self.name = name
        self.text = text
        
    def update(self, data):
        for key in data.keys:
            try:
                setattr(self, key, data[key])
            except:
                logError("SummaryText, update, unknown key, " key)