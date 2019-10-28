################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_tm_item 
FILE
    test_tm_item.py
    
DESCRIPTION
    Unit tests for TmItemClass
    
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
from spell.lib.adapter.tm_item import *
from spell.lang.constants import *
from spell.lang.modifiers import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from tools import FakeTmClass

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest


################################################################################
# Test Cases    

################################################################################    
class TestTmItem(unittest.TestCase):

    item = None
    
    #===========================================================================    
    def setUp(self):
        self.item = TmItemClass( FakeTmClass(), 'TEST' )

    #===========================================================================    
    def tearDown(self):
        self.item = None

    #===========================================================================    
    def test_raw_value(self):
        self.assertEqual(self.item.raw(),0.1)
    
    #===========================================================================    
    def test_eng_value(self):
        self.assertEqual(self.item.eng(),'VALUE')
        
    #===========================================================================    
    def test_default_value(self):
        self.assertEqual(self.item.value(),"VALUE")
    
    #===========================================================================    
    def test_status(self):
        self.assertTrue(self.item.status())
            
    #===========================================================================    
    def test_eq_default(self):
        self.assertTrue(self.item.eq("VALUE"))
    
    #===========================================================================    
    def test_eq_default_fail(self):
        self.assertFalse(self.item.eq("SOME"))
    
    #===========================================================================    
    def test_eq_raw_fail_defconfig(self):
        self.assertFalse(self.item.eq(0.1))
    
    #===========================================================================    
    def test_eq_raw_ok_modifier(self):
        self.assertTrue(self.item.eq(0.1, {ValueFormat:RAW}))

    #===========================================================================    
    def test_eq_raw_ok_parameter(self):
        self.assertTrue(self.item.eq(0.1, ValueFormat = RAW))

    #===========================================================================    
    def test_eq_raw_fail_value(self):
        self.assertFalse(self.item.eq(0.22, ValueFormat = RAW))
    
    #===========================================================================    
    def test_item_setconfig(self):
        self.item.setConfig( {ValueFormat:RAW} )
        self.assertEqual(self.item.getConfig(ValueFormat),RAW)
        
    #===========================================================================    
    def test_eq_raw_ok_modified_config(self):
        self.item.setConfig( {ValueFormat:RAW} )
        v = self.item.value()
        self.assertTrue(self.item.eq(0.1),"Obtained value is " + repr(v))

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTmItem)
    