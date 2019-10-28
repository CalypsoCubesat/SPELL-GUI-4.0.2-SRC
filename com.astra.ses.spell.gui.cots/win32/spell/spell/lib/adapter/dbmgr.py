###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.config 
FILE
    config.py
    
DESCRIPTION
    Setup environment for correct core driver instantiation
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    01/10/2007
"""

###############################################################################

#*******************************************************************************
# SPELL Imports
#*******************************************************************************
from spell.utils.log import *
from spell.lib.exception import DriverException
from spell.lib.adapter.config import Configurable
from spell.lib.adapter.constants.core import *
from spell.config.reader import *
from spell.lib.adapter.database import *
from spell.lib.adapter.dbfile import *
from spell.lib.adapter.dbasrun import *
from spell.lib.adapter.dbsvn import *

#*******************************************************************************
# Local Imports
#*******************************************************************************

#*******************************************************************************
# System Imports
#*******************************************************************************
import os

#*******************************************************************************
# Import Definition
#*******************************************************************************
__all__ = [ 'DBMGR' ]

#*******************************************************************************
# Module Globals
#*******************************************************************************

################################################################################
class DatabaseManagerClass(Configurable):
    
    __ctxName = None
    __databases = {}

    #===========================================================================    
    def __init__(self):
        Configurable.__init__(self)
        self.__databases = {}
        self.__ctxName = None
        LOG("Created")

    #===========================================================================    
    def setup(self, ctxName):
        self.__ctxName = ctxName
        LOG("Loading spacecraft database")
        self.loadDatabase('SCDB')
        LOG("Loading ground database")
        self.loadDatabase('GDB')

    #===========================================================================    
    def cleanup(self):
        self.__databases.clear()
        
    #===========================================================================    
    def __getitem__(self, key):
        if not self.__databases.has_key(key):
            raise DriverException("No such database: " + repr(key))
        return self.__databases.get(key)
    
    #===========================================================================    
    def fromURItoPath(self, dbName):
        LOG("Create database " + repr(dbName))
        idx = dbName.find('://')
        if idx != -1:
            # User database
            dbType = dbName[0:idx]
            dbName = dbName[idx+3:]
            dbPath = Config.instance().getLocationPath(dbType.upper()) + os.sep + dbName 
            LOG("User path: " + repr(dbPath))
        else:
            # Preconfigured database
            location,filename = Config.instance().getContextConfig(self.__ctxName).getDatabaseInfo(dbName)
            if location is None:
                raise DriverException("Unknown database location")
            if filename is None:
                raise DriverException("No database file")
            dbType = location
            lpath = Config.instance().getLocationPath(location)
            dbPath = lpath + os.sep + filename
            
        # Translate path tags
        idx = dbPath.find("$SATNAME$")
        if idx != -1:
            dbPath = dbPath[0:idx] + Config.instance().getContextConfig(self.__ctxName).getSatName() + dbPath[idx+9:]
        idx = dbPath.find("$SATID$")
        if idx != -1:
            dbPath = dbPath[0:idx] + Config.instance().getContextConfig(self.__ctxName).getSC() + dbPath[idx+7:]
            
        LOG("Database path: " + repr(dbPath))
        return dbType, dbPath
        
    #===========================================================================    
    def getDatabaseInstance(self, dbName):
        dbType, dbPath = self.fromURItoPath(dbName)
        
        dbType = dbType.lower()
        LOG("Database type: " + repr(dbType))
        db = None
        
        if dbType == DB_TYPE_FILE:
            db = DatabaseFile(dbName, dbPath)
        elif dbType == DB_TYPE_MMD:
            ext = Config.instance().getLocationExt(dbType.upper())
            LOG("Using default extension for type " + repr(dbType) + ": " + ext)
            db = DatabaseFile(dbName, dbPath, ext)
        elif dbType == DB_TYPE_USR:
            ext = Config.instance().getLocationExt(dbType.upper())
            LOG("Using default extension for type " + repr(dbType) + ": " + ext)
            db = DatabaseFile(dbName, dbPath, ext)
        elif dbType == DB_TYPE_SCDB:
            ext = Config.instance().getLocationExt(dbType.upper())
            LOG("Using default extension for type " + repr(dbType) + ": " + ext)
            db = DatabaseFile(dbName, dbPath, ext)
        elif dbType == DB_TYPE_GDB:
            ext = Config.instance().getLocationExt(dbType.upper())
            LOG("Using default extension for type " + repr(dbType) + ": " + ext)
            db = DatabaseFile(dbName, dbPath, ext)
        elif dbType == DB_TYPE_SQLITE:
            db = DatabaseSQLite(dbName, dbPath)
        elif dbType == DB_TYPE_ASRUN:
            ext = Config.instance().getLocationExt(dbType.upper())
            LOG("Using default extension for type " + repr(dbType) + ": " + ext)
            db = DatabaseAsRun(dbName, dbPath, ext)
        elif dbType == DB_TYPE_SVN:
            ext = Config.instance().getLocationExt(dbType.upper())
            LOG("Using default extension for type " + repr(dbType) + ": " + ext)
            db = DatabaseSubversion(dbName, dbPath, ext)
        else:
            raise DriverException("Unknown database type: " + repr(dbType)) 
        
        self.__databases[dbName] = db 
        return db

    #===========================================================================    
    def createDatabase(self, dbName):
        if not self.__databases.has_key(dbName):
            db = self.getDatabaseInstance(dbName)
        
        db = self.__databases.get(dbName) 
        db.create()
        
        return db
        
    #===========================================================================    
    def loadDatabase(self, dbName):
        if not self.__databases.has_key(dbName):
            db = self.getDatabaseInstance(dbName)
        
        db = self.__databases.get(dbName) 
        db.load()
        
        return db

DBMGR = DatabaseManagerClass()
