#!/usr/bin/python3
"""
Contains class BaseState
"""

from datetime import datetime
import states
import uuid


class BaseState:
    """
    BaseState for future class definitions
    """
    __current_state = ''
    def __init__(self, *args, **kwargs):
        """
        Initializes base model with an id
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
                if kwargs.get("id", None) is None:
                    self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        states.storage.new(self)
        states.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict