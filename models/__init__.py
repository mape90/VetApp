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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#make session Class for use of other classes
Session = sessionmaker()

#make Base
Base = declarative_base()

from configfile import isDBDebugOn, genDBString

from models.sqlhandler import SQLHandler
SqlHandler = SQLHandler(Session=Session, Base=Base, dbname=genDBString(), debug=isDBDebugOn())
#SqlHandler = SQLHandler(Session=Session, Base=Base, dbname=genDBString('postgresql'), debug=isDBDebugOn())