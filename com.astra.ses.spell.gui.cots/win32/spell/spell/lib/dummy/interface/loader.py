###############################################################################
"""
Date: 01/07/2008

Project: UGCS/USL

Description
===========

Model loader for standalone simulator

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
from spell.utils.log import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from tm_sim_item import *
from tc_sim_item import *

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['ModelLoader']

#*******************************************************************************
# Module globals
#*******************************************************************************

TM_ITEMS = 0
TC_ITEMS = 1

################################################################################
class ModelLoader(object):
    
    model = None
    section = None
    tmItems = {}
    tcItems = {}

    #===========================================================================    
    def __init__(self, model):
        self.model = model
        self.section = None
        self.tmItems = {}
        self.tcItems = {}
        
    #===========================================================================    
    def loadFromFile(self, defFile):
        dfn = file(defFile)
        for line in dfn.readlines():
            line = line.strip()
            if line.startswith('#') or len(line)==0: continue
            if line == '[TM ITEMS]':
                self.section = TM_ITEMS
            elif line == '[TC ITEMS]':
                self.section = TC_ITEMS
            else:
                if self.section is None: continue
                elif self.section == TM_ITEMS:
                    components = line.split(";")
                    name = components[0].strip()
                    if name in self.tmItems.keys():
                        LOG("WARNING: discarding duplicated entry for " + repr(name))
                        continue
                    descr = components[1].strip()
                    raw = components[2].strip()
                    eng = components[3].strip()
                    if len(components)>=5:
                        period = int(components[4].strip())
                    else:
                        period = 0
                    self.tmItems[name] = TmItemSimClass(self.model, name, descr, raw, eng, period)
                    LOG("Loaded simulated TM item: " + repr(name))
                elif self.section == TC_ITEMS:
                    components = line.split(";")
                    name = components[0].strip()
                    if name in self.tcItems.keys():
                        LOG("WARNING: discarding duplicated entry for " + repr(name))
                        continue
                    tmitem = components[1].strip()
                    change = components[2].strip()
                    self.tcItems[name] = TcItemSimClass(self.model,name,tmitem,change)
                    LOG("Loaded simulated TC item: " + repr(name))
        return [self.tmItems,self.tcItems]

################################################################################
