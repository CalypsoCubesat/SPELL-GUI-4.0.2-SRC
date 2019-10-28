################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_tc_item 
FILE
    test_tc_item.py
    
DESCRIPTION
    Unit tests for TcItemClass
    
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
from spell.lib.adapter.tc_item import *
from spell.lang.constants import *
from spell.lang.modifiers import *

#*******************************************************************************
# Local imports
#*******************************************************************************
from tools import FakeTcClass

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest


################################################################################
# Test Cases    

################################################################################    
class TestTcItem(unittest.TestCase):

    tc = None
    
    #===========================================================================    
    def setUp(self):
        self.tc = FakeTcClass()

    #===========================================================================    
    def tearDown(self):
        self.tc = None

    #===========================================================================    
    def test_name(self):
        item = self.tc['TC_OK']
        self.assertEqual(item._cmdName, 'TC_OK')

    #===========================================================================    
    def test_parameters(self):
        item = self.tc['TC_OK']
        self.assertEqual(item._getParams(), [])

    #===========================================================================    
    def test_add_parameter_simple(self):
        item = self.tc['TC_s']
        item['PARAM'] = [ 1.0 ]
        params = item._getParams()
        self.assertEqual( len(params), 1)
        param = params[0]
        self.assertEqual( param.name, 'PARAM' )
        self.assertEqual( param.value.get(), 1.0 )
        self.assertEqual( param.value.radix(), DEC )
        self.assertEqual( param.value.format(), ENG )
        self.assertEqual( param.value.units(), "" )
        item.clear()
        params = item._getParams()
        self.assertEqual( len(params), 0)

    #===========================================================================    
    def test_add_parameter_config_1(self):
        item = self.tc['TC_c1']
        item['PARAM'] = [ 0xA, {Radix:HEX} ]
        param = item._getParams()[0]
        self.assertEqual( param.value.get(), 10 )
        self.assertEqual( param.value.radix(), HEX )
        self.assertEqual( param.value.format(), ENG )
        self.assertEqual( param.value.units(), "" )

    #===========================================================================    
    def test_add_parameter_config_2(self):
        item = self.tc['TC_c2']
        item['PARAM'] = [ 1.0, {ValueFormat:RAW} ]
        param = item._getParams()[0]
        self.assertEqual( param.value.get(), 1.0 )
        self.assertEqual( param.value.radix(), DEC )
        self.assertEqual( param.value.format(), RAW )
        self.assertEqual( param.value.units(), "" )

    #===========================================================================    
    def test_add_parameter_config_3(self):
        item = self.tc['TC_c3']
        item['PARAM'] = [ "HOLA", {Units:"deg"} ]
        param = item._getParams()[0]
        self.assertEqual( param.value.get(), "HOLA" )
        self.assertEqual( param.value.radix(), DEC )
        self.assertEqual( param.value.format(), ENG )
        self.assertEqual( param.value.units(), "deg" )

    #===========================================================================    
    def test_send_defaults_ok(self):
        self.tc.setConfig({Notify:False})
        item = self.tc['TC_OK']
        item.clear()
        result = item.send()
        self.assertTrue(result)
        self.assertTrue(item.getIsCompleted())
        self.assertTrue(item.getIsSuccess())

    #===========================================================================    
    def test_send_defaults_fail(self):
        self.tc.setConfig({Notify:False})
        item = self.tc['TC_NOK']
        item.clear()
        result = True
        try:
            item.send()
        except:
            result = False
        self.assertFalse(result)
        self.assertTrue(item.getIsCompleted())
        self.assertFalse(item.getIsSuccess())

    #===========================================================================    
    def test_send_nok_timeout(self):
        self.tc.setConfig({Notify:False})
        item = self.tc['TC_OK']
        item.clear()
        result = True
        try:
            item.send( {Timeout:0.1} )
        except:
            result = False
        self.assertFalse(result)
        self.assertFalse(item.getIsCompleted())
        self.assertFalse(item.getIsSuccess())

################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTcItem)
    