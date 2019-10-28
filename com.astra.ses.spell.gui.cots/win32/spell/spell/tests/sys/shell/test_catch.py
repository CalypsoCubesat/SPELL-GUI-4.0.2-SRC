#!/usr/bin/python
###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests 
FILE
    test_catch.py
    
DESCRIPTION
    System test for testing with try catch
    
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

print
print

try:
	TM.verifyStep( [ 'B167', bw, 0, 1, { Retries:1, ValueFormat:RAW, IsStrict: True} ] )
except TM.VerifyException,e:
	print "FAILED: ",e.reason

print
print

try:
        TM.verify( [ [ 'B167', bw, 0, 1, { Retries:1, ValueFormat:RAW, IsStrict: True} ] ] )
except DriverException,e:
        print "FAILED: ",e.reason


# Must cleanup before exiting. It is MANDATORY for hifly driver,
# but not required for standalone driver.
Cleanup()
