#!/usr/bin/python

#databasetype = 'sqlite:///'

'postgresql://name:pass@ip/dbname'

from os.path import expanduser, exists, dirname
from os import makedirs
from PyQt4.QtGui import QMessageBox


def popErrorMessage(text):
    msgBox = QMessageBox();
    msgBox.setText(text);
    msgBox.exec();

#'postgres:salakala://localhost:5433/vetapp'

_databasename = 'vetapp'
_username = 'vetapp_user'
_pass = 'salakala' #change this to unique + TODO: crypt password
_ip = '192.168.1.68'
_port = '5432'
_bill_directory = '~/bill/'

_debug_val = True

def logDEBUG(_from, _msg):
    if _debug_val :
        print("DEBUG: from: " + str(_from) + ': msg:' + str(_msg))
    
def logERROR(_from, _msg):
    print("ERROR: from: " + str(_from) + ': msd:' + str(_msg))

def isDBDebugOn():
    return False

def getDBName():
    return _databasename;

def getBillPath():
    path = expanduser(_bill_directory)
    
    if not exists(dirname(path)):
        makedirs(dirname(path))
    return path

def genDBString(db_type = 'sqlite'):
    if db_type is 'sqlite':
        return 'sqlite:///' + _databasename
    elif db_type is 'postgresql':
        return 'postgresql://' + _username + ':' + _pass + '@' + _ip +':' + _port + '/' + _databasename
    else:
        print("ERROR: database type is incorrect use sqlite or postgresql")
        return None


