###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.usr.manager 
FILE
    manager.py
DESCRIPTION

    hifly internal user management interface
    
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
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.config.reader import CFG
from spell.lib.hifly.utils.usr_utils import *
from spell.lib.hifly.internals.connection import CONN
from spell.lib.hifly.internals.exception import HiflyException
from spell.lib.hifly.constants import *
from  spell.lib.hifly.modifiers import *
from spell.lib.hifly.interface._GlobalIDL import USERcorbaManager

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['UserManager']

#*******************************************************************************
# Module globals
#*******************************************************************************

###############################################################################
class UserManager( object ):

    """
    Used to manage hifly users
    """
    
    __userManager = None    
    
    #==========================================================================
    def __init__(self):
        LOG("Created")
        self.__userManager = None

    #==========================================================================
    def setup(self, server = None, port = None, family = PRIME):
        """
        Setup the interface. Obtain the user manager handle.
        """
                
        # We need a dedicated CORBA wrapper for accessing GEN satellite
        if not CONN.isReady():
            if not server or not port:
                raise DriverException("Cannot setup connection")
            # If there is no connection already, setup it
            LOG("Adding name service TASKNS")
            CONN.setup("TASKNS", server, port, "GEN", family )
                
        serviceName = "USERmanager"
        serviceType = ""
        serviceClass = USERcorbaManager
        
        # Obtain the event server manager
        LOG("Obtaining user manager" )
        self.__userManager = CONN.getObjectByContextType( "GEN", family, serviceName, serviceType, serviceClass )

    #==========================================================================
    def cleanup(self):
        LOG("Releasing user manager" )
        CONN.releaseObject(self.__userManager)

    #==========================================================================
    def login(self, uname, pwd, role, domain, host, workspace = None ):
        
        if self.__userManager is None:
            raise HiflyException("User manager not available")
        
        try:
            if workspace is None:
                ws = 0
            else:
                ws = workspace
            LOG("Loggin on " + host + " as user '" + uname + 
                     "', domain " + domain + ", role " + role +
                     ", workspace " + repr(ws) )
            self.__userManager.logOnWorkSpace( uname, pwd, domain, host, role, ws )
        except spell.lib.hifly.interface._GlobalIDL.USERcorbaManager.USERexceptionReject,e:
            LOG("Failed login")
            LOG("   Reason: " + repr(e.reason))
            LOG("   Code  : " + userCodeStr(e.rc))
            raise DriverException("Login failed: " + e.reason)

    #==========================================================================
    def logout(self, domain, host ):
        
        if self.__userManager is None:
            raise HiflyException("User manager not available")
        
        try:
            LOG("Loggin off on host " + host + ", domain " + domain)
            self.__userManager.logOff( host, domain )
        except spell.lib.hifly.interface._GlobalIDL.USERcorbaManager.USERexceptionReject,e:
            LOG("Failed logout")
            LOG("   Reason: " + repr(e.reason))
            LOG("   Code  : " + userCodeStr(e.rc))
            raise DriverException("Login failed: " + e.reason)

    #==========================================================================
    def isLoggedIn(self, uname, host, domain ):
        raise NotImplemented
        
    #==========================================================================
    def getUserWorkspace(self, uname, host, domain ):
        raise NotImplemented

    #==========================================================================
    def getUserDomains(self, uname, host ):
        raise NotImplemented
        
    #==========================================================================
    def getAvailableRoles(self, host ):
        raise NotImplemented
