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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

from models import Base
from models.vet import Vet

import datetime

'''
    id
    starttime
    endtime
    vet_id
    owner_id
    amanuensis
    status
    diagnosis
    treatment
'''
                                   
class VisitAnimal(Base):
    __tablename__='visitanimals'
    id = Column(Integer, Sequence('visitanimals_id_seq'), primary_key=True)
    animal_id = Column(Integer, ForeignKey('animals.id'), nullable=False)
    animal = relationship("Animal")
    
    anamnesis = Column(String(1000))
    status = Column(String(1000))
    diagnosis = Column(String(1000))
    treatment = Column(String(1000))
    
    operations = relationship("Operation", backref='visitanimals', cascade="all, delete-orphan")
    
    def __init__(self,animal, anamnesis='', status='', diagnosis='', treatment=''):
        self.animal = animal
        self.animal_id = animal.id
        self.anamnesis = anamnesis
        self.status = status
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.operations = []
    
    def stringList(self):
        return [str(self.id), self.animal.name, self.animal.official_name, 
                self.animal.specie.name if self.animal.specie != None else '', 
                self.animal.race.name if self.animal.race != None else '']
        
    def getType(self=None):
        return 'VisitAnimal'
    
    def update(self,itemList):
        if itemList != None and len(itemList) == 5:
            print('VisitAnimal.update: ',itemList)
            self.anamnesis = itemList[0]
            self.status = itemList[1]
            self.diagnosis = itemList[2]
            self.treatment = itemList[3]
            self.operations = itemList[4]
        else:
            print('VisitAnimal functio update got wrong lenght itemlist')


visit_animals_table = Table('visit_animals_table', Base.metadata,
                      Column('visitanimal_id', Integer, ForeignKey('visitanimals.id')),
                      Column('visit_id', Integer, ForeignKey('visits.id')))


class Visit(Base):
    #Asetetaan taulukon nimi
    __tablename__ = 'visits'
    #maaritellaan taulukon olioiden asetukset
    id = Column(Integer, Sequence('visits_id_seq'), primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    
    vet_id = Column(Integer, ForeignKey('vets.id'), nullable=False)
    vet = relationship("Vet")
    
    owner_id = Column(Integer, ForeignKey('owners.id'))
    owner = relationship("Owner")
    
    visitanimals = relationship("VisitAnimal", secondary = visit_animals_table)
    
  
    def __init__(self, start_time, owner, vet, end_time=None):
        self.start_time = self.setCurrentTime()
        self.owner = owner
        self.owner_id = owner.id
        self.vet = vet
        self.vet_id = vet.id
        self.end_time = end_time
        self.visitanimals = []
   
    def setCurrentTime(self):
        self.endtime = datetime.datetime.now()
    
    def getType(self):
        return 'Visit'  
      
    def update(self, items):
        self.start_time = items[0]
        self.owner = items[1]
        self.owner_id = items[1].id
        self.vet = items[2]
        self.vet_id = items[2].id
        self.end_time = items[3]
        self.visitanimals = items[4]
        
        
    def stringList(self):
        return [str(self.id), self.owner.name, str(self.start_time)]
        
        