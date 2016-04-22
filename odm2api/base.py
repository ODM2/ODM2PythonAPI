



from sqlalchemy.ext.declarative import declarative_base
# #from sqlalchemy import MetaData
# from .ODMconnection import SessionFactory

#only one copy of class at a time
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            #print "Singleton", cls._instances[cls]
        return cls._instances[cls]

#only one copy of class with a particular connection
class SingletonByConn(type):
    _instances= {}

    def __call__(cls, *args, **kwargs):
        conn= args[0].engine
        if (cls, conn) not in cls._instances:

            cls._instances[(cls, conn)] = super(SingletonByConn, cls).__call__(*args, **kwargs)
            #print "Singleton", cls._instances[cls]
        return cls._instances[(cls, conn)]

class serviceBase(object):

    #__metaclass__ = SingletonByConn

    '''
    def __init__(self, session):
        self._session = session
    '''
    def __init__(self,  session_factory, debug=False):
        '''
         must send in either a session_factory #TODO  or a connection, exclusive or
        '''

        # if connection is  None:
        self._session_factory = session_factory
        # else:
        #     self._session_factory = SessionFactory(connection)

        self._session = self._session_factory.getSession()
        self._version = session_factory.version
        self._debug = debug
        #self._sessiona

    #self._session_factory=""
   # def getSessionFactory( session = None):
    def getSession(self):
        if self._session is None:
            self._session = self._session_factory.getSession()

        return self._session


class modelBase():

    Base = declarative_base()
    metadata = Base.metadata
    '''
    metadata =MetaData(schema='odm2')
    print "Schema:", metadata.schema

    def __init__(self, schema):
       self.metadata =MetaData(schema='odm2')
    '''








