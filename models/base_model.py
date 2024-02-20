#!/usr/bin/python3
"""defines all common attributes/methods for other classes"""
import uuid
from datetime import datetime
import models


class BaseModel:
    """Class BaseModel"""

    def __init__(self, *args, **kwargs):
        '''Re-create an instance with this dictionary representatioin'''
        # instance attribute
        date_time = "%Y-%m-%dT%H:%M:%S.%f"
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                elif key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.strptime(value, date_time))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)
            # models.storage.save()

    def __str__(self):
        # return f"{type(self).__name__} {self.to_dict()}"
        return f'[{self.__class__.__name__}] ({self.id}) {self.__dict__}'

    # Public instance methods

    def save(self):
        """" updates updated_at with the current datetime"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        new_dict = {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'name': getattr(self, 'name', ''),
            'my_number': getattr(self, 'my_number', 0),
            '__class__': self.__class__.__name__,
        }
        return new_dict
