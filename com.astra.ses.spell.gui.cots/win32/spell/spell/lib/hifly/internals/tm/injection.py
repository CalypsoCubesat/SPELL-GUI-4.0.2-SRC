###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tm.injection 
FILE
    injection.py
    
DESCRIPTION
    hifly services for telemetry injection (low level interface)
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################


from spell.lib.hifly.internals.connection import CONN
from spell.lib.hifly.internals.exception import HiflyException
from spell.utils.log import *
from spell.lib.hifly.tm import *
from spell.lib.hifly.internals.value import Variant
from spell.lib.adapter.value import *
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.hifly.interface import ITM,ITM_INJ,ITM_INJ__POA
from spell.lib.hifly.interface import IBASE

###############################################################################
class TmInjection(object):
    
    """
    Low level interface to the telemetry injection services
    """
    
    __tmInjector = None
    
    #==========================================================================
    def __init__(self):
        LOG("Created")        
        self.__tmInjector = None

    #==========================================================================
    def setup(self):

        serviceName = ITM_INJ.ParamInjectMngr.ServiceName
        serviceClass = ITM_INJ.ParamInjectMngr
        LOG("Getting TM injection service")
        self.__tmInjector = CONN.getService( serviceName, serviceClass )
       
        if self.__tmInjector is None:
            raise HiflyException("Unable to obtain TM injection service.")

    #==========================================================================
    def cleanup(self):

        if self.__tmInjector:
            LOG("Releasing TM injector")
            CONN.releaseObject(self.__tmInjector)

    #==========================================================================
    def injectTM(self, parameter, value, isEng = True ):
        
        if self.__tmInjector is None:
            raise HiflyException("TM injection service not available")

        LOG("Injecting parameter " + str(parameter) + " with value " + str(value))

        params = []
        theValue = Variant()
        theValue.setT(value)
        theParameter = ITM.InjectParam( parameter, isEng, theValue.getI() )
        params.append( theParameter )
        
        LOG("Injecting now")
        
        try:
            self.__tmInjector.injectParametersWithDefaults( params, "SPELL" )
        except IBASE.NotFound,nf:
            raise HiflyException("Unable to inject, parameter not found", "Not found")
        except IBASE.NotProcessed,np:
            raise HiflyException("Unable to inject, not processed", np.m_reason)
		
