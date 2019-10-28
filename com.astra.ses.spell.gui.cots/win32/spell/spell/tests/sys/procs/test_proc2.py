#!/usr/bin/python

from spell.lang import ENV
ENV.setup("CONFIG_HIFLY")


val1 = Value( 0, LONG, HEX ) 
val2 = Value( 1, LONG, HEX )
val3 = Value( 49249, LONG, HEX ) 
val4 = Value( 32890, LONG, HEX )
val5 = Value( 0, LONG, HEX )
parameters = [ "YTRLYF22OF_1", val1, "YTRLYF22OF_2", val2, "YTRLYF22OF_3", val3,  "YTRLYF22OF_4", val4, "YTRLYF22OF_5", val5 ]

TC["YTRLYF22OF"].send( parameters, None ) 

sleep(15)

ENV.cleanup()
