
from spell.utils.corba import CorbaHelperClass
import spell.ui.remote.SPELL__POA 
from spell.ui.remote.xmlmsg import Message 

class TheGUI(spell.ui.remote.SPELL__POA.Peer):
    
    def __init__(self):
        pass
    
    #==========================================================================    
    def sendMessage(self, msg):
        print "GUI received message: ", msg
    
    #==========================================================================    
    def sendMessageR(self, msg):
        print "GUI received message and return the same: ", msg
        return msg
    

gui = TheGUI()
ch = CorbaHelperClass()

print "initializing client"
ch.initialise("localhost", "9988")
ch.activate()
from time import sleep
sleep(2)
print "get peer object"
server = ch.getObject("SPELL_SERVICE", spell.ui.remote.SPELL__POA.Peer)



print "register our peer"
key = server.registerPeer(gui._this())
print "peer registered with key:", key

try:
    input()
except:
    pass

print "create run message"
msg = Message( "command", "ID01", "GUI" )
msg["Property"] = "value"
print "send message"
server.message( msg.data() )
print "message sent"

try:
    input()
except:
    pass


