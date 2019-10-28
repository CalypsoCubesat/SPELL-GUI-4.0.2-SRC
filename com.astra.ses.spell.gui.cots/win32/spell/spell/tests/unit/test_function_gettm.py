################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_function_gettm 
FILE
    test_function_gettm.py
    
DESCRIPTION
    Unit tests for GetTM function
    
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
from spell.lang.functions import GetTM
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
from tools import *

################################################################################
class TestGetTM(unittest.TestCase):
    
    tm = None
    
    #===========================================================================
    def setUp(self):
        self.tm = FakeTmClass()
        REGISTRY['TM'] = self.tm
        REGISTRY['CIF'] = FakeClientInterface()
        
    #===========================================================================
    def tearDown(self):
        self.tm = None
        REGISTRY.remove('TM')
    
    #===========================================================================
    def test_default_behv(self):
        value = GetTM('TEST', {Notify:False})
        self.assertEqual(value,'VALUE')

    #===========================================================================
    def test_raw_with_modifier(self):
        value = GetTM('TEST', {Notify:False,ValueFormat:RAW})
        self.assertEqual(value,0.1)

    #===========================================================================
    def test_raw_with_config(self):
        self.tm.setConfig( {ValueFormat:RAW} )
        value = GetTM('TEST', {Notify:False})
        self.tm.setConfig( {ValueFormat:ENG} )
        self.assertEqual(value,0.1)

    #===========================================================================
    def test_giving_item(self):
        value = GetTM(self.tm['TEST'], {Notify:False})
        self.assertEqual(value,'VALUE')

    #===========================================================================
    def test_timeout(self):
        self.tm.toWait = 4
        self.assertRaises(DriverException,GetTM,'TEST', {Notify:False,Wait:True,Timeout:0.1,HandleError:False})
        self.tm.toWait = 0.75

    #===========================================================================
    def test_nonexistent(self):
        self.assertRaises(DriverException,GetTM,"NOEXIST",{HandleError:False})

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestGetTM)
    