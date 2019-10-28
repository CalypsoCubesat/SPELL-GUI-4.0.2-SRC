###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.user 
FILE
    user.py
DESCRIPTION
    hifly user management interface
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    25/09/2007
"""

###############################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.log import *
import spell.lib.adapter.user
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.config.reader import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.connection import CONN
from internals.exception import HiflyException
from internals.usr.manager import UserManager
from constants import *

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['USER']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.user.UserInterface

###############################################################################
class UserInterface(superClass):
    
    """
    DESCRIPTION:
        User management library interface. This class is in charge of
        managing the underlying system users, if any.
    """
    
    __domain = None
    __userManager = UserManager()
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
    
    #==========================================================================
    def setup(self, ctxName):
        LOG("Initializing hifly USER interface")
        superClass.setup(self, ctxName)
        self.__userManager.setup()
        self.__domain = Config.instance().getContextConfig(ctxName).getSC()
        LOG("Using domain " + str(self.__domain))

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        self.__userManager.cleanup()
        
    #==========================================================================
    def login(self, username, password, config = {} ):
        if not config.has_key(Role):
            raise DriverException("Expected config parameter: role")
        role = config.get(Role)

        # Get the host name
        if not config.has_key(Host):
            raise DriverException("Expected config parameter: host")
        hostname = config.get(Host)
        
        # Get the domain
        if config.has_key(Domain):
            domain = config.get(Domain)
        else:
            domain = self.__domain

        # Get the workspace        
        if not config.has_key(WS):
            ws = 0
        ws = config.get(WS)
        
        self.__userManager.login( username, password, role, domain, hostname, ws )
        return True
        
    #==========================================================================
    def logout(self, username, config = {}):
        # Get the host name
        if not config.has_key(Host):
            raise DriverException("Expected config parameter: host")
        hostname = config.get(Host)
        
        # Get the domain
        if config.has_key(Domain):
            domain = config.get(Domain)
        else:
            domain = self.__domain
            
        self.__userManager.logout( domain, hostname )
        return True

    #==========================================================================
    def isLoggedIn(self, username, config = {}):
        raise NotImplemented

###############################################################################
# Interface handle
USER = UserInterface()
