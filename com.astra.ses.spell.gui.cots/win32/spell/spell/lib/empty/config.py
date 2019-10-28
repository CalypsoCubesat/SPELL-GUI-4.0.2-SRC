###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.empty.config 
FILE
    config.py
    
DESCRIPTION
    Config interface of empty driver
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    01/10/2007
"""

###############################################################################

#*******************************************************************************
# SPELL Imports
#*******************************************************************************
from spell.utils.log import *

#*******************************************************************************
# Local Imports
#*******************************************************************************

#*******************************************************************************
# System Imports
#*******************************************************************************


###############################################################################
# Module import definition

__all__ = ['CONFIG']

INTERFACE_DEFAULTS = {}

###############################################################################
# Superclass
import spell.lib.adapter.config
superClass = spell.lib.adapter.config.ConfigInterface
        
###############################################################################
class ConfigInterface(superClass):

    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
    
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup empty CFG interface")

    #==========================================================================
    def cleanup(self, shutdown = False):
        superClass.cleanup(self, shutdown)
        LOG("Cleanup empty CFG interface")
        
###############################################################################
# Interface instance
CONFIG = ConfigInterface()
