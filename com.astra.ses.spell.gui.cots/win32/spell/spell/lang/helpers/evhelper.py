###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lang.helpers.evhelper 
FILE
    evhelper.py
    
DESCRIPTION
    Helpers for event management
    
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
from spell.lib.exception import *
from spell.lang.functions import *
from spell.lang.constants import *
from spell.lang.modifiers import *

#*******************************************************************************
# Local Imports
#*******************************************************************************
from basehelper import WrapperHelper

#*******************************************************************************
# System Imports
#*******************************************************************************


###############################################################################
# Module import definition

__all__ = ['Event_Helper']

################################################################################
class Event_Helper(WrapperHelper):

    """
    DESCRIPTION:
        Helper for the Event wrapper.
    """
    __msg = ""    
    
    #===========================================================================
    def __init__(self):
        WrapperHelper.__init__(self, "EV")
        self.__msg = ""
        self._opName = "Event Injection" 

    #===========================================================================
    def _doPreOperation(self, *args, **kargs):
        # Parse arguments
        if len(args)==0:
            raise SyntaxException("No message given")
        self.__msg = args[0]
        if type(self.__msg)!=str:
            raise SyntaxException("Expected a message string")
    
    #===========================================================================
    def _doOperation(self, *args, **kargs ):
        self._write( self.__msg, self._config )
        REGISTRY['EV'].raiseEvent(self.__msg, self._config)            
        return [False,True]

