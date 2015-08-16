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
from sqlalchemy import Integer, Sequence, String, Column
from models import Base
'''
    This class helps us to handle with differSanakirjaences between species
    -name is name of specie
'''
class Specie(Base):
    __tablename__ = "species"  
    id = Column(Integer, Sequence('specie_id_seq'), primary_key=True)
    name = Column(String(100), nullable=False)
    __table_args__ = {'extend_existing': True}
    def __init__(self, name):
        self.name = name