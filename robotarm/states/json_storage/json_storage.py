#!/usr/bin/python3
"""Json File Storage to save states
"""
import json
from json.decoder import JSONDecodeError
import os

class StateJsonStorage:
    """
    Store states in a JSON format file
    """

    __file_path = 'json_store.json'
    __state_objects = {}

    def __init__(self) -> None:
        """when called, initializes the file storage
        """
        file_init_text = """ Test FIle"""

        if os.path.isfile(StateJsonStorage.__file_path):
            return
        with open(StateJsonStorage.__file_path, 'w', encoding='utf8') as fd:    
            fd.write(file_init_text)

    def commit(self, state_obj:dict):
        """commits a new runtime state to the file
        """
        with open(StateJsonStorage.__file_path, 'w', encoding='utf8') as fd:
            try:
                fd.write(json.dumps(state_obj))
            except Exception:
                print(Exception)

    def retrieve(self):
        """retrieve a state
        """
        pass

    def reload(self):
        """reloads states from file to runtime
        """
        try:
            temp = {}
            with open(StateJsonStorage.__file_path, 'r', encoding='utf8') as fd:
                try:
                    temp = json.load(fd)
                except JSONDecodeError:
                    pass
        except FileNotFoundError:
            print('no state or file not found')

        StateJsonStorage.__state_objects.update(temp)
        return StateJsonStorage.__state_objects

    def delete(self):
        """deletes a state from file and or runtime
        """
        pass