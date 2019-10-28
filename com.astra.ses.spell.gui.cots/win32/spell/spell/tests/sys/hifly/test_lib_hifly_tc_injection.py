#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_tc_injection.py
    
DESCRIPTION
    System test for the hifly telecommand injection low level interface.
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly.connection import CONN
from spell.lib.hifly.tc import TC_INJ
from time import sleep
from spell.utils.log import LoggerClass

LoggerClass.globalEnableLog(True)

CONN.setup( "egatec2", "29999", "S1M2", "PRIME" )
CONN.authenticate( "keys/OPE_USER", "OPE_USER" )
CONN.activate()

TC_INJ.setup()
TC_INJ.setMapId(255)
TC_INJ.setVcId(255)
TC_INJ.sendCommand("DDSLTEST", [], [], None)

sleep(10)
TC_INJ.cleanup()






