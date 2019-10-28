################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tm.subscriber
FILE
    subscriber.py
    
DESCRIPTION
    Thread for handling TM parameter registrations 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    15/01/2008
    
REVISION HISTORY
    08/01/2008    10:30    Creation
"""
################################################################################

from spell.lib.hifly.internals.tm.provision import BaseParameterView
from spell.lib.hifly.internals.value import Variant
from spell.lib.hifly.internals.exception import HiflyException
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.exception import *
from spell.utils.log import *
import time,threading

###############################################################################
class TmSubscriber( threading.Thread ):
    """
    DESCRIPTION:
        Handles parameter registrations for hifly 
    """
    
    # Name of the parameter being registered
    __parameter = None
    # Reference to the parameter manager
    __paramManager = None
    # When waiting for updates the uninit registration is used
    __waitUpdate = False
    # For cancelling the process of init registration before updating PM
    __cancel = False
    # Registration errors
    regError = None

    #===========================================================================
    def __init__(self, paramManager, parameterName, waitUpdate = False):
        threading.Thread.__init__(self)
        #LOG("Created")
        self.__paramManager = paramManager
        self.__parameter = parameterName
        self.__waitUpdate = waitUpdate
        self.__cancel = False
        self.regError = None
        
    #===========================================================================
    def cancel(self):
        self.__cancel = True
        
    #===========================================================================
    def run(self):
        # If we are going to wait for an update later in the PM, dont use
        # the init registration
        try:
            if self.__waitUpdate:
                #LOG("Uninit registration")
                self.__paramManager.tmPro.registerTM( self.__parameter )
            else:
                # Otherwise, register the parameter and obtain the initial value
                #LOG("Init registration")
                initValueStruct = self.__paramManager.tmPro.registerTMinit( self.__parameter )
                # Extract the key and the IBASE value from the struct
                key = initValueStruct.m_key
                value = initValueStruct.m_initValue
                # Extract the validity from the IBASE default value            
                validity = True
                if value.m_defaultValue.m_validity != 0:
                    validity = False
    
                # Update the parameter in the parameter manager (PM)
                if not self.__cancel:
                    self.__paramManager._setInitialParameterValue( key, self.__parameter, 
                                                      value, validity )
        except HiflyException,ex:
            self.regError = ex
            return
                        
        #LOG("Registration done")
        return

###############################################################################
        
        
