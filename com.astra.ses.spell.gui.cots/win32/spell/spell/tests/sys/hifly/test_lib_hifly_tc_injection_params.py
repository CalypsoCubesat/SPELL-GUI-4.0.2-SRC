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

from spell.utils.log import LoggerClass
from spell.lib.hifly.connection import CONN
from spell.lib.hifly.tc import TC_INJ
from spell.lib.hifly.value import Variant
import IBASE
from time import sleep

LoggerClass.globalEnableLog(True)

CONN.setup( "egatec2", "29999", "S1M2", "PRIME" )
CONN.authenticate( "keys/OPE_USER", "OPE_USER" )
CONN.activate()

TC_INJ.setup()
val1 = Variant( IBASE.IS_LONG, 0 )
val2 = Variant( IBASE.IS_LONG, 1 )
val3 = Variant( IBASE.IS_LONG, 49249 )
val4 = Variant( IBASE.IS_LONG, 32890 )
val5 = Variant( IBASE.IS_LONG, 0 )

p1 = TC_INJ.commandParam( "YTRLYF22OF_1", True, True, "", IBASE.HEXADECIMAL, val1 )
p2 = TC_INJ.commandParam( "YTRLYF22OF_2", True, True, "", IBASE.HEXADECIMAL, val2 )
p3 = TC_INJ.commandParam( "YTRLYF22OF_3", True, True, "", IBASE.HEXADECIMAL, val3 )
p4 = TC_INJ.commandParam( "YTRLYF22OF_4", True, True, "", IBASE.HEXADECIMAL, val4 )
p5 = TC_INJ.commandParam( "YTRLYF22OF_5", True, True, "", IBASE.HEXADECIMAL, val5 )

parameters = [ p1, p2, p3, p4, p5 ]
TC_INJ.sendCommand( "YTRLYF22OF", parameters, [], None )

sleep(10)
TC_INJ.cleanup()
