#!/usr/bin/python3
"""defines all common attributes/methods for other classes"""
import uuid
from datetime import datetime
import models
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime

Base = declarative_base()


class BaseModel:
    """Class BaseModel"""
    id = Column(String(60), nullable=False, primary_key=True)

    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        '''Re-create an instance with this dictionary representatioin'''
        # instance attribute
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.strptime(
                        value, "%Y-%m-%dT%H:%M:%S.%f"))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """method"""
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    # Public instance methods

    def save(self):
        """" updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """to dict"""
        new_dict = {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': getattr(self, 'name', ''),
            'my_number': getattr(self, 'my_number', 0),
            '__class__': self.__class__.__name__,
        }

        if '_sa_instance_state' in new_dict:
            del new_dict['_sa_instance_state']

        return new_dict

    def delete(self):
        """ delete the current instance from the storage"""
        models.storage.delete(self)
