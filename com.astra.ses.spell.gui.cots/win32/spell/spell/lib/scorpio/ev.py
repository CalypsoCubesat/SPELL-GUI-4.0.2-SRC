################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.ev 
FILE
    ev.py
    
DESCRIPTION
    scorpio services for event management (low level interface)
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Srinivasan Ranganathan
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
# System imports
#*******************************************************************************

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
        self.ctxName = None
    
    #==========================================================================
    def setup(self, ctxName):
        """
        DESCRIPTION:
            Setup the hifly low level interface 
        """
        superClass.setup(self,ctxName)
        scid = Config.instance().getContextConfig(ctxName).getSC()
        # Setup default configuration parameters

    #==========================================================================
    def cleanup(self):
        """
        DESCRIPTION:
            Cleanup the hifly low level interface
        """
        superClass.cleanup(self)

    #==========================================================================
    def _raiseEvent(self, message, config = {} ):

        severity = config.get(Severity)
        scope = config.get(Scope)

        LOG("Raising event, language parameters: " + severity + "," + scope)
        sev = coreSeverityToDriver(severity)
        scp = coreScopeToDriver(scope)
        LOG("Driver severity: " + severityToStr(sev))
        LOG("Driver scope   : " + scopeToStr(scp))
    
    #==========================================================================
    def _registerForEvents(self, view, config = {} ):
        timeMode = config.get(Mode)
        secs = config.get(Time)

    #==========================================================================
    def unregisterForEvents(self):
        LOG("Unregistering events ")

    #==========================================================================
    def pullEvents(self):
        LOG("Pulling Events ")

################################################################################
# Interface instance
EV = EvInterface()
