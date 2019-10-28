################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.empty.tc
FILE
    tc.py
    
DESCRIPTION
    Telecommand interface for empty driver

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

__all__ = ['TC']

###############################################################################
# Superclass
import spell.lib.adapter.tc
superClass = spell.lib.adapter.tc.TcInterface

###############################################################################
class TcInterface(superClass):
    
    """
    DESCRIPTION:
        Telecommand interface. 
    """
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
            
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup empty TC interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup empty TC interface")
    
    #==========================================================================
    def _sendCommand(self, tcItem, config = {} ):
        raise NotAvailable()

    #==========================================================================
    def _sendBlock(self, tcItemList, config = {} ):
        raise NotAvailable()

################################################################################
# Interface handle
TC = TcInterface()
        
                       