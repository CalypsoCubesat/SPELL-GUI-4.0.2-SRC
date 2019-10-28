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
from internals.rsc.misc import MISCservice

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
        self.miscMgr = MISCservice()
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
        LOG("Initializing hifly RSC interface")
        superClass.setup(self,ctxName)
        serviceFail = ""
        try:
            self.icrMgr.setup()
        except BaseException,ex:
            raise DriverException("RSC internal service setup failed", repr(ex))
        try:
            self.miscMgr.setup()
        except BaseException,ex:
            raise DriverException("MISC internal service setup failed", repr(ex))
            

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
            self.miscMgr.cleanup()
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
            
            id = self.miscMgr.getVariable(res)
            if name == id:
                status = self.miscMgr.getVariable(name_status[resIndex])
                break
            
            resIndex = resIndex + 1
                
        if not status:
            raise DriverException("No such resource id: " + name)
        
        if status == "UP":
            return True
        else:
            return False
            
        
    #==========================================================================
    def setResource(self, name, value):
        return self.miscMgr.setVariable(name,value)

    #==========================================================================
    def getResource(self, name):
        return self.miscMgr.getVariable(name)

    #==========================================================================
    def registerResourceMonitor(self, clientStub):
        self.miscMgr.register(clientStub)
        
    #==========================================================================
    def unregisterResourceMonitor(self, clientStub):
        self.miscMgr.unregister(clientStub)

###############################################################################
# Interface handle
RSC = ResourceInterface()
        
        