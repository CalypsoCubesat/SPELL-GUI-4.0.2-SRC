###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.config 
FILE
    config.py
    
DESCRIPTION
    Setup environment for correct core driver instantiation
    
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
from spell.lib.exception import SyntaxException

#*******************************************************************************
# Local Imports
#*******************************************************************************

#*******************************************************************************
# System Imports
#*******************************************************************************


###############################################################################
# Module import definition

__all__ = ['ConfigInterface,Configurable']

INTERFACE_DEFAULTS = {}

NO_CONFIG = [ 'command', 'commands', 'sequence', 'args', 'verify', 'config' ]

###############################################################################
class Configurable(object):
    
    _config = {}
    
    #==========================================================================
    def __init__(self):
        self._config = {}
    
    #==========================================================================
    def setConfig(self, source ):
        if isinstance(source,Configurable):
            self._config = source.getConfig()
        elif type(source)==dict:
            if self._config != source:
                self._config.update(source)
        else:
            raise BaseException("Cannot set configuration from " + repr(source))
            
    #==========================================================================
    def getConfig(self, key = None):
        if key is not None:
            if self._config.has_key(key):
                return self._config.get(key)
            return None
        return self._config

    #==========================================================================
    def addConfig(self, key, value):
        self._config[key] = value

    #==========================================================================
    def delConfig(self, key):
        if self._config.has_key(key):
            del self._config[key]
    
    #==========================================================================
    def buildConfig(self, args, kargs, secondary = {}, defaults = {} ):
        useConfig = {}
        # Parameters coming from defaults
        useConfig.update(defaults)
        # Parameters coming from a secondary source (interfaces)
        useConfig.update(secondary)
        # Parameters coming from this same entity
        useConfig.update(self._config)
        # Parameters coming from user arguments
        
        # Then update the dict with the dictionary type arguments only
        if len(args)>0:
            for arg in args:
                if type(arg)==dict:
                    useConfig.update(arg)
        
        # Parse named arguments, if any
        if len(kargs)>0 and kargs.has_key('config'):
            # Then update the dict with the contents of 'config'
            useConfig.update(kargs.get('config'))
            kargs.pop('config')
        
        # Update the dict with remaining kargs
        for key in kargs.keys():
            if not key in NO_CONFIG:
                useConfig[key] = kargs.get(key)
                
        return useConfig

    #==========================================================================
    def checkConfig(self, globals, locals):
        for key in self._config:
            try:
                object = eval(key, globals, locals)
            except:
                raise SyntaxException("Unknown modifier: " + repr(key))
            if type(object)!=str:
                raise SyntaxException("Not a modifier: " + repr(key))
        
###############################################################################
class ConfigInterface(Configurable):
    """
    DESCRIPTION:
        Base class for driver configuration classes. Child classes shall
        implement the setup() and cleanup() methods. The former is used
        for preparing all objects needed by the driver to work, and the 
        latter is used for cleaning up these objects.
    """
    #==========================================================================
    def __init__(self):
        LOG("Created")
    
    #==========================================================================
    def setup(self, contextName):
        LOG("Setup EV adapter interface")
        # TODO: read from config
        self.setConfig( INTERFACE_DEFAULTS )

    #==========================================================================
    def cleanup(self, shutdown = False):
        LOG("Cleanup EV adapter interface")
        
    