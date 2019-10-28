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
import socket,time,os

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
    domain = None
    family = None
    displayApp = None
    displayArgs = None
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        self.defaults = {Type:CLIENT}
        self.taskMgr = TaskManager()
        self.domain = None
        self.family = None
        self.displayApp = None
        self.displayArgs = None
    
    #==========================================================================
    def setup(self, ctxName):
        """
        Setup the task interface
        """
        try:
            LOG("Initializing hifly TASK interface")
            superClass.setup(self,ctxName)
            self.taskMgr.setup()
    
            ctxInfo = Config.instance().getContextConfig(ctxName)
            self.domain = ctxInfo.getSC()
            self.family = ctxInfo.getFamily()
    
            driverName = ctxInfo.getDriver()
            driverDetails = Config.instance().getDriverConfig(driverName)
    
            self.displayApp = driverDetails['DisplayApp']
            self.displayArgs = driverDetails['DisplayArgs']
        except HiflyException,ex:
            raise DriverException("Unable to load TASK interface: " + ex.message, ex.reason)
        except Exception,ex:
            raise DriverException("Unable to load TASK interface", repr(ex))

    #==========================================================================
    def cleanup(self):
        """
        Cleanup the task interface
        """
        LOG("Cleaning up hifly TASK interface")
        superClass.cleanup(self)
        
    #==========================================================================
    def _startTask(self, taskName, arguments, config = {} ):
        """
        Start a task
        """
        
        if len(config)==0:
            config = self.defaults
        
        # Get the process type
        if not config.has_key(Type):
            type = self.defaults[Type]
            LOG("Using default process type: " + type)
        else:
            type = config.get(Type)
            LOG("Using process type: " + type)

        # Use local display or not
        useDisplay = False
        if config.has_key(HDisplay):
            if config.get(HDisplay) != LOCAL:
                LOG("Using local display")
                useDisplay = True
        if not useDisplay: LOG("Using remote display")

        # Get the host name
        if not config.has_key(Host):
            hostname = socket.gethostname()
        else:
            hostname = config.get(Host)
        LOG("Using host: " + repr(hostname))
        
        # Get the family        
        if config.has_key(Family):
            family = config.get(Family)
        else:
            family = self.family
        LOG("Using family: " + repr(family))
        
        self.taskMgr.useDomainFamily(self.domain, family)
        self.taskMgr.useWorkstation(hostname)
        
        try:        
            LOG("Starting task: " + taskName + " with args: " + repr(arguments))
            result = self.taskMgr.startProcess( type, taskName, arguments, useDisplay )
        except HiflyException,e:
            raise DriverException("Could not start process '" + taskName + "': " + repr(e))

        # Wait a number of seconds in order to be sure that this process is running before the
        # following invocation
        if result and config.has_key(Delay):
            time.sleep(config.get(Delay))
        
        return result
        
    #==========================================================================
    def _stopTask(self, name, config = {} ):
        """
        Stop a task
        """
        if not config.has_key(Type):
            config[Type] = self.defaults[Type] 
        type = config.get(Type)

        # Get the restart flag        
        doRestart = False
        if config.has_key(Mode):
            if config.get(Mode) == RESTART:
                doRestart = True
        
        # Get the host name
        if not config.has_key(Host):
            hostname = socket.gethostname()
        else:
            hostname = config.get(Host)
        LOG("Using host: " + repr(hostname))

        # Get the family        
        if config.has_key(Family):
            family = config.get(Family)
        else:
            family = self.family
        LOG("Using family: " + repr(family))

        self.taskMgr.useDomainFamily(self.domain, family)
        self.taskMgr.useWorkstation(hostname)
        
        try:        
            LOG("Stopping task: " + name)
            result = self.taskMgr.stopProcess( type, name, doRestart )
        except HiflyException,e:
            raise DriverException("Could not stop process '" + name + "': " + repr(e))

        return result

    #==========================================================================
    def _openDisplay(self, displayName, config = {} ):
        if displayName is None or len(displayName)==0:
            args = ""
        else:
            args = self.displayArgs + " " + os.getenv("BIN_DIR") + "/hiflyViews -displays " + str(displayName) + " EXTRA -instance 9 &"
        return self.startTask( self.displayApp, args, config )

    #==========================================================================
    def _printDisplay(self, displayName, config = {} ):
        if displayName is None or len(displayName)==0:
            args = ""
        else:
            now = time.gmtime(time.time())
            nowString = time.strftime("%d/%m/%YT%H:%M:%S.000", now)
            exportFormat = "ps"
            exportFileExtension = ".ps"
            if config.has_key(Format):
                exportFormat = config.get(Format)
                if exportFormat is "jpg":
                    exportFileExtension = ".jpg"
                elif exportFormat is "png":
                    exportFileExtension = ".png"
                elif exportFormat is "ps":
                    exportFileExtension = ".ps"
                elif exportFormat is "vector" or exportFormat is "matrix":
                    exportFileExtension = ".txt"            
            outputFormat = "file"
            outputName = Config.instance().getUserDataDir() + "/../PRINTOUT/" +\
                displayName + time.strftime("_%Y%m%d-%H%M%S", now) + exportFileExtension
            if config.has_key(Printer):
                outputFormat = "printer"
                outputName = config.get(Printer)
            args = self.displayArgs + " " + os.getenv("BIN_DIR") + "/hiflyViews -displays " + str(displayName) +\
                " -export " + exportFormat + " -print -" + outputFormat + " " + outputName +\
                " -starttime " + nowString + " -endtime " + nowString + " EXTRA -instance 9 &"
        return self.startTask( self.displayApp, args, config )
            
    #==========================================================================
    def _closeDisplay(self, displayName, config = {} ):
        if displayName is None or len(displayName)==0:
            args = ""
        else:
            args = self.displayArgs + " " + os.getenv("BIN_DIR") + "/hiflyViews -displays " + str(displayName) + " -closedisplays EXTRA -instance 9 &"
        return self.startTask( self.displayApp, args, config )

    #==========================================================================
    def _checkTask(self, taskName, config = {} ):
        """
        Get the task status
        """
        if not config.has_key(Type):
            type = self.defaults[Type]
        type = config.get(Type)

        # Get the host name
        if not config.has_key(Host):
            hostname = socket.gethostname()
        hostname = config.get(Host)
        
        # Get the family        
        if config.has_key(Family):
            family = config.get(Family)
        else:
            family = self.family
        
        self.taskMgr.useDomainFamily(self.domain, family)
        self.taskMgr.useWorkstation(hostname)

        try:        
            LOG("Checking task: " + taskName)
            status = self.taskMgr.processStatus( type, taskName )
        except HiflyException,e:
            raise DriverException("Could not check process '" + taskName + "': " + repr(e))
        return status
    
###############################################################################
# Interface instance
TASK = TaskInterface()
    