###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.value 
FILE
    user.py
DESCRIPTION
    IBASE.Variant helper class
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    27/09/2007
    
REVISION HISTORY
    27/09/2007    10:30    Creation
"""

###############################################################################

from  spell.lib.hifly.interface import IBASE
from spell.lib.adapter.value import *
from spell.utils.log import LOG

###############################################################################
def radixToIBase(radix):
    if radix == DEC:
        return IBASE.DECIMAL
    elif radix == HEX:
        return IBASE.HEXADECIMAL
    elif radix == OCT:
        return IBASE.OCTAL
    else:
        return IBASE.BINARY

###############################################################################
class Variant:

    #===========================================================================
    def __init__(self, format = None, value = None):
        if (not format is None) and ( not value is None ):
            self.value = IBASE.Variant(format,value)
            self.accessor = self.value._d_to_m[self.value._d]
        else:
            self.value = None
            self.accessor = None

    #===========================================================================
    def setT(self, rawvalue):
        t = type(rawvalue)
        if t == int:
            format = IBASE.IS_LONG
        elif t == long:
            format = IBASE.IS_LONG
        elif t == str:
            format = IBASE.IS_STRING
        elif t == float:
            format = IBASE.IS_FLOAT
        else:
            raise BaseException("Value wrapper: Unrecognised format")
        self.value = IBASE.Variant( format, rawvalue )
        self.accessor = self.value._d_to_m[self.value._d]

    #===========================================================================
    def setV(self, adapterValue):
        theValue = adapterValue.get()
        LOG("Parsing adapter value: " + repr(theValue))
        format = adapterValue.format()
        if format == LONG:
            self.value = IBASE.Variant( IBASE.IS_LONG, theValue )
        elif format == FLOAT:
            self.value = IBASE.Variant( IBASE.IS_FLOAT, theValue )
        elif format == BOOLEAN:
            self.value = IBASE.Variant( IBASE.IS_BOOLEAN, theValue )
        elif format == STRING:
            self.value = IBASE.Variant( IBASE.IS_STRING, theValue )
        elif format == DATETIME:
            self.value = IBASE.Variant( IBASE.IS_TIME, theValue )
        elif type(theValue)==int:
            self.value = IBASE.Variant( IBASE.IS_LONG, theValue )
        elif type(theValue)==float:
            self.value = IBASE.Variant( IBASE.IS_FLOAT, theValue )
        elif type(theValue)==str:
            self.value = IBASE.Variant( IBASE.IS_STRING, theValue )
        else:
            LOG("WARNING!!! UNKNOWN FORMAT: " + repr(format))
            self.value = IBASE.Variant( IBASE.IS_NULL, theValue )
            
        self.accessor = self.value._d_to_m[self.value._d]

    #===========================================================================
    def setI(self, ibase):
        self.value = ibase
        self.accessor = self.value._d_to_m[self.value._d]
        
    #===========================================================================
    def set(self, value):
        self.value.__setattr__( self.accessor, value )

    #===========================================================================
    def get(self):
        if self.value is None:
            return None
        if (self.value._d == IBASE.IS_NULL):
            return None
        return self.value.__getattr__( self.accessor ) 

    #===========================================================================
    def getI(self):
        return self.value 
