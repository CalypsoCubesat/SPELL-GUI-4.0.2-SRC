################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lang.helpers.limhelper
FILE
    limhelper.py
    
DESCRIPTION
    Helpers for limit management wrapper functions. 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    14/09/2009
    
REVISION HISTORY
    14/09/2009    10:30    Creation
"""

################################################################################

from basehelper import WrapperHelper
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.adapter.constants.notification import *
from spell.lib.exception import SyntaxException
from spell.lang.functions import *
from spell.lib.registry import *
from spell.lib.adapter.tm_item import TmItemClass

################################################################################
class AdjustLimits_Helper(WrapperHelper):

    """
    DESCRIPTION:
        Helper for the AdjustLimits wrapper.
    """    
    __verifyList = None
    
    #===========================================================================
    def __init__(self):
        WrapperHelper.__init__(self, "TM")
        self._opName = "Limit adjustment"

    #===========================================================================
    def _doPreOperation(self, *args, **kargs):
        if len(args)==0:
            raise SyntaxException("Expected a TM verification list")
        self.__verifyList = args[0]
        if type(self.__verifyList)!=list:
            raise SyntaxException("Expected a TM verification list")
            
    #===========================================================================
    def _doOperation(self, *args, **kargs ):
        
        result = False
        for condition in self.__verifyList:
            paramName = condition[0]
            paramValue = condition[2]
            operator = condition[1]
            if operator != eq: continue
            if type(paramValue)==str: # Status parameters
                limits = {Expected:paramValue}
                result = REGISTRY['TM'].setLimits( paramName, limits, config = self._config )
            else:
                tolerance = self.getConfig(Tolerance)
                limits = {}
                limits[LoRed] = paramValue - tolerance 
                limits[LoYel] = paramValue - tolerance 
                limits[HiYel] = paramValue + tolerance 
                limits[HiRed] = paramValue + tolerance 
                result = REGISTRY['TM'].setLimits( paramName, limits, config = self._config )
                
        return [False,result]

    #===========================================================================
    def _doRepeat(self):
        self._write("Retry adjust limits", {Severity:WARNING} )
        return [True, None]

    #===========================================================================
    def _doSkip(self):
        self._write("Skip limit adjustment", {Severity:WARNING} )
        return [False, True]

    #===========================================================================
    def _doCancel(self):
        self._write("Cancel limit adjustment", {Severity:WARNING} )
        return [False, False]
