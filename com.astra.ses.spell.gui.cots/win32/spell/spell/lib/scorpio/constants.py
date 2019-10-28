###############################################################################
"""

Date: 01/07/2008

Project: UGCS/USL

Description
===========

Constants for procedures using GMV hifly(r) SPELL driver

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


#==============================================================================
# TASK CONSTANTS
#==============================================================================
#: Process type corresponding to a hifly server
PROCESS_CORE = 'core'
#: Process type corresponding to a hifly client
PROCESS_CLIENT = 'client'
#: Process type corresponding to a generic application
PROCESS_OS = 'os'
#: Family type PRIME (see Family)
PRIME = 'PRIME'
#: Family type BACKUP (see Backup)
BACKUP = 'BACKUP'
#: Unknown task status
TASK_UNKNOWN = 'unknown'
#: Task is starting
TASK_STARTING = 'starting'
#: Task is started
TASK_STARTED = 'started'
#: Task is stopped
TASK_STOPPED = 'stopped'
#: Task has died
TASK_DIED = 'died'
#: Kill the application and restart it (see TaskMode)
RESTART = 'restart'
#: Indicator of local display (see HDisplay)
LOCAL = 'LOCAL'

#==============================================================================
# USER CONSTANTS
#==============================================================================

# Execution results
#: Command execution result 'not executed'
EXEC_UNINIT   = "Not executed"
#: Command execution result 'in progress'
EXEC_PROGRESS = "Execution in progress" 
#: Command execution result 'executed'
EXEC_OK       = "Execution success"
#: Command execution result 'failed'
EXEC_FAIL     = "Verification failed"
#: Command execution result 'timed-out'
EXEC_TIMEOUT  = "Verification timed-out"
#: Command execution result 'uplinked'
UPLINKED      = "Uplinked"

# Generic states for links
#: TM/TC Link status UP 
UP = "UP"
#: TM/TC link status DOWN
DOWN = "DOWN"

# Generic states for checks
#: Generic state: enabled
ENABLED = "ENABLED"
#: Generic state: disabled
DISABLED = "DISABLED"
#: Generic state: override
OVERRIDE = "OVERRIDE"
#: Generic state: no notification
NONOTIF = "NO NOTIFICATION"
#: Generic state: unknown
UNKNOWN = "UNKNOWN"

# Verification stages
#: Verification stage: idle
IDLE            = "Idle"
#: Verification stage: pending
PENDING         = "Pending"
#: Verification stage: passed
PASSED          = "Passed"
#: Verification stage: failed
FAILED          = "Failed"
#: Verification stage: unverified
UNVERIFIED      = "Unverified"
#: Verification stage: unknown
UNKNOWN         = "Unknown"
#: Verification stage: timeout
TIMEOUT         = "Timeout"
#: Verification stage: not applicable
NOT_APPLICABLE  = "Not applicable"

