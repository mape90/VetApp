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
from models.item import *

from configfile import logDEBUG, logERROR



class GlobalVar(Base):
    __tablename__='globalvars'
    id = Column(Integer, Sequence('globalvars_id_seq'), primary_key=True)
    key = Column(String(255), unique=True)
    value = Column(Text)

    def __init__(self, key, value):
        print("DEBUG initing GlobalVar")
        self.key = key
        self.value = value