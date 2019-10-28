################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tc.verifier
FILE
    verifier.py
    
DESCRIPTION
    Verifier class for command execution in hifly 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    08/01/2008
    
REVISION HISTORY
    08/01/2008    10:30    Creation
"""
################################################################################

from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.hifly.constants import *
from  spell.lib.hifly.modifiers import *
from spell.utils.log import *
from spell.lib.hifly.tc import *
from spell.lib.hifly.internals.value import radixToIBase
from spell.lib.hifly.internals.timeacc import secsToStr,timeToStr,getRelTime
import threading,thread
from spell.lib.registry import REGISTRY
from spell.lib.adapter.constants.notification import *

UNINIT_STAGE_STATUS   = "UKN"
ONGOING_STAGE_STATUS  = "Ongoing"
FINISHED_STAGE_STATUS = "Finished"
TIMEOUT_STAGE_STATUS  = "TIMEOUT"

###############################################################################
class CommandExecutionException( BaseException ):
    """
    Raised by the verification classes
    """
    def __init__(self, stage, status):
        BaseException.__init__(self)
        # Name of the failed verificaton stage
        self.stage = stage
        # Failure status
        self.status = status

    def __str__(self):
        return self.stage + " is " + self.status
    
###############################################################################
class ElementStatus(object):
    """
    Describes an element of a command. Applicable to sequences and blocks.
    """
    elementName = ""
    stageName   = UNINIT_STAGE_STATUS
    stageStatus = UNINIT_STAGE_STATUS
    lastUpdate  = None
    completed   = False
    
    def __init__(self):
        self.elementName = ""
        self.stageName   = UNINIT_STAGE_STATUS
        self.stageStatus = UNINIT_STAGE_STATUS
        self.lastUpdate  = None
        self.completed   = False

###############################################################################
class TcVerifierClass( threading.Thread ):
    """
    DESCRIPTION:
        Thread-based verifier for command executions. Monitors
        the execution verification stages, and notifies the
        associated TC item about status changes.
    """

    # Item being verified
    _tc_item        = None
    # Elements of the command (length=1 for simple commands)
    _elementIds     = None
    _elements       = None
    _lastElement    = 0
    # Tc interface
    _tcInterface    = None
    # To control the verification thread
    _interrupt      = False
    _cmdMutex       = None
    # To control updates
    _updateMutex    = None
    # Status of the TC chain
    _systemOk       = True
    # Status of the TC chain
    _systemStatus   = {}
    # Overall verification finished flag
    _finished       = False

    # Timetag flag
    isTimetag = False
    # Load only flag
    isLoadOnly = False
    # Timed out flag
    timedOut = False
    
    #==========================================================================
    def __init__(self, tcInterface):
        threading.Thread.__init__(self)
        self._tcInterface = tcInterface
        
        # Controls the thread execution
        self._interrupt = False
        self._finished = False
        self._cmdMutex = thread.allocate_lock()
        self._updateMutex = thread.allocate_lock()
        self.isTimetag = False
        self.isLoadOnly = False
        self.timedOut = False
        LOG("Created")

    #==========================================================================
    def setItem(self, tc_item):
        self._tc_item = tc_item
        # If we are processing a sequence get the sequence elements
        # for verification
        # For sequence/blocks
        self._elements = None
        self._elementIds = None
        self._lastElement = 0
        if self._tc_item.isComplex():
            LOG("Item to verify is complex")
            # Do not take first element, which is the command itself
            self.__setSequenceInfo( self._tc_item.getElements()[1:] )
        else:
            LOG("Item to verify is simple")

    #==========================================================================
    def setTimetag(self, timetag):
        LOG("Set timetag command: " + repr(timetag))
        self.isTimetag = timetag

    #==========================================================================
    def setLoadOnly(self, loadOnly):
        LOG("Set loadonly command: " + repr(loadOnly))
        self.isLoadOnly = loadOnly

    #==========================================================================
    def __setSequenceInfo(self, seqInfo):
        LOG("Set sequence information (" + str(len(seqInfo)) + ")")
        self._elements = []
        self._elementIds = {} # Maps the multId to _elements index
        self._lastElement = 0
        for seqElement in seqInfo:
            element = ElementStatus()
            element.elementName = seqElement
            LOG("   - Element " + str(len(self._elements)) + ": " + repr(element.elementName))
            element.stageName   = UNINIT_STAGE_STATUS
            element.stageStatus = UNINIT_STAGE_STATUS
            element.lastUpdate  = None
            element.completed   = False
            self._elements += [element]
         
    #==========================================================================
    def run(self):        
        """
        Main thread function. Monitor the command execution.
        """
        try:
            # Launch the monitoring loop
            self.__monitorCommand()
            
        # If there is a verification failure, notify the TC item
        except CommandExecutionException, e:
            LOG("Command execution exception: " + str(e))
            self.__setVerificationFinished()
            self.__setTcItemComplete(False)
            self.__setTcItemStageStatus(e.stage,e.status,"Caught verification exception")
            LOG("Exiting verifier loop")
            return
        
    #==========================================================================
    def stop(self):
        """
        Force the verification control loop stop
        """
        self._interrupt = True

    #==========================================================================
    def updateRequestStatus( self, id, multId, stage, utime, status, complete ):
        """
        DESCRIPTION:
            Callback for the TC view used for updates of the verification stages
        """

        if self.__isVerificationFinished(): return

        self._updateMutex.acquire()
        
        LOG("START REQ " + repr(id) + ":" + repr(multId) + " [" + stage + "=" + status + "] C: " + repr(complete))

        if self._elements is None:
            # Simple command verification
            self._completed = complete
            # The tc item will notify the CIF when updated
            comment = "Stage " + stage + " is " + status 
            self.__setTcItemStageStatus(stage,status,comment)
            # Set element complete flag
            if complete:
                # Set item completed and success
                self.__setTcItemComplete( successFlag = True )
                self.__setVerificationFinished()
        else:
            if len(self._elementIds)==0:
                LOG("Initial sequence status ongoing")
                # First notification comming
                self.__setTcItemStageStatus("Execution",ONGOING_STAGE_STATUS,"")

            # Sequence/blocks verification
            LOG("Get element for id " + repr(id))
            # Get the current element. Notifications may arrive not in order!
            if id in self._elementIds.keys():
                # Notifications for this element already came
                LOG("Got element")
                idx = self._elementIds.get(id)
                element = self._elements[idx]
            else:
                # First time this identifier arrives. Assign it to the next element
                # in the list
                if self._lastElement >= len(self._elements):
                    LOG("=========================================")
                    LOG("ERROR for element id " + repr(id))
                    LOG("Not enough elements: last=" + repr(self._lastElement))
                    LOG("=========================================")
                    self._updateMutex.release()
                    return
                
                LOG("Assigned element " + str(self._lastElement))
                element = self._elements[self._lastElement]
                self._elementIds[id] = self._lastElement
                self._lastElement += 1
                # Reset timeout on TC interface
                self._tcInterface.increaseTimeout()
            
            LOG("Current element is " + element.elementName + " with id "+ repr(id))
                
            # Now we work with the current element. Discard this if the
            # element is already completed.
            if not element.completed:
                LOG("Updating the element status (complete=" + str(complete) + ")" )
                element.lastUpdate = utime
                element.completed  = complete
                element.stage      = stage
                element.status     = status
            
                # The tc item will notify the CIF when updated
                comment = "Stage " + stage + " is " + status 
                itemSuccess = self.__setTcItemStageStatus(stage,status,comment,element.elementName)
                # Set element complete flag
                if complete:
                    LOG("The element is complete (success=" + repr(itemSuccess) + ")")
                    # Set item completed and success
                    self.__setTcItemComplete( successFlag = itemSuccess, elementId = element.elementName )
                    # Execution is completed if this all elements are completed
                    if len(self._elementIds) == len(self._elements):
                        allCompleted = True
                        for e in self._elements:
                            if (e.completed == False):
                                allCompleted = False
                                break
                        if allCompleted:
                            LOG("All elements executed, sequence finished")
                            self.__setTcItemStageStatus("Execution",FINISHED_STAGE_STATUS,"")
                            LOG("Sequence status completed")
                            self.__setTcItemComplete( successFlag = itemSuccess )
                            self.__setVerificationFinished()                
            
        LOG("END REQ " + repr(id) + ":" + repr(multId) + " [" + stage + "=" + status + "] C: " + repr(complete))
        self._updateMutex.release()
            
    #==========================================================================
    def updateSystemStatus( self, gs, nctrs, uv, tm, ifc ):
        """
        DESCRIPTION:
            Callback for the TC view used for TC subsystem links updates
        """
        LOG("SYSTEM  [GS:" + gs + ",NCTRS:" + nctrs + ",UV:" + uv + ",TM:" + tm + ",IFC:" + ifc + "]")
        self._cmdMutex.acquire()
        self._systemStatus['GS'] = gs
        self._systemStatus['NCTRS'] = nctrs 
        self._systemStatus['UV'] = uv 
        self._systemStatus['TM'] = tm
        self._systemStatus['IFC'] = ifc
        self._cmdMutex.release()
        self.__notifySys(gs, ifc, uv, tm)

    #===========================================================================
    def __setVerificationFinished(self):
        self._cmdMutex.acquire()
        self._finished = True        
        self._cmdMutex.release()

    #===========================================================================
    def __isVerificationFinished(self):
        self._cmdMutex.acquire()
        finished = self._finished        
        self._cmdMutex.release()
        return finished

    #===========================================================================
    def __setTcItemStageStatus(self, stageName, stageStatus, comment, elementId = None):
        self._cmdMutex.acquire()
        self._tc_item._setExecutionStageStatus(stageName,stageStatus,comment, elementId )
        self._cmdMutex.release()
        
        # For complex tc items only
        if elementId:
            # Depending on the status the item is failed
            try:
                    
                    self.__checkStageStatus( stageName, stageStatus )
                    return True
            
            except:
                LOG("Complex verification finished due to failure in element " + elementId)
                self.__setTcItemComplete( successFlag = False )
                self.__setVerificationFinished()
                return False

    #===========================================================================
    def __getTcItemStageStatus(self):
        self._cmdMutex.acquire()
        stageName,stageStatus = self._tc_item.getExecutionStageStatus()
        self._cmdMutex.release()
        return [stageName,stageStatus]

    #===========================================================================
    def __checkStageStatus(self, stageName, stageStatus):

        if stageStatus in [PASSED,PENDING,FINISHED_STAGE_STATUS,IDLE,\
                           UNINIT_STAGE_STATUS,ONGOING_STAGE_STATUS]:
            pass
        #===============================================================
        elif stageStatus == UNVERIFIED:
            LOG("Unverified status on stage " + repr(stageName), LOG_ERROR)
            raise CommandExecutionException(stageName, UNVERIFIED)
        #===============================================================
        elif stageStatus == UNKNOWN:
            LOG("Unknown status on stage " + repr(stageName), LOG_ERROR)
            raise CommandExecutionException(stageName, UNKNOWN)
        #===============================================================
        elif stageStatus == FAILED:
            LOG("Failed status on stage " + repr(stageName), LOG_ERROR)
            raise CommandExecutionException(stageName, FAILED)
        #===============================================================
        elif stageStatus == TIMEOUT:
            LOG("Timeout status on stage " + repr(stageName), LOG_ERROR)
            raise CommandExecutionException(stageName, TIMEOUT)
        #===============================================================
        elif stageStatus == NOT_APPLICABLE:
            LOG("Command wont be executed: " + repr(stageName), LOG_ERROR)
            raise CommandExecutionException(stageName, "Command will not be executed")
        #===============================================================
        else:
            LOG("Unexpected status on stage " + repr(stageName), LOG_ERROR)
            raise CommandExecutionException(stageName, "Unexpected: " + repr(stageStatus))
        #===============================================================
            

    #===========================================================================
    def __setTcItemComplete(self, successFlag = True, elementId = None ):
        self._cmdMutex.acquire()
        self._tc_item._setCompleted( successFlag, elementId )
        self._cmdMutex.release()

    #===========================================================================
    def __getTcItemSuccess(self):
        self._cmdMutex.acquire()
        success = self._tc_item.getIsSuccess()
        self._cmdMutex.release()
        return success
        
    #===========================================================================
    def __notifySys(self, gs, ifc, uv, tm ):
        status = gs + "/" + ifc + "/" + uv + "/" + tm
        LOG("Status: " + repr(status), LOG_WARN)

    #==========================================================================
    def __monitorCommand(self):
        """
        Control loop for verification stages. It executes until the
        command verification is completed.
        """
        # Do until the command verification is completed
        while( not self.__isVerificationFinished() ):
            # If there is a failure in a TC system link
            if not self._systemOk:
                # TODO: get which link in particular has failed
                raise CommandExecutionException("System status","NOK")

            # Obtain the current verification stage data
            stageName,stageStatus = self.__getTcItemStageStatus()
            finished = self.__isVerificationFinished()

            # Will raise a CommandExecutionException if there is a failure
            # so that the command monitoring finishes
            self.__checkStageStatus( stageName, stageStatus )
            
            # FIXME: To be replaced by an event!!!
            time.sleep(0.05)
            
            # If the thread is aborted due to an user timeout
            if self._interrupt:
                LOG("Monitor interrupted, TIMEOUT")
                self.timedOut = True
                raise CommandExecutionException("Verification", "Timeout (driver)")
            
            # If it is a timetag, finish for uplinked 
            if self.isTimetag and (stageName == UPLINKED) and (stageStatus == PASSED):
                LOG("Execution monitor finished for TIMETAG")
                self.__setTcItemComplete(True)
                self.__setTcItemStageStatus( stageName, stageStatus, "Timetag loaded")
                self.__setVerificationFinished()
                return
            
            # Load only commands
            if self.isLoadOnly and\
               (stageName=="Application accept") and\
               (stageStatus==PASSED):
                LOG("Execution monitor finished for LOAD ONLY")
                self.__setTcItemComplete(True)
                self.__setTcItemStageStatus( stageName, stageStatus, "Command loaded only")
                self.__setVerificationFinished()
                return
        
        # --- END WHILE -----------------------------------------------------
        
        # Obtain the current verification stage data
        stageName,stageStatus = self.__getTcItemStageStatus()
        success = self.__getTcItemSuccess()

        LOG("Execution finished on stage " + repr(stageName) + "=" + stageStatus) 
        LOG("Success flag: " + repr(success)) 
            
        if (stageStatus != PASSED)  and\
           (stageStatus != UNKNOWN) and\
           (stageStatus != FINISHED_STAGE_STATUS):
            LOG("Execution failed: " + repr(stageStatus) + repr([PASSED,UNKNOWN]))
            raise CommandExecutionException(stageName, stageStatus)
        else:
            LOG("Execution ok")
