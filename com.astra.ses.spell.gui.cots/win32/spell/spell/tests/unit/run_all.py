################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.run_all
FILE
    run_all.py
    
DESCRIPTION
    Launcher for all unit tests
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""
################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.log import *

#*******************************************************************************
# System imports
#*******************************************************************************
import os,sys,unittest

#*******************************************************************************
# Globals
#*******************************************************************************
LOGFILE = file("utests.log", "w")
LOG.showlog = False

################################################################################
if __name__ == "__main__":
    
    def log(msg, newLine = True):
        LOGFILE.write( msg + "\n" )
        if newLine:
            print msg
        else:
            print msg,
    
    # Will hold the list of modules with unit tests    
    test_list = []
    # Will execute the test suites
    runner = unittest.TextTestRunner( stream=LOGFILE, descriptions = False, verbosity = False )
            
    # Load the tests. Only those modules within this directory 'unit', whose
    # name starts with 'test_' will be loaded.
    log("**********************************************************************")
    log("Loading tests")
#    files = os.listdir(".")
#    for f in files:
#        if f.startswith("test_") and not f.endswith("pyc"):
#            test_list.append(f.split(".")[0])
#            log("     - Added test: " + repr(f))
    test_list = [
                 'test_ttime',
                 'test_adapter_tm',
                 'test_tm_item',
                 'test_tc_item',
                 'test_basehelper',
                 'test_function_prompt',
                 'test_function_gettm',
                 'test_function_verify',
                 'test_function_send',
                 'test_function_sendandverify',
                ]
    test_names = [
                 "TIME interface",
                 "TM Adapter Interface",
                 "TM Items",
                 "TC Items",
                 "Base Helper",
                 "Prompt()",
                 "GetTM()",
                 "Verify()",
                 "Send()",
                 "SendAndVerify()",
                 ]
    
    # Run the suites
    log("**********************************************************************")
    log("Running tests\n")
    success = True
    count = 0
    for test in test_list:
        # Import the current module
        module = __import__( test, globals(), locals(), [], -1 )
        # Extract the 'suite' function from the module
        if module.__dict__.has_key('suite'):
            suiteFn = module.__dict__.get('suite')
            # Execute the suite function to retrieve the test suite object
            testSuite = suiteFn()
            log("     - Test suite for " + test_names[count] + " -- " + repr(test) + " (" +\
                 str(testSuite.countTestCases()) + " test cases)", False)
            # Execute the test suite
            result = runner.run(testSuite)
            if result.wasSuccessful():
                print ": OK"
            else:
                print ": FAILED"
            success = success and result.wasSuccessful()
        else:
            msg = "ERROR: unable to load test suite from module " + repr(module)
            log(msg)
        count = count+1
    
    # Finish
    log("**********************************************************************")
    if success:
        log("SUCCESS")
        sys.exit(0)
    else:
        log("FAILED")
        sys.exit(1)

    
    
