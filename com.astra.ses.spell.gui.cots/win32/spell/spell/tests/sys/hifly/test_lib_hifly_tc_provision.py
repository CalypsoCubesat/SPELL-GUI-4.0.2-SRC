#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_tc_provision.py
    
DESCRIPTION
    System test for the hifly telecommand provision (live) low level interface.
    
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

hiflyc.setup( "a1msrv01", "29999", "A2B", "PRIME" )
hiflyc.authenticate( "keys/OPE_USER", "OPE_USER" )
hiflyc.activate()

tc.setup()
tc.registerForCommand()
hiflyc.startBackground()

print "WAITING 60 SECONDS BEFORE SHUTDOWN"
sleep(60)

tc.cleanup()
hiflyc.stop()
