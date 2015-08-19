



from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy import MetaData
# from .ODMconnection import SessionFactory
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            #print "Singleton", cls._instances[cls]
        return cls._instances[cls]

class serviceBase(object):

    __metaclass__ = Singleton

    '''
    def __init__(self, session):
        self._session = session
    '''
    def __init__(self,  session_factory=None, debug=False):
        '''
        must send in either a session_factory or a connection, exclusive or
        '''

        # if connection is  None:
        self._session_factory = session_factory
        # else:
        #     self._session_factory = SessionFactory(connection)

        self._session = session_factory.getSession()


        # self._session.autoflush = False
        #print "Session ", self._session

        # print "ServiceBase Called!", self._session


        self._debug = debug
        #self._sessiona

    #self._session_factory=""
   # def getSessionFactory( session = None):
    def getSession(self):
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








