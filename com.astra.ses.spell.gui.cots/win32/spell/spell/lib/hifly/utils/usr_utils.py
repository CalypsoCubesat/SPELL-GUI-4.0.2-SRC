###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.utils.usr_utils
     
FILE
    usr_utils.py
    
DESCRIPTION
    User management utilities
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    25/09/2007
"""

###############################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
import spell.lib.hifly.interface._GlobalIDL
from spell.lang.constants import *
from spell.lang.modifiers import *
from  spell.lib.hifly.interface._GlobalIDL import *
from  spell.lib.hifly.interface._GlobalIDL__POA import *
from  spell.lib.hifly.constants import *
from  spell.lib.hifly.modifiers import *

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************

#*******************************************************************************
# Import definition
#*******************************************************************************
__all__ = ['userCodeStr']

#*******************************************************************************
# Module globals
#*******************************************************************************
gidl = spell.lib.hifly.interface._GlobalIDL 

USER_OK             = gidl.USERcorbaManager.RE_OK
USER_UNKNOWN        = gidl.USERcorbaManager.RE_NO_SUCH_USER
USER_BAD_SESSION    = gidl.USERcorbaManager.RE_NO_SUCH_WS
USER_BAD_ROLE       = gidl.USERcorbaManager.RE_NO_SUCH_ROLE
USER_DENIED_ROLE    = gidl.USERcorbaManager.RE_CANT_HAVE_ROLE
USER_ROLE_BUSY      = gidl.USERcorbaManager.RE_ROLE_IN_USE
USER_LOGGED         = gidl.USERcorbaManager.RE_LOGGED_ON
USER_NOTLOGGED      = gidl.USERcorbaManager.RE_NOT_LOGGED_ON
USER_BAD_PWD        = gidl.USERcorbaManager.RE_BAD_PASSWORD
USER_BAD_PWD_H      = gidl.USERcorbaManager.RE_BAD_PASSWORD_II
USER_ERROR          = gidl.USERcorbaManager.RE_UNKNOWN

###############################################################################
def userCodeStr( code ):
    if code == USER_OK: 
        return "ok"
    if code == USER_UNKNOWN: 
        return "no such user"
    if code == USER_BAD_SESSION: 
        return "bad session"
    if code == USER_BAD_ROLE: 
        return "bad role"
    if code == USER_DENIED_ROLE: 
        return "denied role"
    if code == USER_ROLE_BUSY: 
        return "role is busy"
    if code == USER_LOGGED: 
        return "another user logged in"
    if code == USER_NOTLOGGED: 
        return "nobody logged in"
    if code == USER_BAD_PWD: 
        return "bad password"
    if code == USER_BAD_PWD_H: 
        return "bad password for handover"
    if code == USER_ERROR: 
        return "unknown error"
    return "unexpected error code" 
