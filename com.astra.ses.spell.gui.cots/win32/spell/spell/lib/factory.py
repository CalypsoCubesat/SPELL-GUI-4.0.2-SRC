################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.driver.factory
FILE
    factory.py
    
DESCRIPTION
    Factory in charge of building the appropiate instance of each lib.adapter
    interfaces
    
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
import spell.lib.empty.config
import spell.lib.empty.tm
import spell.lib.empty.tc
import spell.lib.empty.ev
import spell.lib.empty.task
import spell.lib.empty.resources
import spell.lib.empty.user
from spell.lib.adapter.dbmgr import *

from spell.lib.adapter.constants.core import *
from spell.utils.log import *

#*******************************************************************************
# Local Imports
#*******************************************************************************
 
#*******************************************************************************
# System Imports
#*******************************************************************************
import sys
 
#*******************************************************************************
# Exceptions 
#*******************************************************************************
class FactoryError(BaseException): pass
 
#*******************************************************************************
# Module globals
#*******************************************************************************

__all__ = ['Factory', 'FactoryError' ] 

KNOWN_INTERFACES = [ 'TM', 'TC', 'EV', 'RSC', 'TASK', 'USER', 'CONFIG', 'DBMGR' ]

IFC_PACKAGES = { 'TM':'tm', 'TC':'tc', 'EV':'ev', 
                 'RSC':'resources', 'TASK':'task', 
                 'USER':'user', 'CONFIG':'config' }

__instance__ = None

###############################################################################
class FactoryClass(object):
    
    """
    DESCRIPTION:
        This class is in charge of the instantiation of all proper driver
        classes which support the different adapter interfaces. 
    """
    __driver = None

    #==========================================================================
    def __init__(self):
        self.__driver = None
        
    #==========================================================================
    @staticmethod
    def instance():
        global __instance__
        if __instance__ is None:
            __instance__ = FactoryClass()
        return __instance__
        
    #==========================================================================
    def setup(self, driver):
        """
        DESCRIPTION:
            Setup the factory for using the given driver
            
        ARGUMENTS:
            driver      Driver identifier
            
        RETURNS:
            Nothing

        RAISES:
            Nothing
        """
        LOG("Configure factory for using driver: " + driver)
        self.__driver = driver
        if not driver in KNOWN_DRIVERS:
            raise FactoryError("Unknown driver: " + repr(driver))

    #==========================================================================
    def createGenInterface(self, ifcName):
        """
        DESCRIPTION:
            Create the configuration interface for the configured driver
            
        ARGUMENTS:
            
        RETURNS:
            The requested object

        RAISES:
            Nothing
        """
        LOG("Create " + ifcName + " interface")
        
        if not ifcName in KNOWN_INTERFACES:
            raise FactoryError("Unknown interface: " + repr(ifcName))
        
        try:
            # Import the required package
            LOG("Resolving %s" % ifcName)

            # Obtain the interface instance
            interface = eval(ifcName)
        except:
            LOG("Interface " + repr(ifcName) + 
                " could not be resolved.", severity = LOG_ERROR )
            return self.createEmptyInterface(ifcName)
        
        return interface            

    #==========================================================================
    def createInterface(self, ifcName):
        """
        DESCRIPTION:
            Create the configuration interface for the configured driver
            
        ARGUMENTS:
            
        RETURNS:
            The requested object

        RAISES:
            Nothing
        """
        LOG("Create " + ifcName + " interface")
        
        if not ifcName in KNOWN_INTERFACES:
            raise FactoryError("Unknown interface: " + repr(ifcName))
        
        # Build the full package name
        packageRoot = DRIVER_PACKAGES[self.__driver]
        packageRoot = packageRoot + "." + IFC_PACKAGES.get(ifcName)
        
        try:
            # Import the required package
            LOG("Root " + packageRoot + ' with ' + ifcName)
            importedPackage = __import__(packageRoot, globals(),  locals(), [ifcName], -1)

            # Obtain the interface instance
            interface = importedPackage.__dict__.get(ifcName)
            
            if interface is None:
                raise FactoryError("Unable to create interface " + repr(ifcName))

        except ImportError,err:
            LOG("Interface " + repr(ifcName) + 
                " is not available on driver: " + repr(err), severity = LOG_ERROR )
            return self.createEmptyInterface(ifcName)
        
        return interface            


    #==========================================================================
    def createEmptyInterface(self, ifcName):
        """
        DESCRIPTION:
            Create the empty interface 
            
        ARGUMENTS:
            
        RETURNS:
            The requested object

        RAISES:
            Nothing
        """
        LOG("Create " + ifcName + " EMPTY interface")
        if ifcName == 'CONFIG':
            return spell.lib.empty.config.ConfigInterface()
        elif ifcName == 'TM':
            return spell.lib.empty.tm.TmInterface()
        elif ifcName == 'TC':
            return spell.lib.empty.tc.TcInterface()
        elif ifcName == 'EV':
            return spell.lib.empty.ev.EvInterface()
        elif ifcName == 'TASK':
            return spell.lib.empty.task.TaskInterface()
        elif ifcName == 'USER':
            return spell.lib.empty.user.UserInterface()
        elif ifcName == 'RSC':
            return spell.lib.empty.resources.ResourceInterface()
        else:
            raise FactoryError("Cannot create empty interface '" + ifcName + "'")

###############################################################################
Factory = FactoryClass
