#!/usr/bin/env python

from spell.ui.remote.ui import ui_class
from time import sleep
from spell.utils.log import LoggerClass

LoggerClass.globalEnableLog(True)


UI = ui_class()
UI.setup(None)

try:
    input()
except:
    pass

UI.write("UI message")

try:
    input()
except:
    pass

UI.cleanup()
