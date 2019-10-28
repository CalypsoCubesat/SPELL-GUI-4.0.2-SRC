###############################################################################

"""
PACKAGE 
    spell.lib.scorpio.tc 
FILE
    tc.py
    
DESCRIPTION
    Telecommand interface implementation for scorpio driver
    
COPYRIGHT
    This software is the copyrighted work of SES ENGINEERING
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Srinivasan Ranganathan
"""

###############################################################################

import spell.lib.adapter.tc
from spell.lang.functions import BuildTC
from spell.config.reader import Config
from spell.lib.scorpio.interface.ITC import Callback
from spell.lib.scorpio.interface.ITC import A2100_TC
from spell.lib.scorpio.interface.ITC import STAR2_TC
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.exception import *
from spell.utils.log import *
from spell.utils.log import LoggerClass
from spell.utils.ttime import *
from spell.lang.functions import Prompt
from time import sleep
from string import lower
from threading import Event, Thread
import thread
import MySQLdb
import os,sys

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TC']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.tc.TcInterface
errorString = None

###############################################################################
class TcInterface( superClass, Callback ):
    """
    Concrete implementation of the core tc_class for scorpio driver
    """
    
    __item = None
    __itemList = []
    __itemCount = 0
    _TC = None
    _timer = None
    _ret = 0
    _bus = None
    _statmap = {}
    _lock = None
    _log = None
    _group = False

    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        Callback.__init__(self)
	self._lock = thread.allocate_lock()
        self._log = LoggerClass()
	self._log.initLogFile ("SPEL_Scorpio")
        LOG("Created scorpio TC interface")
    
    #==========================================================================
    def setup(self, ctxName):
        LOG("Initializing scorpio TC interface")

        # Obtain the configuration information for this context
        # The context
        ctx = Config.instance().getContextConfig(ctxName)

	scraft = ctx.getSC()
	cws = ctx.getDriverConfig("CWS")

        host = ctx.getDriverConfig("ARCHIVA")
        db = scraft + "_1"

	self._ret = 0

	self._bus = ctx.getFamily()
	if (self._bus == "STAR2"):
           conn = MySQLdb.connect (host=host,
                   user="root",passwd="",db=db)
	   cursor = conn.cursor()
           query = "select distinct upper(vendor_stat), amc_stat from stat_map"
           cursor.execute (query)
           rows = cursor.fetchall()
           for row in rows:
              self._statmap[row[0]] = row[1]
           cursor.close()
           conn.close()
           self._TC = STAR2_TC()
	elif (self._bus == "LM7000"):
           self._TC = STAR2_TC()
	else:
           self._TC = A2100_TC()

        self._TC.Initialize (scraft, cws, os.getpid(), \
		 self._log.getLogFile().fileno())
        self._TC.setCallback (self.__disown__())
	self._timer = PingTimer (30, self.sendPing)
	self._timer.start()

        superClass.setup(self,ctxName)
        LOG("Finished Initializing scorpio TC interface")

    #==========================================================================
    def cleanup(self):
        LOG("Cleaning up scorpio TC interface")
	self._TC.clearUp()
	self._timer.cancel()
	del self._TC
        superClass.cleanup(self)
        LOG("Got here after Cleaning up scorpio TC interface")
    
    #==========================================================================
    def _sendCommand(self, tcItem, config ):
        """
        DESCRIPTION:
        
        ARGUMENTS:
            
        RETURNS:
       
        RAISES:

        """

	itemConfig = config
	# Commented out update does not work correctly. need to use some other
        # function. a tcItem SendDelay value of None overrides a global delay 
        # which should not be the case
	#itemConfig = config.copy()
	#itemConfig.update (tcItem.getConfig())

	tempConfig = tcItem.getConfig()
	if tempConfig.has_key(SendDelay) and tempConfig.get(SendDelay) != None:
	    itemConfig["SendDelay"] = tempConfig["SendDelay"]
	if tempConfig.has_key(ReleaseTime) and \
	  isinstance(tempConfig.get(ReleaseTime), TIME):
	    itemConfig["ReleaseTime"] = tempConfig["ReleaseTime"]

        print >> sys.stderr, "Sending command: ",tcItem.name(),itemConfig
        LOG("Sending command: " + tcItem.name() + str(itemConfig))

	self.__item = tcItem
	if (self._group == False):
	   self.__itemList.insert (0, tcItem);

	execTimeStr = "+0";
        if itemConfig.has_key(ReleaseTime) and isinstance(itemConfig.get(ReleaseTime), TIME):
	   absTime = itemConfig.get(ReleaseTime)
	   releaseTime = str(absTime.year()) + "," + str(absTime.julianDay()) \
	     + "," + str(absTime.hour()) + "," + str(absTime.minute()) \
	     + "," + str(absTime.second())
	   if (absTime > (TIME("NOW") + 9 * SECOND)):
	      execTimeStr = "/"+releaseTime;
        elif itemConfig.has_key(SendDelay) and itemConfig.get(SendDelay) != None:
	   send_delay = itemConfig.get(SendDelay)
	   execTimeStr = "+"+str(send_delay//3600)+"," \
		+str(send_delay//60%60)+","+str(send_delay%60)
	if (itemConfig != None):
          if itemConfig.has_key(Delay):
             timeout = itemConfig.get(Delay)
             LOG("Overriding timeout: " + repr(timeout))

	names = []
	params = []
        if tcItem._getParams():
	    for param in tcItem._getParams(): 
                parName = param.name
                parVal = param.value.get()
	 	names.append (parName)
		if (isinstance(parVal,basestring)):
                  if (self._statmap.has_key(parVal.upper())):
                    params.append (self._statmap[parVal.upper()])
		  else:
	 	    params.append (parVal)
		else:
	 	    params.append (str(parVal))

	print >> sys.stderr, "Parameters Names ->"
	LOG ("Parameter Names ->")
	print >> sys.stderr, names
	LOG (str(names))
	print >> sys.stderr, "Parameter Values ->"
	LOG ("Parameter Values ->")
	print >> sys.stderr, params
	LOG (str(params))
        # First try to reconnect to servers if previous command failed due
        # to unresponsive server
        if (self._ret == -3):
           self._TC.connect()
        elif (self._ret == -4):
           if self._TC.connectCHServer() == -1:
	     raise DriverException ("ERROR - ", "CHServer not responding")
             return False

        # Get the sequence flag
        isSequence = False
        if itemConfig.has_key(Sequence) and itemConfig.get(Sequence) == True:
            isSequence = True

        # Get the memory load command flag
        isMemoryLoad = hasattr (tcItem, '_isMemoryLoad')

	# Reset the TC driver to start a new command if not a list
	if (self._group == False):
	   self._TC.Reset()

	# Buffer the command list or command
	self._lock.acquire()
	if isSequence:        # Command lists
	  self._ret = self._TC.Send (0, lower(tcItem.name()))
	elif isMemoryLoad:    
	  if tcItem.name() == "DWELL_LD":  # DWELL memory load commands 
	     if not len(params) == 8:
	       raise DriverException ("DWELL_LD needs 8 parameters to dwell")
               return False
	     self._ret = self._TC.SendDWL (tcItem.name(), execTimeStr, \
		 len(params), params)
	  else:               # Memory load commands eg: TRQ_BIAS_LD
	     self._ret = self._TC.SendM (tcItem.name(), execTimeStr, \
		 len(params), names, params)
	else:                 # Dynamic command lists and single commands
	  print >> sys.stderr, names, params
	  self._ret = self._TC.SendDP (tcItem.name(), execTimeStr, len(params), names, params)
	self._lock.release()

	if (self._ret == 1):    # Commanding Error
	   self.__item._setCompleted(False)
           print >> sys.stderr, "COMMANDING ERROR"
	   raise DriverException ("Error Sending Command - ", errorString)
           return False
	elif (self._ret == -3): # Commanding Error
	   self.__item._setCompleted(False)
           print >> sys.stderr, "SERVER DOWN"
	   raise DriverException ("Error Sending Command - ", "Server Down")
	   return False
        elif (self._ret == -4): # CH Server Error
	   self.__item._setCompleted(False)
           print >> sys.stderr, "CH SERVER DOWN"
           raise DriverException ("Error Sending Command - ", "CHServer Down")
           return False

	if (self._group == False):
	   return self._releaseCommands()
	else:
	   return True

    #==========================================================================
    def _releaseCommands (self):
	# Release the command to the S/C
	self._lock.acquire()
	self._ret = self._TC.Release()
	self._lock.release()

	if (self._ret == 0): # Success
	   for i in range(self.__itemCount+1):
	      self.__itemList[i]._setCompleted(True)
	   self.__itemList = []
	   return True
	elif (self._ret == -1): # Haz command skipped
	   if len(self.__itemList) != 0:
	      self.__itemList[self.__itemCount]._setCompleted(False)
           print >> sys.stderr, "HAZARDOUS COMMAND TRANSMISSION SKIPPED"
	   raise UIException ("Hazardous Command Transmission Skipped")
           return False
	elif (self._ret == 1): # Commanding Error
	   if len(self.__itemList) != 0:
	      self.__itemList[self.__itemCount]._setCompleted(False)
           print >> sys.stderr, "COMMANDING ERROR"
	   raise DriverException ("Error Sending Command - ", errorString)
           return False
	elif (self._ret == -3): # Commanding Error
	   if len(self.__itemList) != 0:
	      self.__itemList[self.__itemCount]._setCompleted(False)
           print >> sys.stderr, "SERVER DOWN"
	   raise DriverException ("Error Sending Command - ", "Server Down")
	   return False
        elif (self._ret == -4): # CH Server Error
	   if len(self.__itemList) != 0:
	      self.__itemList[self.__itemCount]._setCompleted(False)
           print >> sys.stderr, "CH SERVER DOWN"
           raise DriverException ("Error Sending Command - ", "CHServer Down")
           return False
	else: 
           return False

    #==========================================================================
    def _sendList(self, tcItemList, config = {} ):
	self.__itemList = tcItemList
        # Sending commands one by one
	self._group = True
	firstCommand = True
	globalDelay = 0
        if config.get(SendDelay) != None:
	   globalDelay = config.get(SendDelay)

	# Reset the TC driver to start a new command list
	self._TC.Reset()
        LOG(" --> Executing list")
        for tcItem in tcItemList:
            LOG(" --> Executing command in list: " + tcItem.name())
	    tcItemConfig = tcItem.getConfig()
            if tcItemConfig.get(SendDelay) == None:
		if globalDelay != 0:
	            tcItemConfig["SendDelay"] = globalDelay
		elif not firstCommand:
	            tcItemConfig["SendDelay"] = 2
		else:
	            tcItemConfig["SendDelay"] = 0
		tcItem.setConfig (tcItemConfig)
            self._sendCommand(tcItem, tcItem.getConfig())            
	    firstCommand = False
	ret = self._releaseCommands()
	self._group = False
	self.__itemCount = 0
	return ret

    #==========================================================================
    def _sendGroup(self, tcItemList, config ):
        """
        DESCRIPTION:
        
        ARGUMENTS:
            
        RETURNS:
       
        RAISES:

        """
        for item in tcItemList:
            print >> sys.stderr, "Sending Grouped Command: ",item.name()
            self.__item = item
        return True

    #==========================================================================
    # Fill itemList from scorpio command lists
    #==========================================================================
    def FillCmdsFromList (self, cmdlist):
	 self.__itemList = []
	 for cmd in cmdlist:
	   if cmd[0] != '.':
	     self.__itemList.append (BuildTC(cmd));

    #==========================================================================
    # callback function to report status changes to GUI
    #==========================================================================
    def report(self, *args):
	 global errorString
	 if args[0] < len(self.__itemList):
	   self.__itemCount = args[0]
	   self.__itemList[args[0]]._setExecutionStageStatus(args[1],args[2])
	   errorString = args[3]

    #==========================================================================
    # C++ to request any input from python
    #==========================================================================
    def userInput(self, *args):
         print >> sys.stderr, "REQUEST USER INPUT FOR COMMAND " + args[0]
	 self._lock.release()
	 ans = Prompt ("Authorize Hazardous Command -> " + args[0] , YES_NO)
	 self._lock.acquire()
 	 if (ans == None):
	   return 0
	 else:
	   return ans	

    #==========================================================================
    # Send keep alive to the scorpio servers
    #==========================================================================
    def sendPing (self):
	 self._lock.acquire()
         self._TC.sendPing()
	 self._lock.release()

################################################################################
# Send ping to Scorpio Servers every interval seconds
################################################################################
class PingTimer (Thread):
   def __init__(self, interval, function):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.waitEvent = Event()
        self.done = Event()

   def run (self):
       while not self.done.isSet():
          self.waitEvent.wait(self.interval)
          if not self.done.isSet() and not self.waitEvent.isSet():
             self.function ()

   def cancel (self):
       self.done.set()
       self.waitEvent.set()

################################################################################
# Interface handle
TC = TcInterface()
