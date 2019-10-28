###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.config 
FILE
    config.py
    
DESCRIPTION
    Setup environment for correct core driver instantiation
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    01/10/2007
"""

###############################################################################

#*******************************************************************************
# SPELL Imports
#*******************************************************************************
from spell.utils.log import *
from spell.config.reader import *
from spell.config.constants import COMMON
from spell.lib.registry import REGISTRY
from spell.lib.exception import DriverException

#*******************************************************************************
# Local Imports
#*******************************************************************************
from interface.model import SimulatorModel

#*******************************************************************************
# System Imports
#*******************************************************************************
import os

###############################################################################
# Module import definition

__all__ = ['CONFIG']

INTERFACE_DEFAULTS = {}

###############################################################################
# Superclass
import spell.lib.adapter.config
superClass = spell.lib.adapter.config.ConfigInterface
        
###############################################################################
class ConfigInterface(superClass):

    #==========================================================================
    def __init__(self):
        superClass.__init__(self)
        LOG("Created")
    
    #==========================================================================
    def setup(self, contextName):
        superClass.setup(self, contextName)
        LOG("Setup standalone CFG interface")
        dataPath = Config.instance().getRuntimeDir()
        driver = Config.instance().getContextConfig(contextName).getDriver()
        driverInfo = Config.instance().getDriverConfig(driver)
        simulationPath = driverInfo['SimPath']
        simulationFile = Config.instance().getContextConfig(contextName).getDriverConfig('Simulation')
        home = Config.instance().getHome()
        if home is None:
            raise DriverException("SPELL home is not defined")
        
        LOG("Loading simulation: " + simulationFile)
        simulationFile = dataPath + os.sep +  simulationPath + \
                         os.sep + simulationFile
        SIM = SimulatorModel()
        SIM.tmClass = REGISTRY['TM']
        SIM.tcClass = REGISTRY['TC']
        SIM.setup( simulationFile )
        REGISTRY['SIM'] = SIM

    #==========================================================================
    def cleanup(self, shutdown = False):
        superClass.cleanup(self, shutdown)
        LOG("Cleanup standalone CFG interface")
        REGISTRY['SIM'].cleanup()
        REGISTRY.remove('SIM')
                
###############################################################################
# Interface instance
CONFIG = ConfigInterface()
