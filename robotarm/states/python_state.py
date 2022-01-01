#!/usr/bin/python3
"""
State object class Module for the Robotarm package
"""
from robotarm.states import storage
class PythonState:
    """
    State object class

    Attributes:
        project_root: Project Root Directory
        project_name[str]: Name of project
        project_version[str]: Project Version
        runtime_version:[str]: Language Robotarm should be initialized to
        framework_library[str]: Framework or library utilized by the project
        enable_git:bool
        database:str
        setup_env:str
        requirements:str
    """
    __state_name = 'Python State'
    project_root = '.'
    project_name = '.'
    project_version = '0.0.1'
    runtime_version = ''
    framework_library = ''
    enable_git = True
    database = ''
    setup_env = True
    requirements = ''

    def __init__(self, *args, **kwargs):
        """instatiates Python State 
        """
        if kwargs is not None:
            self.__dict__.update(kwargs)

        self.save_state()

    def save_state(self):
        """saves a state by calling storage.commit
        """
        state_dict = self.to_dict()
        # save state to file
        storage.commit(state_dict)

    def to_dict(self):
        """Returns attributes in dictionary format

        Returns:
            dict: returns key/value pair of attributes
        """
        # attributes to look for
        keys = [
        'project_root', 
        'project_name',
        'project_version',
        'runtime_version',
        'framework_library',
        'enable_git',
        'database',
        'setup_env',
        'requirements'
        ]
        dict = {}

        # checks for attribute and adds to dict
        for key in keys:
            try:
                dict[key] = self.__getattribute__(key)
            except AttributeError:
                raise(AttributeError)

        return dict