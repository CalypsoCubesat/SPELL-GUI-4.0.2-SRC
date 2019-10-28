#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_tm_provision_ret.py
    
DESCRIPTION
    System test for the hifly telemetry provision (retrieval) low level interface.
    
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

tm.setup()
tm.setTimeMode( ACCESS_TIME_BWD )
tm.setTime( 1190306400, 0, False )
tm.registerTM("SPMFCNM")
#tm.registerTM("SUOBTCOAR")
for count in range(0,20):
    tm.step()
tm.cleanup()
