###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.connection 
FILE
    connection.py
DESCRIPTION
    CORBA wrapper concrete implementation for hifly driver.
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
"""

###############################################################################

import spell.utils.corba
import CORBA
from spell.lib.hifly.internals.authentication import RijndaelEncryptor
from spell.lib.hifly.internals.exception import HiflyException
from spell.lib.hifly.interface import IAUTH
from spell.utils.corba import CorbaHelperClass
from spell.utils.log import *
import sys,os

###############################################################################
class HiflyCorbaHelperClass(object):

    """
    DESCRIPTION:
        Provides authentication service access for hifly SCS 
    """
    
    __chelper = None
    __encryptor = None
    __authServer = None
    __nameID = None
    __started = False
    
    #==========================================================================
    def __init__(self):
        # Create the encryptor class
        self.__encryptor = RijndaelEncryptor()
        self.__authServer = None
        self.__started = False
        LOG("Created")
        
    #==========================================================================
    def setup(self, nameID, nameserver, port, domain, family):
        
        """
        Setup the connection for using the name service running on the
        given server:port, and for the given satellite domain and server family.
        
        Must be invoked before using authentication service.
        """
        
        # Take into account that the driver may be used from outside
        # the spell executor, thus there is no CONN object available
        self.__chelper = CorbaHelperClass()

        if not self.__chelper.isReady():
            LOG("CORBA not initialized yet. Initializing now")
            self.__chelper.initialise()
            
        if not self.__chelper.hasNameService(nameID):
            LOG("Adding name service " + nameID)
            self.__chelper.addNameService( nameID, nameserver, port )
            
        if not self.__chelper.isActivated():
            LOG("CORBA not activated yet. Activating now")
            self.__chelper.activate()
            
        if not self.__chelper.isRunning():
            LOG("CORBA not running. Running now")
            self.__chelper.startBackground()
            
        LOG("Setting name context: " + domain + "/" + family + " on " + nameID)
        self.__chelper.setContext( nameID, str(domain), str(family) )
        
        self.__nameID = nameID
        self.__started = True

    #==========================================================================
    def cleanup(self):
        if self.__started:
            if self.__chelper.isRunning():
                self.__chelper.stop()
                self.__started = False
        
    #==========================================================================
    def authenticate(self, authKey, user):
        
        """
        Authenticate for using hifly services using the given key and the given
        user name. Shall be invoked before accessing any hifly external interface.
        """
        
        # Set the key to the encryptor and encrypt the user name
        self.__encryptor.setKey(authKey)
        enc = self.__encryptor.getEncryptedString(user)
        
        # hifly authentication service parameters
        service = IAUTH.AUTHserverMngr.ServiceName
        serviceClass =  IAUTH.AUTHserverMngr
        
        # Obtain the authentication server manager
        authServerMngr = self.__chelper.getObject( self.__nameID, service , serviceClass )
        
        # Ask the manager for an authentication server
        LOG("Got authentication manager")
        self.__authServer = authServerMngr.getAuthenticationServer(enc);

        if self.__authServer is None:
            raise HiflyException("Could not obtain authentication server")
        
        LOG("Got authentication server")
        
    #==========================================================================
    def getService(self, name, narrowClass):
        
        """
        Obtain a hifly service manager identified by the given name.
        """
        
        if self.__authServer is None: 
            raise HiflyException("Not authenticated yet")

        LOG("Getting service: " + name)
        obj = self.__authServer.getObject( name )
        return obj._narrow( narrowClass )

    #==========================================================================
    def getObject(self, name, narrowClass):
        return self.__chelper.getObject(self.__nameID, name, narrowClass)

    #==========================================================================
    def getObjectByContextType(self, domain, subdomain, name, type, narrowClass):
        return self.__chelper.getObjectByContextType(self.__nameID,\
                                                     domain, subdomain,\
                                                     name, type, narrowClass)    
    
    #==========================================================================
    def releaseObject(self, obj):
        self.__chelper.releaseObject(obj)
        
    #==========================================================================
    def getNSid(self):
        return self.__nameID

    #==========================================================================
    def isReady(self):
        return self.__chelper.isReady()

CONN = HiflyCorbaHelperClass()