###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.tm
FILE
    result.py
    
DESCRIPTION
    Test result structure. Evaluates as boolean expression and
    gives operation details

COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Fabien Bouleau 
    Rafael Chinchilla Camara (GMV)
"""
###############################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.log import *

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************

###############################################################################
# Module import definition

__all__ = ['Result']

###############################################################################
class Result(object):

    """
    Test result structure. Evaluates as boolean expression and
    gives operation details
    """
    _properties = {}
    _test = False

    #===========================================================================
    def __init__(self):
        self._properties = {}
        self._test = False
        
    #===========================================================================
    def __nonzero__(self):
        return self._test

    #===========================================================================
    def __cmp__(self,other):
        return cmp(self._test,other)
    
    #===========================================================================
    def __getitem__(self,key):
        return self._properties[key]

    #===========================================================================
    def __setitem__(self,key,value):
        self._properties[key] = value
        self._evaluate()
    
    #===========================================================================
    def _evaluate(self):
        self._test = False

    #===========================================================================
    def keys(self):
        return self._properties.keys()

    #===========================================================================
    def __str__(self):
        return str(self._test)

    #===========================================================================
    def __repr__(self):
        return repr(self._test)
    
###############################################################################
class TmResult(Result):

    """
    TM verification test result structure. Evaluates as boolean expression and
    gives operation details in the form 'parameter name':'verification status'
    """

    #===========================================================================
    def __init__(self):
        Result.__init__(self)

    #===========================================================================
    def _evaluate(self):
        for key in self._properties:
            if not self[key]: 
                self._test = False
                return
        self._test = True
        
