################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.exception
FILE
    exception.py
    
DESCRIPTION
    Global exceptions used in different SPELL modules
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV) & Fabien Bouleau (SES Engineering)
"""

################################################################################

#*******************************************************************************
# SPELL Imports
#*******************************************************************************

#*******************************************************************************
# Local Imports
#*******************************************************************************
 
#*******************************************************************************
# System Imports
#*******************************************************************************
 
#*******************************************************************************
# Exceptions 
#*******************************************************************************

class SpellException( BaseException ):
    message = None
    reason  = None
    def __init__(self, msg = None, reason = None ):
        BaseException.__init__(self,msg)
        if isinstance(msg,SpellException):
            self.message = msg.message
            self.reason  = msg.reason
        elif type(msg)==str:
            self.message = msg
            self.reason = reason
        if self.message is None:
            self.message = repr(self.__class__)
        if self.reason is None:
            self.reason = "unknown"
    
    def __str__(self):
        return self.message + " ( " + self.reason + " )"
        
class CoreException  ( SpellException ): pass 
class NotAvailable   ( SpellException ): pass
class DriverException( SpellException ): pass
class CancelException( SpellException ): pass
class VerifyException( SpellException ): pass
class SyntaxException( SpellException ): pass 
#*******************************************************************************
# Module globals
#*******************************************************************************

