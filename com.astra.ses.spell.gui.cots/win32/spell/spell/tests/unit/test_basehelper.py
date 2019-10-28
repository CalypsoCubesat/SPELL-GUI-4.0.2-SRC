################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    tests.unit.test_basehelper
FILE
    test_basehelper.py
    
DESCRIPTION
    Unit tests for base helper
    
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
from spell.lang.helpers.basehelper import WrapperHelper 
from spell.lang.constants import *
from spell.lang.modifiers import *

#*******************************************************************************
# System imports
#*******************************************************************************
import unittest

#*******************************************************************************
# Local imports
#*******************************************************************************
from tools import *

################################################################################
class TestBaseHelper(unittest.TestCase):
    
    tf = None
    
    #===========================================================================
    def setUp(self):
        self.tf = TestFunction()
        
    #===========================================================================
    def tearDown(self):
        self.tf = None
    
    def test_init(self):
        self.assertEqual(self.tf.getConfig(),{"A":1,"B":2})

    
################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestBaseHelper)
    