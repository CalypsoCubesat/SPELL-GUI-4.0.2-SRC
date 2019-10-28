###############################################################################
"""

Date: 01/07/2008

Project: UGCS/USL

Description
===========

Modifiers for SPELL functions and interfaces using GMV hifly(r) driver

Authoring
=========

@organization: SES Astra / SES Engineering

@copyright: This software is the copyrighted work of SES Engineering S.A. 
            All rights reserved.
            
@license: License information
    
@author: Rafael Chinchilla Camara (GMV Aerospace & Defence S.A.)

@version: 1.0
@requires: Python 2.5.x
"""
###############################################################################
#: Constant for task management indicating the type of process 
#:
#: See: PROCESS_CORE, PROCESS_CLIENT, PROCESS_OS
ProcType = 'ProcType'
#: Generic constant indicating the domain (spacecraft name)
Domain = 'Domain'
#: Indicates the server family to be used
#:
#: See: PRIME, BACKUP
Family = 'Family'
#: Indicates the host display to be used when opening a TM display
HDisplay = 'HDisplay'
#: Indicates the task mode when starting a hifly task
TaskMode = 'TaskMode'
# Protocol name for TM/TC links
Protocol = "Protocol"
# Channel name for TM/TC links
Channel = "Channel"
#: User role to be used on logins 
Role = 'Role'
#: Workspace to be used on logins
WS = 'WS'
#==============================================================================
# Additional info modifiers (COMMANDING)
#==============================================================================
#: Additional info for command injection: decoder to be used
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Decoder = "Decoder"
#: Additional info for command injection: auto no-op flag
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
ANOOP = "ANOOP"
#: Additional info for command injection: time-tag register number
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Register_Number = "Register_Number"
#: Additional info for command injection: periodic flag for ttag commands
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Periodic = "Periodic"
#: Additional info for command injection: infinite flag for ttag commands
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Infinite = "Infinite"
#: Additional info for command injection: repeat flag for periodic ttag commands
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Repeat = "Repeat"
#: Additional info for command injection: period time for periodic ttag commands
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Period = "Period"
#: Additional info for command injection: upload type
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
Upload = "Upload"
#: Additional info for command injection: sequence offset
#:
#: Applicable to: Space Systems Loral 1300 (NSS12)
SeqOffset = "SeqOffset"
#: Additional info for command injection: LIU to be used: A, B or SYS
#:
#: Applicable to: Eurostar 2000+ (A2B)
Liu = 'Liu'
#: Additional info for command injection: echo mode flag: ON, OFF or SYS
#:
#: Applicable to: Eurostar 3000+ (A3B,A1M)
Echo_Mode = 'Echo_Mode'
#: Additional info for command injection: remote terminal to be used, A, B or SYS
#:
#: Applicable to: Eurostar 3000+ (A3B,A1M)
Remote_Terminal = 'Remote_Terminal'
#: Indicates RTM (Downlink stream)
RTM = 'RTM'
