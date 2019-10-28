################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_adapter_tm
FILE
    test_adapter_tm.py
    
DESCRIPTION
    Unit tests for TmInterface
    
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
from spell.lib.adapter.tm_item import TmItemClass
from spell.lang.constants import *
from spell.lang.modifiers import *
from spell.lib.registry import REGISTRY

#*******************************************************************************
# Local imports
#*******************************************************************************
from tools import *

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest,time

################################################################################
# Test Cases    

################################################################################    
class TestTmInterface(unittest.TestCase):

    item = None
    tm = None
    
    #===========================================================================    
    def setUp(self):
        REGISTRY['CIF'] = FakeClientInterface()
        self.tm = FakeTmClass()
        self.tm.forRaw = 0.1
        self.tm.forEng = 'VALUE'
        self.tm.toWait = 0.75
        self.item = self.tm['TEST']

    #===========================================================================    
    def tearDown(self):
        self.item = None
        self.tm = None

    #===========================================================================    
    def test_obtain_item(self):
        self.assertTrue(isinstance(self.item,TmItemClass), "Bad instance")
        self.assertEqual(self.item.name(),'TEST', "Bad name: " + self.item.name())

    #===========================================================================    
    def test_eq_default_config(self):
        self.assertTrue(self.tm.eq(self.item,"VALUE"))

    #===========================================================================    
    def test_eq_raw_using_modifier(self):
        self.assertTrue(self.tm.eq(self.item,0.1, {ValueFormat:RAW}))

    #===========================================================================    
    def test_eq_raw_using_parameter(self):
        self.assertTrue(self.tm.eq(self.item,0.1, ValueFormat = RAW))

    #===========================================================================    
    def test_eq_eng_failcase(self):
        self.assertFalse(self.tm.eq(self.item,"SOME"))

    #===========================================================================    
    def test_eq_eng_failcase_5_retries(self):
        self.tm.refreshCount = 0
        self.assertFalse(self.tm.eq(self.item,"SOME", {Retries:5}))
        self.assertEqual(self.tm.refreshCount,6, "Refreshed " + str(self.tm.refreshCount) + " times")

    #===========================================================================    
    def test_eq_eng_failcase_2_retries_wait(self):
        start = time.time()
        self.tm.refreshCount = 0
        self.tm.toWait = 1
        self.assertFalse(self.tm.eq(self.item,"SOME", {Retries:2,Wait:True}))
        end = time.time()
        self.assertTrue( (end-start)>2 )
    
    #===========================================================================    
    def test_neq_eng_default_config(self):
        self.assertTrue(self.tm.neq(self.item,"SOME"))

    #===========================================================================    
    def test_neq_eng_fail_case(self):
        self.assertFalse(self.tm.neq(self.item,"VALUE"))

    #===========================================================================    
    def test_setconfig(self):
        self.tm.setConfig( {ValueFormat:RAW} )
        self.assertEqual(self.tm.getConfig(ValueFormat), RAW)
        self.tm.setConfig( {ValueFormat:ENG} )
        self.assertEqual(self.tm.getConfig(ValueFormat), ENG)

    #===========================================================================    
    def test_config_affects_default_behavior(self):
        self.tm.setConfig( {ValueFormat:RAW} )
        self.assertTrue(self.tm.eq(self.item, 0.1))
        self.tm.setConfig( {ValueFormat:ENG} )

    #===========================================================================    
    def test_between_raw_value(self):
        self.assertTrue(self.tm.between(0.0, self.item, 0.2, {ValueFormat:RAW}))

    #===========================================================================    
    def test_between_raw_value_nostrict(self):
        self.assertTrue(self.tm.between(0.1, self.item, 0.1, {ValueFormat:RAW}))

    #===========================================================================    
    def test_between_raw_value_strict(self):
        self.assertFalse(self.tm.between(0.1, self.item, 0.1, {ValueFormat:RAW,Strict:True}))

    #===========================================================================    
    def test_not_between_raw_value(self):
        self.assertTrue(self.tm.not_between(1.0, self.item, 1.2, {ValueFormat:RAW}))

    #===========================================================================    
    def test_not_between_raw_value_nostrict(self):
        self.assertTrue(self.tm.not_between(0.1, self.item, 0.2, {ValueFormat:RAW}))

    #===========================================================================    
    def test_not_between_raw_value_strict(self):
        self.assertFalse(self.tm.not_between(0.1, self.item, 0.2, {ValueFormat:RAW,Strict:True}))

    #===========================================================================    
    def test_get_value_through_ifc(self):
        self.tm.setConfig( {ValueFormat:RAW} )
        self.assertEqual(self.item.value(),0.1)
        self.tm.setConfig( {ValueFormat:ENG} )

    #===========================================================================    
    def test_get_eng_through_ifc(self):
        self.assertEqual(self.item.eng(),'VALUE')

    #===========================================================================    
    def test_get_raw_through_ifc(self):
        self.assertEqual(self.item.raw(),0.1)
    
    #===========================================================================    
    def test_get_status_through_ifc(self):
        self.assertTrue(self.item.status())

    #===========================================================================    
    def test_item_refresh(self):
        self.assertEqual(self.item.raw(), 0.1)
        self.tm.forRaw = 0.5
        self.tm.refresh(self.item)
        self.assertEqual(self.item.raw(), 0.5)
        self.tm.forRaw = 0.1

    #===========================================================================    
    def test_item_refresh_string(self):
        self.assertEqual(self.item.raw(), 0.1)
        self.tm.forRaw = 0.5
        self.tm.refresh('TEST')
        self.assertEqual(self.item.raw(), 0.5)
        self.tm.forRaw = 0.1

    #===========================================================================    
    def test_total_refresh(self):
        self.assertEqual(self.item.raw(), 0.1)
        self.tm.forRaw = 0.5
        self.tm.refresh()
        self.assertEqual(self.item.raw(), 0.5)
        self.tm.forRaw = 0.1
    
    #===========================================================================    
    def test_verify_single_step_ok_case(self):
        steps = [[ 'TEST', eq, "VALUE" ]]
        self.assertTrue(self.tm.verify( steps, {Notify:False} ))

    #===========================================================================    
    def test_verify_single_step_fail_case(self):
        steps = [[ 'TEST', eq, "SOME" ]]
        self.assertFalse(self.tm.verify( steps, {Notify:False} ))

    #===========================================================================    
    def test_verify_single_step_ok_case_using_raw(self):
        steps = [[ 'TEST', eq, 0.1 ]]
        self.assertTrue(self.tm.verify( steps, {Notify:False,ValueFormat:RAW} ))

    #===========================================================================    
    def test_verify_single_step_fail_case_using_raw(self):
        steps = [[ 'TEST', eq, 0.2 ]]
        self.assertFalse(self.tm.verify( steps, {Notify:False,ValueFormat:RAW} ))

    #===========================================================================    
    def test_verify_single_step_ok_case_using_specific_config(self):
        steps = [[ 'TEST', eq, 0.1, {ValueFormat:RAW} ]]
        self.assertTrue(self.tm.verify( steps, {Notify:False} ))

    #===========================================================================    
    def test_verify_single_step_ok_case_using_specific_config(self):
        steps = [[ 'TEST', eq, 0.2, {ValueFormat:RAW} ]]
        self.assertFalse(self.tm.verify( steps, {Notify:False} ))

    #===========================================================================    
    def test_verify_two_steps_specific_config(self):
        steps = [ [ 'TEST', eq, 0.1, {ValueFormat:RAW} ],
                  [ 'TEST', eq, "VALUE"]]
         
        steps1 = [[ 'TEST', eq, 0.1, {ValueFormat:RAW} ]]
         
        steps2 = [[ 'TEST', eq, "VALUE"]]
        
        self.assertTrue(self.tm.verify( steps1, {Notify:False} ), "Raw value is " + repr(self.item.raw())) 
        self.assertTrue(self.tm.verify( steps2, {Notify:False} ), "Def value is " + repr(self.item.value())) 
        self.assertTrue(self.tm.verify( steps , {Notify:False} ))

    #===========================================================================    
    def test_verify_two_steps_one_fails(self):
        steps = [ [ 'TEST1', eq, 0.2, {ValueFormat:RAW} ],
                  [ 'TEST2', eq, "VALUE"]]
         
        self.assertFalse(self.tm.verify( steps , {Notify:False} ))

    #===========================================================================    
    def test_lt_ok_case(self):
        self.assertTrue(self.tm.lt('TEST', 1.0, {ValueFormat:RAW}))

    #===========================================================================    
    def test_lt_fail_case(self):
        self.assertFalse(self.tm.lt('TEST', 0.0, {ValueFormat:RAW}))

    #===========================================================================    
    def test_gt_ok_case(self):
        self.assertTrue(self.tm.gt('TEST', 0.0, {ValueFormat:RAW}))

    #===========================================================================    
    def test_gt_fail_case(self):
        self.assertFalse(self.tm.gt('TEST', 1.0, {ValueFormat:RAW}))
    
    #===========================================================================    
    def test_le_ok_case(self):
        self.assertTrue(self.tm.le('TEST', 0.1, {ValueFormat:RAW}))

    #===========================================================================    
    def test_le_fail_case(self):
        self.assertFalse(self.tm.le('TEST', 0.0, {ValueFormat:RAW}))

    #===========================================================================    
    def test_ge_ok_case(self):
        self.assertTrue(self.tm.ge('TEST', 0.1, {ValueFormat:RAW}))

    #===========================================================================    
    def test_ge_fail_case(self):
        self.assertFalse(self.tm.ge('TEST', 1.0, {ValueFormat:RAW}))

    #===========================================================================    
    def test_neq_ok_case(self):
        self.assertTrue(self.tm.neq('TEST', 1.0, {ValueFormat:RAW}))

    #===========================================================================    
    def test_neq_fail_case(self):
        self.assertFalse(self.tm.neq('TEST', 0.1, {ValueFormat:RAW}))

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTmInterface)
        
    
    