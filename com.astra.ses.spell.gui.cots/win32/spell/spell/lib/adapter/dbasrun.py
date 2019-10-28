from database import *

################################################################################
class DatabaseAsRun(Database):
    
    __filename = None
    __file = None
    
    #===========================================================================
    def __init__(self, name, path, defaultExt = None):
        if defaultExt is not None:
            self.__filename = path + "." + defaultExt
        else:
            self.__filename = path
            
        # Obtain the SPELL data directory
        data = os.getenv("SPELL_DATA")
        if data is None:
            raise DriverException("SPELL data directory not defined")
            
        self.__filename = data + os.sep + self.__filename

        LOG("Instanciated: " + self.__filename)
    
    #===========================================================================
    def id(self):
        return self.__filename

    #===========================================================================
    def create(self):
        self.__file = open(self.__filename, 'w')
        LOG("Created: " + self.__filename)
        return self
    
    #===========================================================================
    def __getitem__(self, key):
        return None

    #===========================================================================
    def __setitem__(self, key, value):
        pass

    #===========================================================================
    def set(self, key, value, format = None):
        pass
            
    #===========================================================================
    def write(self, timestamp, identifier, line = "<n/a>", item = "", value = "", status = "", comment = "", time = ""):
        
        text = "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (timestamp,identifier,line,item,value,status,comment,time)        
        self.__file.write(text)
        self.__file.flush()

    #===========================================================================
    def getFilename(self):
        return self.__filename
    
    #===========================================================================
    def reload(self):
        pass

    #===========================================================================
    def commit(self):
        pass
    
    #===========================================================================
    def keys(self):
        return []
