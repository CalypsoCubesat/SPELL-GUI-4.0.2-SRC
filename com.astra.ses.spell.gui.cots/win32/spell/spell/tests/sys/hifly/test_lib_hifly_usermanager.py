#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_usermanager.py
    
DESCRIPTION
    System test for the hifly user manager interface.
    
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

user.setup( "egatec2", "29999", "PRIME" )

user.login( "command", "cmd", "CMD_001", "S1M2", "egatec2", 4 )
#user.logout( "S1M2", "egatec2" )
 


