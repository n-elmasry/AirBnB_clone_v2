#!/usr/bin/python3
"""  engine DBStorage """
from os import getenv
import models
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """DBStorage"""
    __engine = None
    __session = None

    # Public instance methods
    def __init__(self):
        """Public instance method"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST,  HBNB_MYSQL_DB), pool_pre_ping=True)
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        dict = {}

        for i in classes:
            if cls is None or cls == i:
                objects = self.__session.query(classes[i]).all()
                for obj in objects:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dict[key] = obj
        return dict

        """
        def all(self, cls=None):
            objects = {}

            for cls_name, cls_obj in classes.items():
                if cls is None or cls == cls_obj:
                    query_results = self.__session.query(cls_obj).all()
                    for obj in query_results:
                        key = "{}.{}".format(cls_name, obj.id)
                        objects[key] = obj

            return objects
        """

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session"""
        if obj is not None:
            del obj
            # self.__session.delete(obj)
            self.save

    def reload(self):
        """create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sessionmkr = sessionmaker(bind=self.__engine, expire_on_commit=False)

        Session = scoped_session(sessionmkr)
        self.__session = Session()

    def close(self):
        """clsoes session"""
        self.__session.remove()
