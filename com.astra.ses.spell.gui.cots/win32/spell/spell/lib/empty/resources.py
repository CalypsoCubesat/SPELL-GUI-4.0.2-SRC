################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.empty.resources
FILE
    resources.py
    
DESCRIPTION
    Resource interface for empty driver

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

__all__ = ['RSC']

###############################################################################
# Superclass
import spell.lib.adapter.resources
superClass = spell.lib.adapter.resources.ResourceInterface

###############################################################################
class ResourceInterface(superClass):
    
    """
    DESCRIPTION:
        Empty resource management interface. 
    """
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
            
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup empty RSC interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup empty RSC interface")
    
    #==========================================================================
    def _setLink(self, name, enable, config = {}):
        raise NotAvailable()
        
    #==========================================================================
    def _checkLink(self, name):
        raise NotAvailable()
    
    #==========================================================================
    def _setResource(self, name, value):
        raise NotAvailable()

    #==========================================================================
    def _getResource(self, name):
        raise NotAvailable()

################################################################################
# Interface handle
RSC = ResourceInterface()
        
            