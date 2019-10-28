###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.time 
FILE
    time.py
    
DESCRIPTION
    services for time conversion 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly.interface import IBASE
from spell.lib.hifly.internals.exception import HiflyException
from spell.lib.hifly.internals.connection import CONN
from spell.lib.hifly.utils.time_utils import * 
from string import split,atoi
from spell.utils.ttime import *
import time
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.utils.log import *


###############################################################################
class TimeAccess:
    
    """
    Low level interface to the clock services in TM/TC/EV provision servers
    """
    
    __timeManager = None
    __timeMode = ACCESS_TIME_LIVE
    
    def __init__(self):
        self.__timeManager = None
    
    #==========================================================================
    def setupTimeAccess(self):
        """
        Obtain the time manager and setup datastreams
        """
        self.__timeManager = self.getServiceServer()._get_m_timeMngr()
        if self.__timeManager is None:
            raise HiflyException("Error when setting up time access", "Unable to obtain time manager")
        self.__timeManager.setDataStreams( [ 65535 ] )
        LOG("Time access ready")
        
    #==========================================================================
    def cleanTimeAccess(self):
        """
        Release used objects
        """
        res = self.getServiceServer()
        if res:
            try:
                LOG("Unlocking server: "  + repr(res))
                res.unlock()
            except:
                pass
        if self.__timeManager:
            CONN.releaseObject(self.__timeManager)
        
    #==========================================================================
    def getServiceServer(self):
        """
        To be implemented in child classes
        """
        raise NotImplemented
    
    #==========================================================================
    def getServiceView(self):
        """
        To be implemented in child classes
        """
        raise NotImplemented
        
    #==========================================================================
    def setTimeMode(self, mode):
        """
        Change the time mode (live, playback fwd, bwd)
        """
        
        if self.__timeManager is None:
            raise HiflyException("Time service not available")
        
        LOG("Setting time access to " + timeModeToStr(mode) + " mode (" + repr(mode) + ")")
        
        if mode is ACCESS_TIME_LIVE:
            res = self.getServiceServer().unlock()
            LOG("Unlocking server: "  + repr(res))
        else:
            res = self.getServiceServer().lock(self.getServiceView())
            LOG("Locking server: " + repr(res))
            if not res:
                raise HiflyException("Error while locking/unlocking server: " + repr(res))

        state = self.__timeManager.setMode( mode )
        LOG("Resulting state: " + timeStateToStr(state))
        
        self.__timeMode = mode
        
    #==========================================================================
    def getTimeMode(self):
        return self.__timeMode
        
    #==========================================================================
    def step(self):
        """
        Make the clock do a step
        """
        if self.__timeManager.getMode() == ACCESS_TIME_LIVE:
            raise HiflyException("Cannot step: not in retrieval mode")
        
        state = self.__timeManager.step()
        time = self.__timeManager.getUTC().m_sec
        
        LOG("Stepping")
        
        if state == TIME_OK:
            pass
            #LOG("Time step. Current time: " + repr(time))
        elif state == TIME_TOO_EARLY:
            LOG("Cannot step: no previous packet available. Current time: " + secsToStr(time))
        elif state == TIME_TOO_LATE:
            LOG("Cannot step: no next packet available. Current time: " + secsToStr(time))
        elif state == TIME_INVALID:
            LOG("Cannot step: invalid time.")
        else:
            raise HiflyException("Unknown clock state: " + repr(state))

        minTime = self.__timeManager.getMinTime().m_sec
        maxTime = self.__timeManager.getMaxTime().m_sec
        LOG("Time limits: " + secsToStr(minTime) + "->" + secsToStr(maxTime) )
        
    #==========================================================================
    def setTime(self, timeSec, timeUsec = 0, delta = False):
        """
        Move the clock to the given time
        """
        
        if type(timeSec)==float: timeSec = int(timeSec)
        
        if type(timeSec) != int or type(timeUsec) != int or type(delta) != bool:
            raise HiflyException("setTime: wrong parameters")
         
        sampleTime = IBASE.Time(timeSec, timeUsec, delta) 

        LOG("Setting time to: " + timeToStr(sampleTime))
        
        res = self.__timeManager.setSampleTime(sampleTime)

        LOG("Time set result: " + str(res))


###############################################################################
def getCurrentTime():
    
    """
    Obtain the current time in IBASE format
    """
    timeSec = time.time()
    pair = split( str( timeSec ), '.')
    theTime = IBASE.Time( atoi(pair[0]), atoi(pair[1]), False )
    return theTime

###############################################################################
def getCurrentTimeDelta(delta):
    
    """
    Obtain the current time plus a delta in IBASE format
    """
    timeSec = time.time()
    pair = split( str( timeSec ), '.')
    theTime = IBASE.Time( atoi(pair[0]) + delta, atoi(pair[1]), False )
    return theTime

###############################################################################
def getAbsTime( secs, usecs = 0 ):
    """
    Translate the given secs,usecs to IBASE format
    """
    theTime = IBASE.Time( int(secs), usecs, False )
    return theTime

###############################################################################
def getRelTime( secs, usecs = 0 ):
    """
    Translate the given secs,usecs to relative IBASE format
    """
    theTime = IBASE.Time( secs, usecs, True )
    return theTime

###############################################################################
def timeToStr( secs ):
    """
    Translate the given IBASE time to a readable string
    """
    return time.ctime( secs.m_sec )

###############################################################################
def secsToStr( secs ):
    """
    Translate the given time to a readable string
    """
    return time.ctime( secs )
