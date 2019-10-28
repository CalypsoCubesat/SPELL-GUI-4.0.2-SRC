###############################################################################
"""
Date: 01/07/2008

Project: UGCS/USL

Description
===========

TC item for simulations in standalone driver.

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
from spell.lib.adapter.tc_item import TcItemClass

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['TcItemSimClass']

#*******************************************************************************
# Module globals
#*******************************************************************************

################################################################################
class TcItemSimClass(TcItemClass):

    tmItemName = None
    changeDef = None

    def __init__(self, model, name, tmItemName, change):
        TcItemClass.__init__(self,model.tcClass,name)
        self.tmItemName = tmItemName
        self.changeDef = change
        
    def getTmItemName(self):
        return self.tmItemName
    
    def getTmChange(self):
        return self.changeDef

################################################################################
