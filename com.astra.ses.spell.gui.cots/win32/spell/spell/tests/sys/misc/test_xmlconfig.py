
from spell.core.xmlconfig import *
import os

path = os.getenv("USLPATH") + os.sep + "data" + os.sep + "spell_config.xml"
loader = ConfigLoader( path )

default = loader.getEnvironment("InitialDriver")

c = loader.getConfiguration(default)

print c
print c.getProperty("ProcPathEnv")