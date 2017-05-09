



class serviceBase(object):

    # __metaclass__ = SingletonByConn

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

    def reset_session(self):
        self._session =self._session_factory.getSession() #reset the session in order to prevent memory leaks



from sqlalchemy.ext.declarative import declared_attr

class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {u'schema': 'odm2'}

    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items(): setattr(self, name, value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        valuedict = self.__dict__.copy()
        for v in valuedict.keys():
            if "obj" in v.lower():
                del valuedict[v]
        # del valuedict["_sa_instance_state"]
        return "<%s(%s)>" % (self.__class__.__name__, str(valuedict))


from sqlalchemy.ext.declarative import declarative_base
class modelBase():
    Base = declarative_base(cls=Base)











