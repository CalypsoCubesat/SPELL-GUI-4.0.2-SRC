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
from spell.lang.functions import Verify
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
class TestVerify(unittest.TestCase):
    
    tm = None
    
    #===========================================================================
    def setUp(self):
        self.tm = FakeTmClass()
        REGISTRY['TM'] = self.tm
        REGISTRY['CIF'] = FakeClientInterface()
        self.tm.setConfig({Notify:False})
        
    #===========================================================================
    def tearDown(self):
        self.tm = None
        REGISTRY.remove('TM')
    
    #===========================================================================
    def test_single_verification_true(self):
        self.assertTrue(Verify('TEST', eq, 'VALUE'))
        
    #===========================================================================
    def test_single_verification_false(self):
        self.assertFalse(Verify('TEST', eq, 'STHING'))

    #===========================================================================
    def test_single_verification_failure_nonexistent(self):
        self.assertRaises(DriverException,Verify, 'NOEXIST', eq, 'STHING', {PromptUser:False,HandleError:False})

    #===========================================================================
    def test_composed_verification_true(self):
        self.assertTrue(Verify(['TEST', eq, 'VALUE']))

    #===========================================================================
    def test_composed_verification_false(self):
        self.assertFalse(Verify(['TEST', eq, 'STHING']))

    #===========================================================================
    def test_verification_list_true_true(self):
        self.assertTrue(Verify([['TEST1', eq, 'VALUE'],['TEST2', eq, 'VALUE']]))

    #===========================================================================
    def test_verification_list_true_false(self):
        self.assertFalse(Verify([['TEST1', eq, 'VALUE'],['TEST2', eq, 'STHING']]))

    #===========================================================================
    def test_verification_list_false_false(self):
        self.assertFalse(Verify([['TEST1', eq, 'STHING'],['TEST2', eq, 'STHING']]))

    #===========================================================================
    def test_ontrue_and_skip(self):
        REGISTRY['CIF'].promptAnswer = 'K'
        self.assertTrue(Verify(['TEST', eq, 'VALUE'], {OnTrue:PROMPT}))

    #===========================================================================
    def test_ontrue_and_cancel(self):
        REGISTRY['CIF'].promptAnswer = 'Q'
        self.assertFalse(Verify(['TEST', eq, 'VALUE'], {OnTrue:PROMPT}))

    #===========================================================================
    def test_onfalse_and_skip(self):
        REGISTRY['CIF'].promptAnswer = 'K'
        self.assertTrue(Verify(['TEST', eq, 'STHING'], {OnFalse:PROMPT}))

    #===========================================================================
    def test_onfalse_and_cancel(self):
        REGISTRY['CIF'].promptAnswer = 'Q'
        self.assertFalse(Verify(['TEST', eq, 'STHING'], {OnFalse:PROMPT}))

    #===========================================================================
    def test_auto_skip(self):
        REGISTRY['CIF'].promptAnswer = 'X'
        self.assertTrue(Verify(['NOEXIST', eq, 'VALUE'], {OnFailure:SKIP,PromptUser:False}))

    #===========================================================================
    def test_auto_cancel(self):
        REGISTRY['CIF'].promptAnswer = 'X'
        self.assertFalse(Verify(['NOEXIST', eq, 'VALUE'], {OnFailure:CANCEL,PromptUser:False}))

    #===========================================================================
    def test_syntax_fail_1(self):
        self.assertRaises(SyntaxException, Verify)

    #===========================================================================
    def test_syntax_fail_2(self):
        self.assertRaises(SyntaxException, Verify, 'T025', 'hola')
        
    #===========================================================================
    def test_syntax_fail_3(self):
        self.assertRaises(SyntaxException, Verify, ['T025'])

    #===========================================================================
    def test_syntax_fail_4(self):
        self.assertRaises(SyntaxException, Verify, [['T025']])
        

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestVerify)
    