###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.internals.exifservice
FILE
    exifservice.py
    
DESCRIPTION
    base class for EXIF service users 
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

from spell.lib.hifly.internals.exception import HiflyException
from spell.utils.log import *
from spell.lib.registry import REGISTRY
from spell.lang.constants import *
from spell.lang.modifiers import *
import sys,time,traceback
from decorator import *

@decorator
def EXIF(func, *args, **kwargs):
    repeat = True
    while (repeat):
        repeat = False
        try:
            #LOG("### EXIF IN")
            result = func(*args, **kwargs)
            #LOG("### EXIF OUT")
        except BaseException,ex:
            exs = str(ex)
            LOG("### EXCEPT: " + exs)
            if ("COMM_FAILURE" in exs or "TRANSIENT" in exs or "Unregistered external" in exs):
                if not "TRANSIENT_CallTimedout" in exs:
                    LOG("### RECONNECT")
                    REGISTRY['CIF'].write("Failed to access EXIF service. Reconnecting", {Severity:WARNING})
                    try:
                        args[0].connect(True)
                    except:
                        REGISTRY['CIF'].write("Failed reconnect EXIF service", {Severity:ERROR})
                        raise ex
                else:
                    sys.stderr.write("Retry EXIF call after timeout\n")
                    time.sleep(0.25)
                repeat = True
            else:
                traceback.print_exc( file = sys.stderr )
                raise ex
    return result
