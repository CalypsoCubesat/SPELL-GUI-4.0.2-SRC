################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.tools 
FILE
    tools.py
    
DESCRIPTION
    Auxiliary classes for unit tests
    
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
from spell.lib.adapter.tm import TmInterface
from spell.lib.adapter.tc import TcInterface
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.exception import *
from spell.lib.adapter.config import Configurable
from spell.utils.log import *
from spell.lang.helpers.basehelper import WrapperHelper

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import time

LOG.showlog = False

################################################################################    
class FakeTmClass(TmInterface):
    
    forRaw = 0.1
    forEng = "VALUE"
    toWait = 0.75
    refreshCount = 0
    passedConfig = None

    #===========================================================================    
    def __init__(self):
        TmInterface.__init__(self)
        self.setup("none")
        self.refreshCount = 0
        
    #===========================================================================    
    def _refreshItem(self, param, config ):
        if param.name()=="NOEXIST":
            raise DriverException("NON EXISTENT")
        self.passedConfig = config
        isEng = (config.get(ValueFormat) == ENG)
        self.refreshCount = self.refreshCount + 1
        if config.get(Wait) == True:
            to = config.get(Timeout)  
            if to is not None and (self.toWait > to):
                raise DriverException("TIMEOUT") 
            time.sleep(self.toWait)
        
        param._setEng(self.forEng)
        param._setRaw(self.forRaw)
        param._setStatus(True)
        
        if isEng:
            return [self.forEng,True]
        return [self.forRaw,True]
        
    #===========================================================================    
    def _injectItem(self, param, config ):
        pass

################################################################################    
class FakeTcClass(TcInterface):

    passedConfig = None
    toWait = 2
    
    #===========================================================================    
    def __init__(self):
        TcInterface.__init__(self)
        self.setup("none")
        
    #===========================================================================    
    def _sendCommand(self, tcItem, config):
        self.passedConfig = config
        if tcItem.name() != 'TC_OK':
            tcItem._setCompleted(False)
            raise DriverException("EXECUTION FAILED")
        
        if config.has_key(Timeout):
            to = config.get(Timeout)  
            if to is not None and (self.toWait > to):
                raise DriverException("TIMEOUT") 

        tcItem._setExecutionStageStatus("STAGE 1/3", "PASSED")
        time.sleep(self.toWait/3.0)
        tcItem._setExecutionStageStatus("STAGE 2/3", "PASSED")
        time.sleep(self.toWait/3.0)
        tcItem._setExecutionStageStatus("STAGE 3/3", "PASSED")
        time.sleep(self.toWait/3.0)
        tcItem._setCompleted(True)
        return True 

    #===========================================================================    
    def _sendBlock(self, tcItemList, config):
        self.passedConfig = config
        if config.has_key(Timeout):
            to = config.get(Timeout)  
            if to is not None and (self.toWait > to):
                raise DriverException("TIMEOUT") 

        overall = True        
        for item in tcItemList:
            if item.name() != 'TC_OK':
                if config.has_key(TryAll) and config.get(TryAll):
                    item._setCompleted(False)
                    overall = False
                    continue
                raise DriverException("EXECUTION FAILED")
            
            item._setExecutionStageStatus("STAGE 1/3", "PASSED")
            time.sleep(self.toWait/3.0)
            item._setExecutionStageStatus("STAGE 2/3", "PASSED")
            time.sleep(self.toWait/3.0)
            item._setExecutionStageStatus("STAGE 3/3", "PASSED")
            time.sleep(self.toWait/3.0)
            item._setCompleted(True)
        return overall
                
################################################################################
class FakeClientInterface(Configurable):
        
    promptAnswer = None
    promptOptions = None
    promptMessage = None
    promptConfig = None
    promptType = None
        
    #==========================================================================
    def notifyLine(self):
        LOG("Notify line") 

    #==========================================================================
    def notifyStatus(self, status_code ):
        LOG("Notify status: " + status_code) 
        
    #===========================================================================
    def notifyCode(self, csp, script):
        LOG("Notify code: " + csp) 

    #===========================================================================
    def notify(self, type, name, value, status, reason = ""):
        LOG("Notify: " + type + "," + str(name) + "," + str(value) + "," + str(status) + ":" + reason)

    #===========================================================================
    def notifyError(self, msg, reason):
        LOG("ERROR: " + msg + "," + reason)

    #===========================================================================
    def write(self, message, config):
        LOG("MESSAGE: " + message + "," + repr(config))

    #===========================================================================
    def prompt(self, message, options, config):
        LOG("PROMPT: " + message + "," + repr(options) + "," + repr(config))
        
        self.promptOptions = options
        self.promptMessage = message
        self.promptConfig = config
        self.promptType = config.get(Type)

        return self.promptAnswer


################################################################################
class TestFunction(WrapperHelper):
    
    #===========================================================================
    def _doOperation(self, *args):
        print "OPERATION ARGUMENTS:",args
        
    def _getDefaults(self):
        return {"A":1,"B":2}
        
