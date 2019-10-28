#!/usr/bin/python

from spell.lib.adapter.value import *
from spell.lang import *
ENV.setup("CONFIG")


################################################################

val1 = Value( 0, LONG, HEX ) 
val2 = Value( 1, LONG, HEX )
val3 = Value( 49249, LONG, HEX ) 
val4 = Value( 32890, LONG, HEX )
val5 = Value( 0, LONG, HEX )
parameters = [ "YTRLYF22OF_1", val1, "YTRLYF22OF_2", val2, "YTRLYF22OF_3", val3,  "YTRLYF22OF_4", val4, "YTRLYF22OF_5", val5 ]

print "Sending command YTRLYF22OF"
Send( "YTRLYF22OF", parameters )

print "Current frame counter value:", GetTM("SPMFCNM")

print "Wait for frame counter to have value 15"
WaitForTM( "SPMFCNM", 15 )

print "Verify if frame counter value is 16, no retries"
Verify( [ "SPMFCNM", eq, 16 ] )


################################################################

print
print
try:
	input()
except:
	pass

ENV.cleanup()
