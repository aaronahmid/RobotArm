#!/usr/bin/python3
"""
Contains the FileStorage class
"""

from encodings import utf_8
import json
import states
import os
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
    home = os.getenv('HOME')
    __file_path = f'{home}/.arm/states.json'

    # dictionary - empty but will store all states by id
    __states = {
        'current_state': {
            'id': None,
            'name': None
            }
    }

    def setCurrentState(self, id):
        """
        Sets The current state to use

        Args:
            id [uuid]: unique identifier of states object
        
        Returns:
            None if state does not exists
        """
        if id is None:
            return "id cannot be empty"

        state = states.storage.get(id)
        if state:
            current_state = {
                'id': state.id,
                'name': state.project_name
                }
            self.__states['current_state'] = current_state
            return state

    def removeCurrentState(self):
        current_state = {
                'id': None,
                'name': None
                }
        self.__states['current_state'] = current_state

    def all(self, cls=None):
        """returns the dictionary __states"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__states.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    if key != 'current_state':
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
            if key != 'current_state':
                json_states[key] = self.__states[key].to_dict()
            else:
                json_states[key] = self.__states[key]
        with open(self.__file_path, 'w') as f:
            json.dump(json_states, f)

    def reload(self):
        """deserializes the JSON file to __states"""
        if os.path.isfile(self.__file_path):
            pass
        else:
            with open(self.__file_path, 'x', encoding='utf8') as f:
                f.close()
        if os.stat(self.__file_path).st_size > 1:
            with open(self.__file_path, mode='r', encoding='utf8') as f:
                jo = json.load(f)
                for key in jo:
                    if key != 'current_state':
                        self.__states[key] = classes[jo[key]['__class__']](**jo[key])
                    else:
                        self.__states[key] = jo[key]

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
        for state in all_states.keys():
            if state != 'current_state':
                if (all_states[state].id == id):
                    return all_states[state]

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