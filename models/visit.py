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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Table, Float, Boolean
from sqlalchemy.orm import relationship

from models.translationtables import g_medicines_list

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

    items = relationship("VisitItem", backref='visitanimals', cascade="all, delete-orphan")
    
    def __init__(self,animal, anamnesis='', status='', diagnosis='', treatment=''):
        self.animal = animal
        self.animal_id = animal.id
        self.anamnesis = anamnesis
        self.status = status
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.operations = []
        self.items = []
    
    def stringList(self):
        return [self.animal.name, self.animal.official_name, 
                self.animal.specie.name if self.animal.specie != None else '', 
                self.animal.race.name if self.animal.race != None else '']

    #get visit animal all items
    def getAllItems(self):
        l =[]
        for i in self.items: #list has VisitItems
            l.extend(i.item)
        for oper in operations:
            l.extend(oper.getItems())
        return l

    #return all medicine texts in format {name1 : text1, name2:text2,...}
    def getMedicineDict(self):
        tmp = {}
        for item in self.getAllItems():
            if item.getType() in g_medicines_list:
                for desc in item.customer_descriptions:
                    if desc.specie is self.animal.specie:
                        tmp[item.name] = desc.text
        return tmp

    def getType(self=None):
        return 'VisitAnimal'
    
    def update(self,data):
        for key, item in data.items():
            try:
                setattr(self,key,item)
            except:
                print("DEBUG ERROR VisitAnimal->update(): wrong variable name: " + str(key))


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
    
    owner_id = Column(Integer, ForeignKey('owners.id'), nullable=False)
    owner = relationship("Owner")
    
    visit_reason = Column(String(255), default="")

    visitanimals = relationship("VisitAnimal", secondary = visit_animals_table)

    archive = Column(Boolean, default=False)

    def __init__(self, start_time, owner, vet, end_time=None, visitanimals = []):
        self.start_time = start_time
        self.owner = owner
        self.vet = vet
        self.end_time = end_time
        self.visitanimals = visitanimals
   

    def getPriceDict(self):
        price_dict = {}
        price_dict["operation_price"] = 0.0
        price_dict["accesories_price"] = 0.0
        price_dict["lab_price"] = 0.0
        price_dict["medicine_price"] = 0.0
        price_dict["diet_price"] = 0.0

        for visit_animal in self.visitanimals:
            for operation in visit_animal.operations:
                tmp = operation.getPriceDict()
                for key in tmp:
                    price_dict[key] += tmp[key]

            for visititem in visit_animal.items:
                tmp = visititem.getPriceDict()
                for key in tmp:
                    price_dict[key] += tmp[key]

        return price_dict



    def setCurrentTime(self):
        self.endtime = datetime.datetime.now()
    
    def getType(self):
        return 'Visit'  

    def update(self, data):
        for key, item in data.items():
            try:
                setattr(self,key,item)
            except:
                print("DEBUG ERROR Visit->update(): wrong variable name: " + str(key))

        
    def stringList(self):
        return [str(self.id), self.visit_reason, str(self.start_time)]
        
        