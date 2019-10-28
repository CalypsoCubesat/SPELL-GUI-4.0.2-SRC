###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.ev.provision 
FILE
    provision.py
    
DESCRIPTION
    hifly services for event provision (low level interface)
    
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
from spell.lib.hifly.ev import *
from spell.lib.hifly.interface import IEV_PRO__POA,IEV_PRO,IEV
from spell.lib.hifly.internals.timeacc import TimeAccess

###############################################################################
class EvProvision( TimeAccess, IEV_PRO__POA.EventMngrView ):
    
    """
    Low level interface to the hifly event provision services.
    """
    __evServer = None
    __evServerManager = None
    __evManager = None
    __viewKey = None
    __eventView = None
    
    #==========================================================================
    def __init__(self):
        
        LOG("Created")
        self.__evServer = None
        self.__evServerManager = None
        self.__evManager = None
        self.__viewKey = None

    #==========================================================================
    def ping(self):
        pass

    #==========================================================================
    def setup(self):
        
        """
        Setup the interface. Obtain the event provision manager,
        get an event server and create the events view.
        """
        
        # Event provision service manager parameters
        serviceName = IEV_PRO.EVserverMngr.ServiceName
        serviceClass = IEV_PRO.EVserverMngr
        
        # Obtain the event server manager
        LOG("Obtaining EV provision service")
        self.__evServerManager = CONN.getService( serviceName, serviceClass )
        
        if self.__evServerManager is None:
            raise HiflyException("Could not obtain EV provision service")
        
        # Get a provision server
        LOG("Obtaining EV provision server")
        try:
            self.__evServer = self.__evServerManager.getEVserver(False)
        except Exception,e:
            raise HiflyException("EV provision server not available: ", e)

        # Create the view for subscribed events
        LOG("Creating event view")
        try:
            self.__evManager = self.__evServer._get_m_eventMngr()
        except Exception,e:
            raise HiflyException("EV manager not available: ", e)
        
        #self.__eventView = EvProvisionView()
        
        # Register the view in the event server. A transmission
        # filter is setup in order to get event data only, discarding
        # header/packet raw data.
        LOG("Registering event view")
        filter = IEV.TransmissionFilter( True, False, False, False )
        self.__viewKey = self.__evManager.registerEventView( self._this(), 10, filter )
        LOG("View registered with key " + repr(self.__viewKey))
        
        # Setup the time management interface needed for retrievals 
        LOG("Obtaining time access")
        self.setupTimeAccess()
        
    #==========================================================================
    def cleanup(self):
        
        """
        Perform cleanup operations, releasing objects in the correct order.
        """
        
        LOG("Releasing time access")            
        self.cleanTimeAccess()

        LOG("Releasing events view")
        CONN.releaseObject(self._this())
        
        if self.__evManager: 
            LOG("Releasing events manager")
            CONN.releaseObject(self.__evManager)

        if self.__evServer:
            LOG("Releasing EV server")
            CONN.releaseObject(self.__evServer) 

        if self.__evServerManager:
            LOG("Releasing EV service manager")
            CONN.releaseObject(self.__evServerManager)
        
    #==========================================================================
    def registerForEventType(self, scope, severity):
        
        """
        Register for events of the given scope and severity.
        """
        
        if self.__viewKey is None:
            raise HiflyException("EV provision not available")
        
        # Create an event filter
        eventFilter = IEV.EventFilter(
                "", # Msg id 
                "", # Message
                "", # Application
                "", # Workstation
                scope, # Scope
                severity, # Severity
                [65535], # Default DS
                ""  # SCID
                )
        
        # Register for the events
        result = self.__evManager.registerEvents( self.__viewKey, eventFilter )
        
        LOG("Registration success for (" + scopeToStr(scope) + "|" + severityToStr(severity) + "): " + repr(result))

    #==========================================================================
    def registerForEventCode(self, code):

        """
        Register for events with a particular event code
        """

        if self.__viewKey is None:
            raise HiflyException("EV provision not available")
        
        # Create the event filter
        eventFilter = IEV.EventFilter(
                "[" + code + "]", # Msg id 
                "", # Message
                "", # Application
                "", # Workstation
                EV_SCOPE_ALL, # Scope
                EV_SEV_ALL, # Severity
                [65535], # DS
                ""  # SCID
                )
        
        # Register for those events
        result = self.__evManager.registerEvents( self.__viewKey, eventFilter )
        
        LOG("Registration success for event code " + code + ":" + repr(result))

    #==========================================================================
    def registerUserView(self, userView ):
        
        self.__eventView = userView

    #==========================================================================
    def unregisterUserView(self):
        
        self.__eventView = None

    #==========================================================================
    def registerForAllEvents(self):

        """
        Register for all events raised on the system
        """
        
        if self.__viewKey is None:
            raise HiflyException("EV provision not available")
        
        # Create the event filter
        eventFilter = IEV.EventFilter(
                "", # Msg id 
                "", # Message
                "", # Application
                "", # Workstation
                EV_SCOPE_ALL, # Scope
                EV_SEV_ALL, # Severity
                [], # DS
                ""  # SCID
                )
        
        # Register for events
        result = self.__evManager.registerEvents( self.__viewKey, eventFilter )
        
        LOG("Registration success for all events:" + repr(result))
        
    #==========================================================================
    def getNextData(self):
        
        """
        Get next event data part during retrievals
        """
        events = self.__evManager.getNextData(self.__viewKey)
        self.notifyEvents(events)

    #==========================================================================
    def notifyEvents( self, combinedEvents ):

        LOG("Notify events ( total" + str(len(combinedEvents.m_events)) + ")")
        LOG("              ( OOLs " + str(len(combinedEvents.m_oolInfos)) + ")")
        for ev in combinedEvents.m_events:

            sec = ev.m_time.m_sec
            usec = ev.m_time.m_micro
            ID = ev.m_event.m_id
            text = ev.m_event.m_message
            app = ev.m_event.m_application
            ws = ev.m_event.m_workstation
            scope = scopeToStr(ev.m_event.m_scope)
            sev = severityToStr(ev.m_event.m_severity)
            scid = ev.m_event.m_spacecraft
        
            if self.__eventView:
                self.__eventView.notifyEvent(sec, usec, ID, text, app, ws, scope, sev, scid )
            
            LOG("----------------------------------------------------------")
            LOG("        Event time : " + str(sec) + "," + str(usec) )
            LOG("        ID         : " + ID)
            LOG("        Msg        : " + text)
            LOG("        App        : " + app)
            LOG("        Ws         : " + ws)
            LOG("        Scope      : " + scope)
            LOG("        Severity   : " + sev)
            LOG("        Dstream    : " + str(ev.m_event.m_dataStreamID))
            LOG("        SC         : " + scid)

        
    #==========================================================================
    def getServiceServer(self):
        
        """
        Required by the time management interface. The service provider
        must be given.
        """
        return self.__evServer

    #==========================================================================
    def getServiceView(self):
        return self._this()


