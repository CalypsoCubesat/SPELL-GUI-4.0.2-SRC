###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tc.factory 
FILE
    injection.py
    
DESCRIPTION
    Factorizations for TC services (hifly EXIF versions 5 and 6)
    
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
from spell.lib.hifly.interface import ITC_INJ__POA,ITC_INJ,ITC
from spell.lib.hifly.internals.exception import HiflyException
from spell.utils.log import *
from spell.utils.ttime import *
from spell.lib.hifly.internals.value import Variant
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.hifly.utils.tc_utils import *
from spell.lib.hifly.internals.timeacc import *
from spell.config.reader import Config
from spell.config.constants import COMMON

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import os,sys

#*******************************************************************************
# Module globals
#*******************************************************************************
VERSION_6 = '6X'
VERSION_5 = '5X' 
PLATFORM_GEN = 'GEN'
PLATFORM_E2K = 'E2K'
PLATFORM_E3K = 'E3K'
PLATFORM_S13 = 'S13'

###############################################################################
class TcFactory( object ):

    # Map ID
    __mapID             = None
    # Virtual channel ID
    __vcID              = None
    # Interlock configuration
    __ilockStage        = None
    __ilockType         = None
    # Additional information defaults
    __addInfoKeys       = []
    __addInfoValues     = {}
    __addInfoFile       = None
    # Exif platform
    __exifVersion       = None
    # Spacecraft platform
    __scPlatform        = None
    # Injector server
    __injector          = None
    # Holds the last sequence mapped
    __lastItem = None
    # Holds the mapping for the last sequence
    __lastMapping = None
    
    #==========================================================================
    def __init__(self):
        
        LOG("Created")
        # Default values for MAP ID and virtual channel ID
        self.__mapID = ITC_INJ.MAPID_DEFAULT
        self.__vcID = ITC_INJ.VCID_DEFAULT
        # Interlock default configuration
        self.__ilockStage = ITC_INJ.IL_UV_GS_ACCEPT
        self.__ilockType = ITC.IL_NONE
        # Additional info defaults
        self.__addInfoKeys = []
        self.__addInfoValues = {}
        self.__addInfoFile = None
        self.__injector = None
        # Platform version 
        self.__exifVersion = VERSION_6
        self.__lastItem = None
        self.__lastMapping = None

    #==========================================================================
    def setup(self, ctxName, injector):
        
        LOG("Configuring TC factory")
        
        ctxInfo = Config.instance().getContextConfig(ctxName)
        domain = ctxInfo.getSC()
        driverName = ctxInfo.getDriver()
        driverDetails = Config.instance().getDriverConfig(driverName)

        #-----------------------------------------------------------------------
        # Get additional info data
        #-----------------------------------------------------------------------
        dataPath = Config.instance().getRuntimeDir()
        aiPath = driverDetails['AddInfoPath']
        addInfoPath = dataPath + os.sep + aiPath
        self.__addInfoFile = addInfoPath + os.sep + domain + ".dat" 

        # Get the additional info defaults
        self.__getAddInfoDefaults()

        #-----------------------------------------------------------------------
        # Get the configured platform
        #-----------------------------------------------------------------------
        version = ctxInfo.getDriverConfig('EXIFversion')
        if version is None:
            self.__exifVersion = VERSION_6
        else:
            self.__exifVersion = version
        platform = ctxInfo.getDriverConfig('Platform')
        if platform is None:
            self.__scPlatform = PLATFORM_GEN
        else:
            self.__scPlatform = platform
        #-----------------------------------------------------------------------

        LOG("Configured for EXIF " + repr(self.__exifVersion))
        LOG("Configured for platform " + repr(self.__scPlatform))
        
        self.__injector = injector

    #==========================================================================
    def createCommandParam(self, cmdName, argName, engValue, defCal, unit, radix, value ):
        
        LOG("Creating command parameter " + repr(argName) + " (" + repr(self.__exifVersion) + ")")
        if self.__exifVersion == VERSION_6:
            LOG("Mapping argument names for " + repr(cmdName))
            if self.__lastItem == cmdName:
                pMap = self.__lastMapping
            else:
                try:
                    pMap = self.__injector.getTCParameterMap(cmdName)
                    self.__lastItem = cmdName
                    self.__lastMapping = pMap
                except:
                    raise HiflyException("Could not get argument mapping for command " + cmdName)
                
            found = False
            for paramDefinition in pMap:
                name = paramDefinition.paramName
                desc = paramDefinition.paramDescription
                if argName==name:
                    found = True
                    break
                elif argName==desc:
                    found = True
                    argName = name
                    break
            if not found:
                raise HiflyException("Command argument " + repr(argName) + " not found")
            LOG("Mapped name: " + repr(argName))
            
        var = value
        if not isinstance(value,Variant):
            var = Variant()
            var.setV(value)
        LOG("Param info ------------------- ")
        LOG("  - name :" + argName)
        LOG("  - eng  :" + repr(engValue))
        LOG("  - defc :" + repr(defCal))
        LOG("  - unit :" + repr(unit))
        LOG("  - radx :" + repr(radix))
        LOG("  - value:" + repr(value))
        param = ITC.CommandParam( argName, engValue, defCal, unit, radix, var.getI() )
            
        return param

    #==========================================================================
    def createSequenceParam(self, seqName, argName, engValue, defCal, unit, radix, value ):
        
        LOG("Creating sequence parameter " + repr(argName) + " (" + repr(self.__exifVersion) + ")")
        if self.__exifVersion == VERSION_6:
            LOG("Mapping argument names for " + repr(seqName))
            if self.__lastItem == seqName:
                pMap = self.__lastMapping
            else:
                try:
                    pMap = self.__injector.getSeqFormalParameterMap(seqName)
                    self.__lastItem = seqName
                    self.__lastMapping = pMap
                except:
                    raise HiflyException("Could not get argument mapping for sequence " + seqName)
                
            found = False
            for paramDefinition in pMap:
                name = paramDefinition.paramName
                desc = paramDefinition.paramDescription
                if argName==name:
                    found = True
                    break
                elif argName==desc:
                    found = True
                    argName = name
                    break
            if not found:
                raise HiflyException("Sequence argument " + repr(argName) + " not found")
            LOG("Mapped name: " + repr(argName))
            
        var = value
        if not isinstance(value,Variant):
            var = Variant()
            var.setV(value)
        LOG("Param info ------------------- ")
        LOG("  - name :" + argName)
        LOG("  - eng  :" + repr(engValue))
        LOG("  - defc :" + repr(defCal))
        LOG("  - unit :" + repr(unit))
        LOG("  - radx :" + repr(radix))
        LOG("  - value:" + repr(value.get()))
        param = ITC.CommandParam( argName, engValue, defCal, unit, radix, var.getI() )
            
        return param

    #==========================================================================
    def createCommandParamSet(self, cmdName, name, valueSet ):
        
        params = ITC_INJ.ParameterSet( name, valueSet )
        return params

    #==========================================================================
    def createCommandReleaseInfo(self, config = {} ):
        
        """
        Create a command release information structure
        """
        # All parameters received here go to the additional info except
        # for the execution time.

        # Build the execution time parameter
        # The passed object shall be a TIME instance
        if not config.has_key(Time):
            executionTime = getAbsTime(0,0)
        else:
            timeInst = config.get(Time)
            if timeInst == 0:
                LOG("Setting execution time ASAP")
                executionTime = getAbsTime(0,0)
            elif type(timeInst) == int:
                LOG("Setting execution time from secs " + str(timeInst))
                executionTime = getAbsTime(timeInst,0)
            elif isinstance(timeInst,TIME) and timeInst.isRel():
                # Convert to absolute
                timeInst = (timeInst + NOW)
                LOG("Setting execution time: " + str(timeInst))
                executionTime = getAbsTime(timeInst.abs(),0)
            elif isinstance(timeInst,TIME) and timeInst.isAbs():
                LOG("Setting execution time: " + str(timeInst))
                executionTime = getAbsTime(timeInst.abs(),0)
            else:
                raise HiflyException("Bad execution time format")
        
        # Build the release info        
        release = ITC_INJ.ReleaseInfo(
                                      getAbsTime(0,0), # release time
                                      getAbsTime(0,0), # earliest release time
                                      getAbsTime(0,0), # latest release time
                                      executionTime,
                                      0, #exec register
                                      ITC.CHECK_ENABLED, # static ptv check
                                      ITC.CHECK_ENABLED, # dyn ptv check
                                      True, # cev flag
                                      ACK_FLAGS_ALL
                                      )
        
        # Get the additional info, using defaults first, then override
        addInfoDict = self.__addInfoValues.copy()
        if config.has_key(addInfo):
            LOG("Using user add info")
            for key in config.get(addInfo):
                if key in self.__addInfoKeys:
                    addInfoDict[key] = config.get(addInfo).get(key)

        # Complete the additional info depending on the platform:
        specificInfo = self.__specificAdditionalInfo(config)
        addInfoDict.update(specificInfo)
        
        # Build the additional info string
        addinfoStr = ""
        for key in addInfoDict.keys():
            if len(addinfoStr)!=0: addinfoStr = addinfoStr + ";"
            value = addInfoDict.get(key)
            LOG("Using additional info: " + repr(key) + ":" + repr(value))
            addinfoStr = addinfoStr + key + "=" + value
        LOG("Additional info: " + repr(addinfoStr))
        
        return [release,addinfoStr]

    #==========================================================================
    def createCommandGroupRequest(self, requestList, config):
        LOG("Create command group request")
        group = []
        for request in requestList:
            LOG("Create command group element")
            discriminator = None
            if isinstance( request, ITC_INJ.CommandRequest ):
                discriminator = ITC_INJ.GROUP_CMD
            elif isinstance( request, ITC_INJ.CommandRequestBlock ):
                discriminator = ITC_INJ.GROUP_BLOCK
            elif isinstance( request, ITC_INJ.SequenceRequest ):
                discriminator = ITC_INJ.GROUP_SEQUENCE
            else:
                discriminator = ITC_INJ.GROUP_CMD
            groupElement = ITC_INJ.GroupElement( discriminator, request )
            group += [ groupElement ]
        return group
        

    #==========================================================================
    def createCommandRequest(self, cmdItem, parameters, paramSets, config):
        
        cmdName = cmdItem.name()
        
        # Some non-relevant values
        context = ""
        destination = ""
        
        # Create the command request release information
        LOG("Creating release info")
        release,addinfo = self.createCommandReleaseInfo( config )

        
        return ITC_INJ.CommandRequest(
                            context,
                            destination,
                            self.__mapID,
                            self.__vcID,
                            cmdName,
                            parameters,
                            paramSets,
                            release,
                            self.__ilockType,
                            self.__ilockStage,
                            addinfo,
                            0)

    #==========================================================================
    def createSequenceRequest(self, seqItem, parameters, paramSets, config):

        seqName = seqItem.name()
        
        # Some non-relevant values
        context = ""
        destination = ""
        
        # Create the command request release information
        LOG("Creating release info")
        release,addinfo = self.createCommandReleaseInfo( config )

        return ITC_INJ.SequenceRequest(
                            context,
                            destination,
                            seqName,
                            parameters,
                            paramSets,
                            release,
                            True, # Apply info to commands
                            True, # Convert to inmediate
                            addinfo,
                            0)

    #==========================================================================
    def createCommandRequestBlock(self, releaseSet ):
        block = ITC_INJ.CommandRequestBlock( ITC_INJ.BLOCK_CMD, releaseSet )
        return block
    
    #==========================================================================
    def createCommandRequestSet(self, cmdNames, parameters, paramSets, config ):
        
        releaseSet = []
        
        for name in cmdNames:
            params = parameters.get(name)
            sets = paramSets.get(name)
            request = self.createCommandRequest( name, params, sets, config )
            releaseSet.append(request)
            
        return releaseSet
        
    #==========================================================================
    def getCommandStack(self, request):
        # We cannot proceed with an older EXIF version
        if self.__exifVersion != VERSION_6: return None
        
        try:
            stackCommands = self.__injector.getStackCmd( request )
            return stackCommands
        except:
            return None

    #==========================================================================
    def getCommandBlockStack(self, request):
        # We cannot proceed with an older EXIF version
        if self.__exifVersion != VERSION_6: return None
        
        try:
            stackCommands = self.__injector.getStackCmdBlock( request )
            return stackCommands
        except:
            return None
        
    #==========================================================================
    def getSequenceStack(self, request, notifType ):
        # We cannot proceed with an older EXIF version
        if self.__exifVersion != VERSION_6: return None
        
        try:
            stackCommands = self.__injector.getStackSeq( request, notifType )
            return stackCommands
        except:
            return None
        
    #==========================================================================
    def getGroupStack(self, request):
        # We cannot proceed with an older EXIF version
        if self.__exifVersion != VERSION_6: return None
        
        try:
            stackCommands = self.__injector.getStackGroup( request )
            return stackCommands
        except:
            return None
        
    #==========================================================================
    def __getAddInfoDefaults(self):

        aiFile = file(self.__addInfoFile)
        self.__addInfoKeys = []
        self.__addInfoValues = {}
        for line in aiFile.readlines():
            items = line.split()
            key = items[0]
            self.__addInfoKeys.append(key)
            if len(items)>1:
                value = items[1]
                self.__addInfoValues[key] = value
                LOG("Loaded default addinfo: " + repr(key) + ":" + repr(value))
        aiFile.close()

    #==========================================================================
    def __specificAdditionalInfo(self, config = {} ):
        if (len(config)==0): return {}
        
        result = {}

        if self.__scPlatform == PLATFORM_S13:
            if config.has_key(LoadOnly):
                result['ANOOP'] = 'OFF'
                
        return result
