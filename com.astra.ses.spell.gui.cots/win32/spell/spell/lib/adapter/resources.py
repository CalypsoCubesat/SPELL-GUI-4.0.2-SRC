################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.resources
FILE
    resources.py
    
DESCRIPTION
    Resource management interface
    
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
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.config.reader import Config

#*******************************************************************************
# Local Imports
#*******************************************************************************
from config import Configurable
from interface import Interface

#*******************************************************************************
# System Imports
#*******************************************************************************
import threading,thread,time

###############################################################################
# Module import definition

__all__ = ['ResourceInterface']

INTERFACE_DEFAULTS = { OnFailure:ABORT | SKIP | REPEAT }

###############################################################################
class ResourceInterface(Configurable,Interface):
    
    """
    DESCRIPTION:
        Resource management library interface. This class is in charge of
        managing the underlying system resources.
    """
    
    # List of resources to check
    toCheck = []
    # Status of each resource (OK/NOK)
    rscStatus = {}
    # Callbacks for resource monitoring
    rscCallbacks = []
    __ctxName = None
    
    #==========================================================================
    def __init__(self):
        Interface.__init__(self, "RSC")
        Configurable.__init__(self)
        LOG("Created")
        self.toCheck = [ 'TM', 'TC' ]
        self.rscStatus = {}
        self.rscCallbacks = []
        self.__ctxName = None
    
    #===========================================================================
    def refreshConfig(self):
        ctxConfig = Config.instance().getContextConfig( self.__ctxName )
        languageDefaults = ctxConfig.getInterfaceConfig(self.getInterfaceName())
        if languageDefaults:
            INTERFACE_DEFAULTS.update(languageDefaults)
        self.setConfig( INTERFACE_DEFAULTS )
        LOG("Configuration loaded", level = LOG_CNFG )
    
    #==========================================================================
    def setup(self, contextName):
        LOG("Setup RSC adapter interface")
        self.__ctxName = contextName

    #==========================================================================
    def cleanup(self):
        LOG("Cleanup RSC adapter interface")
        
    #==========================================================================
    def setLink(self, *args, **kargs):
        if len(args)<2:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        linkName = args[0]
        enable = args[1]
         
        return self._setLink( linkName, enable, useConfig )

    #==========================================================================
    def _setLink(self, linkName, enable, config = {} ):
        raise NotImplemented
        
    #==========================================================================
    def checkLink(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        linkName = args[0]
         
        return self._checkLink( linkName, useConfig )

    #==========================================================================
    def _setLink(self, linkName, config = {} ):
        raise NotImplemented

    #==========================================================================
    def setResource(self, *args, **kargs):
        if len(args)<2:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        resourceName = args[0]
        resourceValue = args[1]
         
        return self._setResource( resourceName, resourceValue, useConfig )

    #==========================================================================
    def _setResource(self, resourceName, resourceValue, config = {} ):
        raise NotImplemented
    
    #==========================================================================
    def getResource(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        resourceName = args[0]
         
        return self._getResource( resourceName, useConfig )

    #==========================================================================
    def _getResource(self, resourceName, config = {} ):
        raise NotImplemented

    #==========================================================================
    def getResourceStatus(self, *args, **kargs ):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)
        resource = args[0]
        return self._getResourceStatus( resource, useConfig )
        
    #==========================================================================
    def isResourceOK(self, *args, **kargs ):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)
        resource = args[0]
        return self._isResourceOK( resource, useConfig )

    #==========================================================================
    def addResourceStatusCallback(self, callbackClass ):
        LOG("Add resource monitor: " + repr(callbackClass))
        self.rscCallbacks.append(callbackClass)        

    #==========================================================================
    def _getResourceStatus(self, resource, config = {} ):
        raise NotImplemented

    #==========================================================================
    def _isResourceOK(self, resource, config = {} ):
        raise NotImplemented

    #==========================================================================
    def updateStatus(self, resource, status):
        LOG("Resource status change: " + repr(resource) + ":" + repr(status))
        self.rscStatus[resource] = status
        if len(self.rscCallbacks)>0:
            for cbk in self.rscCallbacks:
                cbk.notifyUpdate(resource,status)
    
    