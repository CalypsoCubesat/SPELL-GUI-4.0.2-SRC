#!/usr/bin/python

from spell.lang import ENV
env.setup("CONFIG_HIFLY")


value = TM["SPMFCNM"].eng()

print "Obtained value: ", value

TM.verify( [ "SPMFCNM", eq, 5 ] )

ENV.cleanup()
