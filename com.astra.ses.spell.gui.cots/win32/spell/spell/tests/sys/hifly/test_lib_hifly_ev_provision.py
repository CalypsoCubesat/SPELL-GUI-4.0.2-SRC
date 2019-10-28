#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_lib_hifly_ev_provision.py
    
DESCRIPTION
    System test for the hifly event provision low level interface.
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly.connection import AUTH
from spell.lib.hifly.ev import *
import spell.lib.adapter.ev 

class MyView(spell.lib.adapter.ev.EvView):

        def notifyEvent(self, sec, usec, ID, text, app, ws, scope, sev, scid ):
                print "EVENT: ",sec,usec,ID,text,app,ws,scope,sev,scid

AUTH.setup( "EGATEC2_NS", "egatec2", "29999", "S2B2", "PRIME" )
AUTH.authenticate( "../data/keys/OPE_USER", "OPE_USER" )

EV = ev_class()
EV.setup()
VIEW = MyView()

EV.registerForEvents( VIEW, TIME_MODE_FWD, 1196085600, 0, False )

for i in range(0,10):
        EV.pullEvents()

try:
        input()
except: pass

EV.cleanup()
AUTH.cleanup()
