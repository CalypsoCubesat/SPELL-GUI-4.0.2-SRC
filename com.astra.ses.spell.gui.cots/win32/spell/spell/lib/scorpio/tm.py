###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.scorpio.tm 
FILE
    tm.py
    
DESCRIPTION
    scorpio services for telemetry management (low level interface)
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Srinivasan Ranganathan
"""

###############################################################################

from time import sleep
from spell.utils.log import *

from math import floor, ceil
import MySQLdb
import spell.lib.adapter.tm
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.scorpio.modifiers import *
from spell.lib.exception import DriverException
from spell.config.reader import Config
from spell.utils.log import LoggerClass
from spell.lib.scorpio.interface.ITC import Limit
import sys

###############################################################################

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TM']

#*******************************************************************************
# Module globals
#*******************************************************************************
superClass = spell.lib.adapter.tm.TmInterface

###############################################################################
class TmInterface( superClass ):
    """
    Concrete implementation of the core tm_class for scorpio driver
    """

    sc = None
    db = None
    host = None
    _bus = None
    _rtm2 = None
    _log = None
    _limit = None
   
    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created scorpio TM interface")
        self.verificationFailure = []
        self._log = LoggerClass()
        self._log.initLogFile ("SPEL_Limits")

    #==========================================================================
    def setup(self, ctxName):
        """
        DESCRIPTION:
            Setup the scorpio low level interface 
        """

        # Obtain the configuration information for this context
        # The context
        ctx = Config.instance().getContextConfig(ctxName)

        self._bus = ctx.getFamily()

        self.__class__.host = ctx.getDriverConfig("ARCHIVA")
        self.__class__.sc = ctx.getSC()
        self.__class__.db = self.__class__.sc + "_2"

	cws = ctx.getDriverConfig("CWS")


	if (self._bus == "A2100"):
          conn = MySQLdb.connect (host=self.__class__.host,
                 user="root",passwd="",db=self.__class__.db)
          cursor = conn.cursor()
          query = "SELECT TRIM(MNEMONIC) from cvt ";
          cursor.execute(query)
          self._rtm2 = cursor.fetchall()
	elif (self._bus == "STAR2"):
          conn = MySQLdb.connect (host=self.__class__.host,
                 user="root",passwd="",db=self.__class__.sc + "_1")
          cursor = conn.cursor()
          query = "select distinct pid_mnemonic from waitFor w, pid_map p "
	  query += "where w.pid = p.pid and format < 19"
          cursor.execute(query)
          self._rtm2 = cursor.fetchall()
	else:
	  self._rtm2 = []

	self._limit = Limit(self.__class__.sc)
	self._limit.Initialize (cws, self._log.getLogFile().fileno())

        superClass.setup(self, ctxName)

    #==========================================================================
    def cleanup(self):
        """
        DESCRIPTION:
            Cleanup the scorpio low level interface
        """
	del self._limit
        superClass.cleanup(self)

    #==========================================================================
    def _refreshItem(self, param, config = {} ):
        isEng = (config.get(ValueFormat) == ENG)
	rtm = 1
	retries = 0;
	stream1 = None
	stream2 = None
	forceRTM = False
	waitUpdate = config.get(Wait)

        if config.has_key(RTM):
	    forceRTM = True
            rtm = config.get(RTM)

    	try:   
            name = param.name().strip()
	    idx = name.find ("->")
	    if idx != -1:
		name = name[0:idx].strip()
            
	    if forceRTM:
	      stream1 = rtm
	      stream2 = rtm
	    elif (name,) in self._rtm2:
	      stream1 = 2
	      stream2 = 1
	    else:
	      stream1 = 1
	      stream2 = 2

	    while True:
	      row = self.getStreamValue (name, isEng, waitUpdate, stream1)

	      if (row == None):
                 raise DriverException("No such TM parameter: " + "'" + name +"'")
		 break
	      elif (int(row[1]) == 0):
	        # If point has a value which is not active and the RTM is not
		# explicitly specified check the other stream
		if not forceRTM:
	          row = self.getStreamValue (name, isEng, waitUpdate, stream2)
	          if row == None:
                      raise DriverException("Parameter Not Active: " + name)
		      break
		  elif int(row[1]) == 1: # Active
	            print >> sys.stderr, "Telemetry point -> ",name, \
			" on RTM-> ",str(stream2), " = ", row[0]
		    break
		  retries += 1
		  if retries > 32:  # Retry for 1 full major frame
		     break;
		  sleep (1)
	      else:
	          print >> sys.stderr, "Telemetry point -> ",name, \
			" on RTM-> ",str(stream1), " = ", row[0]
		  break

            if isEng:
	        param.setName (row[3])
                if (row[2] == "DOUBLE"):
                    param._setEng(float(row[0]))
                elif (row[2] == "STRING"):
                    param._setEng(row[0])
                else: 
                    param._setEng(int(row[0]))
            else:
	        param.setName (row[2])
                if (row[0]-floor(row[0]) == 0):
                    param._setRaw(int(row[0]))
                else:
                    param._setRaw(row[0])
    
            param._setStatus (row[1])
    	
	    if isEng:
               return [param._getEng(), 1]
	    else:
               return [param._getRaw(), 1]
        except Exception,e:
            param._setEng(0)
            param._setRaw(0)
            param._setStatus(False)
            raise DriverException("Unable to obtain TM parameter value: " + repr(e))

    #==========================================================================
    def getStreamValue (self, name, isEng, waitUpdate, rtm):

	    outageTry = 1
            refreshRate = 1

            conn = MySQLdb.connect (host=self.__class__.host,
                   user="root",passwd="",db=self.__class__.sc + "_" + str(rtm))
            cursor = conn.cursor()

	    if waitUpdate:
	      # CTU FRAME CNT valid for A2100 and STAR2, need to see how to
	      # handle SB3000 and SB4000
              if (self._bus == "LM7000"):
                 query = "SELECT TIME_SEC, RVALUE from cvt ";
                 query += "where mnemonic = 'MINOR FRAME NUMBER'"
              else:
                 query = "SELECT TIME_SEC, RVALUE from cvt ";
                 query += "where mnemonic = 'CTU FRAME CNT'"

              cursor.execute(query)
              row = cursor.fetchone()

	      if (row == None): 
		cursor.close()
		conn.close()
		return None

	      timestamp = int(row[0])
	      MF = int(row[1])

	      if (self._bus == "STAR2"):
		refreshRate = 1
                query = "SELECT START_FRAME, SKIP_FRAME FROM waitFor w, "
		query += "pid_map p where w.pid = p.pid "
		query += "and p.pid_mnemonic = '" + name + "'"
		query += "and w.format = (select rvalue from cvt "
		query += "where mnemonic = 'STREAM" + str(rtm) + " TLM ID')"
              elif (self._bus == "LM7000"):
		refreshRate = 2
                query = "SELECT START_FRAME, SKIP_FRAME FROM cvt c ";
                query += "where c.pid = '" + name + "'"
	      else:
		refreshRate = 2
                query = "SELECT START_FRAME, SKIP_FRAME FROM cvt c ";
                query += "where c.mnemonic = '" + name + "'"

              cursor.execute(query)
              row = cursor.fetchone()

	      if (row == None):
		cursor.close()
		conn.close()
		if (self._bus == "STAR2"):  # Return parameter is invalid
		   return [0, 0, 0, 0]
		else:
		   return None

	      StartFrame = int(row[0])
	      SkipFrame = int(row[1])

	      if (SkipFrame == 0):
	        WaitForFrame = (MF + 1)%33
	      elif (MF <= StartFrame):
	        WaitForFrame = -1
	      else:
	        WaitForFrame = (MF+SkipFrame) - ((MF - StartFrame) % SkipFrame)

	      print >> sys.stderr, "Started at Minor Frame ", str(MF)

	      # divide by 2 because A2100 refresh rate is 1/2 sec
	      # Round numbers to its higher value
	      # Minimum sleep time needs to be 1
	      if (MF < StartFrame):
		sleepTime = ceil(float(StartFrame - MF)/refreshRate)
	      elif (MF == StartFrame):
		sleepTime = 1
	      else:
		sleepTime = ceil(float(WaitForFrame - MF)/refreshRate)

	      while (MF < StartFrame or MF < WaitForFrame):
	        prevMF = MF
		prevTimestamp = timestamp
	        if (outageTry == 10):
                  raise DriverException("Telemetry Outage Cannot Proceed: ")
	        sleep (sleepTime)

                if (self._bus == "LM7000"):
                  query = "SELECT TIME_SEC, RVALUE from cvt ";
                  query += "where mnemonic = 'MINOR FRAME NUMBER'"
                else:
                  query = "SELECT TIME_SEC, RVALUE from cvt ";
                  query += "where mnemonic = 'CTU FRAME CNT'"

                cursor.execute(query)
                row = cursor.fetchone()

	        if (row == None):
		  cursor.close()
		  conn.close()
		  return None

	        timestamp = int(row[0])
	        if (timestamp == prevTimestamp):
		  outageTry += 1
	        else:
	          MF = int(row[1])

		  if (MF < prevMF and WaitForFrame == -1):
		      break
		  if (MF <= StartFrame):
                     WaitForFrame = -1
		  elif (WaitForFrame >= 32):
                     WaitForFrame = -1

		  # All subsequent retries after a second
		  sleepTime = 1

	        print >> sys.stderr, "MF = ", MF, " WAITING IN LOOP FOR", name

	      print >> sys.stderr, "Waited TILL Minor Frame ", str(MF)

            if isEng:
		if (self._bus == "STAR2"):
                  query = "SELECT CASE TLM_TYPE WHEN 'STRING' ";
                  query += "THEN IFNULL(VENDOR_STAT,CVALUE) ";
                  query += "WHEN 'DOUBLE' THEN FVALUE ELSE c.IVALUE END, ";
                  query += "ACTIVE, TLM_TYPE, ";
		  query += "concat(rpad(p.pid_mnemonic,40,' '),'->  ',rpad(c.MNEMONIC,15,' ')) ";
		  query += "FROM pid_map p, cvt c ";
                  query += "LEFT JOIN stat_map sm on (sm.AMC_STAT = CVALUE ";
                  query += "AND sm.IVALUE = c.IVALUE) ";
                  query += "where c.pid = p.pid ";
                  query += "and p.pid_mnemonic = '" + name + "'"
                elif (self._bus == "LM7000"):
                  query = "SELECT CASE TLM_TYPE WHEN 'STRING' ";
                  query += "THEN CVALUE ";
                  query += "WHEN 'DOUBLE' THEN FVALUE ELSE c.IVALUE END, ";
                  query += "ACTIVE, TLM_TYPE, c.pid FROM cvt c ";
                  query += "where c.pid = '" + name + "'"
		else:
                  query = "SELECT CASE TLM_TYPE WHEN 'STRING' ";
                  query += "THEN CVALUE ";
                  query += "WHEN 'DOUBLE' THEN FVALUE ELSE c.IVALUE END, ";
                  query += "ACTIVE, TLM_TYPE, c.mnemonic FROM cvt c ";
                  query += "where c.mnemonic = '" + name + "'"
            else:
		if (self._bus == "STAR2"):
                  query = "SELECT RVALUE,ACTIVE, ";
		  query += "concat(rpad(p.pid_mnemonic,40,' '),'->  ',rpad(c.mnemonic,15,' ')) ";
		  query += "FROM cvt c, pid_map p ";
                  query += "where c.pid = p.pid ";
                  query += "and p.pid_mnemonic = '" + name + "'"
                elif (self._bus == "LM7000"):
                  query = "SELECT RVALUE, ACTIVE, c.pid FROM cvt c ";
                  query += "where c.pid = '" + name + "'"
		else:
                  query = "SELECT RVALUE, ACTIVE, c.mnemonic FROM cvt c ";
                  query += "where c.mnemonic = '" + name + "'"
    
            cursor.execute(query)
            row = cursor.fetchone()

	    cursor.close()
	    conn.close()
	    return row

    #==========================================================================
    def _loadLimits (self, limitsFile, config):
        idx = limitsFile.find("//")
        file = limitsFile[idx+2:]
	print >> sys.stderr, "Loading limits file -> ",file
	ret = self._limit.TempFile (file)
	print >> sys.stderr, ret
	if ret[0] != 0:
	   raise DriverException ("ERROR - ", ret[1])

    #==========================================================================
    def _setLimits (self, param, limits, config):
        name = param.name()
	if (name,) in self._rtm2:
	  rtm = 2
	else:
	  rtm = 1

	if limits.has_key (Expected):
	   expectedStatus = limits[Expected]
	   analog = False
	else:
	   analog = True
           loRed = str(limits[LoRed])
           loYel = str(limits[LoYel])
           hiYel = str(limits[HiYel])
           hiRed = str(limits[HiRed])
	   ret = self._limit.Single (str(rtm), name, loRed, hiRed, loYel, hiYel)
	   if ret[0] != 0:
	      raise DriverException ("ERROR - ", ret[1])

	   
    
################################################################################
# Interface handle
TM = TmInterface()
