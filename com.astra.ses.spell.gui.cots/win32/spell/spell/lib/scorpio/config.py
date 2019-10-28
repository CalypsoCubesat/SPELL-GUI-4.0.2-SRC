################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.config 
FILE
    config.py
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
import spell.lib.adapter.config 
from spell.utils.log import *
from spell.config.reader import Config
from spell.config.constants import COMMON
from spell.lib.exception import *

#*******************************************************************************
# System imports
#*******************************************************************************
import os,sys

#*******************************************************************************
# Import Definition
#*******************************************************************************

__all__ = ['CONFIG']


#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.config.ConfigInterface
INTERFACE_DEFAULTS = {}

################################################################################
class ConfigInterface( superClass ):

    __chelper = None

    #==========================================================================    
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
        
    #==========================================================================    
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup Scorpio CFG interface")
        
        # Obtain the configuration information for this context
        # The context
        ctx = Config.instance().getContextConfig(contextName)
        # The driver name
        driverName = ctx.getDriver()
        # The family
        family = ctx.getFamily()
        LOG("Using family: " + repr(family))
        # The spacecraft
        domain = ctx.getSC()
        LOG("Using domain: " + repr(domain))

    #==========================================================================    
    def cleanup(self, shutdown = False):
        LOG("Shutting down")
        
################################################################################
# Instance 
CONFIG = ConfigInterface()
