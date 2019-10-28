################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.dummy.ev
FILE
    ev.py
    
DESCRIPTION
    EV interface for standalone driver

COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Fabien Bouleau 
    Rafael Chinchilla Camara (GMV)
"""
################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.log import *
from spell.lib.exception import *
from spell.lang.constants import *
from spell.lang.modifiers import *

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import sys

###############################################################################
# Module import definition

__all__ = ['EV']

###############################################################################
# Superclass
import spell.lib.adapter.ev
superClass = spell.lib.adapter.ev.EvInterface

###############################################################################
class EvInterface(superClass):
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
    
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self,contextName)
        LOG("Setup standalone EV interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup standalone EV interface")
        
    #==========================================================================
    def _raiseEvent(self, message, config):

        severity = config.get(Severity)
        scope = config.get(Scope)

        if severity == INFORMATION:
            severity = "INFO"
        elif severity == WARNING:
            severity = "WARN"
        elif severity == ERROR:
            severity = "ERROR"
        elif severity == FATAL:
            severity = "FATAL"
            
        if scope == SCOPE_PROC:
            scope = "PROC"
        elif scope == SCOPE_SYS:
            scope = "SYSTEM"
        elif scope == SCOPE_CFG:
            scope = "CONFIG"
        else:
            scope = "UNKNOWN"
        sys.stderr.write("[EVENT] " + repr(message) + " (" + repr(severity) + ":" + repr(scope) + ")\n")
            
    #==========================================================================
    def _registerForEvents(self, view, config = {} ):
        raise DriverException("Service not available in this driver")
    
    #==========================================================================
    def unregisterForEvents(self):
        raise DriverException("Service not available in this driver")

    #==========================================================================
    def pullEvents(self):
        raise DriverException("Service not available in this driver")
            
################################################################################
# Interface instance
EV = EvInterface()            