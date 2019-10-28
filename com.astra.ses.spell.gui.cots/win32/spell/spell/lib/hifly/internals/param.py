################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.param 
FILE
    param.py
DESCRIPTION
    Parameter manager implementation for hifly driver
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    25/09/2007
"""

################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.utils.log import *
from spell.config.reader import Config

#*******************************************************************************
# Local imports
#*******************************************************************************
from tm.provision import BaseParameterView
from tm.subscriber import TmSubscriber 
from value import Variant
from exception import HiflyException

#*******************************************************************************
# System imports
#*******************************************************************************
import time, thread, threading, sys

#*******************************************************************************
# Module globals
#*******************************************************************************
MAX_TIME = 60 # seconds

################################################################################
class ParameterData(object):
    
    __name = None
    __value = None
    __validity = False
    __updated = False
    __acqTime = None
    __isUsing = False
    __lock = None
    
    #==========================================================================
    def __init__(self, name):
        self.__name = name
        self.__value = None
        self.__validity = False
        self.__updated = False
        self.__acqTime = time.time()
        self.__isUsing = False
        self.__lock = thread.allocate_lock()

    #==========================================================================
    def setValue(self, value, validity):
        self.__value = value
        self.__validity = validity
        self.__updated = True

    #==========================================================================
    def isUpdated(self):
        return self.__updated

    #==========================================================================
    def updateAcqTime(self):
        self.__acqTime = time.time() 

    #==========================================================================
    def setIsUsing(self, isUsing):
        self.__lock.acquire()
        try:
            self.__isUsing = isUsing
        finally:
            self.__lock.release()

    #==========================================================================
    def isUsing(self):
        self.__lock.acquire()
        try:
            isUsing = self.__isUsing
        finally:
            self.__lock.release()
        return isUsing

    #==========================================================================
    def setUpdated(self, updated):
        self.__updated = updated

    #==========================================================================
    def getValue(self):
        self.__acqTime = time.time()
        #LOG("Acquire value for " + self.__name + " at " + time.ctime(self.__acqTime))
        self.__updated = False
        return self.__value,self.__validity

    #==========================================================================
    def getAcqTime(self):
        if self.__acqTime is None: return 0.0
        return self.__acqTime
        
################################################################################
class UsageMonitor(threading.Thread):
    
    __pmanager = None
    __working = True
    __lock = None
    __timeout = None
    __cleanupLock = None
    
    #==========================================================================
    def __init__(self, pmanager, timeout, cleanupLock ):
        threading.Thread.__init__(self)
        self.__pmanager = pmanager
        self.__working = True
        self.__timeout = timeout
        self.__lock = thread.allocate_lock()
        self.__cleanupLock = cleanupLock

    #==========================================================================
    def __isWorking(self):
        self.__lock.acquire()
        working = self.__working
        self.__lock.release()
        return working

    #==========================================================================
    def stop(self):
        self.__lock.acquire()
        self.__working = False
        self.__lock.release()
        
    #==========================================================================
    def run(self):
        while(self.__isWorking()):
            time.sleep(2)
            # Prevent any cleanup while the TM interface is busy
            self.__cleanupLock.wait()
            currentTime = time.time()
            parameters = self.__pmanager._getParameterNames()
            #LOG("Checking parameter cache (" + str(len(parameters)) + " parameters)")
            #LOG("Current time: " + time.ctime(currentTime))
            removed = 0
            for paramName in parameters:
                parameter = self.__pmanager._getParameter(paramName)
                if parameter:
                    # If the parameter is being used to get its value, leave it
                    if (parameter.isUsing()): continue
                    acqTime = parameter.getAcqTime()
                    # If parameter was not used yet, leave it
                    if (acqTime==0.0): continue
                    diff = (currentTime-acqTime)
                    if diff>self.__timeout:
                        LOG("### Remove " + paramName + " from cache (" + str(diff) + " seconds old")
                        self.__pmanager.unregisterParameter(paramName)
                        removed += 1
            if removed>0:
                LOG("Removed " + str(removed) + " parameters from cache")

################################################################################
class ParameterManagerClass( BaseParameterView ):
    
    __paramData = {}
    viewRegistered = False
    __lock = None
    tmPro = None
    __uMonitor = None
    __cleanupLock = None
    
    #==========================================================================
    def __init__(self, tmProvision ):
        BaseParameterView.__init__(self)
        self.__paramData = {}
        self.viewRegistered = False
        self.__lock = thread.allocate_lock()
        self.tmPro = tmProvision
        self.__cleanupLock = threading.Event()
        LOG("Created hifly parameter manager")
        
    #==========================================================================
    def setup(self, ctxName):
        LOG("Registering on TM provision interface")
        self.tmPro.setParameterView(self)
        self.viewRegistered = True
        ctxInfo = Config.instance().getContextConfig(ctxName)
        driverName = ctxInfo.getDriver()
        driverDetails = Config.instance().getDriverConfig(driverName)
        try:
            timeout = int(driverDetails['TMCacheTimeout'])
            if timeout is None:
                timeout = MAX_TIME
        except:
            timeout = MAX_TIME
        self.__cleanupLock.set()
        self.__uMonitor = UsageMonitor( self, timeout, self.__cleanupLock )
        self.__uMonitor.start()

    #==========================================================================
    def cleanup(self):
        try:
            self.cleanupContinue()
            self.__uMonitor.stop()
            self.__uMonitor.join()
        except: pass
        parameters = self._getParameterNames()
        for parameter in parameters:
            self.unregisterParameter(parameter)

    #==========================================================================
    def cleanupOnHold(self):
        self.__cleanupLock.clear()

    #==========================================================================
    def cleanupContinue(self):
        self.__cleanupLock.set()

    #==========================================================================
    def notifyParameter(self, paramKey, value ):
        
        self.__lock.acquire()
        try:
            parameterName = self.parameters.get(paramKey)
            if parameterName and self.__paramData.has_key(parameterName):
                model = self.__paramData[parameterName]
                validity = True
                if value.m_defaultValue.m_validity != 0:
                    validity = False
                model.setValue(value, validity)
            else:
                sys.stderr.write("!! retrying notification " + repr(parameterName) + "\n")
            
        finally:
            self.__lock.release()

    #==========================================================================
    def _logInfo(self, key, name, value, validity ):
        LOG("---------------------------------------------")
        LOG("Parameter key     : " + repr(key))
        LOG("Parameter name    : " + repr(name))
        v = Variant()
        v.setI(value.m_defaultValue.m_value)
        LOG("Parameter value   : " + repr(v.get()))
        LOG("Parameter validity: " + repr(validity))
        LOG("---------------------------------------------")

    #==========================================================================
    def _getParameterNames(self):
        params = None
        try:
            self.__lock.acquire()
            params = self.__paramData.keys()
        finally:
            self.__lock.release()
        return params

    #==========================================================================
    def _getParameter(self, paramName):
        param = None
        try:
            self.__lock.acquire()
            # May be none
            param = self.__paramData.get(paramName)
        finally:
            self.__lock.release()
        return param

    #==========================================================================
    def _getParameterValue(self, paramName):
        self.__lock.acquire()
        value = None
        validity = False
        try:
            if paramName in self.__paramData:
                value,validity = self.__paramData[paramName].getValue()
        finally:
            self.__lock.release()
        return value,validity

    #==========================================================================
    def _getDirectParameterValue(self, paramName):
        self.__lock.acquire()
        value = None
        validity = False
        try:
            # This goes directly to EXIF
            value = self.tmPro.getParamValues(paramName)
            # Update the cache model as well
            model = self.__paramData[paramName]
            validity = True
            if value.m_defaultValue.m_validity != 0:
                validity = False
            model.setValue(value, validity)
        finally:
            self.__lock.release()
        return value,validity

    #==========================================================================
    def _getParameterValidity(self, paramName):
        self.__lock.acquire()
        validity = None
        try:
            if paramName in self.__paramData:
                value,validity = self.__paramData[paramName].getValue()
        finally:
            self.__lock.release()
        return validity

    #==========================================================================
    def _createParameterModel(self, paramName):
        try:
            self.__lock.acquire()
            #LOG("Creating parameter model: " + paramName)
            self.__paramData[paramName] = ParameterData(paramName)
        finally:
            self.__lock.release()

    #==========================================================================
    def _deleteParameterModel(self, paramName):
        try:
            self.__lock.acquire()
            del self.__paramData[paramName]
        finally:
            self.__lock.release()

    #==========================================================================
    def _isParameterRegistered(self, paramName):
        registered = False
        try:
            self.__lock.acquire()
            registered = self.__paramData.has_key(paramName)
        finally:
            self.__lock.release()
        return registered

    #==========================================================================
    def _setParameterUpdated(self, paramName, updated):
        self.__lock.acquire()
        try:
            if paramName in self.__paramData:
                self.__paramData[paramName].setUpdated(updated)
            else:
                sys.stderr.write("Cannot set updated " + paramName + "\n")
        finally:
            self.__lock.release()

    #==========================================================================
    def _isParameterUpdated(self, paramName):
        self.__lock.acquire()
        updated = False
        try:
            if paramName in self.__paramData:
                updated = self.__paramData[paramName].isUpdated()
            else:
                sys.stderr.write("Cannot check if parameter " + paramName + " is updated\n")
        finally:
            self.__lock.release()
        return updated

    #==========================================================================
    def _setInitialParameterValue(self, key, paramName, value, validity ):
        self.__lock.acquire()
        try:
            self.__paramData[paramName].setValue(value,validity)
            #self._logInfo( key, paramName, value, validity )
        finally:
            self.__lock.release()
        
    #==========================================================================
    def _parameterIsUsing(self, paramName, isUsing):
        model = self.__paramData[paramName]
        model.setIsUsing(isUsing)
        if isUsing: model.updateAcqTime()

    #==========================================================================
    def registerParameter(self, paramName, waitUpdate, timeout ):
        
        """
        Registers a TM parameter. If desired, b__locks until
        an update reaches.
        """
        
        # No need to continue if the model is there already
        if self._isParameterRegistered(paramName): return
        
        #LOG("Registering parameter: " + paramName)
        self._createParameterModel(paramName)
        
        subscriber = TmSubscriber(self,paramName,waitUpdate)
        subscriber.start()
        
        cTime = time.time()
        sTime = cTime
        while not self._isParameterUpdated(paramName):
            if subscriber.regError is not None:
                self._deleteParameterModel(paramName)
                raise HiflyException("Unable to register parameter " + paramName, "Registration error: " + str(subscriber.regError))
            time.sleep(0.05)
            cTime = time.time()
            if (cTime - sTime)>timeout:
                subscriber.cancel()
                oldvr = self.viewRegistered
                self.viewRegistered = True
                self.unregisterParameter(paramName)
                self.viewRegistered = oldvr
                raise HiflyException("Unable to register parameter " + paramName, "Parameter registration timeout")

    #==========================================================================
    def registerParameterInit(self, paramName ):
        
        """
        Registers a TM parameter and initializes it
        """
        value = None
        validity = False
        try:
            self.__lock.acquire()
            
            self.__paramData[paramName] = ParameterData(paramName)
            # Register for the parameter in EXIF and initialize the value
            try:
                value, validity = self.tmPro.registerTMinit(paramName)
            except HiflyException,ex:
                del self.__paramData[paramName]
                raise ex
            # Refresh the model with the current value
            self.__paramData[paramName].setValue(value,validity)
        finally:
            self.__lock.release()
        return [value,validity]

    #==========================================================================
    def getParameterValue(self, paramName, waitUpdate, timeout, oneShot = False ):

        LOG("Obtain parameter value for " + paramName + " wait=" + repr(waitUpdate) + ", timeout=" + repr(timeout) + ", oneshot=" + repr(oneShot))
        
        # If we require the LRV:
        #   1. Obtain the current value directly 
        # If we want the update:
        #   1. Wait for the update in the cache
        #
        # We keep oneShot for backwards compatibility
        # We need to register the parameter in any case so that it gets
        # instantiated into EXIF TM
    
        value = None
        validity = False
        if (not waitUpdate or oneShot):
            #LOG("Obtaining LRV")
            if not self._isParameterRegistered(paramName):
                LOG("Parameter NOT registered, registering and getting value")
                value, validity = self.registerParameterInit(paramName)
            else:
                self._parameterIsUsing(paramName, True)
                # OLD fashion: this wont detect EXIF outages 
                # value, validity = self._getParameterValue(paramName)
                # If it is already registered, ask EXIF directly about the value
                LOG("Parameter already registered, getting direct value")
                value, validity = self._getDirectParameterValue(paramName)
                self._parameterIsUsing(paramName, False)
        else:
            LOG("Obtaining next sample")
            # If there is no parameter value, subscribe parameter
            if not self._isParameterRegistered(paramName):
                LOG("Register and wait")
                # Register for the parameter and wait for the update
                self.registerParameter(paramName, True, timeout)
                # Now get the value, which shall be the one from the update
                #LOG("Registered, now get value")
                value, validity = self._getParameterValue(paramName)
                #LOG("Got value after registration: " + repr(value))
            else:
                self._parameterIsUsing(paramName, True)
                # If the parameter is in cache, wait for update 
                LOG("Waiting update")
                self._setParameterUpdated(paramName, False)
                cTime = time.time()
                sTime = cTime
                while self._isParameterUpdated(paramName) == False:
                    time.sleep(0.01)
                    cTime = time.time()
                    if (cTime - sTime)>timeout:
                        # At this point try to directly access EXIF LRV. If it fails, this is an
                        # EXIF outage.
                        value, validity = self._getDirectParameterValue(paramName)
                        # If the call just above did not fail, this is a value timeout, not an
                        # EXIF outage.
                        raise HiflyException("Unable to acquire parameter value", "Parameter value timeout")
                # Now get the value, which shall be the one from the update
                LOG("Update came in")
                value, validity = self._getParameterValue(paramName)
                self._parameterIsUsing(paramName, False)

            if value is not None:
                # Reset parameter updates            
                self._setParameterUpdated(paramName,False)
            else:
                LOG("Unregistering parameter due to error")
                self.unregisterParameter(paramName)
                raise HiflyException("Could not obtain parameter update", "Internal driver error")       
            
        # Obtain the value in desired format
        vr = Variant()
        vr.setI(value.m_sourceValue.m_value)
        rawValue = vr.get()
        vr.setI(value.m_engValue.m_value)
        engValue = vr.get()
        vr.setI(value.m_defaultValue.m_value)
        defaultValue = vr.get()
            
        # If there is no engineering value defined (we get none)
        # use the raw value
        if engValue is None:
            engValue = rawValue
        
        # ENG and RAW values are None, then use the defaultValue
        # (for hard-coded synthetic parameters)
        if engValue is None:
            rawValue = defaultValue
            engValue = defaultValue

        LOG("Value obtained: " + repr([engValue,rawValue,validity]))
        return [ engValue, rawValue, validity ]
        
    #==========================================================================
    def unregisterParameter(self, paramName):
        """
        Unsubscribes a TM parameter. 
        """
        if not self.viewRegistered: return
        self.__lock.acquire()
        try:
            if paramName in self.__paramData:
                LOG("Unregistering parameter: " + paramName)
                # May raise a HiflyException
                self.tmPro.unregisterTM( paramName )
        except:
            LOG("Error unregistering parameter " + repr(paramName))
        finally:
            del self.__paramData[paramName]
            self.__lock.release()

