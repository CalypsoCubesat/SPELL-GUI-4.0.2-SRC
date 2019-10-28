################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.config 
FILE
    config.py
DESCRIPTION
    hifly driver setup 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
import spell.lib.adapter.config 
from spell.utils.log import *
from spell.config.reader import Config
from spell.config.constants import COMMON
from spell.lib.exception import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.exception import HiflyException

#*******************************************************************************
# System imports
#*******************************************************************************
import os,sys

#*******************************************************************************
# Import Definition
#*******************************************************************************

__all__ = ['CONFIG']


#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.config.ConfigInterface
INTERFACE_DEFAULTS = {}

################################################################################
class ConfigInterface( superClass ):

    __chelper = None

    #==========================================================================    
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
        
    #==========================================================================    
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup hifly CFG interface")
        
        # Obtain the configuration information for this context
        # The context
        ctx = Config.instance().getContextConfig(contextName)
        # The driver name
        driverName = ctx.getDriver()
        # The family
        family = ctx.getFamily()
        LOG("Using family: " + repr(family))
        # The spacecraft
        domain = ctx.getSC()
        LOG("Using domain: " + repr(domain))

        # Obtain the driver context-specific parameters
        nameid  = ctx.getDriverConfig("NameID")
        nameserver = ctx.getDriverConfig("NameServer")
        nameport = ctx.getDriverConfig("NamePort")

        # Obtain the general driver parameters        
        driverDetails = Config.instance().getDriverConfig(driverName)
        keyPath = Config.instance().getRuntimeDir()+\
                   os.sep + driverDetails['KeyPath']
        key = driverDetails["ExifKey"]
        user = driverDetails["ExifUser"]
        
        if nameid is None:
            raise DriverException("Unable to load driver", "No value: name service id")
        if nameserver is None:
            raise DriverException("Unable to load driver", "No value: name server")
        if nameport is None:
            raise DriverException("Unable to load driver", "No value: name port")
        if family is None:
            raise DriverException("Unable to load driver", "No value: family")
        if domain is None:
            raise DriverException("Unable to load driver", "No value: domain")
        if key is None:
            raise DriverException("Unable to load driver", "No value: key path")
        if user is None:
            raise DriverException("Unable to load driver", "No value: user")
        
        # Obtain the key file
        keypath = keyPath + os.sep + key
        if not os.path.exists(keypath): 
            raise DriverException("Unable to load driver", "Could not open key file " + repr(keypath) )
            
        try:
            from internals.connection import CONN
            # Setup the CORBA/AUTH layer
            CONN.setup( nameid, nameserver, nameport, domain, family )
            CONN.authenticate( keypath, user )
        except HiflyException, e:
            raise DriverException("Could not connect to hifly SCS: " + e.message, e.reason )
        except BaseException, ce:
            raise DriverException("Could not connect to hifly SCS: " + repr(ce) )
        
    #==========================================================================    
    def cleanup(self, shutdown = False):
        if (shutdown == True):
            LOG("Shutting down ORB")
            from internals.connection import CONN
            CONN.cleanup()
        
################################################################################
# Instance 
CONFIG = ConfigInterface()
