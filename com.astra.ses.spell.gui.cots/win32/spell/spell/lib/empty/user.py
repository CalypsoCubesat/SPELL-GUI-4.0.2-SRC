################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.empty.user
FILE
    user.py
    
DESCRIPTION
    User management interface for empty driver

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

__all__ = ['USER']

###############################################################################
# Superclass
import spell.lib.adapter.user
superClass = spell.lib.adapter.user.UserInterface

###############################################################################
class UserInterface(superClass):
    
    """
    DESCRIPTION:
        User management interface. 
    """
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
            
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup empty USER interface")

    #==========================================================================
    def cleanup(self):
        superClass.cleanup(self)
        LOG("Cleanup empty USER interface")
        
    #==========================================================================
    def _login(self, username, password, config = {} ):
        raise NotAvailable()
        
    #==========================================================================
    def _logout(self, username, config = {}):
        raise NotAvailable()

    #==========================================================================
    def _isLoggedIn(self, username, config = {}):
        raise NotAvailable()
            
###############################################################################
# Interface instance
USER = UserInterface()
