###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.tc_provision 
FILE
    tc_provision.py
    
DESCRIPTION
    hifly services for telecommand provision (low level interface)
    
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
from spell.lib.hifly.tc import *
from spell.lib.hifly.interface import ITC_PRO__POA 
from spell.lib.hifly.internals.timeacc import TimeAccess

###############################################################################
class TcProvisionView( ITC_PRO__POA.CommandMngrView ):
    
    """
    Required for telecommand subscriptions
    """
    
    #==========================================================================
    def notifyCommands(self, notifyData):
        """
        Called when a new telecommand entry is read
        """
        LOG("Command notification")

    #==========================================================================
    def ping(self):
        pass

###############################################################################
class TcProvision( TimeAccess ):

    """
    DESCRIPTION:
        This class provides access to the TC provision low level interface
    """

    __tcServerManager = None
    __tcServer = None
    __tcManager = None
    __viewKey = None
    __cmdView = None
    
    #==========================================================================
    def __init__(self):
        
        LOG("Created")
        self.__tcServerManager = None
        self.__tcServer = None
        self.__tcManager = None
        self.__viewKey = None
        self.__cmdView = None

    #==========================================================================
    def setup(self):
        
        """
        Setup the telecommand provision interface
        """
        
        # Telecommand provision manager parameters
        serviceName = ITC_PRO.TCserverMngr.ServiceName
        serviceClass = ITC_PRO.TCserverMngr
        
        # Obtain the service manager
        LOG("Obtaining TC provision service")
        self.__tcServerManager = CONN.getService( serviceName, serviceClass )
        
        if self.__tcServerManager is None:
            raise HiflyException("Could not obtain TC provision service")
        
        # Obtain the provision server
        LOG("Obtaining TC provision server")
        try:
            self.__tcServer = self.__tcServerManager.getTCserver(False)
        except Exception,e:
            raise HiflyException("TC provision server not available: ", e)

        # Obtain a telecommand manager
        LOG("Obtaining command manager")
        try:
            self.__tcManager = self.__tcServer._get_m_commandMngr()
        except Exception,e:
            raise HiflyException("Command manager not available: ", e)
        
        # Create the telecommand view
        LOG("Creating command view")
        self.__cmdView = TcProvisionView()
        
        # Register the view
        LOG("Registering TC view")
        # Create the command filter
        commandFilter = self.__createCommandFilter()
        # Create a packet filter discarding TC raw data
        packetFilter = self.__createTransmissionFilter()
        self.__viewKey = self.__tcManager.registerCommands( self.__cmdView._this(), 10, 
                                                        commandFilter, packetFilter )
        LOG("View registered with key " + repr(self.__viewKey))
        
        LOG("Obtaining time access")
        self.setupTimeAccess()
        
    #==========================================================================
    def cleanup(self):
        
        """
        Perform cleanup operations by releasing objects in proper order
        """
        
        LOG("Releasing time access")            
        self.cleanTimeAccess()

        if self.__cmdView:            
            LOG("Releasing events view")
            CONN.releaseObject(self.__cmdView)
        
        if self.__tcManager: 
            self.__tcManager.unregisterCommands(self.__viewKey)
            LOG("Releasing command manager")
            CONN.releaseObject(self.__tcManager)

        if self.__tcServer:
            LOG("Releasing TC server")
            CONN.releaseObject(self.__tcServer) 

        if self.__tcServerManager:
            LOG("Releasing TC service manager")
            CONN.releaseObject(self.__tcServerManager)
        
    #==========================================================================
    def __createCommandFilter(self):
        
        """
        Create a filter for all telecommands and sources
        """
        commandFilter = ITC.CommandFilter(
                True, # In release time order      
                False, # Enable verify details
                False, # Enable parameters
                False, # Enable raw data
                "", # Name (Regular expression)
                "", # Source name (Regular expression)
                SOURCE_ALL, # Source type
                "", # Subsystem
                "", # Sequence name 
                []) # Verify details, only relevant if enableVerifyDetails
        return commandFilter

    #==========================================================================
    def __createTransmissionFilter(self):
        
        """
        Create a packet filter discarding header/packet raw data
        """
        packetFilter = ITC.TransmissionFilter(True, False, False, False)
        return packetFilter
        
    #==========================================================================
    def registerForCommand(self):
        
        """
        To be done
        """
        if self.__viewKey is None:
            raise HiflyException("TC provision not available")
        
    #==========================================================================
    def getNextData(self):
        
        """
        Get next TC data during retrieval
        """
        commands = self.__tcManager.getNextData(self.__viewKey)
        self.__cmdView.notifyCommands(commands)
        
    #==========================================================================
    def getServiceServer(self):
        
        """
        Required by the time management interface
        """
        return self.__tcServer

    #==========================================================================
    def getServiceView(self):
        """
        Required by the time management interface
        """
        return self.__cmdView._this()

        