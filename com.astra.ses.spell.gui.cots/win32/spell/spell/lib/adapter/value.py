###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.value 
FILE
    user.py
DESCRIPTION
    Variant value helper class
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    02/10/2007
    
REVISION HISTORY
    02/10/2007    10:30    Creation
"""

###############################################################################

from spell.lang.constants import *
from spell.lang.modifiers import *

###############################################################################
class ValueClass:

    """
    This class implements a variant value with the following characteristics:
        - value
        - vtype (long, double...)
        - radix (hex, dec, oct..)
        - format (eng, raw)
        - units (whatsoever)
    """

    #==========================================================================
    def __init__(self, value, format = ENG, radix = DEC, vtype = LONG, units = '', defCal = True):
        self._value = value
        self._vtype = vtype
        if type(value)==int:
            self._vtype = LONG
        elif type(value)==float:
            self._vtype = FLOAT
        elif type(value)==str:
            self._vtype = STRING
        self._format = format
        self._radix = radix
        self._units = units
        self._defCal = defCal

    #==========================================================================
    def set(self, value):
        self._value = value

    #==========================================================================
    def get(self):
        return self._value 

    #==========================================================================
    def format(self, fmt = None):
        if fmt is None:
            return self._format
        else:
            self._format = fmt

    #==========================================================================
    def vtype(self, vt = None):
        if vt is None:
            return self._vtype
        else:
            self._vtype = vt
    
    #==========================================================================
    def radix(self, rd = None):
        if rd is None:
            return self._radix
        else:
            self._radix = rd
    
    #==========================================================================
    def units(self, u = None):
        if u is None:
            return self._units
        else:
            self._units = u
    
    #==========================================================================
    def __repr__(self):
        return "[" + repr(self._value) + ",VType: " + self._vtype + ",Format: " +\
         self._format + ", Radix: " + self._radix + ", Units: " + self._units + "]"
    
    #==========================================================================
    def evaluate(self, radix = DEC):
        cnv = { DEC: '', HEX: '0x', OCT: '0' }
        trns = { HEX: hex, OCT: oct }
        res = None
        
        try:
            if isinstance(self._value, str):
                if self._radix == BIN:
                    res = 0
                    for c in self._value:
                        res = res * 2 + eval(c)
                elif self._radix in cnv:
                    res = eval(cnv[self._radix] + self._value)
            elif isinstance(self._value, long) or isinstance(self._value, int) or isinstance(self._value, float):
                res = self._value
        except:
            res = None
        
        if res is None:
            return None

        if radix in trns:
            res = trns[radix](res)
        elif radix == BIN:
            v = ''
            while res > 0:
                if res % 2 == 1: v = '1' + v
                if res % 2 == 0: v = '0' + v
                res >>= 1
            res = '0b' + v
        
        return res
    