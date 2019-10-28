
from spell.lib.hifly.interface import ICLOCK
from spell.lib.hifly.interface import ICLOCK_PRO
from spell.lang.constants import *
from spell.lang.modifiers import *

###############################################################################
# Time access modes
ACCESS_TIME_LIVE = ICLOCK.REAL_TIME
ACCESS_TIME_STOP = ICLOCK.HISTORY_STOP
ACCESS_TIME_FWD  = ICLOCK.HISTORY_FORWARD
ACCESS_TIME_BWD  = ICLOCK.HISTORY_BACKWARD

###############################################################################
# Clock status
TIME_OK = ICLOCK.OK
TIME_TOO_EARLY = ICLOCK.TOO_EARLY
TIME_TOO_LATE  = ICLOCK.TOO_LATE
TIME_INVALID   = ICLOCK.INVALID

###############################################################################
def timeModeToDriver( mode ):
    
    if mode == TIME_MODE_LIVE: return ACCESS_TIME_LIVE
    if mode == TIME_MODE_FWD: return ACCESS_TIME_FWD
    if mode == TIME_MODE_BWD: return ACCESS_TIME_BWD
    
    raise HiflyException("Unknown time mode: " + str(mode))

###############################################################################
def timeModeToCore( mode ):
    
    if mode == ACCESS_TIME_LIVE: return TIME_MODE_LIVE
    if mode == ACCESS_TIME_FWD: return TIME_MODE_FWD
    if mode == ACCESS_TIME_BWD: return TIME_MODE_BWD
    
    raise HiflyException("Unknown time mode: " + str(mode))

###############################################################################
def timeModeToStr( mode ):
    """
    Utility method for transalting time modes to readable strings
    """
    if mode == ACCESS_TIME_LIVE:
        return "live"
    elif mode == ACCESS_TIME_STOP:
        return "retrieval stop"
    elif mode == ACCESS_TIME_FWD:
        return "retrieval fwd"
    elif mode == ACCESS_TIME_BWD:
        return "retrieval bwd"
    else:
        return "unknown"

###############################################################################
def timeStateToStr( state ):
    """
    Utility method for transalting clock status to readable strings
    """
    if state == TIME_OK:
        return "ok"
    elif state == TIME_TOO_EARLY:
        return "too early"
    elif state == TIME_TOO_LATE:
        return "too late"
    elif state == TIME_INVALID:
        return "invalid"
    else:
        return "unknown"

