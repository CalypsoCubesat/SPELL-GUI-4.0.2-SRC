################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.dummy.tm
FILE
    tm.py
    
DESCRIPTION
    TM interface for standalone driver

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
from spell.lib.registry import REGISTRY

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import os

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
        LOG("Setup standalone TM interface")
        
    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup standalone TM interface")
    
    #===========================================================================
    def _createTmItem(self, mnemonic, description = ""):
        LOG("Creating simulated TM item: " + mnemonic)
        if mnemonic == "NOTFOUND":
            raise DriverException("Parameter not found")
        return REGISTRY['SIM'].getTMitem(mnemonic, description)
    
    #==========================================================================
    def _injectItem(self, param, value, config ):
        REGISTRY['SIM'].changeItem(param,value)
        return True
    
    #==========================================================================
    def _refreshItem(self, param, config ):
        name = param.name()
        if name == "INVALID":
            param._status = False
        elif name == "TIMEOUT":
            import time
            time.sleep(1000)

        eng = (config.get(ValueFormat) == ENG)
        
        if eng:
            value = param._engValue
        else:
            value = param._rawValue
        return [value, param._status]

    #===========================================================================
    def _setLimit(self, param, limit, value, config ):
        REGISTRY['CIF'].write("Set limit for " + repr(param) + ": " + repr(limit) + "=" + repr(value))
        return True

    #===========================================================================
    def _getLimit(self, param, limit, config ):
        REGISTRY['CIF'].write("Get limit for " + repr(param) + ": " + repr(limit))
        return None

    #===========================================================================
    def _getLimits(self, param, config ):
        REGISTRY['CIF'].write("Get limits for " + repr(param))

    #===========================================================================
    def _setLimits(self, param, limits, config ):
        REGISTRY['CIF'].write("Set limits for " + repr(param) + ": " + repr(limits))
               
################################################################################
# Interface handle
TM = TmInterface()
