#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_pm.py
    
DESCRIPTION
    System test for the hifly parameter manager implementation
    
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
from time import sleep

hiflyc.setup( "egatec2", "29999", "S1M2", "PRIME" )
hiflyc.authenticate( "keys/OPE_USER", "OPE_USER" )
hiflyc.activate()
hiflyc.startBackground()
tm.setup()

cont = 0
while cont < 10:
	value = TheParameterManager.getParameterValue("SPMFCNM", DEF, False)
	print "PARAMETER VALUE:", value
	sleep(2.5)
	cont = cont + 1

tm.cleanup()
hiflyc.stop()
