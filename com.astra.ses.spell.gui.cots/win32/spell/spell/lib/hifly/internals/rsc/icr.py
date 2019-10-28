###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.resources 
FILE
    resources.py
    
DESCRIPTION
    Resource management adapter interface f
    
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
from spell.lib.exception import DriverException
from spell.utils.log import *
from spell.lang.constants import *
from spell.lang.modifiers import *

from spell.lib.hifly.interface import ICR

###############################################################################

LINK_OK = 0
UNKNOWN_ERROR = 1
UNKNOWN_NAME = 2
ALLOCATE_ERROR = 3
COMM_ERROR = 4
DISABLE_ERROR = 7
ENABLE_ERROR = 8
CHANNEL_ERROR = 9
PROTOCOL_ERROR = 10

###############################################################################
class IcrManager(object):
    
    """
    DESCRIPTION:
        Resource management library interface. This class is in charge of
        managing the underlying system resources.
    """
    
    __icrManager = None
    
    
    #==========================================================================
    def __init__(self):
        LOG("Created")
    
    #==========================================================================
    def setup(self):
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

        serviceName = ICR.Mngr.ServiceName
        serviceClass = ICR.Mngr
        LOG("Getting resource manager")
        self.__icrManager = CONN.getService( serviceName, serviceClass )
       
        if self.__icrManager is None:
            raise HiflyException("Unable to obtain resource management service.")
        
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
        LOG("Releasing resource manager")            
        if self.__icrManager:
            CONN.releaseObject(self.__icrManager)

        
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
        if self.__icrManager:
            
            try:
                if enable:
                    try:
                        protocol = config.get(Protocol)
                        channel = config.get(Channel)
                    except:
                        raise HiflyException("Bad ICR arguments")
                    
                    self.__icrManager.enable( name, False, protocol, channel )
                else:
                    self.__icrManager.disable( name )
            except Exception,e:
                raise HiflyException(repr(e))

            return True
        else:
            return False
        
