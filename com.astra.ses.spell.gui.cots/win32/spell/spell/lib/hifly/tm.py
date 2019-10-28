################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.tm 
FILE
    tm.py
    
DESCRIPTION
    hifly services for telemetry management (low level interface)
    
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
import spell.lib.adapter.tm
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.registry import REGISTRY
from spell.lib.exception import *
from spell.utils.log import *
from spell.config.reader import Config
from spell.config.constants import COMMON
from spell.lib.adapter.tm_item import TmItemClass

#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.timeacc import *
from internals.tm.provision import TmProvision
from internals.tm.injection import TmInjection
from internals.tm.provision import BaseParameterView
from internals.value import Variant 
from internals.param import ParameterManagerClass
from internals.exception import *
from modifiers import *
from constants import *
from internals.exif import EXIF
#*******************************************************************************
# System imports
#*******************************************************************************
from time import sleep
import os

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TM']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.tm.TmInterface

###############################################################################
class TmInterface( superClass ):
    """
    Concrete implementation of the core tm_class for hifly driver
    """
    
    verificationFailure = []
    tmPro = None
    tmInj = None
    paramManager = None
    __ctxName = None
   
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created hifly TM interface")
        self.verificationFailure = []
        self.tmPro = TmProvision()
        self.tmInj = TmInjection()
        self.paramManager = ParameterManagerClass(self.tmPro)
        self.__ctxName = None

    #==========================================================================
    def setup(self, ctxName):
        """
        DESCRIPTION:
            Setup the hifly low level interface 
        """
        try:
            self.__ctxName = ctxName
            superClass.setup(self, ctxName)
            self.connect()
        except HiflyException,ex:
            raise DriverException("Unable to load TM interface: " + ex.message, ex.reason)
        except Exception,ex:
            raise DriverException("Unable to load TM interface", repr(ex))

    #==========================================================================
    def connect(self, reconnect = False):
        if (reconnect):
            self.disconnect()
        LOG("Initializing TM provision interface")
        self.tmPro.setup()
        LOG("Initializing TM injection interface")
        self.tmInj.setup()
        LOG("Initializing parameter manager")
        self.paramManager.setup(self.__ctxName)

    #==========================================================================
    def disconnect(self):
        LOG("Cleaning up parameter manager")
        self.paramManager.cleanup()
        LOG("Cleaning up TM provision interface")
        self.tmPro.cleanup()
        LOG("Cleaning up TM injection interface")
        self.tmInj.cleanup()

    #==========================================================================
    def cleanup(self):
        """
        DESCRIPTION:
            Cleanup the hifly low level interface
        """
        superClass.cleanup(self)
        self.disconnect()

    #==========================================================================
    @EXIF
    def _injectItem(self, param, value, config = {} ):
        try:
            isEng = (config.get(ValueFormat) == ENG)
            if isinstance(param,TmItemClass):
                param = param.name()
            LOG("Injecting tm item: " + param + ", value= " + repr(value))
            self.tmInj.injectTM( param, value, isEng )
        except HiflyException,e:
            raise DriverException("Could not inject parameter " + repr(param) + ": " + e.message,e.reason)
        return True
    
    #==========================================================================
    @EXIF
    def _refreshItem(self, param, config = {} ):

        name = param.name()
        timeout = config.get(Timeout)
        waitUpdate = config.get(Wait)
        isEng = (config.get(ValueFormat) == ENG)
        if config.has_key(OneShot) and config.get(OneShot)==True:
            oneShot = True
        else:
            oneShot = False
        
        LOG("Refreshing tm item: " + name + ", wait = " + repr(waitUpdate) + ", one shot=" + repr(oneShot))
        try:
            engValue,rawValue,validity = self.paramManager.getParameterValue( name, waitUpdate, timeout, oneShot )
            param._setEng(engValue)
            param._setRaw(rawValue)
            param._setStatus(validity)
            LOG("Refresh done")

            if isEng: return [engValue,validity]
            return [rawValue,validity]
        except HiflyException,e:
            LOG("Error in refresh: " + str(e), LOG_ERROR )
            param._setEng(0)
            param._setRaw(0)
            param._setStatus(False)
            raise DriverException("Unable to obtain TM parameter value: " + e.message, e.reason)

    #===========================================================================
    def _setLimit(self, param, limit, value, config ):
        
        currentLimits = self._getLimits( param, config )
        
        changed = False
        if (limit == LoRed):
            changed = (currentLimits[0] != value) 
            currentLimits[0] = value
        elif (limit == LoYel): 
            changed = (currentLimits[1] != value) 
            currentLimits[1] = value
        elif (limit == HiYel): 
            changed = (currentLimits[2] != value) 
            currentLimits[2] = value
        elif (limit == HiRed): 
            changed = (currentLimits[3] != value) 
            currentLimits[3] = value
        else:
            raise DriverException("Cannot set limit value", "Unknown limit identifier: " + repr(limit))

        if not changed:
            REGISTRY['CIF'].write("Limit remains unchanged with value " + repr(value)) 
            return True
        
        return self._setLimits(param, currentLimits, config)
        
    @EXIF
    #===========================================================================
    def _getLimit(self, param, limit, config ):
        
        if type(param)!=str: param = param.name()
        
        if not self.paramManager._isParameterRegistered(param):
            LOG("Register parameter for limit management")
            self.paramManager.registerParameterInit(param)
        limits = self.tmPro.getCurrentLimits( param )
        
        if (limit == LoRed): return limits[0]
        if (limit == LoYel): return limits[1]
        if (limit == HiYel): return limits[2]
        if (limit == HiRed): return limits[3]
        raise DriverException("Cannot get limit value", "Unknown limit identifier: " + repr(limit))

    @EXIF
    #===========================================================================
    def _getLimits(self, param, config ):
        if type(param)!=str: param = param.name()
        
        if not self.paramManager._isParameterRegistered(param):
            LOG("Register parameter for limit management")
            self.paramManager.registerParameterInit(param)
        limits = self.tmPro.getCurrentLimits( param )

        return limits

    @EXIF
    #===========================================================================
    def _setLimits(self, param, limits, config ):

        
        if limits.has_key(Expected):
            expectedStatus = limits[Expected]
            loRed = None
            loYel = None
            hiRed = None
            hiYel = None
            analog = False
        else:
            analog = True
            expectedStatus = None
            loRed = "<nodef>"
            loYel = "<nodef>"
            hiRed = "<nodef>"
            hiYel = "<nodef>"
            if LoRed in limits: loRed = limits[LoRed]
            if LoYel in limits: loYel = limits[LoYel]
            if HiYel in limits: hiYel = limits[HiYel]
            if HiRed in limits: hiRed = limits[HiRed]

        if type(param)!=str: param = param.name()
        
        appCriteria = self.tmPro.getAppCriteria( param )
        activeCriteria = []
         
        for crit in appCriteria:
            acName = crit.m_name
            acEnabled = crit.m_enabled
            if acEnabled: activeCriteria.append(acName)
        
        LOG("Active applicability criteria for " + param + ": " + repr(activeCriteria))
        
        if len(activeCriteria) == 0:
            LOG("No applicability criteria enabled. Discarding modification", LOG_WARN)
            return False
        
        result = True
        try:
            if not self.paramManager._isParameterRegistered(param):
                LOG("Register parameter for limit management")
                self.paramManager.registerParameterInit(param)
            for crit in activeCriteria:
                if analog:
                    LOG("Modifying analog limit definition for " + param)
                    result = result and self.tmPro.modifyNumericOOL( param, crit, loRed, loYel, hiYel, hiRed )
                else:
                    LOG("Modifying state limit definition for " + param)
                    result = result and self.tmPro.modifyStateOOL( param, crit, expectedStatus )
        except HiflyException,ex:
            raise DriverException("Unable to apply OOL definition: " + ex.message, ex.reason)   

        if not result:
            REGISTRY['CIF'].write("Unable to modify OOL definition for " + param + " (no definitions found)", {Severity:WARNING} )
                
        return result

    #===========================================================================
    def _operationStart(self):
        superClass._operationStart(self)
        self.paramManager.cleanupOnHold()

    #===========================================================================
    def _operationEnd(self):
        superClass._operationEnd(self)
        self.paramManager.cleanupContinue()

################################################################################
# Interface handle
TM = TmInterface()
