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
    Fabien Bouleau (SES-ENGINEERING)
"""
################################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.ttime import *

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
class TestTimeInterface(unittest.TestCase):

    #===========================================================================    
    def setUp(self):
        pass

    #===========================================================================    
    def tearDown(self):
        pass

    #===========================================================================    
    def test_ttime_constants(self):
        hour = str(HOUR)
        minute = str(MINUTE)
        second = str(SECOND)
        day = str(DAY)

        self.assertEqual(hour, '+000 01:00:00')
        self.assertEqual(minute, '+000 00:01:00')
        self.assertEqual(second, '+000 00:00:01')
        self.assertEqual(day, '+001 00:00:00')

    #===========================================================================    
    def test_ttime_getting_seconds(self):
        reltime = TIME('+000 01:02:03')
        abstime = TODAY
        
        self.assertEqual(reltime.rel(), 1 * 3600 + 2 * 60 + 3)
        self.assertEqual(abstime.rel(), None)
    
    #===========================================================================    
    def test_ttime_cnv_number_T437(self):
        r1 = TIME(183845)
        r2 = TIME(544089.987654321)
        
        self.assertEqual(str(r1), '+002 03:04:05')
        self.assertEqual(str(r2), '+006 07:08:09.987654')
    
    #===========================================================================    
    def test_ttime_type(self):
        reltime = TIME('+000 01:02:03')
        abstime = TODAY
        
        self.assertEquals(reltime.isRel(), True)
        self.assertEquals(reltime.isAbs(), False)
        self.assertEquals(abstime.isRel(), False)
        self.assertEquals(abstime.isAbs(), True)

    #===========================================================================    
    def test_ttime_microseconds_T415(self):
        t1 = TIME("+12:34:56.789")
        t2 = TIME("-12:34:56.789")
        t3 = TIME("+004 12:34:56.789")
        t4 = TIME("-001 12:34:56.789")
        t5 = TIME("12-DEC-2008 12:34:56.789")

        self.assertEquals(str(t1), "+000 12:34:56.789000")
        self.assertEquals(str(t2), "-001 11:25:03.211000")
        self.assertEquals(str(t3), "+004 12:34:56.789000")
        self.assertEquals(str(t4), "-002 11:25:03.211000")
        self.assertEquals(str(t5), "12-Dec-2008 12:34:56.789000")

    #===========================================================================    
    def test_ttime_newformats_T415(self):
        t1 = TIME("2008/12/11")
        t2 = TIME("2008-12-11")
        t3 = TIME("11/12/2008")
        t4 = TIME("11-12-2008")

        self.assertEquals(str(t1), "11-Dec-2008 00:00:00")
        self.assertEquals(str(t2), "11-Dec-2008 00:00:00")
        self.assertEquals(str(t3), "11-Dec-2008 00:00:00")
        self.assertEquals(str(t4), "11-Dec-2008 00:00:00")
        
    #===========================================================================    
    def test_ttime_copying_now(self):
        abstime = TIME(NOW)
        self.assertEqual(isinstance(abstime._val, str), False)
    
    #===========================================================================    
    def test_ttime_day_of_year(self):
        t1 = TIME("2009-188-17:00:00")
        t2 = TIME("2009-188 17:00:00")
        t3 = TIME("2009-188-17:00")
        t4 = TIME("2009-188 17:00")
        t5 = TIME("2009-188")

        self.assertEquals(str(t1), "07-Jul-2009 17:00:00")
        self.assertEquals(str(t2), "07-Jul-2009 17:00:00")
        self.assertEquals(str(t3), "07-Jul-2009 17:00:00")
        self.assertEquals(str(t4), "07-Jul-2009 17:00:00")
        self.assertEquals(str(t5), "07-Jul-2009 00:00:00")
    
################################################################################
# Test Suite    
def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTimeInterface)
