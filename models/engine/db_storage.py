#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import os
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """This class manages storage of hbnb models in a mysql database"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine"""
        _user = os.getenv('HBNB_MYSQL_USER')
        _password = os.getenv('HBNB_MYSQL_PWD')
        _host = os.getenv('HBNB_MYSQL_HOST')
        _database = os.getenv('HBNB_MYSQL_DB')
        data = (_user, _password, _host, _database)
        tconnection = 'mysql+mysqldb://{}:{}@{}:3306/{}'
        self.__engine = create_engine(tconnection.format(*data),
                                      pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objects = {}
        classes = [City, State, User, Place, Amenity, Review]

        if cls is None:
            l_objs = []
            [l_objs.extend(self.__session.query(c).all()) for c in classes]
        else:
            if type(cls) == str:
                cls = eval(cls)
            l_objs = self.__session.query(cls).all()

        [objects.update({"{}.{}"
                         .format(type(obj).__name__, obj.id): obj})
         for obj in l_objs]
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reload all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the working SQLAlchemy session."""
        self.__session.close()
