from __future__ import (absolute_import, division, print_function)

class serviceBase(object):
    def __init__(self,  session_factory, debug=False):
        """Must send in either a session_factory."""

        self._session_factory = session_factory

        self._session = self._session_factory.getSession()
        self._version = session_factory.version
        self._debug = debug

    def getSession(self):
        if self._session is None:
            self._session = self._session_factory.getSession()

        return self._session

    def reset_session(self):
        self._session = self._session_factory.getSession()


class Base(object):
    from sqlalchemy.ext.declarative import declared_attr

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __table_args__ = {u'schema': 'odm2'}

    def __init__(self, *args, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        valuedict = self.__dict__.copy()
        for v in valuedict.keys():
            if 'obj' in v.lower():
                del valuedict[v]

            if v == "_sa_instance_state":
                del valuedict["_sa_instance_state"]
        return "<%s(%s)>" % (self.__class__.__name__, str(valuedict))



class modelBase():
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base(cls=Base)
