################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.task
FILE
    task.py
    
DESCRIPTION
    Task management interface
    
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
from spell.lib.registry import REGISTRY 
from spell.config.reader import *

#*******************************************************************************
# Local Imports
#*******************************************************************************
from config import Configurable
from interface import Interface
#*******************************************************************************
# System Imports
#*******************************************************************************

###############################################################################
# Module import definition

__all__ = ['TaskInterface']

INTERFACE_DEFAULTS = { OnFailure:ABORT | SKIP | REPEAT }

###############################################################################
class TaskInterface(Configurable,Interface):
    
    """
    DESCRIPTION:
        Task management library interface. This class is in charge of
        managing the underlying system processes, if any.
    """
    __ctxName = None
    
    #==========================================================================
    def __init__(self):
        Interface.__init__(self, "TASK")
        Configurable.__init__(self)
        self.__ctxName = None
        LOG("Created")
    
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
        LOG("Setup TASK adapter interface")
        self.__ctxName = contextName
        self.refreshConfig()
    
    #==========================================================================
    def cleanup(self):
        LOG("Cleanup TASK adapter interface")

    #==========================================================================
    def openDisplay(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)
        displayName  = args[0]
         
        return self._openDisplay( displayName, useConfig )

    #==========================================================================
    def printDisplay(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)
        displayName  = args[0]
         
        return self._printDisplay( displayName, useConfig )

    #==========================================================================
    def closeDisplay(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)
        displayName  = args[0]
         
        return self._closeDisplay( displayName, useConfig )
        
    #==========================================================================
    def startTask(self, *args, **kargs):
        if len(args)<2:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)
        
        # Reconfigure the host if needed
        if not useConfig.has_key(Host):
             useConfig[Host]=REGISTRY['EXEC'].getControllingHost()
        
        taskName  = args[0]
        if len(args)==1:
            arguments = ""
        else:
            arguments = args[1]
         
        return self._startTask( taskName, arguments, useConfig )
        
    #==========================================================================
    def stopTask(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        taskName = args[0]
         
        return self._stopTask( taskName, useConfig )

    #==========================================================================
    def checkTask(self, *args, **kargs):
        if len(args)<1:
            raise SyntaxException("Wrong arguments")
        
        useConfig = self.buildConfig(args, kargs, self.getConfig(), INTERFACE_DEFAULTS)

        taskName = args[0]
         
        return self._checkTask( taskName, useConfig )

    #==========================================================================
    def _startTask(self, taskName, arguments, config = {} ):
        raise NotImplemented
        
    #==========================================================================
    def _stopTask(self, taskName, config = {} ):
        raise NotImplemented

    #==========================================================================
    def _checkTask(self, taskName, config = {} ):
        raise NotImplemented

    #==========================================================================
    def _openDisplay(self, displayName, config = {} ):
        raise NotImplemented

    #==========================================================================
    def _printDisplay(self, displayName, config = {} ):
        raise NotImplemented
        
    #==========================================================================
    def _closeDisplay(self, displayName, config = {} ):
        raise NotImplemented
