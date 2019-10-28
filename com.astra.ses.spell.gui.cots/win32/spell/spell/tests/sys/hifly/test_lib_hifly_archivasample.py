#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_archivasample.py
    
DESCRIPTION
    Example script for USL usage in hifly clients remote control.
    
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

user.setup( "egatec2", "29999", "PRIME" )
taskm.setup( "egatec2", "29999" )

taskm.useWorkstation( "egaws4" )
user.logout( "S1M1", "egaws4" )
user.logout( "S1M2", "egaws4" )
user.login( "command", "cmd", "CMD_002", "S1M1", "egaws4", 1 )
user.login( "command", "cmd", "CMD_003", "S1M2", "egaws4", 2 )

s1m1_el = DefaultTaskDelegate("Event logger on S1M1")
s1m2_el = DefaultTaskDelegate("Event logger on S1M2")

try:
	input("Press enter to start domain S1M1\n")
except: pass

taskm.useDomainFamily( "S1M1", "PRIME" )
#taskm.registerClientProcess( "Event logger S1M1", "Event_LoggerClass", s1m1_el )
taskm.startProcess( PROCESS_CLIENT, "LAUNCHER", "-w 1 ../config/MMI/MMI_mm_s1m1" )
taskm.startProcess( PROCESS_CLIENT, "Event_LoggerClass", "-w 1" )

try:
	input("Press enter to start domain S1M2\n")
except: pass

taskm.useDomainFamily( "S1M2", "PRIME" )
#taskm.registerClientProcess( "Event logger S1M2", "Event_LoggerClass", s1m2_el )
taskm.startProcess( PROCESS_CLIENT, "LAUNCHER", "-w 1 ../config/MMI/MMI_mm_s1m2" )
taskm.startProcess( PROCESS_CLIENT, "Event_LoggerClass", "-w 1" )

