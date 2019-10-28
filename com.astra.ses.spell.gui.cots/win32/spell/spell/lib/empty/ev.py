################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.empty.ev
FILE
    empty.py
    
DESCRIPTION
    EV interface for empty driver

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

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        
    #==========================================================================
    def _raiseEvent(self, message, config):
        raise NotAvailable()
            
    #==========================================================================
    def _registerForEvents(self, view, config = {} ):
        raise NotAvailable()
    
    #==========================================================================
    def unregisterForEvents(self):
        raise NotAvailable()

    #==========================================================================
    def pullEvents(self):
        raise NotAvailable()
            
################################################################################
# Interface instance
EV = EvInterface()            