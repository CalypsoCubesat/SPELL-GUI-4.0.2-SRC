################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.task 
FILE
    task.py
DESCRIPTION
    hifly Task management interface
    
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
from spell.utils.log import *
import spell.lib.adapter.task
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.exception import DriverException

#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.task.taskcontrol import *
from constants import *
from internals.exception import HiflyException

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TASK']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.task.TaskInterface 

###############################################################################
class TaskInterface( superClass ):

    taskMgr = None
    defaults = {}
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        self.defaults = {Family:PRIME,ProcType:PROCESS_CLIENT}
        self.taskMgr = TaskManager()
    
    #==========================================================================
    def setup(self, ctxName):
        """
        Setup the task interface
        """
        LOG("Initializing hifly TASK interface")
        superClass.setup(self,ctxName)
        self.taskMgr.setup()

    #==========================================================================
    def cleanup(self):
        """
        Cleanup the task interface
        """
        LOG("Cleaning up hifly TASK interface")
        superClass.cleanup(self)
        
    #==========================================================================
    def startTask(self, name, arguments = [] , config = {} ):
        """
        Start a task
        """
        
        if len(config)==0:
            config = self.defaults
        
        # Get the process type
        if not config.has_key(ProcType):
            config[ProcType] = self.defaults[ProcType]
        type = config.get(ProcType)

        # Use local display or not
        useDisplay = False
        if config.has_key(Display):
            if config.get(Display) == LOCAL:
                useDisplay = True

        # Get the host name
        if not config.has_key(Host):
            raise DriverException("Expected config parameter: host")
        hostname = config.get(Host)
        
        # Get the domain
        if not config.has_key(Domain):
            raise DriverException("Expected config parameter: domain")
        domain = config.get(Domain)

        # Get the family        
        if not config.has_key(Family):
            config[Family] = self.defaults[Family]
        family = config.get(Family)
        
        self.taskMgr.useDomainFamily(domain, family)
        self.taskMgr.useWorkstation(hostname)
        
        try:        
            LOG("Starting task: " + name)
            self.taskMgr.startProcess( type, name, arguments, useDisplay )
        except HiflyException,e:
            raise DriverException("Could not start process '" + name + "': " + repr(e))
        
        return True
        
    #==========================================================================
    def stopTask(self, name, config = {} ):
        """
        Stop a task
        """
        if not config.has_key(ProcType):
            config[ProcType] = self.defaults[ProcType] 
        type = config.get(ProcType)

        # Get the restart flag        
        doRestart = False
        if config.has_key(TaskMode):
            if config.get(TaskMode) == RESTART:
                doRestart = True
        
        # Get the host name
        if not config.has_key(Host):
            raise DriverException("Expected config parameter: host")
        hostname = config.get(Host)
        
        # Get the domain
        if not config.has_key(Domain):
            raise DriverException("Expected config parameter: domain")
        domain = config.get(Domain)

        # Get the family        
        if not config.has_key(Family):
            config[Family] = self.defaults[Family]
        family = config.get(Family)
        
        self.taskMgr.useDomainFamily(domain, family)
        self.taskMgr.useWorkstation(hostname)
        
        try:        
            LOG("Stopping task: " + name)
            self.taskMgr.stopProcess( type, name, doRestart )
        except HiflyException,e:
            raise DriverException("Could not stop process '" + name + "': " + repr(e))

        return True

    #==========================================================================
    def taskStatus(self, name, config = {} ):
        """
        Get the task status
        """
        if len(config)==0:
            config = self.defaults
        
        if not config.has_key(ProcType):
            raise DriverException("Expected config parameter: process type")
        type = config.get(ProcType)

        # Get the host name
        if not config.has_key(Host):
            raise DriverException("Expected config parameter: host")
        hostname = config.get(Host)
        
        # Get the domain
        if not config.has_key(Domain):
            raise DriverException("Expected config parameter: domain")
        domain = config.get(Domain)

        # Get the family        
        if not config.has_key(Family):
            raise DriverException("Expected config parameter: family")
        family = config.get(Family)
        
        self.taskMgr.useDomainFamily(domain, family)
        self.taskMgr.useWorkstation(hostname)

        try:        
            LOG("Checking task: " + name)
            status = self.taskMgr.processStatus( type, name )
        except HiflyException,e:
            raise DriverException("Could not check process '" + name + "': " + repr(e))
        return status
    
###############################################################################
# Interface instance
TASK = TaskInterface()
    