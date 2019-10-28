###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.adapter.constants.notification
FILE
    lang.py
DESCRIPTION
    Constants for notifications
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    17/07/2008
"""

###############################################################################


###############################################################################
# UI notification fields
NOTIF_PROC_ID     = "ProcId"
NOTIF_SUBPROC_ID  = "SubProcId"
NOTIF_LINE        = "Line"
NOTIF_DATA_TYPE   = "DataType"
NOTIF_ITEM_TYPE   = "ItemType"
NOTIF_ITEM_NAME   = "ItemName"
NOTIF_ITEM_VALUE  = "ItemValue"
NOTIF_ITEM_STATUS = "ItemStatus"
NOTIF_ITEM_REASON = "ItemReason"
NOTIF_ITEM_TIME   = "ItemTime"
NOTIF_ITEM_EOS    = "EndOfScript"
NOTIF_STATUS      = "Status"

###############################################################################
# UI notification type values
DATA_TYPE_NOTIF  = 'ITEM'
NOTIF_TYPE_VAL   = 'VALUE'
NOTIF_TYPE_VERIF = 'VERIFICATION'
NOTIF_TYPE_EXEC  = 'EXECUTION'
NOTIF_TYPE_SYS   = 'SYSTEM'
NOTIF_TYPE_TIME  = 'TIME'

###############################################################################
# UI notification status values
NOTIF_STATUS_OK = 'SUCCESS'
NOTIF_STATUS_PR = 'IN PROGRESS'
NOTIF_STATUS_FL  = 'FAILED'
NOTIF_STATUS_SP  = 'SKIPPED'

###############################################################################
# Item separator
ITEM_SEP = ",,"
