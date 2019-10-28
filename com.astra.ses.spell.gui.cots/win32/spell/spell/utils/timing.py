################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.utils.timing
FILE
    timing.py
    
DESCRIPTION
    Performance and timing utilities
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV) & Fabien Bouleau (SES Engineering)
"""

################################################################################

#*******************************************************************************
# SPELL Imports
#*******************************************************************************
from spell.utils.log import *

#*******************************************************************************
# Local Imports
#*******************************************************************************
 
#*******************************************************************************
# System Imports
#*******************************************************************************
import time,sys
 
#*******************************************************************************
# Exceptions 
#*******************************************************************************
 
#*******************************************************************************
# Module globals
#*******************************************************************************

################################################################################
class TMR(object):
    
    @staticmethod
    def tick(name = "."):
        
        import __main__
        
        if not __main__.__dict__.get('TIMING'):
            __main__.__dict__['TIMING'] = time.clock()
        else:
            current = time.clock()
            theTime = current - __main__.__dict__.get("TIMING")
            LOG("*************************** [" + name + "] time: %.2g" % theTime)
            __main__.__dict__.pop("TIMING")

    @staticmethod
    def time():
        LOG("*********************************** " + repr(time.time()))
        