#!/usr/bin/python

#databasetype = 'sqlite:///'

'postgresql://name:pass@ip/dbname'

from os.path import expanduser, exists, dirname
from os import makedirs

_databasename = 'data.db'
_username = 'VetApp'
_pass = 'MDdlMjNiZWVjZmVhMjI5Y2JkMmIzNWFh' #change this to unique + TODO: crypt password
_ip = 'localhost'
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


