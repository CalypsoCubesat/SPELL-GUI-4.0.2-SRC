from dbfile import *
import os.path
from spell.utils.log import *

################################################################################
class DatabaseSubversion(DatabaseFile):
    
    #===========================================================================
    def __init__(self, name, path, defaultExt = None):
        try:
            import pysvn
            self.__client = pysvn.Client()
        except:
            self.__client = None
            raise DriverException("Cannot import pysvn")

        super(DatabaseSubversion, self).__init__(name, path, defaultExt)
        
    #===========================================================================
    def load(self):
        super(DatabaseSubversion, self).load()

    #===========================================================================
    def status(self):
        client = self.__client
        filename = self._getPathName()

        LOG('Checking the status of the Subversion database %s' % filename)

        if not os.path.exists(filename):
            return None

        try:
            statuslst = client.status(filename, recurse = False, update = True)
        except Exception, ex:
            raise DriverException("Cannot get the Subversion database status (%s)" % ex)

        return statuslst[0]

    #===========================================================================
    def create(self):
        client = self.__client
        filename = self._getPathName()

        status = self.status()
        exists = False

        if status is not None:
            if status.entry is not None:
                exists = True

        if not exists:
            super(DatabaseSubversion, self).create()
            client.add(filename) 
            client.propset('svn:needs-lock', '*', filename)
            client.checkin([filename], '\n')
        else:
            self.lock()
            super(DatabaseSubversion, self).create()
            self.unlock()

        return self
    
    #===========================================================================
    def __del__(self):
        self.unlock()
        
    #===========================================================================
    def lock(self):
        import pysvn

        client = self.__client
        filename = self._getPathName()

        status = self.status()

       	if status.entry is None:
            raise DriverException("The database is not under revision control")

        if status.entry.schedule == pysvn.wc_schedule.add:
            client.checkin([filename], '\n')

        client.lock(filename, '\n', force = True)

    #===========================================================================
    def unlock(self):
        client = self.__client
        filename = self._getPathName()

        status = self.status()
        
        if status.entry.lock_token is None: return
        
        LOG('Unlocking Subversion database ' + filename)
        client.unlock(filename)        

    #===========================================================================
    def commit(self):
        client = self.__client
        filename = self._getPathName()

        self.lock()

        super(DatabaseSubversion, self).commit()

        LOG('Saving Subversion database ' + filename)
        client.checkin([filename], '\n', keep_locks = True)

        self.unlock()

