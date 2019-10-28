###############################################################################

"""
(c) SES-ASTRA 2008

PACKAGE 
    spell.lib.hifly.authentication 
FILE
    encryptor.py
DESCRIPTION
    Rijndael algorithm wrapper for hifly authentication phase
    
    Usage: 
        encryptor = RijndaelEncryptor()
        encryptor.setKey(keyfile)
        bytes = encryptor.getEncrypted('username')
        
    A EncryptException is raised on error.
    
COPYRIGHT
    This software is the copyrighted work of SES ASTRA S.A.
    All rights reserved.
    
PROJECT
    UGCS/USL
    
AUTHOR
    Rafael Chinchilla Camara (GMV)
    
DATE
    30/08/2007
    
REVISION HISTORY
    30/08/2007    12:30    Creation
"""

import spell.utils.rijndael
import os,sys
import string

###############################################################################
class EncryptException:
    
    """
    Exception raised when there is some error during the encryption process
    """
    
    def __init__(self, msg):
            self.msgStr = msg
    
    def msg(self):
        """
        Provides the exception message
        """
        return self.msgStr


###############################################################################
class RijndaelEncryptor(object):
    
    """
    Wrapper for the Rijndael algorithm implementation to provide
    the encrypted user name as a byte array, and for loading the
    authentication key from a file
    """
    
    #==========================================================================
    def __init__(self):
        # Initialize values 
        self.keyFile = None
        self.keyLen = 16
        self.authKey = None
        self.encryptor = None

    #==========================================================================
    def __createEncryptor(self):
        # Create the Rijndael encryptor instance with the given
        # key and the given block size
        self.encryptor = spell.utils.rijndael.rijndael(self.authKey, self.keyLen)

    #==========================================================================
    def setBlockSize(self, newsize):
        
        """
        Change the encoding block size
        """
        
        self.keyLen = newsize
        # Recreate encryptor if needed
        if (self.authKey is None): return
        if (self.encryptor is None): return
        self.__createEncryptor()

    #==========================================================================
    def setKey(self, filename):

        """ 
        Loads the authentication key from the given file 
        """
                
        # Read 'keyLen' bytes from the input file
        try:
            self.keyFile = os.open(filename,os.O_RDONLY)
        except Exception:
            raise EncryptException("Could not open file: " + filename)
        
        # Set the read data as the authentication key
        self.authKey = os.read( self.keyFile, self.keyLen )
        
        # Check the key correctness
        if (len(self.authKey)<self.keyLen):
            self.authKey = None
            raise EncryptException("File: " + filename 
                        + " does not contain a valid key")

        # Create the encryptor instance            
        self.__createEncryptor()
            
    #==========================================================================
    def getEncryptedString(self, plaintext):
    
        """
        Obtain the encrypted string of the given text
        """
            
        if (self.authKey is None):
            raise EncryptException("No authentication key defined")
        
        if (self.encryptor is None):
            raise EncryptException("No encryptor available")

        if(len(plaintext)>self.keyLen):
            raise EncryptException("Too big block")
        
        if(len(plaintext)<self.keyLen):
            plaintext = string.ljust(plaintext, self.keyLen) 
        
        encoded = self.encryptor.encrypt(plaintext)
        
        return encoded
    
    #==========================================================================
    def getEncryptedBytes(self, plaintext):
        
        """
        Obtain the encrypted string of the given text as a byte array
        """
        encoded = self.getEncryptedString(plaintext)
        # Decompose the string in a byte array
        bytes = []
        for i in range(0,len(encoded)):
            bytes.append( ord(encoded[i]))
            
        return bytes
    
    #==========================================================================
    def testMe(self):
        #TODO: unit test
        pass    
            