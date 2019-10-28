################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.task.taskcontrol 
FILE
    taskcontrol.py
DESCRIPTION
    hifly internal Task management interface
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    21/09/2007
"""

################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.lib.hifly.internals.connection import CONN
from spell.lib.hifly.internals.exception import HiflyException,DriverException
from spell.lib.hifly.interface._GlobalIDL import *
from spell.lib.hifly.interface._GlobalIDL__POA import *
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.hifly.constants import *
from  spell.lib.hifly.modifiers import *
from spell.utils.log import *
from spell.config.reader import Config

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import socket
from time import sleep

###############################################################################
class TaskInterest( TKCOMcorbaGUIinterest ):
    
    """
    Used to monitor application status
    """
    
    #==========================================================================
    def __init__(self, taskManager, domain, family, mnemonic):
        self.taskManager = taskManager
        self.mnemonic = mnemonic
        self.delegate = None
        self.domain = domain
        self.family = family
        self.registered = False

    #==========================================================================
    def register(self):
        
        """
        Register the interest for the configured application
        """
        if self.registered:
            raise HiflyException("Monitor already registered for " + self.mnemonic)
        
        result = self.taskManager.GUIinterestedIn(
                        self.mnemonic,
                        0,
                        self._this(),
                        self.family,
                        self.domain,
                        True)
        
        if not result:
            raise HiflyException("Could not register interest on " + self.mnemonic )
    
    #==========================================================================
    def setDelegate(self, delegate):
        self.delegate = delegate
    
    #==========================================================================
    def getDelegate(self):
        return self.delegate

    #==========================================================================
    def applicationStopped( self, screenNumber ):
        if not self.delegate is None:
            self.delegate.applicationStopped()

    #==========================================================================
    def applicationStarting( self, screenNumber ):
        if not self.delegate is None:
            self.delegate.applicationStarting()

    #==========================================================================
    def applicationStarted( self, screenNumber ):
        if not self.delegate is None:
            self.delegate.applicationStarted()

    #==========================================================================
    def applicationDied( self, screenNumber ):
        if not self.delegate is None:
            self.delegate.applicationDied()

    #==========================================================================
    def applicationUnknown( self, screenNumber ):
        if not self.delegate is None:
            self.delegate.applicationUnknown()

    #==========================================================================
    def alive(self):
        pass

###############################################################################
class DefaultTaskDelegate:

        def __init__(self, appname):
                self.appname = appname

        def applicationStarted(self):
                LOG(self.appname + " started")

        def applicationStarting(self):
                LOG(self.appname + " starting")

        def applicationStopped(self):
                LOG(self.appname + " stopped")

        def applicationDied(self):
                LOG(self.appname + " died")

        def applicationUnknown(self):
                LOG(self.appname + " unknown state")

###############################################################################
class TaskManager( object ):

    """
    Used to start/stop hifly applications
    """
    
    
    #==========================================================================
    def __init__(self):
        LOG("Created")
        self.nameServer = None
        self.namePort = None
        self.workstation = None
        self.taskManager = None
        self.domain = None
        self.family = None
        self.interests = {}

    #==========================================================================
    def setup(self, server = None, port = None, family = PRIME ):
        """
        Setup the interface. Obtain the TASK manager handle.
        """
        # We need a dedicated CORBA wrapper for accessing GEN satellite
        if not CONN.isReady():
            if not server or not port:
                raise DriverException("Cannot setup connection")
            # If there is no connection already, setup it
            LOG("Adding name service TASKNS")
            CONN.setup("TASKNS", server, port, "GEN", family )
    
    #==========================================================================
    def useWorkstation(self, workstation):
        
        """
        Set the workstation name to manage applications in
        """
        # Get the service name for the given workstation
        self.workstation = workstation
        serviceName = "TASKmanager"
        serviceType = workstation
        serviceClass = TKCOMcorbaProcessList
        
        # Obtain the event server manager
        LOG("Obtaining task manager for workstation " + self.workstation )
        self.taskManager = CONN.getObjectByContextType( "GEN", "TASK", serviceName, serviceType, serviceClass )
        LOG("Manager: " + repr(self.taskManager) )

    #==========================================================================
    def useDomainFamily(self, domain, family):
        
        """
        Set the domain and family of the applications to be managed
        """
        
        LOG("Set domain/family: " + domain + "/" + family )
        self.domain = domain
        self.family = family

    #==========================================================================
    def startProcess(self, processType, mnemonic, arguments, useDisplay = False):
        
        """
        Start a hifly client process
        """
        
        if self.taskManager is None:
            raise HiflyException("No task manager available")

        if self.domain is None:
            raise HiflyException("No domain selected")

        if processType == CLIENT:
            fam = "CLIENT"
        else:
            fam = self.family

        environment = []

        if useDisplay:
            host = socket.gethostname()        
            LOG("Using display on: " + host)
            environment.append("DISPLAY=" + host + ":0.0")

        LOG("Starting process " + mnemonic + "," + repr(arguments) + " on " + 
                 self.domain + "/" + self.family + "/" + fam + " (" + self.workstation + ")" )        
        result = self.taskManager.startProcess(
                                      mnemonic,
                                      0,
                                      arguments,
                                      environment,
                                      0,
                                      fam,
                                      "",
                                      self.family,
                                      self.domain
                                      )
        LOG("Result: " + repr(result))
        return result

    #==========================================================================
    def stopProcess(self, processType, mnemonic, doRestart):
        
        """
        Stop a hifly core process
        """
        
        if self.taskManager is None:
            raise DriverException("No task manager available")

        if self.domain is None:
            raise DriverException("No domain selected")

        if processType == CLIENT:
            fam = "CLIENT"
        else:
            fam = self.family

        LOG("Stopping process " + mnemonic + " on " + 
                 self.domain + "/" + self.family + " (" + self.workstation + ")" )        
        result = self.taskManager.stopProcess(
                                      mnemonic,
                                      0,
                                      doRestart,
                                      fam,
                                      self.family,
                                      self.domain
                                      )
        LOG("Result: " + repr(result))
        return result

    #==========================================================================
    def registerProcess(self, name, processType, mnemonic, delegate = None):
        
        """
        Register interest for the given process, using the given delegate
        """

        if processType == CLIENT:
            fam = "CLIENT"
        else:
            fam = self.family
        
        if self.interests.get(name) is None:
            LOG("Registering interest on " + name)
            int = TaskInterest(self.taskManager, self.domain, fam, mnemonic)
            int.register()
            if not (delegate is None):
                int.setDelegate(delegate)
            self.interests[name] = int


    #==========================================================================
    def unregisterProcess(self, name):
        
        """
        Unregister interest for a given process
        """

        if not (self.interests.get(name) is None):
            LOG("Unregistering interest on " + name)
            del self.interests[name]

    #==========================================================================
    def processStatus(self, processType, mnemonic ):
        
        """
        Obtain the status of the given core process
        """
        
        self.taskStatus = None
        
        self.registerProcess( "PROCESS_STATUS", processType, mnemonic, self )
        
        while self.taskStatus is None:
            sleep(0.5)
            
        self.unregisterProcess( "PROCESS_STATUS" )
            
        return self.taskStatus

    #==========================================================================
    def applicationStopped( self ):
        self.taskStatus = TASK_STOPPED

    #==========================================================================
    def applicationStarting( self ):
        self.taskStatus = TASK_STARTING

    #==========================================================================
    def applicationStarted( self ):
        self.taskStatus = TASK_STARTED

    #==========================================================================
    def applicationDied( self ):
        self.taskStatus = TASK_DIED

    #==========================================================================
    def applicationUnknown( self ):
        self.taskStatus = TASK_UNKNOWN
