#!/usr/bin/python3
"""
State object class Module for the Robotarm package
"""
import json


class BaseState:
    """
    State object class

    Attributes:
        project_root: Project Root Directory
        project_name[str]: Name of project
        project_version[str]: Project Version
        language:[str]: Language Robotarm should be initialized to
        framework_library[str]: Framework or library utilized by the project
        enable_git:bool
        database:str
        setup_env:str
        requirements:str
    """
    project_root = '.'
    project_name = '.'
    project_version = '0.0.1'
    language = ''
    framework_library = ''
    enable_git = True
    database = ''
    setup_env = False
    requirements = ''

    def __init__(self, *args, **kwargs):
        if kwargs is not None:
            for key in kwargs.keys():
                setattr(self, key, kwargs[key])

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def to_json():
        pass
