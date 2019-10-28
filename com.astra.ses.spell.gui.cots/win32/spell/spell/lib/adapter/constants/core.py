###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.constants.core
FILE
    misc.py
DESCRIPTION
    Core constants and identifiers
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    01/10/2007
"""
###############################################################################

from spell.lang.constants import eq,neq,lt,le,gt,ge,bw,nbw

###############################################################################
# AVAILABLE DRIVER IDENTIFIERS
DRIVER_HIFLY = "hifly"
DRIVER_DUMMY = "STANDALONE"
DRIVER_SCORPIO = "SCORPIO"

KNOWN_DRIVERS = [ DRIVER_HIFLY, DRIVER_DUMMY, DRIVER_SCORPIO ]

DRIVER_PACKAGES = { DRIVER_HIFLY:'spell.lib.hifly', 
                    DRIVER_DUMMY:'spell.lib.dummy',
                    DRIVER_SCORPIO:'spell.lib.scorpio' }

###############################################################################
# Services
SVC_EXMGR = 'EXMGR'
SVC_TM = 'TM'
SVC_TC = 'TC'
SVC_UI = 'UI'
SVC_SMGR = 'SMGR'
SVC_PMGR = 'PMGR'

###############################################################################
KEY_SEPARATOR = ":"

###############################################################################
COMP_SYMBOLS = { eq:"=", neq:"!=", lt:"<", le:"<=", gt:">", ge:">=", bw:"bw", nbw:"nbw" }


