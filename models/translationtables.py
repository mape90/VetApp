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
import datetime

g_operationbase_translation_dict = {"OperationBase":"Operaatio", "VaccinationBase":'Rokotus',
                                    "SurgeryBase":'Leikkaus', "MedicationBase":"Lääkitys",
                                    "LabBase":"Laboratoriotutkimus", "LamenessBase":'Ontumatutkimus',
                                    "XrayBase":'Röntkentutkimus', "UltrasonicBase":'Ultraäänitutkimus',
                                    "EndoscopyBase": "Endoskooppitutkimus" ,"DentalexaminationBase":"Hammashoito"}

#these items are in two dict so you need to change only this dict to cahange names in both
g_base_and_item_dict = {"Medicine":"Lääke","Vaccine":"Rokote"}

g_item_translation_dict = {"Item":"Tuote","Medicine":g_base_and_item_dict["Medicine"],
                           "Vaccine":g_base_and_item_dict["Vaccine"],"Feed":"Rehu"}

g_item_name_dict = {"Item":"Tuote","Medicine":g_base_and_item_dict["Medicine"],
                    "Vaccine":g_base_and_item_dict["Vaccine"],"Feed":"Rehu", "Drug":"Huumausaine"}

#translate operation name to item name both in user language (i.e, finnish)
g_item_to_base_dict = {g_operationbase_translation_dict['VaccinationBase'] : g_base_and_item_dict["Vaccine"],
g_operationbase_translation_dict['MedicationBase'] : g_base_and_item_dict["Medicine"]}

g_unique_tabs = ["MainMenuTab","VetTab","SearchTab", "WarehouseTab", "AppointmentTab","ItemCreatorTab", "OperationBaseCreatorTab"]

g_tab_name_dict = {'VisitTab':'Käynti','AnimalTab':'Eläin', 'OwnerTab':'Omistaja',
                   'SearchTab':'Etsi', 'MainMenuTab':'Päävalikko', 'WarehouseTab':'Varasto',
                   'AppointmentTab':'Ajanvaraus', 'VetTab':'Eläinlääkäri',
                   'BillTab':'Lasku', 'ItemCreatorTab':'Tuotehallinta',
                   "OperationBaseCreatorTab":"Operaatiohallinta","SummaryTab":"Yhteenveto"}


g_visit_end_time_start = "1.1.2000"

g_item_alv_dict = {"Item":1,"Medicine":2,'Drug':2, "Vaccine":2,"Feed":3}

g_save_error_message = "Ei voida tallentaa, tietoja puuttuu!"

g_treewidget_button_texts = {'add':'Lisää', 'remove':'Poista', 'open':'Avaa','check':'Tehty'}

g_error_msg_dict = {'database_init': 'Tietokannan alustaminen epäonnistui. Ota yhteyttä ylläpitoon.'}

g_payment_time_dict = dict([('Heti',datetime.timedelta(days=0)),('1 vk',datetime.timedelta(days=7)),('2 vk',datetime.timedelta(days=14))])

g_preset_durations = [('kuukausi',30), ('1/2 vuosi',180), ('1 vuosi',365),
                       ('2 vuotta',730), ('3 vuotta',1095), ('5 vuotta',1825)]





