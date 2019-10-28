from database import *

################################################################################
class DatabaseFile(Database):
    
    __filename = None
    
    #===========================================================================
    def __init__(self, name, path, defaultExt = None):
        super(DatabaseFile, self).__init__()
        
        self.__name = name
        self.__path = path
        self.__defaultExt = defaultExt
        
        dataHome = os.getenv("SPELL_DATA").replace('/', os.sep)
        if dataHome is None:
            raise DriverException("SPELL_DATA environment variable not defined")

        # Append the data home to the path
        path = dataHome + os.sep + path.replace('/', os.sep)

        # First check if there is an extension in the file. If there is no
        # extension, append the default extension (if there is one).
        filename = os.path.basename(path)
        if (not len(filename.split("."))>1) and (defaultExt is not None): 
            path += "." + defaultExt
            
        self.__filename = path

        LOG("Instanciated: " + name)
    
    #===========================================================================
    def id(self):
        return os.path.basename(self.__filename)

    #===========================================================================
    def create(self):
        super(DatabaseFile, self).__init__()
        try:
            open(self.__filename, 'w').close()
        except Exception, ex:
            raise DriverException('Cannot create database', str(ex))
        return self
    
    #===========================================================================
    def load(self):
        path = self.__filename
        
        LOG("Load DB from file: " + repr(path))

        # If the file exists go on directly. Otherwise try to find it
        # no matter the case of the name
        if not os.path.exists(path):
            basepath = os.path.dirname(path)
            filename = os.path.basename(path)
            found = False
            for root, dirs, files in os.walk( basepath, topdown=False ):
                for f in files:
                    if f.upper() == filename.upper():
                        path = basepath + os.sep + f
                        found = True
            if not found:
                raise DriverException("Database file not found: " + repr(path))
        
        self.__filename = path
        
        # Load the file contents
        lines = file(self.__filename).readlines()
        self._vkeys = []
        self._types = {}
        self._properties = {}
        for line in lines:
            line = line.strip()
            if line.startswith("#"): continue
            if len(line.strip())==0: continue
            key = line.split()[0]
            orig_value = " ".join(line.split()[1:])
            value,vtype = ImportValue(orig_value)
            if self._properties.has_key(key):
                LOG("WARNING: duplicated database key: " + repr(key))
            else:
                self[key] = value
                if vtype:
                    self._types[key] = vtype 

    #===========================================================================
    def reload(self):
        self.load()

    #===========================================================================
    def commit(self):
        os.remove(self.__filename)
        db = os.open(self.__filename, os.O_CREAT | os.O_WRONLY)
        for key in self._vkeys:
            value = self._properties.get(key)
            os.write( db, key + '\t')

            if self._types.has_key(key):
                vtype = self._types.get(key)
                value = ExportValue(value,vtype)
                os.write( db, value )                    
            else:
                if type(value)==str:
                    os.write( db, '"' + value + '"' )
                else:
                    os.write( db, str(value))
                    
            os.write( db, '\n' )
        os.close(db)
        
    #===========================================================================
    def keys(self):
        return self._vkeys

    #===========================================================================
    def has_key(self, key):
        return (key in self._vkeys)

    #===========================================================================
    def _getPathName(self):
        return self.__filename
