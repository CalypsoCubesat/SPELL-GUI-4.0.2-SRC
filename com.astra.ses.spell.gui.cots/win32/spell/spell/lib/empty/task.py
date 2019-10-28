################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.dummy.task
FILE
    task.py
    
DESCRIPTION
    Task management interface for empty driver

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

__all__ = ['TASK']

###############################################################################
# Superclass
import spell.lib.adapter.task
superClass = spell.lib.adapter.task.TaskInterface

###############################################################################
class TaskInterface(superClass):
    
    """
    DESCRIPTION:
        Empty task management interface. 
    """
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
            
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup empty TASK interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup empty TASK interface")
    
    #==========================================================================
    def _startTask(self, name, config = {}  ):
        raise NotAvailable()
        
    #==========================================================================
    def _stopTask(self, name, config = {} ):
        raise NotAvailable()

    #==========================================================================
    def _checkTask(self, name, config = {} ):
        raise NotAvailable()

################################################################################
# Interface handle
TASK = TaskInterface()
        
            