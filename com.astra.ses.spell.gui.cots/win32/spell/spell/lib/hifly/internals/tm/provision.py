###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tm.provision 
FILE
    provision.py
    
DESCRIPTION
    hifly services for telemetry provision (low level interface)
    
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
import spell.lib.hifly.interface.IBASE
from spell.lib.hifly.interface import ITM_PRO__POA,ITM_PRO,ITM,IMIB
from spell.lib.hifly.internals.timeacc import TimeAccess

###############################################################################
class BaseParameterView( ITM_PRO__POA.ParameterView ):
    
    """
    Required for tm parameter subscriptions
    """
    
    #==========================================================================
    def __init__(self):
        self.parameters = {}
    
    #==========================================================================
    def addParamName(self, paramKey, paramName):
        """
        Add a parameter name to the list of viewed parameters
        """
        self.parameters[paramKey] = paramName

    #==========================================================================
    def delParamName(self, paramKey):
        """
        Delete a parameter from the list of viewed parameters
        """
        del self.parameters[paramKey]
    
    #==========================================================================
    def notifyParameter(self, paramKey, value ):
        """
        Called when one of the viewed parameters is updated
        """
        try:
            theValue = Variant()
            theValue.setI(value.m_defaultValue.m_value)
            theTime = value.m_sampleTime.m_sec
        except Exception,e:
            LOG("Error while parsing param value: " + repr(e))
        
    #==========================================================================
    def notifyOverflow(self):
        """
        Not used
        """
        pass

    #==========================================================================
    def owNotifyOverflow(self):
        """
        Not used
        """
        pass

    #==========================================================================
    def ping(self):
        """
        Not used
        """
        pass

###############################################################################
class TmProvision( TimeAccess ):
    
    """
    Low level interface to the telemetry provision services
    """
    
    __parameters = {}
    __paramKeys = {}
    __paramManager = None
    __tmServer = None
    __tmManager = None
    __paramView = None
    
    #==========================================================================
    def __init__(self):
        LOG("Created")
        self.__parameters = {}
        self.__paramKeys = {}
        self.__paramManager = None
        self.__tmServer = None
        self.__tmManager = None
        self.__paramView = None

    #==========================================================================
    def setup(self):

        LOG("Creating parameter view")
        self.__paramView = BaseParameterView()
        
        serviceName = ITM_PRO.TMserverMngr.ServiceName
        serviceClass = ITM_PRO.TMserverMngr
        LOG("Getting TM service manager")
        self.__tmManager = CONN.getService( serviceName, serviceClass )
       
        if self.__tmManager is None:
            raise HiflyException("TM interface setup failed", "Unable to obtain TM provision service.")
        
        LOG("Getting dedicated TM server")
        self.__tmServer = self.__tmManager.getTMserver(False)
        
        if self.__tmServer is None:
            raise HiflyException("TM interface setup failed", "Unable to obtain TM provision server")
        
        LOG("Getting parameter manager")
        self.__paramManager = self.__tmServer._get_m_parameterMngr()
        
        if self.__paramManager is None:
            raise HiflyException("TM interface setup failed", "Unable to obtain parameter manager")
        
        LOG("Obtaining time access")
        self.setupTimeAccess()

    #==========================================================================
    def cleanup(self):

        for p in self.__parameters.keys():
            LOG("Releasing parameter " + p)
            param = self.__parameters.get(p)
            CONN.releaseObject(param)

        LOG("Releasing time access")            
        self.cleanTimeAccess()

        LOG("Releasing parameter view")            
        if self.__paramView:
            self.__paramView._this()._release()
        
        if self.__paramManager: 
            LOG("Releasing parameter manager")
            CONN.releaseObject(self.__paramManager)

        if self.__tmServer:
            LOG("Releasing TM server")
            CONN.releaseObject(self.__tmServer) 

        if self.__tmManager:
            LOG("Releasing TM manager")
            CONN.releaseObject(self.__tmManager)
            
    #==========================================================================
    def setParameterView(self, view):
        LOG("Overriding parameter view")
        self.__paramView = view
            
    #==========================================================================
    def getParamName(self, key):
        for param in self.__paramKeys.keys():
            if self.__paramKeys[param] == key:
                return param
        return "Unknown"

    #==========================================================================
    def getParamKey(self, name):
        return self.__paramKeys[name]        

    #==========================================================================
    def getParamValues(self, name):
        if not name in self.__parameters:
            return None
        allValues = None
        try:
            # In current EXIF version, the view key is ignored
            allValues = self.__parameters[name].getFullData(0)         
        except Exception,e:
            LOG("Failed to retrieve parameter " + repr(name) + " value (DIRECT): " + repr(e))
            raise HiflyException("Unable to obtain parameter " + repr(name) + " LRV", str(e))
        return allValues

    #==========================================================================
    def registerTM(self, paramName):
        
        if self.__paramManager is None:
            raise HiflyException("Failed to register parameter", "TM provision service not available")
        
        onChange = IMIB.PARAM_RAW_VALUE
        onUpdate = True
        onlyOnce = False
        try:
            LOG("Obtaining parameter model for " + paramName)
            param = self.__paramManager.getParameter(paramName, self.__paramView._this())
            LOG("Registering parameter " + paramName)
            paramKey = param.registerParam( self.__paramView._this(), 300, onUpdate, onChange, onlyOnce )
            LOG("Parameter " + paramName + " registered with key " + repr(paramKey))
            self.__paramView.addParamName( paramKey, paramName)
            self.__parameters[paramName] = param
            self.__paramKeys[paramName] = paramKey
        except spell.lib.hifly.interface.IBASE.NotFound, nof:
            LOG("Failed to register parameter, not found: '" + paramName + "'", LOG_ERROR )
            raise HiflyException("Failed to register parameter", "Parameter '" + paramName + "' not found")
        except Exception,e:
            LOG("Failed to register parameter, error: " + str(e), LOG_ERROR )
            raise HiflyException("Failed to register parameter", str(e))
        #LOG("Parameter " + paramName + " registered")

    #==========================================================================
    def registerTMinit(self, paramName):
        
        if self.__paramManager is None:
            raise HiflyException("Failed to register parameter (I)", "TM provision service not available")
        
        onChange = IMIB.PARAM_RAW_VALUE
        onUpdate = True
        onlyOnce = False
        initValue = None
        initValidity = False
        try:
            LOG("Obtaining parameter " + paramName)
            param = self.__paramManager.getParameter(paramName, self.__paramView._this())
            LOG("Registering parameter (I) " + paramName)
            initValueStruct = param.registerParamInit( self.__paramView._this(), 10, onUpdate, onChange, onlyOnce )

            initValue = initValueStruct.m_initValue
            # Extract the validity from the IBASE default value            
            if initValue.m_defaultValue.m_validity != 0:
                initValidity = False
            else:
                initValidity = True
            
            LOG("Parameter " + paramName + " registered/initialized with key " + repr(initValueStruct.m_key))
            self.__paramView.addParamName( initValueStruct.m_key, paramName)
            self.__parameters[paramName] = param
            self.__paramKeys[paramName] = initValueStruct.m_key
        except spell.lib.hifly.interface.IBASE.NotFound, nof:
            LOG("Failed to register parameter, not found (I): '" + paramName + "'", LOG_ERROR )
            raise HiflyException("Failed to register parameter (I)", "Parameter '" + paramName + "' not found")
        except Exception,e:
            LOG("Failed to register parameter (I), error: " + str(e), LOG_ERROR )
            raise HiflyException("Failed to register parameter (I)", ". Unknown error: " + str(e))
        return [initValue,initValidity]

    #==========================================================================
    def unregisterTM(self, paramName):

        LOG("Unregistering " + paramName + " from TM chain")

        if self.__paramManager is None:
            raise HiflyException("Failed to unregister parameter", "TM provision service not available")

        key = self.__paramKeys.get(paramName)
        if key is None:
            raise HiflyException("Failed to unregister parameter", "Parameter " + paramName + " not found")
        else:
            param = self.__parameters.get(paramName)
            param.unregisterView(key)
            del self.__parameters[paramName]
            del self.__paramKeys[paramName]
            self.__paramView.delParamName(key)
            LOG("Parameter unregistered from view")

    #==========================================================================
    def getServiceServer(self):
        return self.__tmServer

    #==========================================================================
    def getServiceView(self):
        return self.__paramView._this()

    #==========================================================================
    def modifyNumericOOL(self, parameter, appCrit, loRed, loYellow, hiYellow, hiRed ):
        try:
            paramObj = self.__parameters.get(parameter)
            if (loRed != "<nodef>") and (hiRed != "<nodef>"):
                paramObj.modifyOOLvalues( str(loRed), str(hiRed), appCrit, True)
            if (loYellow != "<nodef>") and (hiYellow != "<nodef>"):
                paramObj.modifyOOLvalues( str(loYellow), str(hiYellow), appCrit, False)
        except ITM.requestNotMatched:
            return False
        except Exception,ex:
            raise HiflyException("Failed to modify analog OOL definition for " + parameter, str(ex))
        return True

    #==========================================================================
    def modifyStateOOL(self, parameter, appCrit, expectedStatus ):
        try:
            paramObj = self.__parameters.get(parameter)
            paramObj.modifyOOLvalues( expectedStatus, "", appCrit, True)
        except ITM.requestNotMatched:
            return False
        except Exception,ex:
            raise HiflyException("Failed to modify status OOL definition for " + parameter, str(ex))
        return True
        
    #==========================================================================
    def getAppCriteria(self, paramName ):
        ## WARNING this is a temporary patch until further hifly delivery
        class appCrit:
            m_name = 'TrueCrit'
            m_enabled = True
        ac = appCrit()
        return [ ac ]
        ## WARNING this is a temporary patch until further hifly delivery
        list = None
        try:
            list = self.__paramManager.getAppCriteria( paramName )
        except Exception,ex:
            raise HiflyException("Failed to get applicability criteria for " + paramName, str(ex))
        return list

    #==========================================================================
    def getCurrentLimits(self, paramName ):
        limits = []
        try:
            paramObj = self.__parameters.get(paramName)
            if (paramObj is None):
                self.registerTMinit(paramName)
                paramObj = self.__parameters.get(paramName)
            low = paramObj.getActualLowLimit()
            high = paramObj.getActualHighLimit()
            lowValue = Variant()
            lowValue.setI( low )
            highValue = Variant()
            highValue.setI( high )
            #TODO: this could not be consistent, but we lack of a better
            # interface in EXIF TM right now...
            limits.append( lowValue.get() )
            limits.append( lowValue.get() )
            limits.append( highValue.get() )
            limits.append( highValue.get() )
        except Exception,ex:
            raise HiflyException("Failed to get current OOL for " + paramName, str(ex))
        return limits
