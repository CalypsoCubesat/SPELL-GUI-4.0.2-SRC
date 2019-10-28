from spell.lib.exception import DriverException
from spell.utils.log import *
from spell.utils.ttime import TIME
from spell.config.reader import *
from spell.lang.constants import *
from spell.lang.modifiers import *

################################################################################
def SpecialType( value, orig_value ):
    vtype = None
    if type(value) == int:
        if orig_value.startswith("0x"):
            vtype = HEX
        elif orig_value.startswith("0") and not "." in orig_value:
            vtype = OCT
        elif orig_value.startswith("0b"):
            len = len(orig_value)-2
            vtype = BIN + str(len)
    elif isinstance(value,TIME):
        vtype = DATETIME
    return vtype        

################################################################################
def ImportValue( orig_value ):
    value = orig_value
    vtype = None
    try:
        value = eval(orig_value,{},{})
        vtype = SpecialType(value, orig_value)
    except (NameError,SyntaxError):
        try:
            value = TIME(orig_value)
            vtype = DATETIME
            LOG("WARNING: converting " + orig_value + " to date: " + str(value))
        except:
            # Check for binary strings
            if orig_value.startswith("0b"):
                value = int(orig_value[2:],2)
                length = len(orig_value)-2
                vtype = BIN + str(length)
                LOG("Converting to binary: " + repr(orig_value))
            else:
                value = orig_value
                vtype = None
                LOG("WARNING: converting to string: " + repr(value))
    return [value,vtype]

################################################################################
def ExportValue( value, vtype ):
    if vtype == HEX:
        value = hex(value).upper()
        value = '0x' + value[2:]
    elif vtype == OCT:
        value = oct(value)
    elif vtype.startswith(BIN):
        len = int(vtype[3:])
        value = '0b' + int2bin(value, count = len)
    elif vtype == TIME:
        value = "T(" + str(value) + ")"
    return value