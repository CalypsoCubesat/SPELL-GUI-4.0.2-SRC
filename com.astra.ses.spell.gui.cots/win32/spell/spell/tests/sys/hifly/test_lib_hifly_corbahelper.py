#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_corbahelper.py
    
DESCRIPTION
    System test for the hifly CORBA helper.
    Setups a connection to the given server:port and
    authenticates the connection with hifly.
    
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

CONN.setup( "egatec2", "29999", "S1M2", "PRIME" )
CONN.authenticate( "keys/OPE_USER", "OPE_USER" )
CONN.activate()
CONN.start()
