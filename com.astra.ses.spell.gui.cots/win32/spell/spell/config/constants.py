################################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.config.constants
FILE
    constants.py
    
DESCRIPTION
    Constants defining XML configuration file tags and properties
    
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
 
#*******************************************************************************
# Module globals
#*******************************************************************************

# Default configuration file name
CONFIG_FILE_NAME = "spell_config.xml"

# Sections of the configuration file
LISTENER = "listener"
CONTEXT  = "context"
EXECUTOR = "executor"
DRIVERS  = "drivers"
DRIVER   = "driver"
CONTEXTS = "contexts"
DATABASES= "databases"
LANGUAGE = "language"
COMMON   = "common"

# Sections listed here will become groups of properties in the config reader
CONFIG_SECTIONS = [ LISTENER, CONTEXT, EXECUTOR, DATABASES, COMMON ]

################################################################################

