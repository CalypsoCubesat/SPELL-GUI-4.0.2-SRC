################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.dummy.resources
FILE
    resources.py
    
DESCRIPTION
    Resource interface for standalone driver

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
        Resource management library interface. This class is in charge of
        managing the underlying system resources.
    """
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
            
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup standalone RSC interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup standalone RSC interface")
    
    #==========================================================================
    def _setLink(self, name, enable, config = {}):
        pass
        
    #==========================================================================
    def _checkLink(self, name):
        return True
    
    #==========================================================================
    def _setResource(self, name, value):
        pass

    #==========================================================================
    def _getResource(self, resourceName, config = {} ):
        return "<NONE>"

    #==========================================================================
    def _getResourceStatus(self, resource, config = {} ):
        return True

    #==========================================================================
    def _isResourceOK(self, resource, config = {} ):
        return True


################################################################################
# Interface handle
RSC = ResourceInterface()
        
            