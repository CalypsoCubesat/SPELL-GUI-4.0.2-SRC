###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.tc.tcview 
FILE
    injection.py
    
DESCRIPTION
    Telecommand injection status view 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""
###############################################################################

#*******************************************************************************
# SPELL imports
#*******************************************************************************
from spell.utils.log import *
from spell.lib.hifly.interface import ITC_INJ__POA,ITC_INJ,ITC
from spell.lib.hifly.utils.tc_utils import *
from spell.lib.hifly.internals.timeacc import *

#*******************************************************************************
# Local imports
#*******************************************************************************

#*******************************************************************************
# System imports
#*******************************************************************************
import os,sys

###############################################################################
class TCinjectionView( ITC_INJ__POA.CommandInjectMngrView ):
    
    """
    Required for injected command status monitoring
    """
    
    #==========================================================================
    def __init__(self):
        LOG("Created")
        self._delegate = None
 
    #==========================================================================
    def ping(self):
        pass

    #==========================================================================
    def setDelegate(self, delegate):
        self._delegate = delegate

    #==========================================================================
    def removeDelegate(self):
        if not self._delegate is None:
            del self._delegate
            self._delegate = None
    
    #==========================================================================
    def updateRequestStatus( self, notificationInfo ):
        
        """
        Called when an injected command (request) changes its status
        """
        # Ignore this request = notificationInfo.m_tcRequestID
        tcRequestID = notificationInfo.m_request_id
        multID = [notificationInfo.m_multiplexer_id.m_id,notificationInfo.m_multiplexer_id.m_elemIndex]
        stage = stageStr(notificationInfo.m_stage)
        utime = notificationInfo.m_updateTime.m_sec
        status = cevStr(notificationInfo.m_stage_status)
        complete = notificationInfo.m_completed_flag

        #LOG("Notify TC update *************************************")
        #LOG("    TC REQUEST : " + repr(tcRequestID))
        #LOG("    MULTIPLEXER: " + repr(multID))
        #LOG("    STAGE      : " + stage)
        #LOG("    CEV STATUS : " + status)
        #LOG("    COMPLETED  : " + repr(notificationInfo.m_completed_flag))
        #LOG("    UPDATED    : " + timeToStr(notificationInfo.m_updateTime))

        # Notify the delegate about the update
        # Tipically, the delegate is an entity which has sent a command
        #   and wants to monitor its execution.
        if not self._delegate is None:
            self._delegate.updateRequestStatus( tcRequestID, multID, stage, utime, status, complete )

    #==========================================================================
    def updateSystemStatus(self, systemStatus):
        
        """
        Called when the status of one of the parts of the TC chain or its
        dependencies changes
        """
        il = systemStatus.m_global_il_status
        lnk = systemStatus.m_link_status
        ptvs = systemStatus.m_ptv_stat_check_status
        ptvd = systemStatus.m_ptv_dyn_check_status
        cev = systemStatus.m_cev_check_status
        mmm = systemStatus.m_mmm_status

        request = il.m_request_id.m_id
        gs = linkStatusStr(lnk.m_tc_gs_link_status)
        nctrs = linkStatusStr(lnk.m_tc_nctrs_link_status)
        uv = linkStatusStr(lnk.m_tc_uv_link_status)
        tm = linkStatusStr(lnk.m_tc_tm_flow_status)
        ifc = linkStatusStr(lnk.m_tc_exif_status)
        
        LOG("Notify TC system status ------------------------------")
        LOG("    REQUEST    : " + repr(request))
        LOG("    INTERLOCK  : " + repr(il.m_il_type) + "," +  repr(il.m_il_status))
        LOG("    GS LINK    : " + gs)
        LOG("    NCTRS LINK : " + nctrs)
        LOG("    TC SPACON  : " + linkStatusStr(lnk.m_tc_spacon_link_status))
        LOG("    UV LINK    : " + uv)
        LOG("    TM FLOW    : " + tm)
        LOG("    EXIF       : " + ifc)
        LOG("    STC PTV    : " + checkStateStr(ptvs))
        LOG("    DYN PTV    : " + checkStateStr(ptvd))
        LOG("    CEV CHECK  : " + checkStateStr(cev))
        LOG("    MMM STATUS : " + MMMtoStr(mmm))
        LOG("    OBQM SPACE : " + repr(systemStatus.m_obqm_space_status[0].m_spaceAvailable))

        # Notify the delegate about the update
        # Tipically, the delegate is an entity which has sent a command
        #   and wants to monitor its execution.
        if not self._delegate is None:
            self._delegate.updateSystemStatus( gs, nctrs, uv, tm, ifc )

