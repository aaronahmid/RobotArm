#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
import states
from states.base_state import BaseState
from states.django_state import DjangoState

classes = {
    "DjangoState": DjangoState,
    "BaseStatel": BaseState,
    #"FlaskState": FlaskState
    }


class JsonFileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "states.json"
    # dictionary - empty but will store all states by id
    __states = {
        'current_state': ''
    }

    def all(self, cls=None):
        """returns the dictionary __states"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__states.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    if key is not 'current_state':
                        new_dict[key] = value
            return new_dict
        return self.__states

    def new(self, obj):
        """sets in __states the obj with key obj.id"""
        if obj is not None:
            key = obj.id
            self.__states[key] = obj

    def save(self):
        """serializes __states to the JSON file (path: __file_path)"""
        json_states = {}
        for key in self.__states:
            json_states[key] = self.__states[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_states, f)

    def reload(self):
        """deserializes the JSON file to __states"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__states[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __states if it's inside"""
        if obj is not None:
            key = obj.id
            if key in self.__states:
                del self.__states[key]

    def close(self):
        """call reload() method for deserializing the JSON file to states"""
        self.reload()

    def get(self, id):
        """
        Returns the object based on the its ID, or
        None if not found
        """

        all_states = states.storage.all()
        for value in all_states.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of states in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(states.storage.all(clas).values())
        else:
            count = len(states.storage.all(cls).values())

        return count