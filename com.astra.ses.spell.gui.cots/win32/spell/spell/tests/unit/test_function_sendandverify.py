################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_function_verify
FILE
    test_function_verify.py
    
DESCRIPTION
    Unit tests for Verify function
    
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
from spell.lang.functions import SendAndVerify
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.registry import REGISTRY
from spell.lib.exception import *

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest

#*******************************************************************************
# Local imports
#*******************************************************************************
from tools import *

################################################################################
class TestSendAndVerify(unittest.TestCase):
    
    tm = None
    tc = None
    
    #===========================================================================
    def setUp(self):
        self.tm = FakeTmClass()
        self.tc = FakeTcClass()
        REGISTRY['TC'] = self.tc
        REGISTRY['TM'] = self.tm
        REGISTRY['CIF'] = FakeClientInterface()
        self.tc.setConfig({Notify:False})
        
    #===========================================================================
    def tearDown(self):
        self.tc = None
        REGISTRY.remove('TC')
        self.tm = None
        REGISTRY.remove('TM')
    
    #===========================================================================
    def test_send_cmdname(self):
        self.assertTrue(SendAndVerify( command = 'TC_OK') )

    #===========================================================================
    def test_send_item(self):
        tc = self.tc['TC_OK']
        self.assertTrue(SendAndVerify( command = tc ))

    #===========================================================================
    def test_send_syntax_fail_1(self):
        raised = False
        try:
            SendAndVerify()
        except:
            raised = True
        self.assertTrue(raised)

    #===========================================================================
    def test_send_syntax_fail_2(self):
        raised = False
        try:
            SendAndVerify( command = 'TC_OK', args = [] )
        except:
            raised = True
        self.assertTrue(raised)

    #===========================================================================
    def test_send_syntax_fail_3(self):
        raised = False
        try:
            SendAndVerify( 'TC_OK', args = [] )
        except:
            raised = True
        self.assertTrue(raised)

    #===========================================================================
    def test_send_cmdname_fail_skip(self):
        REGISTRY['CIF'].promptAnswer = "K"
        self.assertTrue(SendAndVerify( command = 'TC_FAIL'))

    #===========================================================================
    def test_send_cmdname_fail_cancel(self):
        REGISTRY['CIF'].promptAnswer = "Q"
        self.assertFalse(SendAndVerify( command = 'TC_FAIL'))

    #===========================================================================
    def test_send_cmdname_verify_simple(self):
        self.assertTrue(SendAndVerify(command = 'TC_OK', verify = ['TEST', eq, 'VALUE']))

    #===========================================================================
    def test_send_cmdname_verify_simple_failtc_skip(self):
        REGISTRY['CIF'].promptAnswer = "K"
        self.assertTrue(SendAndVerify( command = 'TC_FAIL', verify = ['TEST', eq, 'VALUE']))

    #===========================================================================
    def test_send_cmdname_verify_simple_failtc_skip(self):
        REGISTRY['CIF'].promptAnswer = "Q"
        self.assertFalse(SendAndVerify( command = 'TC_FAIL', verify = ['TEST', eq, 'VALUE']))

    #===========================================================================
    def test_send_cmdname_verify_simple_failtm_skip(self):
        REGISTRY['CIF'].promptAnswer = "K"
        self.assertTrue(SendAndVerify( command = 'TC_OK', verify = ['TEST', eq, 'STHING']))

    #===========================================================================
    def test_send_cmdname_verify_simple_failtm_cancel(self):
        REGISTRY['CIF'].promptAnswer = "Q"
        self.assertFalse(SendAndVerify( command = 'TC_OK', verify = ['TEST', eq, 'STHING']))

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSendAndVerify)
    