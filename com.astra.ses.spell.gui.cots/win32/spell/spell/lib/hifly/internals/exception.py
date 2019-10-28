###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.exception 
FILE
    exception.py
    
DESCRIPTION
    Exceptions raised by hifly driver library
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.exception import DriverException

###############################################################################
class HiflyException(DriverException):
    
    """
    Raised by the hifly low level interfaces when an error occurs.
    """
    def __init__(self, msg, reason = None):
        DriverException.__init__(self, msg, reason)
