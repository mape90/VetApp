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
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship

from models import Base
from models.postoffice import PostOffice

import hashlib

'''
    Vet
    -id
    -name
    -address
    -post_office_id
    -post_nunmber
    -password_hash
    -y_number
    -vet_number
    -Bank_name
    -IBAN
    
    CustomerText
    -id
    -vet_id
    -language
    -text
    
    ContactInfo
    -id
    -vet_id
    -name
    -text
    -type
    
    Phonenumber(ContactInfo)
    -id
    
    Email(ContactInfo)
    -id
'''

class Vet(Base):
    __tablename__ = 'vets'
    id = Column(Integer, Sequence('vets_id_seq'), primary_key=True)
    name = Column(String(255))
    
    address = Column(String(255))
    post_office_id = Column(Integer, ForeignKey('postoffices.id'))
    post_office = relationship("PostOffice")
    postnumber_id = Column(Integer, ForeignKey('postnumbers.id'))
    postnumber = relationship("PostNumber")
    
    password_hash = Column(String(128))
    
    y_number = Column(String(50))
    vet_number = Column(String(50))
    alv_number = Column(String(50))
    
    bank_name = Column(String(255))
    
    IBAN = Column(String(30))
    SWIF = Column(String(25))

    archive = Column(Boolean, default=False)
    
    
    customertexts = relationship("CustomerText")
    contactinfos = relationship("ContactInfo")
    def __init__(self, data):
        self.update(data)
        
        self.name = name
        self.address = address
        self.post_office = post_office
        if post_office != None:
            self.post_office_id = post_office.id
        self.postnumber = postnumber
        if postnumber != None:
            self.postnumber_id = postnumber.id
        self.y_number= y_number
        self.vet_number = vet_number
        #self.alv_number = alv_number
        self.bank_name = bank_name
        self.IBAN = IBAN
        self.SWIF = SWIF
        finnish_text = CustomerText(language='FIN', text=customertexts[0])
        english_text = CustomerText(language='EN', text=customertexts[1])
        swedish_text = CustomerText(language='SWE', text=customertexts[2])
        
        self.customertexts = [finnish_text,english_text,swedish_text]
        
        for info in contactinfos:
            self.contactinfos.append(info)

    def hashPassword(self, password, name):
        return hashlib.sha512(password.encode("utf-8") + name.encode("utf-8")).hexdigest()
    
    def checkPassword(self, password):
        if self.password_hash != None:
            return self.password_hash == self.hashPassword(password, self.name)
        else:
            print("ERROR: Unset password! DEBUG continue with True")
            return True
    
    def getType(self=None):
        return 'Vet'
    
    def updateCustomerText(self, key, text):
        for customertext in self.customertexts:
            if(customertext.language == key):
                customertext.text = text
                return
        #add key if it wanst found
        customertext.append(CustomerText(language=key, text=text))
    
    def update(self, data):
        for key, item in data.items():
            if hasattr(self, key):
                setattr(self, key, item)
            elif key in ["FIN", "EN", "SWE"]:
                self.updateCustomerText(key, item)
            elif key is "password":
                if "name" in data:
                    setattr(self, key, self.hashPassword(item, data["name"]))
                elif self.name != None:
                    setattr(self, key, self.hashPassword(item, self.name))
                else:
                    print("ERROR vet do not have name. Can not salt password!")
            else:
                print("DEBUG ERROR Vet->update(): wrong variable name: " + str(key))


class CustomerText(Base):
    __tablename__='customertexts'
    id = Column(Integer, Sequence('customertexts_id_seq'), primary_key=True)
    vet_id = Column(Integer, ForeignKey('vets.id'), nullable=False)
    language = Column(String(3), nullable=False)
    text = Column(Text)
    def __init__(self, language, text):
        self.language = language
        self.text = text
    
    def update(self, newText):
        self.text = newText


class ContactInfo(Base):
    __tablename__='contactinfos'
    id = Column(Integer, Sequence('contactinfos_id_seq'), primary_key=True)
    name = Column(String(255))
    text = Column(Text, nullable=False)
    vet_id = Column(Integer, ForeignKey('vets.id'), nullable=False) 
    type = Column(String(50))
    __mapper_args__ = {'polymorphic_identity':'contactinfo','polymorphic_on':type}
    def __init__(self,name, text):
        self.name = name
        self.text = text

class Phonenumber(ContactInfo):
    __tablename__='phonenumbers'
    id = Column(Integer, ForeignKey('contactinfos.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'phonenumber',}
    def __init__(self,name, text):
        super().__init__(name, text)

  
class Email(ContactInfo):
    __tablename__='emails'
    id = Column(Integer, ForeignKey('contactinfos.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity':'email',}
    def __init__(self, name, text):
        super().__init__(name, text)
