#!/usr/bin/python
# -*- coding: utf-8
#-------------------------------------------------------------------
#This class is made to work as a interface to database 
#for other widgets
#
#
#crator: Markus Peltola, last update 24.2.2013
#-------------------------------------------------------------------
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

from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker

from sqlalchemy import or_, and_

from sqlalchemy.orm.exc import NoResultFound

#this is for logging data TODO: configure it
#import logging

#import database objects
from models.appointment import Appointment
from models.item import Item, Vaccine, Medicine, Feed, ItemDescription, ALV
from models.note import Note
from models.todo import Todo
from models.owner import Owner
from models.animal import Animal, Color, Sex, Race, WeightControl
from models.picture import Picture
from models.postoffice import PostOffice, PostNumber
from models.specie import Specie
from models.visit import Visit, VisitAnimal
from models.vet import Vet, CustomerText, ContactInfo, Phonenumber, Email
from models.operation import Operation, Vaccination, Surgery, Lab, Medication, Lameness, Xray, Ultrasonic, Basic
from models.operation import Endoscopy, Dentalexamination, OperationBase, VaccinationBase
from models.operation import SurgeryBase, MedicationBase, LamenessBase, XrayBase
from models.operation import UltrasonicBase, EndoscopyBase, DentalexaminationBase, LabBase, PhoneRecipie, RecipieMedicine
from models.bill import Bill
from models.globalvar import GlobalVar
from models.summarytext import SummaryText

from sqlalchemy.pool import SingletonThreadPool
import datetime


'''
    Initialize and configure database
    -dbname is string that contains information about db ie 'sqlite:///vetapp.db'
     Db can be connected to some external server in wanted
    -debug: is it is true more information about db is printed
'''
class SQLHandler(object):
    def __init__(self, Session, Base, dbname='sqlite:///:memory:', debug=False):
        self.dbname = dbname
        #self.debug = debug
        #self.engine = create_engine(dbname, echo=debug, poolclass=SingletonThreadPool)
        #self.engine = create_engine(dbname, echo=debug, 
                                    #poolclass=SingletonThreadPool,
                                    #isolation_level='SERIALIZABLE')  

        print(dbname)
        self.engine = create_engine(dbname, pool_size=20, max_overflow=0, echo=debug)

        self.Session = Session
        self.Base = Base
        self.session = Session()
        
    def usesLite(self):
        return 'sqlite' in self.dbname 
    
    def initialize(self):
        self.Session.configure(bind=self.engine)
        self.Base.metadata.bind = self.engine

        self.Base.metadata.create_all(self.engine)
        from sqlalchemy.exc import OperationalError
        try:
            print("Make objects")

            return True
        except OperationalError:
            print("error while creating objets")
            return False

    '''-------------OBJECT CREATORS---------------'''    
    def Owner(self,name, address, post_office_id, postnumber_id, email, phonenumber, other_info, flags=0):
        return Owner(name, address, post_office_id, postnumber_id, email, phonenumber, other_info, flags)
    
    def Appointment(self,owner_id, start_time, end_time, amanuensis):
        return Appointment(owner_id, start_time, end_time, amanuensis)
    
    def Picture(self,description, path):
        return Picture(description, path)
    
    def PostOffice(self, name):
        return PostOffice(name)
    
    def PostNumber(self, post_office_id, number):
        return PostNumber(post_office_id, number)
    
    def Visit(self, start_time, owner, vet, end_time=None):
        return Visit(start_time, owner, vet, end_time)
    
    def VisitAnimal(self, animal, anamnesis='', status='', diagnosis='', treatment=''):
        return VisitAnimal(animal, anamnesis, status, diagnosis, treatment)
    #--------VET RELATED-----#
    
    def Vet(self, name, address, post_office, postnumber, y_number, vet_number,bank_name, IBAN, SWIF, customertext, contactinfos):
        return Vet(name, address, post_office, postnumber, y_number, vet_number,bank_name, IBAN, SWIF, customertext, contactinfos)
    
    def CustomerText(self,language, text):
        return CustomerText(language, text)
    
    def ContactInfo(self,name, text):
        return ContactInfo(name, text)
        
    def Phonenumber(self,name, text):
        return Phonenumber(name, text)
    
    def Email(self,name,text):
        return Email(name,text)
    
    def Note(self, vet_id, title, text):
        return  Note(vet_id, title, text)
    
    def Todo(self, vet_id, name, deadline, text):
        return Todo(vet_id, name, deadline, text)
    
    #---------GLOBAL VARS-----#

    def GlobalVar(self, key, value):
        return GlobalVar(key,value)

    def getGlobalVar(self,key):
        print("DEBUG try to find global var with key: ", key)
        return float(self.session.query(GlobalVar).filter(GlobalVar.key==key).one().value)


    #----------ITEMS---------#
    def getItemCreators(self):
        return [Item, Vaccine, Medicine, Feed]
    
    
    def ALV(self, alv, alv_class):
        return ALV(alv, alv_class)
    
    def getALV(self, alv_class):
        #print("DEBUG: sqlHandler trys to get alv of class: ", alv_class)
        return self.session.query(ALV).filter(ALV.alv_class==alv_class).one().alv
    
    def setALV(self, alv_class, alv):
        alv_temp = self.session.query(ALV).filter(ALV.alv_class==alv_class).one()
        alv_temp.alv = alv
        self.session.commit()
    
    
    def Item(self, name, item_type, description, stock_price, price, barcode='', image_path=''):
        return Item(name, item_type, description, stock_price, price, barcode, image_path)
    
    def Vaccine(self,name, description, stock_price, price, barcode='', image_path='', duration=None):
        return Vaccine(name, description, stock_price, price, barcode, image_path, duration)
    
    def Medicine(self, name, description, stock_price, price, barcode='', image_path='', duration=None):
        return Medicine(name, description, stock_price, price, barcode, image_path, duration)
    
    def Feed(self, name, description, stock_price, price, barcode='', image_path=''):
        return Feed(self, name, description, stock_price, price, barcode, image_path)
    
    def ItemDescription(self, specie_id, text):
        return ItemDescription(specie_id, text)
    
    #------Operations-------#
    
    def Operation(self, price, description):
        return Operation(price, description)
    
    def Basic(self, price, description, base):
        return Basic(price, description, base)
    
    def Vaccination(self,price, description, base):
        return Vaccination(price, description, base)
    
    def Surgery(self,price, description, base):
        return Surgery(price, description, base)
        
    def Lab(self,price, description, base, path=''):
        return Lab(price, description, base, path)
    
    def Medication(self, price, description, base):
        return Medication(price, description, base)
    
    def Lameness(self, price, description, base):
        return Lameness(price, description, base)
    
    def Xray(self, price, description, base):
        return Xray(price, description, base)
    
    def Ultrasonic(self, price, description, base):
        return Ultrasonic(price, description, base)
    
    def Endoscopy(self,price, description, base):
        return Endoscopy(price, description, base)
    
    def Dentalexamination(self, price, description, base):
        return Dentalexamination(price, description, base)
    
    def isLabType(self, item):
        return type(item) is Lab
    
    #------Operationbases-------#
    
    def OperationBase(self, name, price, description):
        return OperationBase(name, price, description)
    
    def LabBase(self, name, price, description):
        return LabBase(name, price, description)
    
    def LamenessBase(self,name,  price, description):
        return LamenessBase(name, price, description)
    
    def XrayBase(self,name,  price, description):
        return XrayBase(name, price, description)
    
    def UltrasonicBase(self,name,  price, description):
        return UltrasonicBase(name, price, description)
    
    def EndoscopyBase(self,name, price, description):
        return EndoscopyBase(name, price, description)
    
    def DentalexaminationBase(self,name,  price, description):
        return DentalexaminationBase(name, price, description)
    
    def SurgeryBase(self, name, price, description, items=[]):
        return SurgeryBase(name, price, description, items)
    
    def MedicationBase(self,name,  price, description, item):
        return MedicationBase(name, price, description, item)
    
    def VaccinationBase(self, name, price, description, duration, need_resit, item):
        return VaccinationBase(name, price, description, duration, need_resit, item)

    
    #------ANIMAL RELATED-----------#
    def Animal(self, name, official_name, race_id, specie_id, sex_id, 
                 color_id, birthday, micro_num, rec_num, tattoo, 
                 insurance, passport, other_info):
        return Animal(name, official_name, race_id, specie_id, sex_id, 
                 color_id, birthday, micro_num, rec_num, tattoo, 
                 insurance, passport, other_info)
    
    def Specie(self,name, picture_path=''):
        return Specie(name, picture_path)
    
    def Color(self, name, specie_id):
        return Color(name, specie_id)
    
    def Sex(self, name):
        return Sex(name)
    
    def Race(self,name, specie_id):
        return Race(name, specie_id)
    
    def WeightControl(self, animal_id, weight):
        return WeightControl(animal_id, weight)
    
    def searchAnimalOwners(self, session, animal_id):
        return session.query(Owner).filter(Owner.animals.any(Animal.id==animal_id)).all()
    
    def RecipieMedicine(self, medicine, count=1):
        return RecipieMedicine(medicine, count)
    
    def PhoneRecipie(self, animal, recipiemedicines=[]):
        return PhoneRecipie(animal,recipiemedicines)
    
    
    '''--------------------------------------------'''
    
    def Bill(self,data):
        return Bill(data)
    
    def getBill(self, session, visit):
        item = session.query(Bill).filter(Bill.visit_id == visit.id).all()
        if(len(item)):
            return item[0]
        else:
            return None 
    
    '''-------------------------------------------'''

    def getAnimalVisits(self, session, animal):
        print("getAnimalVisits")
        if animal != None:
            visits = session.query(Visit).join(Visit.visitanimals).filter(VisitAnimal.animal_id == animal.id)

            print("visits: ", visits)

            return visits
        else:
            print("return empty")
            return []

    '''-------------------------------------------'''

    def searchOwner(self, session, question, start = 0, end = 20):
        return session.query(Owner).filter(Owner.name.like('%' + question+'%')).order_by(Owner.name)[start:end]
    
    def searchColor(self, session, specie_id):
        return session.query(Color).filter(Color.specie_id == specie_id).order_by(Color.name)
    
    def searchVet(self, session, vet_id=None):
        if vet_id == None:
            return session.query(Vet).order_by(Vet.name)[:]
        else:
            return session.query(Vet).filter(Vet.id == vet_id).one()

    def searchPostOffice(self, session, postnumber=None):
        if postnumber != None:
            try:
                return [session.query(PostOffice).filter(PostOffice.id==postnumber.post_office_id).one()]
            except NoResultFound:
                return None
        else:
            return session.query(PostOffice).order_by(PostOffice.name)
        
    def searchPostNumber(self, session, postOffice=None):
        if postOffice != None:
            return session.query(PostNumber).filter(PostNumber.post_office_id == postOffice.id).order_by(PostNumber.number)
        else:
            return session.query(PostNumber).order_by(PostNumber.number)
   
    
    #------------ANIMAL SEARCH--------#
    def searchAnimal(self, session, question, start = 0, end = 20):
        return session.query(Animal).filter(or_(Animal.name.like('%'+question+'%'), Animal.official_name.like('%'+question+'%'))).order_by(Animal.name)[start:end]
 
    def searchAnimalVisits(self, session, animal):
        return session.query(Visit).filter(Visit.visitanimals.any(VisitAnimal.animal_id == animal.id)).all()
    
    
    def searchAnimalOperations(self, session, animal):
        return session.query(Operation).filter(Operation.visitanimal_id.in_(
               session.query(VisitAnimal).filter(VisitAnimal.animal_id == animal.id).all()))
    
    
#   def searchAnimalMedications(self, session, animal):
#       return session.query(Medication).filter(Medication.visitanimal_id.in_(
#       session.query(VisitAnimal).filter(VisitAnimal.animal_id == animal.id).all())))
        
    def searchAnimalPictures(self, session, animal):
        pass
    
    def searchAnimalPhoneRecipies(self, session, animal):
        return session.query(PhoneRecipie).filter(PhoneRecipie.animal_id == animal.id).all()
        
    '''
        Search all species
    '''
    def searchSpecie(self, session):
        return session.query(Specie).order_by(Specie.name)
    
    '''
        Search all Sex related to specific specie
    '''
    def searchSex(self, session):
        return session.query(Sex).order_by(Sex.name)
    
    '''
        Search all Races related to specific specie
    '''
    def searchRace(self, session, specie_id):
        return session.query(Race).filter(Race.specie_id == specie_id).order_by(Race.name)
    
    
    def searchAnimalWeights(self, session, animal):
        if animal != None and not not animal.id:
            return session.query(WeightControl).filter(WeightControl.animal_id == animal.id).order_by(WeightControl.date)[:]
    
    def searchItem(self, session, question, start=0, end=50):
        return session.query(Item).filter(Item.name.like('%' + question + '%'))[start:end]
    
    def searchPhoneRecipies(self, session, start=0,end=50): 
        return session.query(PhoneRecipie).order_by(PhoneRecipie.made_time)[start:end]
    
    #summary functions
    
    def SummaryText(self, name, text):
        #print(self.session.query(SummaryText).filter(SummaryText.name==name).all())
        if not self.session.query(SummaryText).filter(SummaryText.name==name).all():
            return SummaryText(name, text)
        else:
            print("ERROR: SummaryText, set to None")
            return None
    
    def searchSummary(self, session, question):
        return session.query(SummaryText).filter(SummaryText.name.like('%'+ question +'%')).all()
    
    #---------------------------------#
    #
    #         Search functions
    #---------------------------------#
    
    def searchLineSearchVisit(self, session, question, params):
        return session.query(Visit).filter(and_((Visit.owner_id==params[0].id) if (params[0] != None) else None, 
                                                (Visit.visitanimals.any(VisitAnimal.animal_id == params[1].id)) if (params[1] != None) else None,
                                                (Visit.vet_id == params[2]) if (params[2] != None) else None,
                                                (Visit.start_time > (params[3] - datetime.timedelta(days=1))),
                                                (Visit.start_time < (params[4] + datetime.timedelta(days=1)))))
    
    def searchLineSearchAnimal(self, session, question, params):
        return session.query(Animal).filter(and_(Animal.name.like('%' + question + '%'),
                                                 Animal.specie_id == params[0].id if params[0] != None else None,
                                                 Animal.race_id == params[1].id if params[1] != None else None,
                                                 Animal.color_id == params[2].id if params[2] != None else None,
                                                 Animal.sex_id == params[3].id if params[3] != None else None,
                                                 Animal.birthday > (params[4] - datetime.timedelta(days=1)),
                                                 Animal.birthday < (params[5] + datetime.timedelta(days=1))))
    
    def searchLineSearchBill(self, session, question, params):
        return session.query(Bill).filter(and_(Bill.visit.vet_id == params[1].id,
                                               Bill.visit.start_time > (params[2] - datetime.timedelta(days=1)),
                                               Bill.visit.start_time < (params[3] + datetime.timedelta(days=1))))
    
    def searchRealItem(self, session, question):
        return session.query(Item).filter(Item.item_type=='Item').filter(Item.name.like('%'+ question +'%'))
    
    def searchMedicine(self, session, question):
        return session.query(Medicine).filter(Medicine.name.like('%'+ question +'%'))
    
    def searchVaccine(self, session, question):
        return session.query(Vaccine).filter(Vaccine.name.like('%'+ question +'%'))
    
    def searchFeed(self, session, question):
        return session.query(Feed).filter(Feed.name.like('%'+ question +'%'))
    
    def searchOperationBase(self, session, question):
        return session.query(OperationBase).filter(OperationBase.name.like('%'+question+'%'))
    
    #---------------------------------#
    #
    #
    #---------------------------------#
    
    def addItem(self, session, item):
        if item != None:
            print("DEBUG: SQLHandler->addItem(), item == " + str(item))
            session.add(item)
            session.commit()
        else:
            print("ERROR: SQLHandler->addItem(). Item is None: " + str(item))
    
    def addItems(self, session, itemlist):
        if itemlist != None and len(itemlist) > 0:
            print("DEBUG: SQLHandler->addItems(), itemlist len == " + str(len(itemlist)))
            session.add_all(itemlist)
            session.commit()
        else:
            print("ERROR: SQLHandler->addItems(). List is none or empty: " + str(itemlist))
    
    def removeItem(self, session, item):
        session.delete(item)
        session.commit()
    
    '''
        return session
    '''
    def newSession(self):
        session = self.Session()
        print('SqlHandler->newSession() session is ',session)
        return session
    
    '''
        Just commits session
    '''
    def commitSession(self, session):
        session.commit()
        
    '''
        commits and closes session
        After this session is invalid
    '''
    def closeSession(self, session):
        session.close()
        
        
    def makeCopy(self, session, item):
        return session.query(type(item)).filter(type(item).id==item.id).one()
    
    