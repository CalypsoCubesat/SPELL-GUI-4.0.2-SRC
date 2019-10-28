################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_function_prompt
     
FILE
    test_function_prompt.py
    
DESCRIPTION
    Unit tests for Prompt function
    
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
from spell.lang.functions import Prompt
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.registry import REGISTRY

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest

#*******************************************************************************
# Local imports
#*******************************************************************************
from tools import FakeClientInterface

################################################################################
class TestPrompt(unittest.TestCase):
    
    cif = None
    
    #===========================================================================
    def setUp(self):
        self.cif = FakeClientInterface()
        REGISTRY['CIF'] = self.cif
        
    #===========================================================================
    def tearDown(self):
        self.cif = None
        REGISTRY.remove('CIF')
    
    #===========================================================================
    def test_default(self):
        self.cif.promptAnswer = True
        result = Prompt("MESSAGE")
        self.assertTrue(result)
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, OK_CANCEL )

    #===========================================================================
    def test_ok_modifier(self):
        result = Prompt("MESSAGE", {Type:OK} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, OK )

    #===========================================================================
    def test_ok_parameter(self):
        result = Prompt("MESSAGE", Type = OK )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, OK )

    #===========================================================================
    def test_cancel_modifier(self):
        result = Prompt("MESSAGE", {Type:CANCEL} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, CANCEL )

    #===========================================================================
    def test_cancel_parameter(self):
        result = Prompt("MESSAGE", Type = CANCEL )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, CANCEL )
    
    #===========================================================================
    def test_ok_cancel_modifier(self):
        result = Prompt("MESSAGE", {Type:OK_CANCEL} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, OK_CANCEL )

    #===========================================================================
    def test_ok_cancel_parameter(self):
        result = Prompt("MESSAGE", Type = OK_CANCEL )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, OK_CANCEL )
    
    #===========================================================================
    def test_yes_modifier(self):
        result = Prompt("MESSAGE", {Type:YES} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, YES )

    #===========================================================================
    def test_yes_parameter(self):
        result = Prompt("MESSAGE", Type = YES )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, YES )
    
    #===========================================================================
    def test_no_modifier(self):
        result = Prompt("MESSAGE", {Type:NO} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, NO )

    #===========================================================================
    def test_no_parameter(self):
        result = Prompt("MESSAGE", Type = NO )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, NO )
   
    #===========================================================================
    def test_yes_no_modifier(self):
        result = Prompt("MESSAGE", {Type:YES_NO} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, YES_NO )

    #===========================================================================
    def test_yes_no_parameter(self):
        result = Prompt("MESSAGE", Type = YES_NO )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, YES_NO )
        
    #===========================================================================
    def test_alpha_modifier(self):
        result = Prompt("MESSAGE", {Type:ALPHA} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, ALPHA )

    #===========================================================================
    def test_alpha_parameter(self):
        result = Prompt("MESSAGE", Type = ALPHA )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, ALPHA )
        
    #===========================================================================
    def test_num_modifier(self):
        result = Prompt("MESSAGE", {Type:NUM} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, NUM )

    #===========================================================================
    def test_num_parameter(self):
        result = Prompt("MESSAGE", Type = NUM )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, NUM )

    #===========================================================================
    def test_alpha_modifier(self):
        result = Prompt("MESSAGE", {Type:ALPHA} )
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, ALPHA )

    #===========================================================================
    def test_list_default(self):
        result = Prompt("MESSAGE", options = ['A:First', 'B:Second'], Type = LIST )
        self.assertEqual(self.cif.promptOptions, ['A:First', 'B:Second'])
        self.assertEqual(self.cif.promptMessage, "MESSAGE")
        self.assertEqual(self.cif.promptType, LIST )

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestPrompt)
    