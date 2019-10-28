import os,sys
from spell.lib.exception import DriverException
from spell.utils.log import *
from spell.config.reader import *
#from spell.lang.constants import *
#from spell.lang.modifiers import *
from spell.config.constants import COMMON
from spell.utils.vimport import ImportValue,ExportValue

DB_TYPE_FILE   = 'file'
DB_TYPE_MMD    = 'mmd'
DB_TYPE_USR    = 'usr'
DB_TYPE_SCDB   = 'scdb'
DB_TYPE_GDB    = 'gdb'
DB_TYPE_SQLITE = 'sqlite'
DB_TYPE_MYSQL  = 'sql'
DB_TYPE_ASRUN  = 'ar'
DB_TYPE_SVN    = 'svn'

################################################################################
class Database(object):
    
    #===========================================================================
    def __init__(self):
        self._vkeys = []
        self._types = {}
        self._properties = {}

        if type(self) is  Database:
            raise NotImplemented()
    
    #===========================================================================
    def __getitem__(self, key):
        raise NotImplemented()

    #===========================================================================
    def __setitem__(self, key, value):
        raise NotImplemented()

    #===========================================================================
    def create(self):
        raise NotImplemented()
    
    #===========================================================================
    def load(self):
        raise NotImplemented()
    
    #===========================================================================
    def reload(self):
        raise NotImplemented()

    #===========================================================================
    def id(self):
        raise NotImplemented()

    #===========================================================================
    def commit(self):
        raise NotImplemented()

    #===========================================================================
    def __getitem__(self, key):
        if not self._properties.has_key(key):
            raise DriverException("No such key: " + repr(key))
        return self._properties.get(key)

    #===========================================================================
    def __setitem__(self, key, value):
        if not key in self._properties.keys():
            self._vkeys.append(key)
        self._properties[key] = value

    #===========================================================================
    def set(self, key, value, format = None):
        if not key in self._properties.keys():
            self._vkeys.append(key)
        self._properties[key] = value
        if format:
            self._types[key] = format

################################################################################
def int2bin(n, count=24):
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])
