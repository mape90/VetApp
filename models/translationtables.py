#!/usr/bin/python
# -*- coding: utf-8
'''
Created on Apr 16, 2013

@author: mp
'''
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

g_operationbase_translation_dict = {"OperationBase":"Operaatio", "VaccinationBase":'Rokotus', "SurgeryBase":'Leikkaus', "MedicationBase":"Lääkitys", "LabBase":"Laboratoriotutkimus", "LamenessBase":'Ontumatutkimus', "XrayBase":'Röntkentutkimus', "UltrasonicBase":'Ultraäänitutkimus', "EndoscopyBase": "Endoskooppitutkimus" ,"DentalexaminationBase":"Hammashoito"}


#ATTENTION these two list have to have same names Rokote == Rokote, Lääke==Lääke
g_item_translation_dict = {"Item":"Tuote","Medicine":"Lääke","Vaccine":"Rokote","Feed":"Rehu"}

#this is used to select correct item in itemcreatordialog
g_operationbase_to_item_translation_dict = {"VaccinationBase":"Rokote","MedicationBase":"Lääke"}

g_visit_end_time_start = "1.1.2000"

g_item_alv_dict = {"Item":1,"Medicine":2,"Vaccine":2,"Feed":3}

g_item_name_dict = {"Item":"Tuote","Medicine":"Lääkeaine","Vaccine":"Rokote","Feed":"Rehu"}

g_unique_tabs = ["MainMenuTab","VetTab","SearchTab", "WarehouseTab", "AppointmentTab"]

g_tab_name_dict = {'VisitTab':'Käynti','AnimalTab':'Eläin', 'OwnerTab':'Omistaja', 'SearchTab':'Etsi', 'MainMenuTab':'Päävalikko', 'WarehouseTab':'Varasto',  'AppointmentTab':'Ajanvaraus', 'VetTab':'Eläinlääkäri',}











