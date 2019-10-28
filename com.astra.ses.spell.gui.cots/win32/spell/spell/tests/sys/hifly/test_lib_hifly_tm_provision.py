#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_tm_provision.py
    
DESCRIPTION
    System test for the hifly tm provision (live) low level interface.
    
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
hiflyc.startBackground()

tm.setup()
tm.registerTM("SPMFCNM")
tm.registerTM("SUOBTCOAR")

try: 
    input("Type enter to shutdown") 
except: 
    pass

tm.cleanup()
hiflyc.stop()
