################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.driver.registry
FILE
    registry.py
    
DESCRIPTION
    Global registry where all core adapter interfaces are stored when ready.
    
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
class RegistryError(BaseException): pass
 
#*******************************************************************************
# Module globals
#*******************************************************************************

__all__ = [ 'REGISTRY', 'RegistryError' ]

__instance__ = None

################################################################################
class RegistryClass(object):
    
    __objects = {}
    
    #===========================================================================
    def __init__(self):
        self.__objects  = {}
        
    #==========================================================================
    @staticmethod
    def instance():
        global __instance__
        if __instance__ is None:
            __instance__ = RegistryClass()
        return __instance__
        
    #===========================================================================
    def __getitem__(self, key):
        if not self.__objects.has_key(key):
            raise RegistryError("No such object: " + repr(key))
        return self.__objects.get(key)
        
    #===========================================================================
    def __setitem__(self, key, object):
        self.__objects[key] = object

    #===========================================================================
    def exists(self, key):
        return self.__objects.has_key(key)

    #===========================================================================
    def remove(self, key):
        if self.__objects.has_key(key):
            self.__objects.pop(key)

    #===========================================================================
    def interfaces(self):
        return self.__objects.keys()
    
################################################################################
REGISTRY = RegistryClass.instance()