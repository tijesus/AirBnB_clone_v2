#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Interger, DateTime
from sqlalchemy.ext.declarative import declarative_base
import models


Base = declarative_base()
class BaseModel():
    """A base class for all hbnb models"""
    id = Column(String(60), primary_key= True);
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if "create_at" not in kwargs.keys():
                self.created_at = datetime.now()
            if "update_at" not in kwargs.keys():
                self.updated_at = datetime.now()
            if "id" not in kwargs.keys():
                self.id = str(uuid.uuid4())
            for k, v in kwargs.items():
                if k in ["created_at", "updated_at"]:
                    fmt = "%Y-%m-%dT%H:%M:%S.%f"
                    setattr(self, k, datetime.strptime(v, fmt))
                elif k != "__class__":
                    setattr(self, k, v)
            del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.save()
        storage.new(self)

    def to_dict(self, save_to_disk=False):
        """Convert instance into dict format"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].isoformat()
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].isoformat()
        if '_password' in new_dict:
            new_dict['password'] = new_dict['_password']
            new_dict.pop('_password', None)
        if 'amenities' in new_dict:
            new_dict.pop('amenities', None)
        if 'reviews' in new_dict:
            new_dict.pop('reviews', None)
        new_dict["__class__"] = self.__class__.__name__
        new_dict.pop('_sa_instance_state', None)
        if not save_to_disk:
            new_dict.pop('password', None)
        return new_dict

    def delete(self):
        """Delete current instance from storage by calling its delete method"""
        models.storage.delete(self)    
