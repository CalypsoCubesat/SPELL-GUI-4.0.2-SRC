#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_ev_injection.py
    
DESCRIPTION
    System test for the hifly event injection low level interface.
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly import *

hiflyc.setup( "egatec2", "29999", "S1M2", "PRIME" )
hiflyc.authenticate( "keys/OPE_USER", "OPE_USER" )
hiflyc.activate()

evi.setup()
evi.setEventParams( "SPEL", "N/A", "S1M2" )
evi.injectEvent( "Test event", EV_SCOPE_SYSTEM, EV_SEV_INFORMATION )
evi.cleanup()
