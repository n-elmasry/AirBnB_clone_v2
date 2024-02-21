#!/usr/bin/python3
"""will allow you to change storage type directly by using an environment variable"""
# from models.engine.file_storage import FileStorage
# storage = FileStorage()
# storage.reload
from os import getenv
storage_type = getenv('HBNB_TYPE_STORAGE')


if storage_type == "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
