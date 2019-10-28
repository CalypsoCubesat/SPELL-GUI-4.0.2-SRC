#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_appmanager.py
    
DESCRIPTION
    System test for the hifly application manager interface.
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly.task import *

from time import sleep

class Delegate:

	def applicationStarted(self):
		print "Delegate: started"

	def applicationStarting(self):
		print "Delegate: starting"

	def applicationStopped(self):
		print "Delegate: stopped"

	def applicationDied(self):
		print "Delegate: died"

	def applicationUnknown(self):
		print "Delegate: unknown"
	

D = Delegate()

TASKM.setup( "egatec2", "29999" )
TASKM.useWorkstation( "egatec2" )
TASKM.useDomainFamily( "S1M2", "PRIME" )

TASKM.startProcess( PROCESS_CORE, "SAPIF", "" )

sleep(3)

print TASKM.processStatus( PROCESS_CORE, "SAPIF" )

sleep(5)

