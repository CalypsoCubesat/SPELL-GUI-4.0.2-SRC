################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.ev 
FILE
    ev.py
    
DESCRIPTION
    hifly services for event management (low level interface)
    
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
from spell.lang.constants import *
from spell.lang.modifiers import *
import spell.lib.adapter.ev
from spell.lib.exception import *
from spell.utils.log import * 
from spell.config.reader import *
            
#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.timeacc import *
from internals.exception import *
from utils.ev_utils import *
from internals.ev.injection import EvInjection
from internals.ev.provision import EvProvision
from interface.ICLOCK import NotPossible,TOO_EARLY,TOO_LATE,INVALID,TOO_MANY_STREAMS

#*******************************************************************************
# System imports
#*******************************************************************************
import socket

#*******************************************************************************
# Import definition
#*******************************************************************************

__all__ = ['EV']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.ev.EvInterface

################################################################################
class EvInterface( superClass ):
    
    """
    Concrete implementation of the core ev_class for hifly driver
    """
    evPro = None
    evInj = None
    ctxName = None
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
        # Create the internal hifly interfaces
        self.evPro = EvProvision()
        self.evInj = EvInjection()
        self.ctxName = None
    
    #==========================================================================
    def setup(self, ctxName):
        """
        DESCRIPTION:
            Setup the hifly low level interface 
        """
        try:
            superClass.setup(self,ctxName)
            scid = Config.instance().getContextConfig(ctxName).getSC()
            hostname = socket.gethostname()
            # Setup default configuration parameters
            self.evInj.setEventParams(hostname, scid )
            # Setup internals 
            LOG("Initializing hifly EV provision interface")
            self.evPro.setup()
            LOG("Initializing hifly EV injection interface")
            self.evInj.setup()
            LOG("hifly EV interfaces ready")
        except HiflyException,ex:
            raise DriverException("Unable to load EV interface: " + ex.message, ex.reason)
        except Exception,ex:
            raise DriverException("Unable to load EV interface", repr(ex))

    #==========================================================================
    def cleanup(self):
        """
        DESCRIPTION:
            Cleanup the hifly low level interface
        """
        superClass.cleanup(self)
        LOG("Cleaning up hifly EV provision interface")
        self.evPro.cleanup()
        LOG("Cleaning up hifly EV injection interface")
        self.evInj.cleanup()

    #==========================================================================
    def _raiseEvent(self, message, config = {} ):

        severity = config.get(Severity)
        scope = config.get(Scope)

        LOG("Raising event, language parameters: " + str(severity) + "," + str(scope))
        sev = coreSeverityToDriver(severity)
        scp = coreScopeToDriver(scope)
        LOG("Driver severity: " + severityToStr(sev))
        LOG("Driver scope   : " + scopeToStr(scp))
        try:
            LOG("Inject event: '" + message + "'")
            self.evInj.injectEvent( message, sev, scp )
            LOG("Event injected")
        except HiflyException,e:
            raise DriverException("Could not inject event: " + repr(e))
    
    #==========================================================================
    def _registerForEvents(self, view, config = {} ):

        LOG("Registering for events")
        timeMode = config.get(Mode)
        LOG("Using mode " + str(timeMode))
        theTime  = config.get(Time)
        if type(theTime) in [int,float]:
            theTime = int(theTime)
        elif isinstance(theTime,TIME):
            theTime = theTime.abs()
        elif type(theTime)==str:
            if len(theTime.strip())==0:
                if timeMode != TIME_MODE_LIVE:
                    raise DriverException("Cannot register for events", "Given an empty date")
                else:
                    theTime = None
            else:
                theTime = TIME(theTime).abs()
        else:
            raise DriverException("Cannot register for events", "Invalid time format: " + repr(theTime))
        LOG("Using time " + str(theTime))
        #TODO: usecs in TIME    
        usecs = 0
        #TODO: delta
        delta = False
        
        LOG("Monitoring all events in " + timeMode)
        mode = timeModeToDriver(timeMode)
        
        LOG("Register interest in all events")
        self.evPro.registerUserView( view )
        self.evPro.registerForAllEvents()
        LOG("Driver time mode: " + mode)
        self.evPro.setTimeMode( mode )
        if ((timeMode != TIME_MODE_LIVE) and (theTime>0)):
            LOG("Moving clock to time " + secsToStr(theTime))
            if type(usecs)!=int: usecs = int(usecs)
            self.evPro.setTime( int(theTime), usecs, delta )
        LOG("Registration done")

    #==========================================================================
    def unregisterForEvents(self):
        self.evPro.unregisterUserView()

    #==========================================================================
    def pullEvents(self):

        mode = timeModeToCore(self.evPro.getTimeMode())
        if mode == TIME_MODE_LIVE:
            raise DriverException("Cannot pull events: not in retrieval mode")
        try:        
            self.evPro.getNextData()
        except NotPossible,ex:
            r = ex.m_reason
            if r == TOO_LATE:
                msg = "No events at the given time, too late"
            elif r == TOO_EARLY:
                msg = "No events at the given time, too early"
            elif r == INVALID:
                msg = "Invalid time"
            else:
                msg = "No events at the given time"
            raise DriverException("Unable to retrieve events",msg)
        
################################################################################
# Interface instance
EV = EvInterface()
