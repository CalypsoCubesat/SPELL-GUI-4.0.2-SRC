################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.empty.tm
FILE
    tm.py
    
DESCRIPTION
    TM interface for empty driver

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

__all__ = ['TM']

###############################################################################
# Superclass
import spell.lib.adapter.tm
superClass = spell.lib.adapter.tm.TmInterface

###############################################################################
class TmInterface( superClass ):
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
            
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup empty TM interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup empty TM interface")
    
    #==========================================================================
    def _injectItem(self, param, value, config ):
        raise NotAvailable()        
    
    #==========================================================================
    def _refreshItem(self, param, config ):
        raise NotAvailable()        

    #===========================================================================
    def _setLimit(self, param, limit, value, config ):
        raise NotAvailable()

    #===========================================================================
    def _getLimit(self, param, limit, config ):
        raise NotAvailable()

    #===========================================================================
    def _getLimits(self, param, config ):
        raise NotAvailable()

    #===========================================================================
    def _setLimits(self, param, limits, config ):
        raise NotAvailable()

################################################################################
# Interface handle
TM = TmInterface()
