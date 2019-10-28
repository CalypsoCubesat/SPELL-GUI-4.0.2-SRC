#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_catch.py
    
DESCRIPTION
    System test for testing event provision using the standalone interface
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lang.shell import *
from spell.utils.ttime import tt
import spell.lib.adapter.ev 

class MyView(spell.lib.adapter.ev.EvView):

        def notifyEvent(self, sec, usec, ID, text, app, ws, scope, sev, scid ):
                print "EVENT: ",sec,usec,ID,text,app,ws,scope,sev,scid

Setup("EGATEC2_S2B2_BACKUP")

from __main__ import EV

VIEW = MyView()

theTime = tt('17/01/2008 17:00').abs()

EV.registerForEvents( VIEW, TIME_MODE_FWD, theTime, 0, False )

for i in range(0,10):
    EV.pullEvents()

try:
    input()
except: pass

Cleanup()
