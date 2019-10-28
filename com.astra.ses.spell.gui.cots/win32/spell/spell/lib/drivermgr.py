################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.driver.driver
FILE
    driver.py
    
DESCRIPTION
    Driver manager class implementation
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV) & Fabien Bouleau (SES Engineering)
"""

################################################################################

#*******************************************************************************
# SPELL Imports
#*******************************************************************************
from spell.config.reader import *
from spell.utils.log import *
from spell.lib.exception import DriverException

#*******************************************************************************
# Local Imports
#*******************************************************************************
from registry import *
from factory import *
 
#*******************************************************************************
# System Imports
#*******************************************************************************
import traceback,sys
 
#*******************************************************************************
# Exceptions 
#*******************************************************************************
 
#*******************************************************************************
# Module globals
#*******************************************************************************

GENERIC_INTERFACES = [ 'DBMGR' ]
INTERNAL_INTERFACES = [ 'CONFIG' ]
HOME_TAG = "$SPELL_HOME$"

__all__ = [ 'DriverManager' ]

__instance__ = None

################################################################################
class DriverManagerClass(object):
    
    driver = None
    contextName = None
    context = None
    interfaces = []
    libraries = []
    loaded = None
    
    #===========================================================================
    def __init__(self):
        self.driver = None
        self.interfaces = []
        self.libraries = []
        self.loaded = None
    
    #==========================================================================
    @staticmethod
    def instance():
        global __instance__
        if __instance__ is None:
            __instance__ = DriverManagerClass()
        return __instance__
    
    #===========================================================================
    def setup(self, contextName):

        # Get the context information
        self.contextName = contextName
        self.context = Config.instance().getContextConfig(contextName)
        # Obtain the corresponding driver 
        self.driver = self.context.getDriver()
        
        REGISTRY['CTX'] = self.context

        if self.loaded is not None: 
            # Do not load the same driver twice
            if self.loaded == self.driver: return True 
            success = self.cleanup()
            if not success:
                raise DriverException("Unable to load driver","Could not cleanup previously loaded driver " + str(self.loaded))

        driverInfo = Config.instance().getDriverConfig(self.driver)
        self.interfaces = []
        self.libraries = []
        
        for iif in INTERNAL_INTERFACES:
            self.interfaces.append(iif)
        driverInterfaces = driverInfo.getInterfaces()
        
        if len(driverInterfaces)>0:
            driverInterfaces = driverInterfaces.split(",")
            for iif in driverInterfaces:
                self.interfaces.append(iif)

        libraries = driverInfo.getLibraries()
        if len(libraries)>0:
            self.libraries = libraries.split(",")
        
        LOG("Using driver:" + self.driver)
        LOG("Using interfaces: " + repr(self.interfaces))
        LOG("Using libraries: " + repr(self.libraries))

        try:         
            # Configure the factory
            Factory.instance().setup(self.driver)
            # Preload libraries
            for lib in self.libraries:
                lib = lib.strip(" \n\r")
                lib = Config.instance().resolvePath(lib)
                LOG("Appending to path: " + lib)
                sys.path.append(lib)
            # Create driver interfaces
            self.createInterfaces()
            # Initialize driver interfaces
            self.initInterfaces()
            # Set the driver as loaded
            self.loaded = self.driver
        except DriverException,e:
            traceback.print_exc(file = sys.stderr)
            raise e
        except BaseException,e:
            traceback.print_exc(file = sys.stderr)
            raise DriverException("Unable to load driver",repr(e))

    #==========================================================================
    def cleanup(self, force = False, shutdown = False ):
        list = []
        for ifc in self.interfaces:
            list.append(ifc)
        list.reverse()
        # Forcing will try to cleanup everything ignoring errors
        if force:
            for ifc in list:
                # Attempt to clean all interfaces,
                # whatever it happens
                if REGISTRY.exists(ifc):
                    try:
                        LOG("Cleaning up driver interface " + ifc)
                        if ifc == 'CONFIG':
                            REGISTRY[ifc].cleanup(shutdown)
                        else:
                            REGISTRY[ifc].cleanup()
                    except:pass
        else:
            for ifc in list:
                if REGISTRY.exists(ifc):
                    LOG("Cleaning up driver interface " + ifc)
                    if ifc == 'CONFIG':
                        REGISTRY[ifc].cleanup(shutdown)
                    else:
                        REGISTRY[ifc].cleanup()
        self.loaded = None
        return True
    
    #==========================================================================
    def createInterfaces(self):
        LOG("Creating interfaces")
        for ifc in self.interfaces:
            REGISTRY[ifc] = Factory.instance().createInterface(ifc)
        LOG("Creating generic interfaces")
        for ifc in GENERIC_INTERFACES:
            REGISTRY[ifc] = Factory.instance().createGenInterface(ifc)
            self.interfaces.append(ifc)

    #==========================================================================
    def initInterfaces(self):
        LOG("Initializing interfaces")
        for ifc in self.interfaces:
            LOG("Initializing " + ifc)
            REGISTRY[ifc].setup(self.contextName)

################################################################################
DriverManager = DriverManagerClass
