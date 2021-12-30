#!/usr/bin/python3
"""Json File Storage to save states
"""

import robotarm
import pathlib

BASE_DIR = pathlib.Path.

class StateJsonStorage:
    """
    Store states in a JSON format file
    """

    __file_path = 'json_store.json'
    __state_objects = {}

    def commit(self):
        """commits a new runtime state to the file
        """
        pass

    def retrieve(self):
        """retrieve a state
        """
        pass

    def reload(self):
        """reloads states from file to runtime
        """
        pass

    def delete(self):
        """deletes a state from file and or runtime
        """
        pass