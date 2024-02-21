#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Table, Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    name = ""
