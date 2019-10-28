#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_shell_getconst.py
    
DESCRIPTION
    System test for the shell mode
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

# Setup the shell mode
from spell.lang.shell import *
# Initialize the environment and driver. If no driver is given,
# the standalone is used.
Setup()
# Obtain the internal objects from __main__ package.
# Used objects are:
# - TM for telemetry issues
# - TC for telecommands
# - ENV for environment
# - PM for telemetry parameters management (used by TM)
# - UI user interface
from __main__ import TM

# Once imported, TM object can be used directly instead of using a wrapper
# function.
TM['B167'].refresh()

print "B167 ENG=", TM['B167'].eng()
print "B167 RAW=", TM['B167'].raw()

# Must cleanup before exiting. It is MANDATORY for hifly driver,
# but not required for standalone driver.
Cleanup()
