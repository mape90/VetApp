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

from sqlalchemy import Column, Integer, String, Date, Sequence, ForeignKey
from sqlalchemy.orm import relationship

import datetime
#import Base from init file
from models import Base
from models.specie import Specie
#from models.picture import Picture
#from models.owner import Owner

'''
classes:
    Animal
    Color
    Sex
    Race
'''

'''
    Class Animal
    Has all information about Animal
    -name(String(50)) is nickname
    -official_name(String(50)) is offical name
    -race_id(int) is id of animal race_id
    -race is link to the race objet behind race_id (Many to one)
    -specie_id(int) is id of specie
    -specie is link (Many to one)
    -sex_id(int) is id of sex 
    -sex is link (Many to one)
    -color_id(int) is id of color 
    -color (Many to one)
    -birthday = Column(Date)
    -micro_num = Column(String(50))
    -rec_num = Column(String(50))
    -tattoo = Column(Sring(50))
    -insurance = Column(String(100))
    -main_owner_id = Column(Integer, ForeignKey('owners.id'))
    -animal_picture_path = Column(Integer, ForeignKey('pictures.id'))
    -passport = Column(String(50))
    -other_info = Column(String(255))
    -death_day = Column(Date)
    -flags = Column(Integer)
'''
class Animal(Base):
    #Asetetaan taulukon nimi
    __tablename__ = 'animals'
    #maaritellaan taulukon olioiden asetukset
    id = Column(Integer, Sequence('animals_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    official_name = Column(String(50))
    birthday = Column(Date)
    micro_num = Column(String(50))
    rec_num = Column(String(50))
    tattoo = Column(String(50))
    insurance = Column(String(200))
    passport = Column(String(100))
    other_info = Column(String(500))
    death_day = Column(Date)
    flags = Column(Integer)
    
    #Setup Many to one links
    
    specie_id = Column(Integer, ForeignKey('species.id'))
    specie = relationship("Specie")
    
    sex_id = Column(Integer, ForeignKey('sexs.id'))
    sex = relationship("Sex")
    
    race_id = Column(Integer, ForeignKey('races.id'))
    race = relationship("Race")
    
    color_id = Column(Integer, ForeignKey('colors.id'))
    color = relationship("Color")
    
    __table_args__ = {'extend_existing': True}
    def __init__(self, name, official_name, race_id, specie_id, sex_id, 
                 color_id, birthday, micro_num, rec_num, tattoo, 
                 insurance, passport, other_info):
        self.name = name
        self.official_name = official_name
        self.race_id = race_id
        self.specie_id = specie_id
        self.sex_id = sex_id
        self.color_id = color_id
        self.birthday = birthday
        self.micro_num = micro_num
        self.rec_num = rec_num
        self.tattoo = tattoo
        self.insurance = insurance
        self.passport = passport
        self.other_info = other_info
        self.death_day = None
        self.flags = 0
    #return datetime object that has age of animal
    def getAge(self):
        return self.birthday - datetime.datetime.now()
    
    def getType(self):
        return 'Animal'
    
    def getName(self):
        return 'Eläin'
    
    def update(self, items):
        self.name = items[0]
        self.official_name = items[1]
        self.race_id = items[2]
        self.specie_id = items[3]
        self.sex_id = items[4]
        self.color_id = items[5]
        self.birthday = items[6]
        self.micro_num = items[7]
        self.rec_num = items[8]
        self.tattoo = items[9]
        self.insurance = items[10]
        self.passport = items[11]
        self.other_info = items[12]
        self.death_day = items[13]
        self.flags = items[14]
        
    def stringList(self):
        return [str(self.id), self.name, self.official_name, self.specie.name if self.specie != None else '', self.race.name if self.race != None else '']

    
    def picurePath(self):
        if self.specie != None:
            return self.specie.picture_path
        else:
            return ''
    
    '''
    This class just saves space because we dont have to save color string to for all animals
    -name is name of color
    '''
class Color(Base):
    __tablename__ = 'colors'
    id = Column(Integer, Sequence('colors_id_seq'), primary_key=True)
    specie_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    specie = relationship("Specie")
    name = Column(String(50), nullable=False)
    __table_args__ = {'extend_existing': True}
    def __init__(self, name, specie_id):
        self.name = name
        self.specie_id = specie_id

'''
    This class helps us to handle with different sex names between species
    -specie_id is specie_id
'''
class Sex(Base):
    __tablename__ = 'sexs'
    id = Column(Integer, Sequence('sex_id_seq'), primary_key=True)
    name = Column(String(50), nullable=False)
    __table_args__ = {'extend_existing': True}
    def __init__(self, name):
        self.name = name
        
        
class Race(Base):
    __tablename__ = 'races'
    id = Column(Integer, Sequence('races_id_seq'), primary_key=True)
    specie_id = Column(Integer, ForeignKey('species.id'), nullable=False)
    specie = relationship("Specie")
    name = Column(String(50), nullable=False)
    __table_args__ = {'extend_existing': True}
    def __init__(self, name, specie_id):
        self.name = name
        self.specie_id = specie_id


class WeightControl(Base):
    __tablename__='weightcontrols'
    id = Column(Integer, Sequence('weightcontrols_id_seq'), primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    animal = relationship("Animal")
    date = Column(Date)
    weight = Column(Integer)
    __table_args__ = {'extend_existing': True}
    def __init__(self, animal_id, weight):
        self.animal_id = animal_id
        self.weight = weight
        self.date = datetime.date.today()
    
    def stringList(self):
        return [str(self.id),str(self.date), str(self.weight)+' Kg']
    