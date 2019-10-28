###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.resources 
FILE
    resources.py
    
DESCRIPTION
    Resource management interface for hifly driver
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.lib.exception import *
from spell.utils.log import *
from spell.lang.constants import *
from spell.lang.modifiers import *
import spell.lib.adapter.resources 

#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.rsc.icr import IcrManager
from internals.exception import HiflyException
from modifiers import *
from constants import *

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = [ 'RSC' ]

#*******************************************************************************
# Module globals
#*******************************************************************************

superClass = spell.lib.adapter.resources.ResourceInterface

###############################################################################
class ResourceInterface ( superClass ):
    
    """
    DESCRIPTION:
        Resource management library interface. This class is in charge of
        managing the underlying system resources.
    """
    
    icrMgr = None
    miscMgr = None
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        self.icrMgr = IcrManager()
        LOG("Created hifly RSC interface")
    
    #==========================================================================
    def setup(self, ctxName):
        """
        DESCRIPTION:
            Setup the task management interface.
            
        ARGUMENTS:
            configuration   Configuration object
            
        RETURNS:
            Nothing.
       
        RAISES:
            NotImplemented since it has to be implemented by drivers.
        """
        try:
            LOG("Initializing hifly RSC interface")
            superClass.setup(self,ctxName)
            serviceFail = ""
            self.icrMgr.setup()
        except HiflyException,ex:
            raise DriverException("Unable to load RSC interface: " + ex.message, ex.reason)
        except Exception,ex:
            raise DriverException("Unable to load RSC interface", repr(ex))

    #==========================================================================
    def cleanup(self):
        """
        DESCRIPTION:
            Cleanup the task management interface.
            
        ARGUMENTS:
            Nothing.
            
        RETURNS:
            Nothing.
       
        RAISES:
            NotImplemented since it has to be implemented by drivers.
        """
        LOG("Cleaning up hifly RSC interface")
        superClass.cleanup(self)
        try:
            self.icrMgr.cleanup()
        except: pass

    #==========================================================================
    def setLink(self, name, enable = True, config = {}):
        """
        DESCRIPTION:
            Set the status of a link
            
        ARGUMENTS:
            enable      If true, enable the link. Otherwise disable it.
            name        Link name
            config      Configuration parameters
                        
        RETURNS:
            True if success
       
        RAISES:
            NotImplemented since it has to be implemented by drivers.
        """
        return self.icrMgr.setLink(name, enable, config)
        
    #==========================================================================
    def checkLink(self, name):
        
        name_resources = [ 'TMP1_RESOURCE_ID', 'TMP2_RESOURCE_ID', 'TC_RESOURCE_ID' ]
        name_status = ['TMP1_LINK_STATUS', 'TMP2_LINK_STATUS', 'TC_LINK_STATUS']

        status = None
        resIndex = 0
        for res in name_resources:
            
            id = self._getResource(res)
            if name == id:
                status = self._getResource(name_status[resIndex])
                break
            
            resIndex = resIndex + 1
                
        if not status:
            raise DriverException("No such resource id: " + name)
        
        if status == "UP":
            return True
        else:
            return False
            
        
    #==========================================================================
    def _setResource(self, resourceName, resourceValue, config = {} ):
        # It is obligued that we use the TM interface for this
        from spell.lib.registry import REGISTRY
        LOG("Setting MISCconfig value for " + repr(resourceName) + ":" + repr(resourceValue))
        return REGISTRY['TM']._injectItem( resourceName, resourceValue )

    #==========================================================================
    def _getResource(self, resourceName, config = {} ):
        # It is obligued that we use the TM interface for this
        from spell.lib.registry import REGISTRY
        LOG("Obtaining MISCconfig value of " + repr(resourceName))
        REGISTRY['TM'].addConfig(OneShot,True)
        resourceItem = REGISTRY['TM'][resourceName]
        REGISTRY['TM'].delConfig(OneShot)
        value = resourceItem.value()
        validity = resourceItem.status()
        if not validity:
            raise DriverException("Resource " + repr(resourceName) + " invalid")
        return value

    #==========================================================================
    def _getResourceStatus(self, resource, config = {} ):
        # Not implemented until we are allowed to access MISC interface
        return False
    
    #==========================================================================
    def _isResourceOK(self, resource, config = {} ):
        # Not implemented until we are allowed to access MISC interface
        return False
        
    #==========================================================================
    def _registerResourceMonitor(self, clientStub):
        # Not used until we are allowed to access MISC interface
        self.miscMgr.register(clientStub)
        
    #==========================================================================
    def _unregisterResourceMonitor(self, clientStub):
        # Not used until we are allowed to access MISC interface
        self.miscMgr.unregister(clientStub)

###############################################################################
# Interface handle
RSC = ResourceInterface()
        
        
