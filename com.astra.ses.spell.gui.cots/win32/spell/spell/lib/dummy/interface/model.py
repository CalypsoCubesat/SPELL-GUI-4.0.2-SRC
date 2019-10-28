###############################################################################
"""
Date: 01/07/2008

Project: UGCS/USL

Description
===========

Simulator for standalone driver.

Authoring
=========

@organization: SES Astra / SES Engineering

@copyright: This software is the copyrighted work of SES Engineering S.A. 
            All rights reserved.
            
@license: License information
    
@author: Rafael Chinchilla Camara (GMV Aerospace & Defence S.A.)
@author: Fabien Bouleau (SES Engineering S.A.)

@version: 1.0
@requires: Python 2.5.x"""

################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.lib.adapter.config import Configurable
from spell.lib.exception import *
from spell.lang.constants import *
from spell.lang.modifiers import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from loader import ModelLoader
from tm_sim_item import *
from tc_sim_item import *

#*******************************************************************************
# System imports
#*******************************************************************************
import time,os,sys
import threading,thread

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['SimulatorModel']

#*******************************************************************************
# Module globals
#*******************************************************************************

################################################################################
class SimulatorModel(threading.Thread,Configurable):
    
    tmClass = None
    tcClass = None
    currentTime = None
    isWorking = True
    lock = None
    tmItems = {}
    tcItems = {}

    #===========================================================================    
    def __init__(self):
        threading.Thread.__init__(self)
        Configurable.__init__(self)
        self.tmClass = None
        self.tcClass = None
        self.currentTime = time.time()
        self.isWorking = True
        self.lock = thread.allocate_lock()
        self.tmItems = {}
        self.tcItems = {}
    
    #===========================================================================    
    def working(self, w = None):
        self.lock.acquire()
        if w is None:
            ret = self.isWorking
        else:
            self.isWorking = w
            ret = None
        self.lock.release()
        return ret
    
    #===========================================================================    
    def setup(self, defFile = None):
        # Load simulated items
        if defFile:
            self.load(defFile)
        self.start()

    #===========================================================================    
    def load(self, defFile):
        loader = ModelLoader(self)
        tmItems,tcItems = loader.loadFromFile(defFile)
        self.tmItems = tmItems
        self.tcItems = tcItems
    
    #===========================================================================    
    def cleanup(self):
        self.working(False)
    
    #===========================================================================    
    def run(self):
        while (self.working()):
            time.sleep(1)
            self.lock.acquire()
            self.currentTime = time.time()
            for itemName in self.tmItems.keys():
                self.tmItems[itemName].refreshSimulatedValue()
            self.lock.release()
                
    def getCurrentTime(self):
        return self.currentTime
    
    #===========================================================================    
    def executeCommand(self, tcItemName):
        
        tcItem = self.getTCitem(tcItemName)
        
        tmItemName = tcItem.getTmItemName()
        
        tmItem = self.getTMitem(tmItemName)
        
        changeDef = tcItem.getTmChange()
        self.lock.acquire()
        tmItem.change( changeDef )
        self.lock.release()

    #===========================================================================    
    def changeItem(self, tmItemName, value):
        tmItem = self.getTMitem(tmItemName)
        tmItem.change(value)

    #===========================================================================    
    def getTMitem(self, name, description = ""):
        if not self.tmItems.has_key(name):
            tmItem = TmItemSimClass(self,name,description,'0','"SIMVALUE"', 0)
        else:
            tmItem = self.tmItems[name]
        return tmItem

    #===========================================================================    
    def getTCitem(self, name):
        tcItem = TcItemSimClass(self,name,'PARAM','0')
        return tcItem
