################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_adapter_value
FILE
    test_adapter_value.py
    
DESCRIPTION
    Unit tests for ValueClass
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Fabien Bouleau (SES-ENGINEERING)
"""
################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.lib.adapter.value import ValueClass
from spell.lang.constants import *

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest,time

################################################################################
# Test Cases    

################################################################################    
class TestValueClass(unittest.TestCase):
    
    #===========================================================================    
    def setUp(self):
        pass
    
    #===========================================================================    
    def tearDown(self):
        pass

    #===========================================================================    
    def test_set_value_num_decimal(self):
        self.assertEqual(ValueClass(123).evaluate(), 123)

    #===========================================================================    
    def test_set_value_num_hexa(self):
        self.assertEqual(ValueClass('100', radix = HEX).evaluate(), 256)

    #===========================================================================    
    def test_set_value_num_octal(self):
        self.assertEqual(ValueClass('211', radix = OCT).evaluate(), 137)

    #===========================================================================    
    def test_set_value_num_bin(self):
        self.assertEqual(ValueClass('100101', radix = BIN).evaluate(), 37)

    #===========================================================================    
    def test_get_value_num_decimal(self):
        self.assertEqual(ValueClass(123).evaluate(DEC), 123)

    #===========================================================================    
    def test_get_value_str_decimal(self):
        self.assertEqual(ValueClass('123', radix = DEC).evaluate(DEC), 123)

    #===========================================================================    
    def test_get_value_num_hexa(self):
        self.assertEqual(ValueClass(256).evaluate(HEX), '0x100')

    #===========================================================================    
    def test_set_value_num_octal(self):
        self.assertEqual(ValueClass(282).evaluate(OCT), '0432')

    #===========================================================================    
    def test_set_value_num_bin(self):
        self.assertEqual(ValueClass(232).evaluate(BIN), '0b11101000')

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestValueClass)
        
    
    