################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.utils.ev_utils
    
FILE
    ev_utils.py
    
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
from spell.lib.hifly.interface import IEV
import spell.lang.constants

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************

#*******************************************************************************
# Module globals
#*******************************************************************************

###############################################################################
# Event scopes (to be used in procedures)            
EV_SCOPE_SYSTEM    = IEV.SYSTEM
EV_SCOPE_SOFTWARE  = IEV.SOFTWARE
EV_SCOPE_MIB       = IEV.MIB
EV_SCOPE_LOG       = IEV.LOG
EV_SCOPE_ALL       = IEV.SYSTEM | IEV.SOFTWARE | IEV.MIB | IEV.LOG  

###############################################################################
# Event severities (to be used in procedures)            
EV_SEV_WARNING     = IEV.WARNING
EV_SEV_ERROR       = IEV.ERROR
EV_SEV_FATAL       = IEV.FATAL
EV_SEV_INFORMATION = IEV.INFORMATION
EV_SEV_ALL         = IEV.WARNING | IEV.ERROR | IEV.FATAL | IEV.INFORMATION  

###############################################################################
def scopeToStr(scope):
    
    """
    Utility method to translate a given scope to a readable string
    """
    if scope == EV_SCOPE_SYSTEM:    return "system"
    if scope == EV_SCOPE_SOFTWARE:  return "software"
    if scope == EV_SCOPE_MIB:       return "mib"
    if scope == EV_SCOPE_LOG:       return "log"
    if scope == EV_SCOPE_ALL:       return "all"
    return "ukn/mix"

###############################################################################
def coreScopeToDriver(scope):
    
    """
    Utility method to translate a given scope to a readable string
    """
    if scope == spell.lang.constants.SCOPE_SYS: return EV_SCOPE_SYSTEM
    if scope == spell.lang.constants.SCOPE_PROC:return EV_SCOPE_SOFTWARE
    if scope == spell.lang.constants.SCOPE_CFG: return EV_SCOPE_MIB
    return EV_SCOPE_ALL
    
###############################################################################
def severityToStr(sev):

    """
    Utility method to translate a given severity to a readable string
    """

    if sev == EV_SEV_WARNING:       return "warning"
    if sev == EV_SEV_ERROR:         return "error"
    if sev == EV_SEV_FATAL:         return "fatal"
    if sev == EV_SEV_INFORMATION:   return "information"
    if sev == EV_SEV_ALL:           return "all"
    return "ukn/mix"

###############################################################################
def coreSeverityToDriver(sev):
    
    """
    Utility method to translate a given scope to a readable string
    """
    if sev == spell.lang.constants.WARNING:      return EV_SEV_WARNING
    if sev == spell.lang.constants.ERROR:        return EV_SEV_ERROR
    if sev == spell.lang.constants.FATAL:        return EV_SEV_FATAL
    if sev == spell.lang.constants.INFORMATION:  return EV_SEV_INFORMATION
    return EV_SEV_ALL
