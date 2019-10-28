###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tc.injection 
FILE
    injection.py
    
DESCRIPTION
    hifly services for telecommand injection (low level interface)
    
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
from spell.lib.hifly.internals.connection import CONN
from spell.lib.hifly.internals.exception import HiflyException
from spell.utils.log import *
from spell.lib.hifly.internals.value import *
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.hifly.interface import ITC_INJ__POA,ITC_INJ,ITC
from spell.lib.hifly.utils.tc_utils import *
from spell.lib.hifly.internals.timeacc import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from tcview import TCinjectionView

#*******************************************************************************
# System imports
#*******************************************************************************
import os,sys

###############################################################################
class Request( object ):
    id = None
    itemName = None
    status = None
    
    def __init__(self, itemName):
        self.itemName = itemName
        self.id = None
        self.status = None

###############################################################################
class TcInjection( object ):
    
    """
    DESCRIPTION:
        This class provides the command injection interface for hifly.
    """
    
    # TC injector object
    tcInjector          = None
    # TC injector objects manager
    __tcInjectorManager = None
    # The execution status view
    __tcStatusView      = None
    # The command object factory
    __tcFactory = None
    
    #==========================================================================
    def __init__(self):
        
        LOG("Created")
        # CORBA objects
        self.tcInjector = None
        self.__tcInjectorManager = None
        self.__tcStatusView = None
        self.__tcFactory = None

    #==========================================================================
    def setup(self, ctxName):
        
        """
        Setup the telecommand injection interface
        """
        # TC injection manager parameters
        serviceName = ITC_INJ.TCinjectServerMngr.ServiceName
        serviceClass = ITC_INJ.TCinjectServerMngr
        
        # Obtain the TC injection service manager
        LOG("Obtaining TC injection service")
        self.__tcInjectorManager = CONN.getService( serviceName, serviceClass )
        
        if self.__tcInjectorManager is None:
            raise HiflyException("Could not obtain TC injection service")

        # Create the TC injection view        
        LOG("Creating TC status view")
        self.__tcStatusView = TCinjectionView()
        
        # Obtain the TC injector
        LOG("Obtaining TC injection server")
        try:
            self.tcInjector = self.__tcInjectorManager.getTCinjectMngr( self.__tcStatusView._this(), 10, "USL" )
        except Exception,e:
            raise HiflyException("TC injection server not available")

        LOG("Ready")

    #==========================================================================
    def cleanup(self):
        
        """
        Perform cleanup operations, releasing objects in the proper order
        """        
        LOG("Releasing TC status view")
        if self.__tcStatusView:            
            CONN.releaseObject(self.__tcStatusView)
        
        if self.tcInjector: 
            try:
                LOG("Releasing TC injector")
                self.tcInjector.deregister()
            except:pass
            CONN.releaseObject(self.tcInjector)

        if self.__tcInjectorManager:
            LOG("Releasing TC injection manager")
            CONN.releaseObject(self.__tcInjectorManager) 
        LOG("TC injection interface clean")

    #==========================================================================
    def setFactory(self, factory):
        self.__tcFactory = factory

    #==========================================================================
    def prepareCommand(self, cmdItem, verifier, config = {} ):
        """
        Prepare for sending a command with parameters
        """
        if self.tcInjector is None:
            raise HiflyException("TC injection not available")
        
        parameters = self.__processParameters(cmdItem,False)
        paramSets = []
        
        cmdItem._setExecutionStageStatus("Preparation", "Ongoing", "Building request")
        
        # Create a command request
        LOG("Creating TC request")
        request = self.__tcFactory.createCommandRequest(cmdItem, parameters, paramSets, config)
        
        # Obtain the expanded stack
        LOG("Obtaining stack information")
        stackCommands = self.__tcFactory.getCommandStack( request )
        self.__completeItemInformation(cmdItem,stackCommands,verifier)
        
        return request

    #==========================================================================
    def isCriticalCommand(self, cmdName, config = {} ):
        """
        Check whether a command is critical
        """
        if self.tcInjector is None:
            raise HiflyException("TC injection not available")
        try:
            LOG("Checking if the command is critical " + repr(cmdName) )
            isCritical = self.tcInjector.confirmCriticalCommand( cmdName )
        except ITC_INJ.CommandInjectMngr.UnknownCommand,ex:
            sys.stderr.write("UNKNOWN COMMAND: " + cmdName + "\n")
            raise HiflyException("Unknown command " + cmdName,repr(ex) )
        except Exception,ex:
            sys.stderr.write(repr(ex)+"\n")
            raise HiflyException("Could not confirm if the command is critical", repr(ex) )
        return isCritical

    #==========================================================================
    def getSequenceStack(self, request, config = {} ):
        """
        Return the command list for a sequence
        """
        return self.__tcFactory.getSequenceStack( request, ITC_INJ.NOTIFY_ALL )

    #==========================================================================
    def sendCommand(self, cmdItem, request, config = {} ):
        """
        Send a command with parameters
        """
        if self.tcInjector is None:
            raise HiflyException("TC injection not available")

        cmdName = cmdItem.name()
        try:
            # Actually inject the request
            cmdItem._setExecutionStageStatus("Injection", "Ongoing", "Injecting request")
            LOG("Injecting command " + repr(cmdName) )
            requestID = self.tcInjector.injectCmd( request )
            LOG("Request ID is " + repr(requestID))
        except ITC_INJ.CommandInjectMngr.InjectionFailed,ex:
            sys.stderr.write("INJECTION FAILED: "+ repr(ex.reason) + "\n")
            raise HiflyException("Injection failed",repr(ex.reason) )
        except Exception,ex:
            sys.stderr.write(repr(ex)+"\n")
            raise HiflyException("Could not inject command", repr(ex) )
        return requestID

    #==========================================================================
    def prepareBlock(self, cmdBlock, verifier, config = {} ):
        """
        Send a block with parameters
        """
        if self.tcInjector is None:
            raise HiflyException("TC injection not available")

        #TODO
        cmdNames = []
        parameters = self.__processParametersBlock(cmdBlock)
        paramSets = []

        LOG("Creating the command block request")        
        releaseSet = self.__tcFactory.createCommandRequestSet( cmdNames, parameters, paramSets, config )
        block = self.__tcFactory.createCommandRequestBlock( releaseSet )

        # Obtain the expanded stack
        LOG("Obtaining stack information")
        stackCommands = self.__tcFactory.getCommandBlockStack( block )
        self.__completeItemInformation(cmdBlock,stackCommands,verifier)

        return block

    #==========================================================================
    def sendCommandBlock(self, cmdBlock, request, config = {} ):
        """
        Send a command block
        """

        # Inject the command request
        LOG("Injecting command block")
        try:
            cmdBlock._setExecutionStageStatus("Injection", "Ongoing", "Injecting request")
            requestID = self.tcInjector.injectCmdBlock( request )
            LOG("Request ID is " + repr(requestID))
        except ITC_INJ.CommandInjectMngr.InjectionFailed,ex:
            sys.stderr.write("INJECTION FAILED: "+ repr(ex.reason) + "\n")
            raise HiflyException("Injection failed",repr(ex.reason) )
        except Exception,ex:
            sys.stderr.write(repr(ex)+"\n")
            raise HiflyException("Could not inject command block", repr(ex) )
        return requestID
        
    #==========================================================================
    def prepareSequence(self, seqItem, verifier, config = {} ):
        """
        Prepare for sending a sequence with parameters
        """
        if self.tcInjector is None:
            raise HiflyException("TC injection not available")
        
        parameters = self.__processParameters(seqItem,True)
        LOG("Processed parameters: " + str(len(parameters)))
        paramSets = []
        
        seqItem._setExecutionStageStatus("Preparation", "Ongoing", "Building request")
        
        # Create a command request
        LOG("Creating Sequence request")
        request = self.__tcFactory.createSequenceRequest(seqItem, parameters, paramSets, config)
        
        # Obtain the expanded stack
        LOG("Obtaining stack information")
        stackCommands = self.__tcFactory.getSequenceStack( request, ITC_INJ.NOTIFY_ALL )
        self.__completeItemInformation(seqItem,stackCommands,verifier)
        
        return request
        
    #==========================================================================
    def sendSequence(self, seqItem, request, config = {} ):
        
        """
        Send a sequence with parameters
        """
        seqName = seqItem.name()
        try:
            # Inject the command request
            LOG("Injecting sequence " + repr(seqName) )
            seqItem._setExecutionStageStatus("Injection", "Ongoing", "Injecting request")
            requestID = self.tcInjector.injectSeq( request, ITC_INJ.NOTIFY_ALL )
            LOG("Request ID is " + repr(requestID))
        except ITC_INJ.CommandInjectMngr.InjectionFailed,ex:
            sys.stderr.write("INJECTION FAILED: "+ repr(ex.reason) + "\n")
            raise HiflyException("Injection failed",repr(ex.reason) )
        except Exception,ex:
            sys.stderr.write(repr(ex)+"\n")
            raise HiflyException("Could not inject sequence", repr(ex) )            
        return requestID

    #==========================================================================
    def prepareGroup(self, groupItem, cmdItemList, verifier, config = {} ):
        """
        Prepare for sending a group of commands with parameters
        """
        if self.tcInjector is None:
            raise HiflyException("TC injection not available")

        requestList = []

        for item in cmdItemList:
            LOG("Creating command request for " + repr(item.name()))
            parameters = self.__processParameters(item, False)
            request = self.__tcFactory.createCommandRequest(item, parameters, [], config)
            requestList += [request]
        
        LOG("Creating TC group request")
        groupRequest = self.__tcFactory.createCommandGroupRequest( requestList, config )
        
        LOG("Obtaining stack information")
        stackCommands = self.__tcFactory.getGroupStack( groupRequest )
        self.__completeItemInformation( groupItem, stackCommands, verifier )
        
        return groupRequest
        
    #==========================================================================
    def sendGroup(self, groupItem, groupRequest, config = {} ):
        
        """
        Send a command group with parameters
        """
        try:
            # Inject the command request
            LOG("Injecting command group")
            groupItem._setExecutionStageStatus("Injection", "Ongoing", "Injecting request")
            requestID = self.tcInjector.injectGroup( groupRequest )
            LOG("Request ID is " + repr(requestID))
        except ITC_INJ.CommandInjectMngr.InjectionFailed,ex:
            sys.stderr.write("INJECTION FAILED: "+ repr(ex.reason) + "\n")
            raise HiflyException("Injection failed",repr(ex.reason) )
        except Exception,ex:
            sys.stderr.write(repr(ex)+"\n")
            raise HiflyException("Could not inject sequence", repr(ex) )            
        return requestID

    #==========================================================================
    def clearVerification(self):
        self.__tcStatusView.removeDelegate()

    #==========================================================================
    def __completeItemInformation(self, item, stack, verifier):

        # Establish the relationship with the verifier
        self.__tcStatusView.setDelegate( verifier )
        # Update the verifier information with the stack
        if stack and len(stack)>1:
            elements = []
            for cmd in stack:
                elements.append( cmd.m_commandName )
            item._setElements(elements)
        verifier.setItem( item )
        
    #==========================================================================
    def __processParameters(self, tcItem, isSequence):
        paramList = tcItem._getParams()
        processedParams = []
        # If the command has parameters
        if paramList:
            for param in paramList:
                LOG("Processing parameter: " + repr(param) + ":" + repr(param.value))
                parName = param.name
                parVal = Variant()
                parVal.setV(param.value)
                isEng = (param.value.format() == ENG)
                defCal = (param.value.format() == ENG)
                units = param.value.units()
                radix = radixToIBase(param.value.radix())
                if isSequence:
                    tcItem._setExecutionStageStatus("Preparation", "Ongoing", "Parameter " + parName)
                    cmdParam = self.__tcFactory.createSequenceParam( tcItem.name(), parName, isEng, defCal, units, radix, parVal )
                else:
                    cmdParam = self.__tcFactory.createCommandParam( tcItem.name(), parName, isEng, defCal, units, radix, parVal )
                processedParams.append(cmdParam)
        LOG("Total TC arguments: " + str(len(processedParams)))
        return processedParams

    #==========================================================================
    def __processParametersBlock(self, tcItems):
        return []

