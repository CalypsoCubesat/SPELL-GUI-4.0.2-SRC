################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.tc 
FILE
    tc.py
    
DESCRIPTION
    hifly services for telecommand management (low level interface)
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.lib.adapter.value import *
from spell.lang.constants import *
from spell.lang.modifiers import *
import spell.lib.adapter.tc
from spell.lib.adapter.tc_item import TcItemClass
from spell.utils.log import *
from spell.utils.ttime import *
from spell.lib.registry import *
from spell.lib.adapter.constants.notification import *
from spell.lib.exception import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from internals.timeacc import *
from internals.tc.verifier import *
from internals.tc.injection import TcInjection
from internals.tc.provision import TcProvision
from internals.tc.factory import TcFactory,VERSION_6,VERSION_5
from internals.value import Variant
from utils.tc_utils import *
from internals.exception import HiflyException
from internals.exif import EXIF

#*******************************************************************************
# System imports
#*******************************************************************************
import os 

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TC']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.tc.TcInterface

###############################################################################
class TcInterface( superClass ):
    """
    Concrete implementation of the core tc_class for hifly driver
    """

    # The command execution verifier
    verifier = None
    # TC injection interface
    tcInj = None
    # TC provision interface
    tcPro = None
    # TC factory
    tcFactory = None
    # Command timeout
    __timeout = None
    # Context name
    __ctxName = None
    
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created hifly TC interface")
        self.verifier = None
        self.tcInj = TcInjection()
        self.tcPro = TcProvision()
        self.__ctxName = None
        self.__timeout = None
    
    #==========================================================================
    def _createTcItem(self, mnemonic, description = ""):
        item = TcItemClass(self, mnemonic, description)
        return item
    
    #==========================================================================
    def setup(self, ctxName):
        try:
            self.__ctxName = ctxName
            LOG("Initializing TC interface")
            superClass.setup(self,ctxName)
            LOG("Initializing TC factory")
            self.tcFactory = TcFactory()
            self.tcInj.setFactory(self.tcFactory)
            self.connect()
        except HiflyException,ex:
            raise DriverException("Unable to load TC interface: " + ex.message, ex.reason)
        except Exception,ex:
            raise DriverException("Unable to load TC interface", repr(ex))

    #==========================================================================
    def cleanup(self):
        LOG("Cleaning up TC injection interface")
        superClass.cleanup(self)
        self.disconnect()
    
    #==========================================================================
    def connect(self, reconnect = False):
        if (reconnect):
            self.disconnect()
        LOG("Initializing TC internals")
        self.tcInj.setup(self.__ctxName)
        self.tcFactory.setup(self.__ctxName,self.tcInj.tcInjector)

    #==========================================================================
    def disconnect(self):
        LOG("Cleaning TC internals")
        self.tcPro.cleanup()
        self.tcInj.cleanup()

    #==========================================================================
    @EXIF
    def _sendBlock(self, tcItemList, config ):
        raise NotAvailable()

    #==========================================================================
    @EXIF
    def _sendList(self, tcItemList, config = {} ):
        
        # Create a group item
        groupItem = self['GROUP']
        
        self.__parseItemConfig(config)
        
        LOG("Creating verifier")
        if self.verifier:
            del self.verifier
            self.verifier = None
        self.verifier = TcVerifierClass(self)

        # Reset the command before sending
        groupItem._reset()
        
        try:
            request = self.tcInj.prepareGroup( groupItem, tcItemList, self.verifier, config )
            reqID = self.tcInj.sendGroup( groupItem, request, config )
        except HiflyException, ex:
            groupItem._setExecutionStageStatus("Preparation", "Failed", "Exception while building request")
            groupItem._setCompleted(False)
            raise DriverException("Send failed:" + ex.message, ex.reason)

        # Set timetag date
        self.verifier.setTimetag(False)
        # Set loadonly flag
        self.verifier.setLoadOnly(False)
                
        LOG("Command sent, verifying")
        
        # Verify the command by monitoring the verif stages updates
        timedOut = self.__verifyCommand( reqID, False, False )
        
        LOG("Command verification finished (timed out=" + repr(timedOut) + ")")

        # Return the execution result
        if timedOut:
            raise DriverException("Command verification timed out")
        elif not groupItem.getIsSuccess():
            stage,status = groupItem.getExecutionStageStatus()
            reason = str(stage) + ":" + str(status)
            raise DriverException("Command execution failed: " + reason)
        
        stage,status = groupItem.getExecutionStageStatus()
        return True

    #==========================================================================
    @EXIF
    def _checkCriticalCommands(self, tcList, config ):
        
        try:
            if (config.has_key(ConfirmCritical) and (config.get(ConfirmCritical) == True)):
                LOG("Checking critical commands")
                criticalCommands = ""
                if not (config.has_key(Sequence) and (config.get(Sequence) == True)):
                    for tcItem in tcList:
                       tcItem._setExecutionStageStatus("Preparation", "Ongoing", "Checking if the command is critical")
                       isCritical = self.tcInj.isCriticalCommand( tcItem.name(), config)
                       if isCritical:
                           criticalCommands = criticalCommands + " " + tcItem.name()
                if criticalCommands != "":
                    LOG("Confirm execution of critical commands:" + criticalCommands)
                    self._confirmExecution("critical commands:" + criticalCommands)
        except HiflyException, ex:
            tcItem._setExecutionStageStatus("Preparation", "Failed", "Exception while checking critical commands")
            tcItem._setCompleted(False)
            raise DriverException("Send failed:" + ex.message, ex.reason)

    #==========================================================================
    @EXIF
    def _checkCriticalSequence(self, tcItem, request, config ):
        
        try:
            if (config.has_key(ConfirmCritical) and (config.get(ConfirmCritical) == True)):
                LOG("Checking critical commands in sequence")
                criticalCommands = ""
                sequenceStack = self.tcInj.getSequenceStack(request, config)
                if sequenceStack is not None:
                    tcItem._setExecutionStageStatus("Preparation", "Ongoing", "Checking critical commands in the sequence")
                    for sequenceItem in sequenceStack:
                        isCritical = self.tcInj.isCriticalCommand( sequenceItem.m_commandName , config)
                        if isCritical is True:
                            criticalCommands = criticalCommands + " " + sequenceItem.m_commandName
                if criticalCommands != "":
                    LOG("Confirm execution of sequence with critical commands:" + criticalCommands)
                    self._confirmExecution("sequence with critical commands:" + criticalCommands)
        except HiflyException, ex:
            tcItem._setExecutionStageStatus("Preparation", "Failed", "Exception while checking critical commands")
            tcItem._setCompleted(False)
            raise DriverException("Send failed:" + ex.message, ex.reason)

    #==========================================================================
    @EXIF
    def _sendCommand(self, tcItem, config ):
        
        # Create a new execution verifier for this item
        LOG("Creating verifier")
        if self.verifier:
            del self.verifier
            self.verifier = None
        self.verifier = TcVerifierClass(self)

        timetag,exectime,isSequence,isLoadOnly = self.__parseItemConfig(config)
        
        config[Time] = exectime
        useConfig = self._config.copy()
        useConfig.update(config)
        
        # Send the command to the TC subsystem
        LOG("Execution time: " + str(exectime))                    
        LOG("Is sequence   : " + repr(isSequence))                    
        LOG("Load only     : " + repr(isLoadOnly))                    
        LOG("Timetagged    : " + repr(timetag))
        
        # Reset the command before sending
        tcItem._reset()
        
        try:
            if isSequence:
                request = self.tcInj.prepareSequence( tcItem, self.verifier, useConfig )
                self._checkCriticalSequence(tcItem, request, useConfig)
                reqID = self.tcInj.sendSequence( tcItem, request, useConfig )
            else:
                request = self.tcInj.prepareCommand( tcItem, self.verifier, useConfig )
                reqID = self.tcInj.sendCommand( tcItem, request, useConfig)
        except HiflyException, ex:
            tcItem._setExecutionStageStatus("Preparation", "Failed", "Exception while building request")
            tcItem._setCompleted(False)
            raise DriverException("Send failed:" + ex.message, ex.reason)

        # Set timetag date
        self.verifier.setTimetag(timetag)
        # Set loadonly flag
        self.verifier.setLoadOnly(isLoadOnly)
                
        LOG("Command sent, verifying")
        
        # Verify the command by monitoring the verif stages updates
        timedOut = self.__verifyCommand( reqID, timetag, isLoadOnly )
        
        LOG("Command verification finished (timed out=" + repr(timedOut) + ")")

        # Return the execution result
        if timedOut:
            raise DriverException("Command verification timed out")
        elif not tcItem.getIsSuccess():
            stage,status = tcItem.getExecutionStageStatus()
            reason = str(stage) + ":" + str(status)
            raise DriverException("Command execution failed: " + reason)
        
        stage,status = tcItem.getExecutionStageStatus()
        return True

    #==========================================================================
    def __verifyCommand(self, requestID, timetag, isLoadOnly):
        """
        Create a verifier object and launch it. If the execution timeout
        is exceeded, interrupt the verifier and set the execution as failed.
        """
        
        # Get the verification start time
        starttime = time.time()
        currenttime = starttime
        # Launch the verification
        self.verifier.start()
        # Execution timeout control loop
        LOG("Start timeout control loop (" + repr(self.__timeout) + ")")
        verificationTimedOut = True
        while( (currenttime - starttime) < self.__timeout ):
            time.sleep(0.1)
            currenttime = time.time()
            if not self.verifier.isAlive():
                LOG("Verifier finished, exiting control loop")
                verificationTimedOut = False 
                break
        LOG("Exit timeout control loop (timed out=" + repr(verificationTimedOut) + ")")
        # Unlink the verifier and the tc view
        self.tcInj.clearVerification()
        # If the loop was interrupted due a timeout, the thread
        # is still alive and must be stopped
        if self.verifier.isAlive():
            self.verifier.stop()
        # Remove the verifier
        del self.verifier
        self.verifier = None
        return verificationTimedOut    

    #==========================================================================
    def __parseItemConfig(self, config):
        # Get the default timeout value
        self.__timeout = self.getConfig(Timeout)
        
        # Adjust values of timeout and execTime
        if config.has_key(Timeout):
            tValue = config.get(Timeout)
            if isinstance(tValue,TIME):
                self.__timeout = tValue.abs()
            elif type(tValue)==str:
                self.__timeout = TIME(tValue).abs()
            elif type(tValue)==int or type(tValue)==float:
                self.__timeout = tValue
            else:
                raise DriverException("Bad time format")
            LOG("Overriding timeout: " + repr(self.__timeout))
        config[Timeout] = self.__timeout
        
        timetag = False
        exectime = self.getConfig(Time)
        if config.has_key(Time):
            tValue = config.get(Time)
            if tValue == 0:
                exectime = 0
                timetag = False 
            elif isinstance(tValue,TIME):
                exectime = tValue
                timetag = True
            elif type(tValue)==str:
                exectime = TIME(tValue)
                timetag = True
            elif type(tValue)==int or type(tValue)==float:
                exectime = TIME(tValue)
                timetag = True
            else:
                raise DriverException("Bad time format")
        config[Time] = exectime

        # Get the sequence flag
        isSequence = False
        if config.has_key(Sequence) and config.get(Sequence) == True:
            isSequence = True

        # Get the load only flag
        isLoadOnly = False
        if config.has_key(LoadOnly) and config.get(LoadOnly) == True:
            isLoadOnly = True
            
        return [timetag,exectime,isSequence,isLoadOnly]


    #==========================================================================
    def increaseTimeout(self):
        self.__timeout += self.__timeout

###############################################################################
# Interface handle
TC = TcInterface()
