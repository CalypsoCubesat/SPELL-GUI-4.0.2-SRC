################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.config.drivers
FILE
    drivers.py
    
DESCRIPTION
    Driver configuration entity definition
    
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
from base import ConfigItem, ConfigError
from constants import *
 
#*******************************************************************************
# System Imports
#*******************************************************************************
import os
import xml.dom.minidom
from xml.dom.minidom import Node
 
#*******************************************************************************
# Exceptions 
#*******************************************************************************
 
#*******************************************************************************
# Module globals
#*******************************************************************************

__all__ = [ 'DriverConfig' ]

PROPERTIES=['name', 'interfaces', 'lib', 'maxproc']

################################################################################
class DriverConfig(ConfigItem):
    
    """
    Configuration entity for Drivers. 
    @see: ConfigItem for details.
    """
    
    #===========================================================================            
    def __init__(self, configFile):
        if not os.path.exists(configFile):
            raise ConfigError("Cannot find driver configuration file: " + configFile) 
        document = xml.dom.minidom.parse(configFile)
        node = document.getElementsByTagName(DRIVER)[0]
        ConfigItem.__init__(self,node, PROPERTIES)
        # Load the driver properties node
        self.__loadDriverProperties(node)
        
    #===========================================================================            
    def getName(self):
        return self["name"]
    
    #===========================================================================            
    def getId(self):
        return self["id"]

    #===========================================================================            
    def getInterfaces(self):
        ifc = self['interfaces']
        if ifc is None:
            return ""
        return ifc

    #===========================================================================            
    def getLibraries(self):
        lib = self['lib']
        if lib is None:
            return ""
        return lib

    #===========================================================================            
    def getMaxProcs(self):
        maxp = self['maxproc']
        if maxp is None:
            return 10
        return maxp
    
    #===========================================================================            
    def __loadDriverProperties(self, node):
        for properties in node.getElementsByTagName("properties"):
            
            for property in properties.getElementsByTagName("property"):
                name = str(property.getAttribute("name"))
                if name is None or len(name)==0:
                    raise ConfigError("Cannot find driver property name")
                for pchild in property.childNodes:
                    if pchild.nodeType == Node.TEXT_NODE:
                        value = pchild.data
                        if value is None or len(value)==0:
                            raise ConfigError("Cannot find driver property value")
                        self[name] = str(value)
                        break
        