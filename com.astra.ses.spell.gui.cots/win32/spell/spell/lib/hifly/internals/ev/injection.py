###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.ev.injection 
FILE
    injection.py
    
DESCRIPTION
    hifly services for event injection (low level interface)
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly.internals.connection import CONN
from spell.lib.hifly.internals.exception import HiflyException
from spell.utils.log import *
from spell.lib.hifly.utils.ev_utils import *
from spell.lib.hifly.ev import *
from spell.lib.hifly.interface import IEV_INJ__POA,IEV_INJ,IEV

###############################################################################
class EvInjectionView( IEV_INJ__POA.EventInjectMngrView ):
    
    """
    View used for event injection subscriptions (not used 
    but must be provided)
    """
       
    #==========================================================================
    def updateSystemCmdUpdate(self, responseInfo):
        """
        Not used in the hifly driver
        """
        pass

    #==========================================================================
    def ping(self):
        pass

###############################################################################
class EvInjection( object ):
    
    """
    DESCRIPTION:
        Low level interface for hifly event injection services
    """

    __evInjector = None
    __evInjManager = None
    __evView = None
    __chelper = None
    
    #==========================================================================
    def __init__(self):
        
        LOG("Created")
        self.__evInjector = None
        self.__evInjManager = None
        self.__evView = None
        
    #==========================================================================
    def setup(self):
        
        """
        Obtains the hifly event injection manager, obtains an injector server
        from it, and creates the view used for event subscription. 
        """
        
        # Event injection manager paramenters
        serviceName = IEV_INJ.EventInjectManager.ServiceName
        serviceClass = IEV_INJ.EventInjectManager
        
        # Obtain the manager
        LOG("Getting EV injection service manager")
        self.__evInjManager = CONN.getService( serviceName, serviceClass )
        
        if self.__evInjManager is None:
            raise HiflyException("Could not obtain EV injection manager")
        
        # Create the events view
        self.__evView = EvInjectionView()
        
        # Obtain one event injector
        LOG("Obtaining event injector")
        self.__evInjector = self.__evInjManager.registerView( self.__evView._this(), 10 )
    
        if self.__evInjector is None:
            raise HiflyException("Could not obtain EV injector")
                
    #==========================================================================
    def cleanup(self):
        
        """
        Perform cleanup operations, release CORBA objects in the proper
        order
        """
        
        if self.__evView:            
            LOG("Releasing EV injection view")
            CONN.releaseObject(self.__evView._this())
        
        if self.__evInjector: 
            LOG("Releasing EV injector")
            CONN.releaseObject(self.__evInjector)

        if self.__evInjManager:
            LOG("Releasing EV injection manager")
            CONN.releaseObject(self.__evInjManager) 

    #==========================================================================
    def setEventParams(self, ws, scid ):
        
        """
        Configure event parameters
            - Application name
            - Workstation name
            - Spacecraft ID
        """
        
        LOG("Setting event parameters: " + ws + "," + scid)
        self.app = "SPELL"
        self.ws = ws
        self.scid = scid

    #==========================================================================
    def injectEvent(self, msg, severity, scope):
        
        """
        Inject an event into the system, described by:
            - The event message
            - The scope (software, mib, etc)
            - The severity (info, warning, etc)
        """
        
        # Check that we have a valid injector
        if self.__evInjector is None:
            raise HiflyException("EV injection service not available")
        
        # Create the event object
        event = IEV.Event(
                          "SPELL",       # EIS007 will be used always
                          " " + msg,     # Attach the message
                          self.app, 
                          self.ws,
                          scope,
                          severity,
                          self.__evInjector.getDefaultDataStream(),
                          self.scid
                          )
        
        LOG("Sending event: '" + msg + "' (" + scopeToStr(scope) + "|" + 
                 severityToStr(severity) + ")")

        # Inject the event
        self.__evInjector.injectEvent(event)



