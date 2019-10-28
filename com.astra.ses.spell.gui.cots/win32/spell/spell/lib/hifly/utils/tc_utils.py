
from spell.lib.hifly.interface import ITC
from spell.lib.hifly.interface import ITC_INJ
from spell.lib.hifly.interface import ITC_INJ__POA
from spell.lib.hifly.interface import ITC_PRO
from spell.lib.hifly.interface import ITC_PRO__POA
from spell.lib.hifly.constants import *
from  spell.lib.hifly.modifiers import *

# Define an all-pass filter for acknowledgement flags
ACK_FLAGS_ALL = ITC_INJ.PUS_ACK_ACCEPT | ITC_INJ.PUS_ACK_START | \
                ITC_INJ.PUS_ACK_PROGRESS | ITC_INJ.PUS_ACK_COMPLETE | \
                ITC_INJ.ACK_MIB_DEFAULT

# Telecommand source identifiers
SOURCE_MANS = ITC.MANUAL_STACK
SOURCE_AUTO = ITC.AUTO_STACK
SOURCE_EXIF = ITC.EXT_SOURCE
SOURCE_ALL = SOURCE_MANS | SOURCE_AUTO | SOURCE_EXIF

###############################################################################
def linkStatusStr(status):
    """
    Utility method to translate TC link status to readable string
    """
    if status == ITC_INJ.LINK_UP:    return UP
    if status == ITC_INJ.LINK_DOWN:  return DOWN
    return UNKNOWN

###############################################################################
def checkStateStr(state):
    """
    Utility method to translate check state to readable string
    """
    if state == ITC.CHECK_ENABLED:         return ENABLED
    if state == ITC.CHECK_DISABLED:        return DISABLED
    if state == ITC.CHECK_OVERRIDE:        return OVERRIDE
    if state == ITC.CHECK_NO_NOTIFICATION: return NONOTIF
    return UNKNOWN

###############################################################################
def MMMtoStr(mode):
    """
    Utility method to translate master manual mode status to readable string
    """
    mstr = "['" + mode.m_host + "':"
    if mode.m_active: 
        mstr = mstr + "active]"
    else:
        mstr = mstr + "inactive]"
    return mstr

###############################################################################
def stageStr(stage):
    """
    Utility method to translate verif stage names to readable string
    """
    if stage == ITC.PTV_DYNAMIC:     return "Dynamic PTV"
    if stage == ITC.PTV_STATIC:      return "Static PTV"
    if stage == ITC.MCS_RELEASE:     return "MCS release"
    if stage == ITC.UV_GS_RECEIVE:   return "GS Receive"
    if stage == ITC.UV_GS_UPLINK:    return "Uplinked"
    if stage == ITC.UV_ONB_ACCEPT:   return "Onboard accept"
    if stage == ITC.EV_APP_ACCEPT:   return "Application accept"
    if stage == ITC.EV_START_EXEC:   return "Start execution"
    if stage == ITC.EV_PROGRESS_0:   return "EVP 0"
    if stage == ITC.EV_PROGRESS_1:   return "EVP 1"
    if stage == ITC.EV_PROGRESS_2:   return "EVP 2"
    if stage == ITC.EV_PROGRESS_3:   return "EVP 3"
    if stage == ITC.EV_PROGRESS_4:   return "EVP 4"
    if stage == ITC.EV_PROGRESS_5:   return "EVP 5"
    if stage == ITC.EV_PROGRESS_6:   return "EVP 6"
    if stage == ITC.EV_PROGRESS_7:   return "EVP 7"
    if stage == ITC.EV_PROGRESS_8:   return "EVP 8"
    if stage == ITC.EV_PROGRESS_9:   return "EVP 9"
    if stage == ITC.EV_END_EXEC:     return "Execution confirmed"
    return "Unknown"

#############################################################################
def cevStr(status):
    
    """
    Utility method to translate CEV status to readable string
    """

    if status == ITC.IDLE:             return IDLE
    if status == ITC.PENDING:          return PENDING
    if status == ITC.PASSED:           return PASSED
    if status == ITC.FAILED:           return FAILED
    if status == ITC.UNVERIFIED:       return UNVERIFIED
    if status == ITC.UNKNOWN:          return UNKNOWN
    if status == ITC.TIMEOUT:          return TIMEOUT
    if status == ITC.NOT_APPLICABLE:   return NOT_APPLICABLE
    return UNKNOWN

