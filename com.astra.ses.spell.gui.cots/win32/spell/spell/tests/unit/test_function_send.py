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
from spell.lang.functions import Send
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
class TestSend(unittest.TestCase):
    
    tc = None
    
    #===========================================================================
    def setUp(self):
        self.tc = FakeTcClass()
        REGISTRY['TC'] = self.tc
        REGISTRY['CIF'] = FakeClientInterface()
        self.tc.setConfig({Notify:False})
        
    #===========================================================================
    def tearDown(self):
        self.tc = None
        REGISTRY.remove('TC')
    
    #===========================================================================
    def test_send_cmdname(self):
        self.assertTrue(Send( command = 'TC_OK'))

    #===========================================================================
    def test_send_item(self):
        tc = self.tc['TC_OK']
        self.assertTrue(Send( command = tc))

    #===========================================================================
    def test_send_syntax_fail_1(self):
        self.assertRaises(SyntaxException, Send)

    #===========================================================================
    def test_send_syntax_fail_2(self):
        raised = False
        try:
            Send( command = 'TC_OK', args = [] )
        except:
            raised = True
        self.assertTrue(raised)

    #===========================================================================
    def test_send_syntax_fail_3(self):
        raised = False
        try:
            Send( 'TC_OK', args = [] )
        except:
            raised = True
        self.assertTrue(raised)

    #===========================================================================
    def test_send_cmdname_fail_skip(self):
        REGISTRY['CIF'].promptAnswer = "K"
        self.assertTrue(Send( command = 'TC_FAIL'))

    #===========================================================================
    def test_send_cmdname_fail_cancel(self):
        REGISTRY['CIF'].promptAnswer = "Q"
        self.assertFalse(Send( command = 'TC_FAIL'))

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestSend)
    