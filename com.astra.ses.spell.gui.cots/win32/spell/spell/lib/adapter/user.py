################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.user
FILE
    user.py
    
DESCRIPTION
    User management interface
    
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
from spell.lib.exception import *
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.config.reader import *

#*******************************************************************************
# Local Imports
#*******************************************************************************
from config import Configurable
from interface import Interface

#*******************************************************************************
# System Imports
#*******************************************************************************

###############################################################################
# Module import definition

__all__ = ['UserInterface']

INTERFACE_DEFAULTS = { OnFailure:ABORT | SKIP | REPEAT }

###############################################################################
class UserInterface(Configurable, Interface):
    
    """
    DESCRIPTION:
        User management library interface. This class is in charge of
        managing the underlying system users, if any.
    """
    __ctxName = None
    
    #==========================================================================
    def __init__(self):
        Interface.__init__(self, "USR")
        Configurable.__init__(self)
        LOG("Created")
    
    #===========================================================================
    def refreshConfig(self):
        ctxConfig = Config.instance().getContextConfig( self.__ctxName )
        languageDefaults = ctxConfig.getInterfaceConfig(self.getInterfaceName())
        if languageDefaults:
            INTERFACE_DEFAULTS.update(languageDefaults)
        self.setConfig( INTERFACE_DEFAULTS )
        LOG("Configuration loaded", level = LOG_CNFG )
    
    #==========================================================================
    def setup(self, contextName):
        LOG("Setup USER adapter interface")
        self.__ctxName = contextName
        self.refreshConfig()

    #==========================================================================
    def cleanup(self):
        LOG("Cleanup USER adapter interface")
        
    #==========================================================================
    def login(self, *args, **kargs):
        if len(args)<2:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        user     = args[0]
        password = args[1]
         
        return self._login( user, password, useConfig )
        
    #==========================================================================
    def logout(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        user = args[0]
         
        return self._logout( user, useConfig )

    #==========================================================================
    def isLoggedIn(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        user = args[0]
         
        return self._isLoggedIn( user, useConfig )
                    
    #==========================================================================
    def _login(self, username, password, config = {} ):
        raise NotImplemented
        
    #==========================================================================
    def _logout(self, username, config = {}):
        raise NotImplemented

    #==========================================================================
    def _isLoggedIn(self, username, config = {}):
        raise NotImplemented
